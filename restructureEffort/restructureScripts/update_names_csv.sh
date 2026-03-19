#!/usr/bin/env bash

set -euo pipefail

CSV_FILE=""
TARGET=""
APPLY=false

usage() {
    echo "Usage:"
    echo "  $0 --csv file.csv --file target.md [--apply]"
    echo "  $0 --csv file.csv --dir  folder/    [--apply]"
    exit 1
}

# ---- Parse arguments ----
while [[ $# -gt 0 ]]; do
    case "$1" in
        --csv) CSV_FILE="$2"; shift 2 ;;
        --file) TARGET="$2"; shift 2 ;;
        --dir)  TARGET="$2"; shift 2 ;;
        --apply) APPLY=true; shift 1 ;;
        *) usage ;;
    esac
done

[[ -z "$CSV_FILE" || -z "$TARGET" ]] && usage
[[ ! -f "$CSV_FILE" ]] && { echo "CSV not found: $CSV_FILE"; exit 1; }

echo
if $APPLY; then
    echo ">>> APPLY MODE (changes will be written)"
else
    echo ">>> DRY RUN (no changes written)"
fi
echo

# ---- Process CSV ----
while IFS=, read -r raw_old raw_new; do

    # Remove surrounding quotes
    old="${raw_old//\"/}"
    new="${raw_new//\"/}"

    # Remove CR, LF, leading/trailing whitespace
    old=$(printf "%s" "$old" | tr -d '\r' | sed 's/^[ \t]*//;s/[ \t]*$//')
    new=$(printf "%s" "$new" | tr -d '\r' | sed 's/^[ \t]*//;s/[ \t]*$//')

    # Skip header and empty lines
    [[ "$old" == "old" ]] && continue
    [[ -z "$old" ]] && continue

    # Extract filenames
    old_file=$(basename "$old")
    new_file=$(basename "$new")

    # Escape sed meta chars (& / \)
    sed_old=$(printf "%s" "$old_file" | sed 's/[&/\]/\\&/g')
    sed_new=$(printf "%s" "$new_file" | sed 's/[&/\]/\\&/g')

    echo "Mapping: $old_file → $new_file"

    # ---- Single file mode ----
    if [[ -f "$TARGET" ]]; then
        if grep -q "$old_file" "$TARGET"; then
            if $APPLY; then
                sed -i "" "s|$sed_old|$sed_new|g" "$TARGET"
            else
                echo "  Would replace inside: $TARGET"
            fi
        fi

    # ---- Directory mode ----
    elif [[ -d "$TARGET" ]]; then
        while IFS= read -r file; do
            [[ -z "$file" ]] && continue
            if $APPLY; then
                sed -i "" "s|$sed_old|$sed_new|g" "$file"
            else
                echo "  Would replace inside: $file"
            fi
        done < <(grep -Rl "$old_file" "$TARGET" || true)

    else
        echo "ERROR: Target is neither file nor directory"
        exit 1
    fi

done < "$CSV_FILE"

echo
if $APPLY; then
    echo ">>> DONE (changes applied)"
else
    echo ">>> DONE (dry run)"
fi