#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple, Optional

# ---------- Regexes ----------
HEADING_RE = re.compile(r'^(?P<hashes>#{1,6})(?P<space>\s+)(?P<title>.*?)(\s+#+\s*)?$')
FENCE_RE = re.compile(r'^([ \t]*)(```|~~~)')  # start or end of fenced blocks (incl. MyST)
YAML_FM_DELIM = re.compile(r'^---\s*$')
NUM_PREFIX_RE = re.compile(r'^\s*\d+(\.\d+)*\s*[:.)-]?\s+')
LABEL_RE = re.compile(r'^\([^)]+\)=\s*$')  # MyST label line, e.g. (sec:foo)=
ATTR_TAIL_RE = re.compile(r'^(?P<core>.*?)(?P<attrs>\s+\{[^\}]+\})\s*$')

# ---------- Helpers ----------
def slugify(text: str, maxlen: int = 60) -> str:
    text = text.strip().lower()
    text = re.sub(r'[`~!@#$%^&*()+={}\[\]|\\:;"\',.<>/?]+', ' ', text)
    text = re.sub(r'\s+', '-', text).strip('-')
    return (text or "section")[:maxlen].rstrip('-')

def read_file_lines(p: Path) -> List[str]:
    with p.open('r', encoding='utf-8') as f:
        return f.readlines()

def strip_yaml_front_matter(lines: List[str]) -> Tuple[List[str], List[str]]:
    """Return (body_without_front_matter, front_matter_lines)."""
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
        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group(2)
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

def split_core_and_attrs(title: str) -> Tuple[str, str]:
    """
    Split a heading's title into (core, attrs), preserving attrs like '{#id .class}'.
    """
    m = ATTR_TAIL_RE.match(title.strip())
    if m:
        return m.group('core').rstrip(), m.group('attrs')
    return title.strip(), ""

def normalize_heading_title(title: str, strip_numbers: bool) -> str:
    t = title.strip()
    if strip_numbers:
        t = NUM_PREFIX_RE.sub('', t).strip()
    return t if t else "Section"

def adjust_start_for_label(lines: List[str], start_i: int, max_blank_before_label: int) -> int:
    """
    If a MyST label '(name)=' appears within 'max_blank_before_label' blank lines above the heading,
    shift the chunk start upward so the label (and the adjacent blank if any) travel with the section.
    """
    j = start_i - 1
    blanks = 0
    # Walk up over up to max_blank_before_label blank lines
    while j >= 0 and blanks < max_blank_before_label and lines[j].strip() == "":
        blanks += 1
        j -= 1
    if j >= 0 and LABEL_RE.match(lines[j]):
        # Include the label line and any blanks between label and heading
        return j
    return start_i

def demote_headings(chunk: List[str], split_level: int) -> List[str]:
    """
    Demote headings so that split_level -> H1, split_level+1 -> H2, etc.
    (Ignore headings inside fenced code blocks.)
    """
    in_fence = False
    fence_marker = None
    out = []
    shift = split_level - 1

    for line in chunk:
        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group(2)
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

def split_by_headings(lines: List[str], split_level: int, max_blank_before_label: int
                      ) -> List[Tuple[str, List[str], Tuple[int,int]]]:
    """
    Split into chunks by headings of `split_level`.
    Returns list of (section_title, section_lines (incl. attached label), (start_idx, end_idx))
    """
    headings = detect_headings(lines, split_level)
    if not headings:
        return []

    chunks = []
    for idx, (start_i, _, title) in enumerate(headings):
        adj_start = adjust_start_for_label(lines, start_i, max_blank_before_label)
        end_i = headings[idx + 1][0] if idx + 1 < len(headings) else len(lines)
        chunk = lines[adj_start:end_i]
        chunks.append((title, chunk, (adj_start, end_i)))
    return chunks

def trim_trailing_blank_lines(lines: List[str]) -> List[str]:
    j = len(lines)
    while j > 0 and lines[j-1].strip() == "":
        j -= 1
    # Keep existing newline on the last non-blank line (if any)
    return lines[:j] + (["\n"] if j and not lines[j-1].endswith("\n") else [])

def guess_rel_from_base(base_dir: Path, p: Path) -> str:
    return p.relative_to(base_dir).as_posix()

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
        # Demote headings inside the chunk first
        chunk = demote_headings(raw_chunk, split_level=split_level)

        # Find first heading line to rewrite as H1, preserving attrs and stripping numeric prefixes
        display_title = None
        for i, line in enumerate(chunk):
            m = HEADING_RE.match(line)
            if m:
                orig_title = m.group('title').rstrip()
                core, attrs = split_core_and_attrs(orig_title)
                clean_core = normalize_heading_title(core, strip_numbers=strip_numbers)
                chunk[i] = f"# {clean_core}{attrs}\n"
                display_title = clean_core
                break

        if display_title is None:
            # Fallback: no heading found (unexpected); synthesize one from original detected title
            core, attrs = split_core_and_attrs(raw_title)
            clean_core = normalize_heading_title(core, strip_numbers=strip_numbers)
            chunk.insert(0, f"# {clean_core}{attrs}\n")
            display_title = clean_core

        slug = slugify(display_title)
        fname = f"{prefix}{k:02d}-{slug}.md"
        fpath = outdir / fname

        if fpath.exists() and not overwrite:
            raise FileExistsError(f"Refusing to overwrite existing file: {fpath}. Use --force to overwrite.")

        with fpath.open('w', encoding='utf-8') as f:
            f.writelines(chunk)

        written.append((display_title, fpath))

    return written

# ---------- Main ----------
def main():
    ap = argparse.ArgumentParser(
        description="Split a Jupyter Book chapter Markdown file into section files, rewrite the top-level file to only its intro, and rename the original to a backup."
    )
    ap.add_argument("CHAPTER_FILE",
                    help="Path to the chapter Markdown file (e.g., chapter2.md)")
    ap.add_argument("--split-level", type=int, default=2,
                    help="Heading level to split on (default: 2 for '##').")
    ap.add_argument("--max-blank-before-label", type=int, default=1,
                    help="Max number of blank lines allowed between a MyST label '(name)=' and the heading below for the label to be attached to that section (default: 1).")
    ap.add_argument("--strip-numbers", action="store_true",
                    help="Strip numeric prefixes like '2.1 ' from new file titles.")
    ap.add_argument("--prefix", default="sec-",
                    help="Filename prefix for split files (default: 'sec-').")
    ap.add_argument("--outdir", default=None,
                    help="Output directory for split files (default: <input_stem>/).")
    ap.add_argument("--backup-suffix", default="-orig",
                    help="Suffix appended to the original filename when renaming (default: '-orig').")
    ap.add_argument("--force", action="store_true",
                    help="Overwrite existing split files/top-level file/backup if present.")

    args = ap.parse_args()

    in_path = Path(args.CHAPTER_FILE).resolve()
    if not in_path.exists():
        sys.exit(f"Input file not found: {in_path}")

    base_dir = in_path.parent
    base_stem = in_path.stem
    outdir = Path(args.outdir).resolve() if args.outdir else None

    # Read and parse original
    original_lines = read_file_lines(in_path)
    body_lines, fm_lines = strip_yaml_front_matter(original_lines)

    # Identify section chunks (with label capture)
    chunks = split_by_headings(
        body_lines,
        split_level=args.split_level,
        max_blank_before_label=args.max-blank-before-label if hasattr(args, 'max-blank-before-label') else args.max_blank_before_label
    )  # (title, lines, (start, end))

    if not chunks:
        sys.exit(f"No level {args.split_level} headings ('{'#'*args.split_level} ') found outside code fences in {in_path.name}.")

    # Determine intro (content before the first section, respecting attached labels)
    first_start = chunks[0][2][0]  # adjusted start index of first chunk within body_lines
    intro_lines = trim_trailing_blank_lines(body_lines[:first_start])

    # Backup original file
    backup_path = in_path.with_name(f"{base_stem}{args.backup_suffix}{in_path.suffix}")
    if backup_path.exists() and not args.force:
        sys.exit(f"Backup target already exists: {backup_path} (use --force to overwrite).")
    # If --force and backup exists, delete it first
    if backup_path.exists() and args.force:
        backup_path.unlink()
    in_path.rename(backup_path)

    # Write new top-level file (front matter + intro only) at the original path
    if in_path.exists() and not args.force:
        sys.exit(f"Refusing to overwrite top-level file: {in_path} (use --force).")
    with in_path.open('w', encoding='utf-8') as f:
        f.writelines(fm_lines + intro_lines)

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
    for display_title, path in written:
        rel = guess_rel_from_base(base_dir, path)
        print(f"      - file: {rel}")

    print("\n# Notes:")
    print(f"# - Original file was renamed to: {guess_rel_from_base(base_dir, backup_path)}")
    print("# - The new top-level file now contains ONLY the intro (content before the first split-level heading/label).")
    print("# - Split files keep labels above the heading if they were within the allowed blank-line window.")
    print("# - Heading attributes like '{#id .class}' are preserved; numeric prefixes can be stripped from the visible title with --strip-numbers.")
    print("# - Use --split-level=3 to split H3 subsections instead of H2.")
    print("# - Adjust --prefix and --outdir to control filenames and destination directory.")

if __name__ == "__main__":
    main()
