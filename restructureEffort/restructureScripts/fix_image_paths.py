#!/usr/bin/env python3
import argparse
import json
import os
import re
from pathlib import Path
from typing import Tuple, List

# -------- Regex patterns --------
MD_IMAGE = re.compile(r'(!\[[^\]]*\]\()(?P<url>[^)\s]+)(\))')
HTML_IMAGE = re.compile(r'(<img[^>]*\ssrc=["\'])(?P<url>[^"\'>]+)(["\'])', re.IGNORECASE)
MYST_FIGURE = re.compile(r'(```\{figure\}\s+)(?P<url>\S+)(?P<rest>.*?\n```)', re.DOTALL)

# -------- URL helpers --------
def is_external(url: str) -> bool:
    return url.startswith(("http://", "https://", "#", "data:"))

def looks_like_image_path(url: str) -> bool:
    """Detect old figs/images or absolute content paths."""
    return any(p in url for p in [
        "figs/", "images/", "/figs/", "/images/",
        "content/", "../figs", "./figs", "../images", "./images"
    ])

def find_part(doc_path: Path) -> str | None:
    parts = doc_path.parts
    try:
        i = parts.index("content")
        return parts[i+1] if i+1 < len(parts) else None
    except ValueError:
        return None

def relative_to_assets(doc: Path, image_name: str) -> str:
    part = find_part(doc)
    if not part:
        return image_name
    target = Path("content") / part / "assets" / image_name
    rel = os.path.relpath(target, start=str(doc.parent))
    return Path(rel).as_posix()

# -------- Core rewrite logic --------
def rewrite_urls(text: str, doc: Path):
    """Return (new_text, replacements_list)."""
    replacements = []

    def handle(url: str):
        if is_external(url):
            return url, None
        if looks_like_image_path(url):
            new_url = relative_to_assets(doc, Path(url).name)
            if new_url != url:
                return new_url, (url, new_url)
        return url, None

    # Markdown image replacement
    def md_repl(m):
        url = m.group("url")
        new_url, rep = handle(url)
        if rep:
            replacements.append(rep)
        return f"{m.group(1)}{new_url}{m.group(3)}"

    # HTML <img> replacement
    def html_repl(m):
        url = m.group("url")
        new_url, rep = handle(url)
        if rep:
            replacements.append(rep)
        return f"{m.group(1)}{new_url}{m.group(3)}"

    # MyST figure replacement
    def fig_repl(m):
        url = m.group("url")
        new_url, rep = handle(url)
        rest = m.group("rest")
        if rep:
            replacements.append(rep)
        return f"{m.group(1)}{new_url}{rest}"

    text = MD_IMAGE.sub(md_repl, text)
    text = HTML_IMAGE.sub(html_repl, text)
    text = MYST_FIGURE.sub(fig_repl, text)

    return text, replacements


def process_md(path: Path, apply: bool, full_report: bool) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[skip] cannot read {path}: {e}")
        return 0

    new_text, replacements = rewrite_urls(text, path)
    edits = len(replacements)

    if edits > 0:
        print(f"[report] {path} — {edits} edit(s)")
        if full_report:
            for old, new in replacements:
                print(f"    OLD: {old}")
                print(f"    NEW: {new}")
        if apply:
            path.write_text(new_text, encoding="utf-8")
            print(f"[fix] {path}")

    return edits


def process_ipynb(path: Path, apply: bool, full_report: bool) -> int:
    try:
        raw = path.read_text(encoding="utf-8")
        nb = json.loads(raw)
    except Exception as e:
        print(f"[skip] cannot read/parse {path}: {e}")
        return 0

    total_replacements = 0
    replacements_per_file = []

    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "markdown":
            src = "".join(cell.get("source", []))
            new_src, replacements = rewrite_urls(src, path)
            if replacements:
                cell["source"] = [new_src]
                total_replacements += len(replacements)
                replacements_per_file.extend(replacements)

    if total_replacements > 0:
        print(f"[report] {path} — {total_replacements} edit(s)")
        if full_report:
            for old, new in replacements_per_file:
                print(f"    OLD: {old}")
                print(f"    NEW: {new}")

        if apply:
            path.write_text(json.dumps(nb, ensure_ascii=False), encoding="utf-8")
            print(f"[fix] {path}")

    return total_replacements


# -------- Main --------
def main():
    ap = argparse.ArgumentParser(description="Depth-aware rewrite of image paths to content/<PART>/assets/")
    ap.add_argument("--root", default="content", help="Directory to process (default: content)")
    ap.add_argument("--apply", action="store_true", help="Write changes (default: dry-run)")
    ap.add_argument("--full-report", action="store_true", help="Show each exact replacement")
    args = ap.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        print(f"ERROR: root directory not found: {root}")
        return

    print(f"Mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"Full report: {'ON' if args.full_report else 'OFF'}")
    print(f"Scanning: {root}\n")

    total_files = 0
    total_edits = 0

    for p in root.rglob("*"):
        if p.suffix.lower() == ".md":
            edits = process_md(p, args.apply, args.full_report)
        elif p.suffix.lower() == ".ipynb":
            edits = process_ipynb(p, args.apply, args.full_report)
        else:
            continue

        if edits > 0:
            total_files += 1
            total_edits += edits

    print("\n===== SUMMARY =====")
    print(f"Files with edits: {total_files}")
    print(f"Total edits: {total_edits}")
    if not args.apply:
        print("(dry-run — no changes written)")
    print("===================\n")


if __name__ == "__main__":
    main()