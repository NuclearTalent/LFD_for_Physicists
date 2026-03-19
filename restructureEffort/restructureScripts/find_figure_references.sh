#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <figure-directory>"
    echo "Example: $0 content/OtherTopics/figs"
    exit 1
fi

FIGDIR="$1"

if [[ ! -d "$FIGDIR" ]]; then
    echo "ERROR: Directory does not exist: $FIGDIR"
    exit 1
fi

# Collect all figure file basenames (e.g. "posterior.png")
mapfile -t FIGS < <(find "$FIGDIR" -type f -print0 | xargs -0 -n1 basename | sort -u)

echo "Found ${#FIGS[@]} figure files in $FIGDIR"
echo

# Search area: all markdown and ipynb under content/
SEARCHBASE="content"

# Loop over all figs and search for references in MD and IPYNB
for fig in "${FIGS[@]}"; do
    echo "=== Searching references to: $fig ==="

    # grep -R doesn't handle ipynb well unless we treat them as plain text
    # Use -I to ignore binary detection, treating everything as text
    matches=$(grep -RIl "$fig" "$SEARCHBASE" --include="*.md" --include="*.ipynb" || true)

    if [[ -z "$matches" ]]; then
        echo "  No references found."
    else
        for m in $matches; do
            echo "  → $m"
        done
    fi

    echo
done