#!/usr/bin/env bash

set -euo pipefail

# ----------------------------
# Default settings
# ----------------------------
APPLY=false
CSV_FILE=""

usage() {
    echo "Usage:"
    echo "  $0 --csv rename-map.csv [--apply]"
    echo ""
    echo "Default mode: dry run"
    exit 1
}

# ----------------------------
# Parse arguments
# ----------------------------
while [[ $# -gt 0 ]]; do
    case "$1" in
        --csv)
            CSV_FILE="$2"
            shift 2
            ;;
        --apply)
            APPLY=true
            shift 1
            ;;
        *)
            usage
            ;;
    esac
done

# ----------------------------
# Validate CSV input
# ----------------------------
if [[ -z "$CSV_FILE" ]]; then
    echo "ERROR: No CSV file provided."
    usage
fi

if [[ ! -f "$CSV_FILE" ]]; then
    echo "ERROR: CSV file does not exist: $CSV_FILE"
    exit 1
fi

# ----------------------------
# Mode information
# ----------------------------
if $APPLY; then
    echo ">>> APPLY MODE — files will be moved with git mv"
else
    echo ">>> DRY RUN — no files will be modified"
fi

echo

# ----------------------------
# Process CSV
# ----------------------------
while IFS=, read -r old new; do

    # Skip header or empty lines
    [[ -z "$old" ]] && continue
    [[ "$old" == "\"old\"" ]] && continue

    # Remove surrounding quotes safely
    old="${old%\"}"; old="${old#\"}"
    new="${new%\"}"; new="${new#\"}"

    # Skip malformed rows
    [[ -z "$old" || -z "$new" ]] && continue

    # Report action
    echo "Mapping: $old  →  $new"

    if $APPLY; then
        # Ensure target directory exists
        mkdir -p "$(dirname "$new")"
        git mv "$old" "$new"
    else
        echo "  Would move: $old → $new"
    fi

done < "$CSV_FILE"

echo
if $APPLY; then
    echo ">>> DONE — files moved"
else
    echo ">>> DONE — dry run only"
fi