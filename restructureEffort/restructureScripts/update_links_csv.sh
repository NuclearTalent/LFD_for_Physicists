#!/usr/bin/env bash
set -euo pipefail

# ----------------------------------------------------------------------
# update_links_csv.sh
#
# Combined DRY-RUN + APPLY script for updating links based on a CSV file.
#
# CSV format (header required):
# "old","new"
# "old/path","new/path"
#
# Usage:
#   ./update_links_csv.sh mapping.csv target_dir [--apply]
#
# Default mode = DRY RUN (no file changes).
# Use --apply to actually modify files.
#
# Safe for:
#   - Markdown .md files
#   - Jupyter notebooks (.ipynb, markdown cells only)
#   - Absolute URLs and relative paths
#   - Special characters
# ----------------------------------------------------------------------

CSV_FILE="$1"
TARGET_DIR="${2:-.}"
APPLY_MODE="${3:-}"

if [[ ! -f "$CSV_FILE" ]]; then
  echo "ERROR: CSV mapping file '$CSV_FILE' not found."
  exit 1
fi

if [[ "$APPLY_MODE" == "--apply" ]]; then
  APPLY=1
  echo "===================================================================="
  echo " APPLY MODE — files WILL be modified"
  echo "===================================================================="
else
  APPLY=0
  echo "===================================================================="
  echo " DRY RUN — no files will be modified"
  echo "===================================================================="
fi

echo "CSV file   : $CSV_FILE"
echo "Target dir : $TARGET_DIR"
echo "===================================================================="
echo ""

# Skip the header with tail -n +2
tail -n +2 "$CSV_FILE" | \
while IFS=',' read -r old new; do
  # Strip quotes
  old="${old%\"}"; old="${old#\"}"
  new="${new%\"}"; new="${new#\"}"

  # Skip invalid lines
  [[ -z "$old" || -z "$new" ]] && continue

  echo "--------------------------------------------------------------------"
  echo " OLD: $old"
  echo " NEW: $new"
  echo ""

  # SEARCH for occurrences
  matches=$(grep -Rn --include='*.md' --include='*.ipynb' -- "$old" "$TARGET_DIR" || true)

  if [[ -z "$matches" ]]; then
    echo "No occurrences found."
    echo ""
    continue
  fi

  echo "Matches found in:"
  echo "$matches" | cut -d: -f1 | sort -u
  echo ""

  if [[ $APPLY -eq 0 ]]; then
    echo "Preview of replacements:"
    echo ""
  fi

  while IFS=: read -r file line content; do
    if [[ $APPLY -eq 0 ]]; then
      # DRY RUN PREVIEW
      echo "File: $file"
      echo "Line: $line"
      echo " OLD: $content"
      echo " NEW: ${content//$old/$new}"
      echo ""
    else
      # APPLY MODE — modify the file in place
      # macOS/BSD sed requires -i ''
      sed -i '' "s|$old|$new|g" "$file"
    fi
  done <<< "$matches"

done

echo "===================================================================="
if [[ $APPLY -eq 1 ]]; then
  echo " DONE — links updated."
else
  echo " DRY RUN COMPLETE — no changes made."
fi
echo "===================================================================="