#!/usr/bin/env bash
set -euo pipefail

ROOT="content"         # default search root
APPLY=false
INCLUDE_PLAIN_FIGS=false
BACKUP_EXT=""          # e.g., ".bak" to keep backups

usage() {
  cat <<EOF
Usage: $0 [--root <dir>] [--apply] [--include-plain-figs] [--backup-ext .bak]

Find and replace figure references from:
  ./figs/<name>  -->  ../assets/<name>

Options:
  --root <dir>            Root directory to scan (default: content)
  --apply                 Apply changes (in-place). Default: dry-run (no modifications)
  --include-plain-figs    Also convert 'figs/<name>' (without leading './') to '../assets/<name>'
  --backup-ext <ext>      Keep a backup when applying (e.g., .bak). Default: no backup
  -h, --help              Show this help

Examples:
  Dry-run:
    $0 --root content

  Apply:
    $0 --root content --apply

  Apply and also convert 'figs/foo.png' (no leading ./):
    $0 --root content --include-plain-figs --apply

  Apply with backups:
    $0 --root content --apply --backup-ext .bak
EOF
}

# --- Parse args ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --root) ROOT="$2"; shift 2 ;;
    --apply) APPLY=true; shift 1 ;;
    --include-plain-figs) INCLUDE_PLAIN_FIGS=true; shift 1 ;;
    --backup-ext) BACKUP_EXT="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1"; usage; exit 1 ;;
  esac
done

if [[ ! -d "$ROOT" ]]; then
  echo "ERROR: Root directory does not exist: $ROOT" >&2
  exit 1
fi

echo
if $APPLY; then
  echo ">>> APPLY MODE — references will be rewritten"
  [[ -n "$BACKUP_EXT" ]] && echo ">>> Backups enabled with extension: $BACKUP_EXT"
else
  echo ">>> DRY RUN — no changes will be written"
fi
$INCLUDE_PLAIN_FIGS && echo "Note: Also converting 'figs/<name>' (no leading './')"

echo

# Collect candidate files that contain ./figs/ (and optionally figs/)
# --include limits to markdown and notebooks
# -I treats binary files as text; ipynb are JSON but often contain UTF-8
GREP_PAT='\.\/figs\/'   # literal "./figs/"

if $INCLUDE_PLAIN_FIGS; then
  # Combine both patterns:
  # We'll first collect files that contain either "./figs/" or "figs/"
  mapfile -t files < <(grep -RIl --include="*.md" --include="*.ipynb" -E '\.\/figs\/|(^|[^.])figs\/' "$ROOT" || true)
else
  mapfile -t files < <(grep -RIl --include="*.md" --include="*.ipynb" '\.\/figs\/' "$ROOT" || true)
fi

if [[ ${#files[@]} -eq 0 ]]; then
  echo "No files with matching patterns found under: $ROOT"
  exit 0
fi

# Function to count matches in a file
count_matches() {
  local file="$1"
  local cnt=0
  local c1 c2
  c1=$(grep -o '\.\/figs\/' "$file" | wc -l | tr -d ' ')
  cnt=$((cnt + c1))
  if $INCLUDE_PLAIN_FIGS; then
    # Count 'figs/' that are not preceded by a dot (avoid double counting ./figs/)
    # This is a heuristic; we'll still safely replace below.
    c2=$(grep -o -E '(^|[^.])figs\/' "$file" | wc -l | tr -d ' ')
    cnt=$((cnt + c2))
  fi
  echo "$cnt"
}

# Dry-run preview
if ! $APPLY; then
  total=0
  for f in "${files[@]}"; do
    n=$(count_matches "$f")
    if [[ "$n" -gt 0 ]]; then
      echo "$f  —  $n match(es)"
      # Show the lines with context
      # Show ./figs/ matches
      grep -n --color=always '\.\/figs\/' "$f" || true
      if $INCLUDE_PLAIN_FIGS; then
        # Show 'figs/' matches probably not preceded by dot
        grep -n -E '(^|[^.])figs\/' "$f" || true
      fi
      echo
      total=$((total + n))
    fi
  done
  echo "Summary: ${#files[@]} file(s) contain at least one candidate match."
  echo "Total matches reported (approximate): $total"
  echo "Run with --apply to perform replacements."
  exit 0
fi

# --- APPLY mode ---
# In-place replace using perl (-i is portable across macOS/Linux)
# 1) Replace "./figs/" -> "../assets/"
# 2) If requested, replace "figs/" (not already "./figs/") -> "../assets/"
#    We'll perform a cautious regex to avoid double-replacing the previous change.
for f in "${files[@]}"; do
  # Ensure parent dir for file exists (it should) and file is writable
  if [[ ! -w "$f" ]]; then
    echo "WARN: Skipping (not writable): $f"
    continue
  fi

  # Backups: perl -i$BACKUP_EXT; if empty, no backup
  if [[ -n "$BACKUP_EXT" ]]; then
    # Step 1: ./figs/ -> ../assets/
    perl -0777 -i"$BACKUP_EXT" -pe 's|\./figs/|../assets/|g' "$f"
    # Step 2 (optional): plain 'figs/' not preceded by dot or slash becomes ../assets/
    if $INCLUDE_PLAIN_FIGS; then
      perl -0777 -i"$BACKUP_EXT" -pe 's|(?<![./])figs/|../assets/|g' "$f"
    fi
  else
    perl -0777 -i -pe 's|\./figs/|../assets/|g' "$f"
    if $INCLUDE_PLAIN_FIGS; then
      perl -0777 -i -pe 's|(?<![./])figs/|../assets/|g' "$f"
    fi
  fi

  echo "Rewrote: $f"
done

echo
echo "Done."
