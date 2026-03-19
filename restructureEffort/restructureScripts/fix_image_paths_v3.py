#!/usr/bin/env python3
"""
fix_image_paths_v3_1.py
Safely rewrite image URLs ONLY inside MyST {figure}, {image}, Markdown images, and HTML <img>.
Never touch other text, never rewrite bare paths or LaTeX identifiers.
Depth-aware rewrite to content/<PART>/assets/<basename>.
"""

import argparse
import json
import os
import re
from pathlib import Path

# ------------------------------------------------------------------------------
# Patterns: STRICTLY capture only the URL slots of valid image/figure constructs
# ------------------------------------------------------------------------------

# :::{figure} <url> (three or more :)
FIGURE_COLON = re.compile(
	r"(:{3,}\{figure\}\s+)(?P<url>\S+)", 
	re.IGNORECASE
)

# ```{figure} <url>  (3 or more backticks)
FIGURE_FENCE = re.compile(
    r"(`{3,}\{figure\}\s+)(?P<url>\S+)",
    re.IGNORECASE
)

IMAGE_COLON  = re.compile(
	r"(:{3,}\{image\}\s+)(?P<url>\S+)", 
	re.IGNORECASE
)


# ```{image} <url>
IMAGE_FENCE = re.compile(
    r"(`{3,}\{image\}\s+)(?P<url>\S+)",
    re.IGNORECASE
)

# Inline {image} <url>
IMAGE_INLINE = re.compile(
    r"(\{image\}\s+)(?P<url>\S+)",
    re.IGNORECASE
)

# Markdown image
MD_IMAGE = re.compile(
    r"(!\[[^\]]*\]\()(?P<url>[^)\s]+)(\))"
)

# HTML <img src="...">
HTML_IMG = re.compile(
    r'(<img[^>]*\ssrc=["\'])(?P<url>[^"\'>]+)(["\'])',
    re.IGNORECASE
)

SUPPORTED = [FIGURE_COLON, FIGURE_FENCE, IMAGE_FENCE, IMAGE_INLINE, MD_IMAGE, HTML_IMG, IMAGE_COLON]

# ------------------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------------------

def is_external(url: str) -> bool:
    return url.startswith(("http://", "https://", "#", "data:"))

def is_legacy_image_path(url: str) -> bool:
    """
    Only consider URLs to be fixed if they look like image paths.
    We require:
      - known image extension
      - and old "figs/" or "images/" path components
    """
    img_exts = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".pdf", ".webp")
    if not any(url.lower().split("?")[0].endswith(ext) for ext in img_exts):
        return False

    triggers = (
        url.startswith("./figs/") or
        url.startswith("../figs/") or
        url.startswith("figs/") or
        url.startswith("./images/") or
        url.startswith("../images/") or
        url.startswith("images/") or
        "/figs/" in url or
        "/images/" in url or
        url.startswith("content/")
    )

    return triggers and not is_external(url)


def find_part(doc_path: Path) -> str | None:
    """Return the <PART> under content/<PART>/..."""
    parts = doc_path.parts
    if "content" not in parts:
        return None
    i = parts.index("content")
    if i + 1 < len(parts):
        return parts[i + 1]
    return None


def compute_assets_rel(doc_path: Path, url: str) -> str:
    part = find_part(doc_path)
    if not part:
        return url
    basename = Path(url).name
    target = Path("content") / part / "assets" / basename
    rel = os.path.relpath(target, start=doc_path.parent)
    return Path(rel).as_posix()


def rewrite_text(text: str, doc_path: Path):
    """
    Apply all allowed rewrites. Only modify the URL positions captured by regex groups.
    Returns: new_text, [(old_url, new_url), ...]
    """
    replacements = []

    def make_replacer(prefix_group=None, suffix_group=None):
        """
        Create a function to replace the URL-only portion inside matched constructs.
        """
        def repl(m):
            url = m.group("url")
            if not is_legacy_image_path(url):
                return m.group(0)

            new_url = compute_assets_rel(doc_path, url)
            if new_url == url:
                return m.group(0)

            replacements.append((url, new_url))

            if prefix_group is None:
                # Simple case: URL is a standalone group we can replace directly.
                start, end = m.span("url")
                return m.string[m.start():start] + new_url + m.string[end:m.end()]
            else:
                # HTML case with prefix/suffix groups preserved.
                return f"{m.group(prefix_group)}{new_url}{m.group(suffix_group)}"

        return repl

    new_text = text

    for pat in SUPPORTED:
        if pat is HTML_IMG:
            # HTML <img src="URL">
            new_text = pat.sub(make_replacer(prefix_group=1, suffix_group=3), new_text)
        else:
            new_text = pat.sub(make_replacer(), new_text)

    return new_text, replacements


# ------------------------------------------------------------------------------
# File processors
# ------------------------------------------------------------------------------

def process_md(path: Path, apply: bool, full_report: bool) -> int:
    text = path.read_text(encoding="utf-8")
    new_text, reps = rewrite_text(text, path)

    if reps:
        print(f"[report] {path} — {len(reps)} edit(s)")
        if full_report:
            for old, new in reps:
                print(f"    OLD: {old}")
                print(f"    NEW: {new}")
        if apply:
            path.write_text(new_text, encoding="utf-8")
            print(f"[fix] {path}")
    return len(reps)


def process_ipynb(path: Path, apply: bool, full_report: bool) -> int:
    try:
        nb = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[skip] {path}: cannot parse JSON ({e})")
        return 0

    total = 0
    all_reps = []

    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "markdown":
            src = "".join(cell.get("source", []))
            new_src, reps = rewrite_text(src, path)
            if reps:
                cell["source"] = [new_src]
                total += len(reps)
                all_reps.extend(reps)

    if total:
        print(f"[report] {path} — {total} edit(s)")
        if full_report:
            for old, new in all_reps:
                print(f"    OLD: {old}")
                print(f"    NEW: {new}")
        if apply:
            path.write_text(json.dumps(nb, ensure_ascii=False), encoding="utf-8")
            print(f"[fix] {path}")

    return total


# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Safely rewrite image URLs inside {figure}/{image}/markdown/html to <PART>/assets/<basename>.")
    ap.add_argument("--root", default="content", help="Directory to scan")
    ap.add_argument("--apply", action="store_true", help="Write changes")
    ap.add_argument("--full-report", action="store_true", help="Show all replacements")
    args = ap.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        print(f"ERROR: directory does not exist: {root}")
        return

    print(f"Mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"Full report: {'ON' if args.full_report else 'OFF'}")
    print(f"Scanning root: {root}\n")

    files_changed = 0
    edits_total = 0

    for p in root.rglob("*"):
        if p.suffix.lower() == ".md":
            edits = process_md(p, args.apply, args.full_report)
        elif p.suffix.lower() == ".ipynb":
            edits = process_ipynb(p, args.apply, args.full_report)
        else:
            continue

        if edits:
            files_changed += 1
            edits_total += edits

    print("\n===== SUMMARY =====")
    print(f"Files changed: {files_changed}")
    print(f"Total edits:   {edits_total}")
    if not args.apply:
        print("(dry-run: no changes written)")
    print("===================\n")


if __name__ == "__main__":
    main()
    