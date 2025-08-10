#!/usr/bin/env python3
import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Optional

HEADING_RE = re.compile(r'^(?P<hashes>#{1,6})(?P<space>\s+)(?P<title>.*?)(\s+#+\s*)?$')
FENCE_RE = re.compile(r'^(```|~~~)')  # start or end of fenced blocks
YAML_FM_DELIM = re.compile(r'^---\s*$')
NUM_PREFIX_RE = re.compile(r'^\s*\d+(\.\d+)*\s*[:.)-]?\s+')

def slugify(text: str, maxlen: int = 60) -> str:
    text = text.strip().lower()
    text = re.sub(r'[`~!@#$%^&*()+={}\[\]|\\:;"\',.<>/?]+', ' ', text)
    text = re.sub(r'\s+', '-', text)
    text = text.strip('-')
    if not text:
        text = "section"
    return text[:maxlen].rstrip('-')

def read_file_lines(p: Path) -> List[str]:
    with p.open('r', encoding='utf-8') as f:
        return f.readlines()

def strip_yaml_front_matter(lines: List[str]) -> Tuple[List[str], List[str]]:
    """Return (without_front_matter, front_matter_lines)."""
    if len(lines) >= 3 and YAML_FM_DELIM.match(lines[0]):
        fm = [lines[0]]
        i = 1
        while i < len(lines):
            fm.append(lines[i])
            if YAML_FM_DELIM.match(lines[i]):
                break
            i += 1
        return (lines[i+1:], fm)
    return (lines, [])

def detect_headings(lines: List[str], split_level: int) -> List[Tuple[int, int, str]]:
    """
    Find headings of the requested level outside fenced code blocks.
    Returns list of (line_index, level, title).
    """
    in_fence = False
    fence_marker = None
    found = []

    for i, line in enumerate(lines):
        m_fence = FENCE_RE.match(line.lstrip())
        if m_fence:
            marker = m_fence.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker
            else:
                if marker == fence_marker:
                    in_fence = False
                    fence_marker = None
            continue

        if in_fence:
            continue

        m = HEADING_RE.match(line)
        if m:
            lvl = len(m.group('hashes'))
            if lvl == split_level:
                title = m.group('title').strip()
                found.append((i, lvl, title))
    return found

def demote_headings(chunk: List[str], split_level: int) -> List[str]:
    """
    Demote headings so that split_level becomes 1, split_level+1 -> 2, etc.
    Ignore headings inside fenced code blocks.
    """
    in_fence = False
    fence_marker = None
    out = []
    shift = split_level - 1

    for line in chunk:
        m_fence = FENCE_RE.match(line.lstrip())
        if m_fence:
            marker = m_fence.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker
            else:
                if marker == fence_marker:
                    in_fence = False
                    fence_marker = None
            out.append(line)
            continue

        if not in_fence:
            m = HEADING_RE.match(line)
            if m:
                level = len(m.group('hashes'))
                new_level = max(1, level - shift)
                title = m.group('title').rstrip()
                line = f"{'#' * new_level} {title}\n"
        out.append(line)
    return out

def split_by_headings(lines: List[str], split_level: int) -> List[Tuple[str, List[str], Tuple[int,int]]]:
    """
    Split into chunks by headings of `split_level`.
    Returns list of (section_title, section_lines_including_heading, (start_idx, end_idx))
    """
    headings = detect_headings(lines, split_level)
    if not headings:
        return []

    chunks = []
    for idx, (start_i, _, title) in enumerate(headings):
        end_i = headings[idx + 1][0] if idx + 1 < len(headings) else len(lines)
        chunk = lines[start_i:end_i]
        chunks.append((title, chunk, (start_i, end_i)))
    return chunks

def normalize_heading_title(title: str, strip_numbers: bool) -> str:
    t = title.strip()
    if strip_numbers:
        t = NUM_PREFIX_RE.sub('', t).strip()
    return t if t else "Section"

def write_chunks(
    base_dir: Path,
    base_stem: str,
    chunks: List[Tuple[str, List[str], Tuple[int,int]]],
    split_level: int,
    strip_numbers: bool,
    prefix: str,
    outdir: Optional[Path],
    overwrite: bool,
) -> List[Tuple[str, Path]]:
    """
    Write each chunk as its own file. Returns list of (display_title, path).
    """
    if outdir is None:
        outdir = base_dir / base_stem  # e.g., chapter2/
    outdir.mkdir(parents=True, exist_ok=True)

    written = []
    for k, (raw_title, raw_chunk, _range) in enumerate(chunks, start=1):
        title = normalize_heading_title(raw_title, strip_numbers=strip_numbers)
        # Demote headings
        chunk = demote_headings(raw_chunk, split_level=split_level)

        # Replace the first heading line with a clean H1
        for i, line in enumerate(chunk):
            m = HEADING_RE.match(line)
            if m:
                chunk[i] = f"# {title}\n"
                break

        slug = slugify(title)
        fname = f"{prefix}{k:02d}-{slug}.md"
        fpath = outdir / fname

        if fpath.exists() and not overwrite:
            raise FileExistsError(f"Refusing to overwrite existing file: {fpath}. Use --force to overwrite.")

        with fpath.open('w', encoding='utf-8') as f:
            f.writelines(chunk)

        written.append((title, fpath))

    return written

def guess_rel_from_base(base_dir: Path, p: Path) -> str:
    return p.relative_to(base_dir).as_posix()

def trim_trailing_blank_lines(lines: List[str]) -> List[str]:
    j = len(lines)
    while j > 0 and lines[j-1].strip() == "":
        j -= 1
    return lines[:j] + (["\n"] if j and not lines[j-1].endswith("\n") else [])

def main():
    ap = argparse.ArgumentParser(
        description="Split a Jupyter Book chapter Markdown file into section files AND rewrite the top-level file to only its intro. The original file is renamed to a backup."
    )
    ap.add_argument("input", metavar="CHAPTER_FILE",
                help="Path to the chapter Markdown file (e.g., chapter2.md)")
    ap.add_argument("--split-level", type=int, default=2, help="Heading level to split on (default: 2 for '##').")
    ap.add_argument("--strip-numbers", action="store_true",
                    help="Strip numeric prefixes like '2.1 ' from new file titles.")
    ap.add_argument("--prefix", default="sec-", help="Filename prefix for split files (default: 'sec-').")
    ap.add_argument("--outdir", default=None,
                    help="Output directory for split files (default: <input_stem>/).")
    ap.add_argument("--backup-suffix", default="-orig",
                    help="Suffix appended to the original filename when renaming (default: '-orig').")
    ap.add_argument("--force", action="store_true", help="Overwrite existing split files/top-level file if present.")
    args = ap.parse_args()

    in_path = Path(args.input).resolve()
    if not in_path.exists():
        sys.exit(f"Input file not found: {in_path}")

    base_dir = in_path.parent
    base_stem = in_path.stem
    outdir = Path(args.outdir).resolve() if args.outdir else None

    # Read and parse original
    original_lines = read_file_lines(in_path)
    body_lines, fm_lines = strip_yaml_front_matter(original_lines)

    chunks = split_by_headings(body_lines, split_level=args.split_level)
    if not chunks:
        sys.exit(f"No level {args.split_level} headings ('{'#'*args.split_level} ') found outside code fences in {in_path.name}.")

    # Determine intro (content before the first split-level heading)
    first_start = chunks[0][2][0]  # start index of first chunk within body_lines
    intro_lines = body_lines[:first_start]
    intro_lines = trim_trailing_blank_lines(intro_lines)

    # Prepare new top-level content = (front matter if any) + intro
    new_top_lines = fm_lines + intro_lines

    # Backup original file (rename)
    backup_path = in_path.with_name(f"{base_stem}{args.backup_suffix}{in_path.suffix}")
    if backup_path.exists() and not args.force:
        sys.exit(f"Backup target already exists: {backup_path} (use --force to overwrite).")
    in_path.rename(backup_path)

    # Write new top-level file at the original path (contains only intro/preface)
    if in_path.exists() and not args.force:
        sys.exit(f"Refusing to overwrite top-level file: {in_path} (use --force).")
    with in_path.open('w', encoding='utf-8') as f:
        f.writelines(new_top_lines)

    # Write split section files
    written = write_chunks(
        base_dir=base_dir,
        base_stem=base_stem,
        chunks=chunks,
        split_level=args.split_level,
        strip_numbers=args.strip_numbers,
        prefix=args.prefix,
        outdir=outdir,
        overwrite=args.force,
    )

    # Print a suggested _toc.yml snippet
    print("\nSuggested _toc.yml snippet:\n")
    print("  - file: " + guess_rel_from_base(base_dir, in_path))
    print("    sections:")
    for title, path in written:
        rel = guess_rel_from_base(base_dir, path)
        print(f"      - file: {rel}")

    print("\n# Notes:")
    print(f"# - Original file was renamed to: {guess_rel_from_base(base_dir, backup_path)}")
    print("# - The new top-level file now contains ONLY the intro (content before the first split-level heading).")
    print("# - Split files have their headings demoted so each starts with a single '# Title'.")
    print("# - If your chapter lives at 'chapter2/index.md', adjust paths accordingly in _toc.yml.")
    print("# - Run again with --split-level=3 to split H3 subsections into files.")

if __name__ == "__main__":
    main()
