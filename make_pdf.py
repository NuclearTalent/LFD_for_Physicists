#!/usr/bin/env python3
"""
Create a PDF from a Jupyter Book 1 ``singlehtml`` build using Playwright.

Expected input:
    _build/singlehtml/index.html

Default output:
    _build/pdf/book.pdf

Before running:

    jupyter-book build . --builder singlehtml
    python -m pip install playwright
    python -m playwright install chromium

Then run:

    python make_pdf.py

This version:
  * reads print typography/page-break rules from ``pdf_print.css``;
  * adds configurable PDF page numbers;
  * repairs nested ``content/_images`` and ``content/_static`` URLs;
  * uses configurable margins;
  * retains ordinary internal and external links;
  * expands dropdown admonitions;
  * suppresses hidden code input while preserving visible figure output;
  * opens ``hide-cell`` wrappers for printing but hides their code input;
  * converts local HTML images to data URLs before printing;
  * converts bare links to common image files in ``_images`` into images;
  * reports missing or unsupported figure resources.
"""

from __future__ import annotations

import functools
import inspect
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page, sync_playwright


# =============================================================================
# User configuration
# =============================================================================

BUILD_DIR = Path("_build/singlehtml").resolve()
HTML_FILE = BUILD_DIR / "index.html"
PDF_FILE = Path("_build/pdf/book_compact.pdf").resolve()

PAGE_FORMAT = "Letter"

PDF_MARGINS = {
    "top": "0.65in",
    "right": "0.70in",
    # Leave enough room for the page-number footer.
    "bottom": "0.75in",
    "left": "0.70in",
}

# Page-number footer. Set SHOW_PAGE_NUMBERS = False to remove it.
SHOW_PAGE_NUMBERS = True
PAGE_NUMBER_FONT_SIZE = "9px"
PAGE_NUMBER_COLOR = "#555"

# Choose one of:
#   "number"         ->  17
#   "page_of_total"  ->  Page 17 of 243
PAGE_NUMBER_STYLE = "number"

VIEWPORT = {
    "width": 1440,
    "height": 1000,
}

REPORT_NAVIGATIONS = True
PREPARATION_ATTEMPTS = 8

# Convert same-origin PNG/JPEG/GIF/WebP/SVG images to data URLs before
# Chromium prints the page. This makes figure embedding independent of
# subsequent relative-path resolution.
INLINE_LOCAL_IMAGES = True

# Jupyter Book/Sphinx assets normally live at the root of the HTML build.
# Some singlehtml/theme combinations redirect to a nested page such as
# content/About.html while leaving asset references as _images/foo.
# The local server below maps nested requests such as
# /content/_images/foo.png to /_images/foo.png.
ROOT_ASSET_DIRECTORIES = (
    "_images",
    "_static",
    "_downloads",
    "_sources",
)

# Save a full-page PNG of the prepared HTML beside the PDF. This is useful
# for distinguishing an HTML-rendering problem from a PDF-printing problem.
SAVE_DEBUG_SCREENSHOT = False
DEBUG_SCREENSHOT = Path("_build/pdf/book-preprint.png").resolve()


# =============================================================================
# Print-specific CSS
# =============================================================================

# Keep print typography and page-breaking rules in a separate file.
# The CSS file should live next to this script.
SCRIPT_DIR = Path(__file__).resolve().parent
PRINT_CSS_FILE = SCRIPT_DIR / "pdf_print.css"


# =============================================================================
# JavaScript
# =============================================================================

WAIT_FOR_RESOURCES = r"""
async () => {
    const waitWithTimeout = async (promise, milliseconds) => {
        await Promise.race([
            Promise.resolve(promise).catch(() => undefined),
            new Promise(resolve => setTimeout(resolve, milliseconds))
        ]);
    };

    for (const image of document.querySelectorAll("img")) {
        image.loading = "eager";

        /*
         * A stale or unsuitable srcset can override src. For a static PDF,
         * using the resolved src is more predictable.
         */
        image.removeAttribute("srcset");
        image.removeAttribute("sizes");
    }

    if (document.fonts && document.fonts.ready) {
        await waitWithTimeout(document.fonts.ready, 20000);
    }

    if (
        window.MathJax &&
        window.MathJax.startup &&
        window.MathJax.startup.promise
    ) {
        await waitWithTimeout(window.MathJax.startup.promise, 30000);
    }

    await Promise.all(
        Array.from(document.images).map(async image => {
            if (!image.complete) {
                await new Promise(resolve => {
                    let finished = false;

                    const finish = () => {
                        if (finished) {
                            return;
                        }

                        finished = true;
                        image.removeEventListener("load", finish);
                        image.removeEventListener("error", finish);
                        resolve();
                    };

                    image.addEventListener("load", finish, {once: true});
                    image.addEventListener("error", finish, {once: true});
                    setTimeout(finish, 20000);
                });
            }

            if (typeof image.decode === "function") {
                await waitWithTimeout(image.decode(), 10000);
            }
        })
    );

    await new Promise(resolve =>
        requestAnimationFrame(() =>
            requestAnimationFrame(resolve)
        )
    );
}
"""


PREPARE_DOCUMENT = r"""
() => {
    function isDropdownAdmonition(details) {
        return (
            details.matches(
                "details.admonition, details.dropdown, " +
                ".admonition.dropdown details, .dropdown.admonition details"
            ) ||
            details.closest(".admonition.dropdown, .dropdown.admonition") !== null
        );
    }

    function isNotebookCodeWrapper(details) {
        /*
         * Handle both common structures:
         *
         *   <details class="hide ..."><div class="cell">...</div></details>
         *
         * and a details element nested inside a tagged cell.
         */
        return (
            details.closest(
                ".tag_hide-input, .tag_hide-output, .tag_hide-cell"
            ) !== null ||
            details.querySelector(
                ":scope > .cell, :scope > .cell_input, :scope > .cell_output"
            ) !== null ||
            (
                details.classList.contains("hide") &&
                (
                    details.closest(".cell") !== null ||
                    details.querySelector(".cell_input, .cell_output") !== null
                )
            )
        );
    }

    function prepareForPDF() {
        /*
         * Open dropdown admonitions.
         *
         * Open notebook details wrappers too, because an output figure may
         * be inside the same wrapper as hidden code. CSS hides the input,
         * leaving the figure visible.
         */
        for (const details of document.querySelectorAll("details")) {
            if (isDropdownAdmonition(details)) {
                details.open = true;
            } else if (isNotebookCodeWrapper(details)) {
                details.open = true;
                details.dataset.pdfCodeWrapper = "true";
            }
        }

        for (
            const admonition of document.querySelectorAll(
                ".admonition.dropdown, .dropdown.admonition"
            )
        ) {
            admonition.classList.remove("toggle-hidden");
            admonition.classList.remove("toggle-hidden-print");
            admonition.setAttribute("open", "");

            for (const child of admonition.querySelectorAll("details")) {
                child.open = true;
            }

            for (
                const button of admonition.querySelectorAll(
                    "button.toggle-button, .toggle-button"
                )
            ) {
                button.setAttribute("aria-expanded", "true");
            }
        }

        /*
         * Mark image links. The print CSS suppresses any generated URL text
         * for these anchors while leaving the link annotation itself intact.
         */
        for (
            const link of document.querySelectorAll(
                "a.image-reference, a.reference.image-reference, " +
                "a[href*='_images/']"
            )
        ) {
            link.dataset.pdfImageLink = "true";
        }

        /*
         * Repair residual cross-document links in a singlehtml build.
         */
        for (const link of document.querySelectorAll('a[href*=".html#"]')) {
            const href = link.getAttribute("href");

            if (!href || !href.includes("#")) {
                continue;
            }

            const hash = href.substring(href.indexOf("#"));
            let targetID;

            try {
                targetID = decodeURIComponent(hash.substring(1));
            } catch {
                targetID = hash.substring(1);
            }

            if (targetID && document.getElementById(targetID)) {
                link.setAttribute("href", hash);
            }
        }
    }

    prepareForPDF();

    if (!window.__jupyterBookPDFPreparationInstalled) {
        window.addEventListener("beforeprint", prepareForPDF);
        window.__jupyterBookPDFPreparationInstalled = true;
    }
}
"""


PREPARE_IMAGES = r"""
async ({inlineLocalImages}) => {
    const supportedPattern =
        /\.(?:png|jpe?g|gif|webp|svg)(?:$|[?#])/i;

    const unsupportedFigurePattern =
        /\.(?:pdf|eps|ps)(?:$|[?#])/i;

    const report = {
        imageElementsInitially: document.images.length,
        imageElementsFinally: 0,
        createdFromImageLinks: 0,
        localImagesInlined: 0,
        loadedImages: 0,
        brokenImages: [],
        unsupportedFigureLinks: []
    };

    const waitWithTimeout = async (promise, milliseconds) => {
        await Promise.race([
            Promise.resolve(promise).catch(() => undefined),
            new Promise(resolve => setTimeout(resolve, milliseconds))
        ]);
    };

    const blobToDataURL = blob => new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.addEventListener("load", () => resolve(reader.result), {
            once: true
        });
        reader.addEventListener("error", () => reject(reader.error), {
            once: true
        });
        reader.readAsDataURL(blob);
    });

    /*
     * If the HTML contains a bare link to a supported file in _images
     * instead of an <img>, replace its visible text with an actual image.
     * The anchor remains, so clicking the figure still opens the original.
     */
    for (const link of Array.from(document.querySelectorAll("a[href]"))) {
        const rawHref = link.getAttribute("href");

        if (!rawHref) {
            continue;
        }

        let url;

        try {
            url = new URL(rawHref, document.baseURI);
        } catch {
            continue;
        }

        const isLikelyFigure =
            url.pathname.includes("/_images/") ||
            link.classList.contains("image-reference");

        if (!isLikelyFigure) {
            continue;
        }

        link.dataset.pdfImageLink = "true";

        if (unsupportedFigurePattern.test(url.pathname)) {
            report.unsupportedFigureLinks.push(url.href);
            continue;
        }

        if (
            supportedPattern.test(url.pathname) &&
            !link.querySelector("img, svg, object, embed")
        ) {
            const image = document.createElement("img");
            image.src = url.href;
            image.alt =
                link.getAttribute("title") ||
                link.textContent.trim() ||
                url.pathname.split("/").pop() ||
                "Figure";
            image.loading = "eager";
            image.dataset.pdfCreatedFromLink = "true";

            link.replaceChildren(image);
            report.createdFromImageLinks += 1;
        }
    }

    for (const image of Array.from(document.images)) {
        image.loading = "eager";
        image.removeAttribute("srcset");
        image.removeAttribute("sizes");

        const rawSource =
            image.getAttribute("src") ||
            image.currentSrc;

        if (!rawSource) {
            report.brokenImages.push("(image with no src)");
            continue;
        }

        let url;

        try {
            url = new URL(rawSource, document.baseURI);
        } catch {
            report.brokenImages.push(rawSource);
            continue;
        }

        /*
         * Inline only same-origin, supported images. External images are
         * left intact because fetching them may be blocked by CORS.
         */
        if (
            inlineLocalImages &&
            url.origin === window.location.origin &&
            supportedPattern.test(url.pathname) &&
            !rawSource.startsWith("data:")
        ) {
            try {
                const response = await fetch(url.href, {
                    cache: "force-cache"
                });

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }

                const blob = await response.blob();
                const dataURL = await blobToDataURL(blob);

                image.src = dataURL;
                report.localImagesInlined += 1;
            } catch (error) {
                report.brokenImages.push(
                    `${url.href} (${String(error)})`
                );
                continue;
            }
        }

        if (!image.complete) {
            await new Promise(resolve => {
                const finish = () => resolve();
                image.addEventListener("load", finish, {once: true});
                image.addEventListener("error", finish, {once: true});
                setTimeout(finish, 15000);
            });
        }

        if (typeof image.decode === "function") {
            await waitWithTimeout(image.decode(), 10000);
        }

        if (image.naturalWidth > 0 && image.naturalHeight > 0) {
            report.loadedImages += 1;
        } else {
            report.brokenImages.push(url.href);
        }
    }

    report.imageElementsFinally = document.images.length;

    /*
     * De-duplicate diagnostics.
     */
    report.brokenImages = Array.from(new Set(report.brokenImages));
    report.unsupportedFigureLinks =
        Array.from(new Set(report.unsupportedFigureLinks));

    return report;
}
"""


# =============================================================================
# Python helpers
# =============================================================================

class BookHTTPRequestHandler(SimpleHTTPRequestHandler):
    """
    Serve the Sphinx build while repairing nested asset URLs.

    For example, a request for

        /content/_images/figure.png

    is served from

        BUILD_DIR/_images/figure.png

    when the redirected HTML page lives under ``content/``.
    """

    server_version = "JupyterBookPDFServer/1.0"

    def _normalized_request_path(self) -> str:
        parts = urlsplit(self.path)
        normalized_path = parts.path

        for directory in ROOT_ASSET_DIRECTORIES:
            marker = f"/{directory}/"
            marker_position = normalized_path.find(marker)

            if marker_position > 0:
                normalized_path = normalized_path[marker_position:]
                self.server.asset_rewrite_count += 1  # type: ignore[attr-defined]
                break

        return urlunsplit(
            ("", "", normalized_path, parts.query, "")
        )

    def do_GET(self) -> None:
        self.path = self._normalized_request_path()
        super().do_GET()

    def do_HEAD(self) -> None:
        self.path = self._normalized_request_path()
        super().do_HEAD()

    def log_message(self, format: str, *args: object) -> None:
        # Suppress hundreds of routine local HTTP access messages.
        return


def start_local_server() -> tuple[ThreadingHTTPServer, threading.Thread, int]:
    """Start the asset-repairing HTTP server in a background thread."""

    handler = functools.partial(
        BookHTTPRequestHandler,
        directory=str(BUILD_DIR),
    )

    server = ThreadingHTTPServer(
        ("127.0.0.1", 0),
        handler,
    )
    server.asset_rewrite_count = 0  # type: ignore[attr-defined]

    thread = threading.Thread(
        target=server.serve_forever,
        name="jupyter-book-pdf-server",
        daemon=True,
    )
    thread.start()

    port = int(server.server_address[1])
    return server, thread, port


def is_navigation_error(error: PlaywrightError) -> bool:
    message = str(error)

    navigation_phrases = (
        "Execution context was destroyed",
        "most likely because of a navigation",
        "Cannot find context with specified id",
    )

    return any(phrase in message for phrase in navigation_phrases)


def wait_for_document_ready(
    page: Page,
    navigation_state: dict[str, int],
    attempts: int = PREPARATION_ATTEMPTS,
) -> None:
    for attempt in range(1, attempts + 1):
        navigation_count_at_start = navigation_state["count"]

        try:
            page.wait_for_load_state(
                "domcontentloaded",
                timeout=120_000,
            )

            page.wait_for_timeout(1000)
            page.evaluate(WAIT_FOR_RESOURCES)
            page.wait_for_timeout(1000)

            if navigation_state["count"] == navigation_count_at_start:
                return

            print(
                "The main page navigated while resources were being "
                f"prepared; retrying ({attempt}/{attempts})..."
            )

        except PlaywrightError as error:
            if not is_navigation_error(error) or attempt == attempts:
                raise

            print(
                "The page navigated while resources were being prepared; "
                f"retrying ({attempt}/{attempts})..."
            )
            page.wait_for_timeout(1000)

    raise RuntimeError(
        "The page did not remain stable long enough to prepare it for PDF "
        f"output after {attempts} attempts."
    )


def make_pdf_options(page: Page) -> dict[str, Any]:
    """Construct PDF options supported by the installed Playwright version."""

    options: dict[str, Any] = {
        "path": str(PDF_FILE),
        "format": PAGE_FORMAT,
        "margin": PDF_MARGINS,
        "print_background": True,
        "prefer_css_page_size": False,
    }

    if SHOW_PAGE_NUMBERS:
        if PAGE_NUMBER_STYLE == "page_of_total":
            footer_content = (
                'Page <span class="pageNumber"></span> '
                'of <span class="totalPages"></span>'
            )
        else:
            footer_content = '<span class="pageNumber"></span>'

        options.update(
            {
                "display_header_footer": True,
                "header_template": "<div></div>",
                "footer_template": f"""
                    <div style="
                        width: 100%;
                        text-align: center;
                        font-family: Arial, Helvetica, sans-serif;
                        font-size: {PAGE_NUMBER_FONT_SIZE};
                        color: {PAGE_NUMBER_COLOR};
                    ">
                        {footer_content}
                    </div>
                """,
            }
        )

    parameters = inspect.signature(page.pdf).parameters

    if "outline" in parameters:
        options["outline"] = True
    else:
        print(
            "Note: this Playwright version does not expose PDF outlines; "
            "continuing without them."
        )

    if "tagged" in parameters:
        options["tagged"] = True
    else:
        print(
            "Note: this Playwright version does not expose tagged-PDF "
            "output; continuing without it."
        )

    return options


def print_image_report(report: dict[str, Any]) -> None:
    print(
        "Figure preparation: "
        f"{report['imageElementsInitially']} image elements initially; "
        f"{report['createdFromImageLinks']} created from image links; "
        f"{report['localImagesInlined']} local images inlined; "
        f"{report['loadedImages']} images loaded."
    )

    broken = report.get("brokenImages", [])

    if broken:
        print("\nWARNING: These image resources did not load:")
        for item in broken[:20]:
            print(f"  - {item}")
        if len(broken) > 20:
            print(f"  ... and {len(broken) - 20} more")

    unsupported = report.get("unsupportedFigureLinks", [])

    if unsupported:
        print(
            "\nWARNING: These figure links use PDF/EPS/PS files. Chromium "
            "cannot use them as ordinary HTML <img> elements. Convert them "
            "to PNG, JPEG, WebP, or SVG in the Jupyter Book source:"
        )
        for item in unsupported[:20]:
            print(f"  - {item}")
        if len(unsupported) > 20:
            print(f"  ... and {len(unsupported) - 20} more")


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    if not HTML_FILE.exists():
        raise FileNotFoundError(
            f"The expected HTML file does not exist:\n"
            f"    {HTML_FILE}\n\n"
            "Build the book first with:\n"
            "    jupyter-book build . --builder singlehtml"
        )

    PDF_FILE.parent.mkdir(parents=True, exist_ok=True)

    if SAVE_DEBUG_SCREENSHOT:
        DEBUG_SCREENSHOT.parent.mkdir(parents=True, exist_ok=True)

    server, server_thread, port = start_local_server()
    url = f"http://127.0.0.1:{port}/index.html"

    browser = None

    try:

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)

            context = browser.new_context(
                viewport=VIEWPORT,
                device_scale_factor=1,
            )
            page = context.new_page()

            navigation_state = {"count": 0}

            def report_navigation(frame) -> None:
                if frame == page.main_frame:
                    navigation_state["count"] += 1
                    if REPORT_NAVIGATIONS:
                        print(
                            "Main-page navigation "
                            f"{navigation_state['count']}: {frame.url}"
                        )

            page.on("framenavigated", report_navigation)

            response = page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=120_000,
            )

            if response is not None and not response.ok:
                raise RuntimeError(
                    f"Could not load {url}: "
                    f"HTTP {response.status} {response.status_text}"
                )

            wait_for_document_ready(page, navigation_state)

            if not PRINT_CSS_FILE.exists():
                raise FileNotFoundError(
                    f"The print CSS file does not exist:\n"
                    f"    {PRINT_CSS_FILE}"
                )

            page.add_style_tag(
                content=PRINT_CSS_FILE.read_text(encoding="utf-8")
            )
            page.evaluate(PREPARE_DOCUMENT)

            image_report = page.evaluate(
                PREPARE_IMAGES,
                {"inlineLocalImages": INLINE_LOCAL_IMAGES},
            )
            print_image_report(image_report)

            # PREPARE_IMAGES may have created images from bare links.
            # Wait once more for decoding and layout.
            page.evaluate(WAIT_FOR_RESOURCES)

            page.emulate_media(media="print")
            page.evaluate(PREPARE_DOCUMENT)
            page.wait_for_timeout(750)

            if SAVE_DEBUG_SCREENSHOT:
                page.screenshot(
                    path=str(DEBUG_SCREENSHOT),
                    full_page=True,
                )
                print(f"Saved pre-print screenshot:\n    {DEBUG_SCREENSHOT}")

            page.pdf(**make_pdf_options(page))

            context.close()
            browser.close()
            browser = None

        print(f"Created PDF:\n    {PDF_FILE}")

    finally:
        if browser is not None:
            try:
                browser.close()
            except Exception:
                pass

        server.shutdown()
        server.server_close()
        server_thread.join(timeout=5)

        rewrite_count = getattr(server, "asset_rewrite_count", 0)
        if rewrite_count:
            print(
                "Repaired nested Jupyter Book asset requests: "
                f"{rewrite_count}"
            )


if __name__ == "__main__":
    main()
