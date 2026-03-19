#!/usr/bin/env bash

set -euo pipefail

TOC_FILE=""
STRICT=false

usage() {
    echo "Usage: $0 --toc _toc.yml [--strict]"
    exit 1
}

# ---- Parse arguments ----
while [[ $# -gt 0 ]]; do
    case "$1" in
        --toc)
            TOC_FILE="$2"
            shift 2
            ;;
        --strict)
            STRICT=true
            shift 1
            ;;
        *)
            usage
            ;;
    esac
done

[[ -z "$TOC_FILE" ]] && usage
[[ ! -f "$TOC_FILE" ]] && { echo "ERROR: file not found: $TOC_FILE"; exit 1; }

echo "Validating paths in: $TOC_FILE"
echo

# ---- Extract file paths robustly ----
paths=$(grep -E "^[[:space:]]*file:[[:space:]]*" "$TOC_FILE" \
        | grep -v "^[[:space:]]*#" \
        | sed 's/^[[:space:]]*file:[[:space:]]*//' \
)

missing=()
directories=()

while IFS= read -r path; do
    # normalize line
    path=$(echo "$path" | tr -d '\r' | xargs)

    [[ -z "$path" ]] && continue

    if [[ ! -e "$path" ]]; then
        echo "❌ Missing: $path"
        missing+=("$path")
        continue
    fi

    if [[ -d "$path" ]]; then
        echo "⚠️  Warning: directory referenced as file: $path"
        directories+=("$path")
        continue
    fi

    echo "✔ Found: $path"

done <<< "$paths"

echo
echo "=========================================="
echo "Summary"
echo "=========================================="

if [[ ${#missing[@]} -eq 0 ]]; then
    echo "✔ No missing files"
else
    echo "❌ Missing files (${#missing[@]}):"
    printf '   %s\n' "${missing[@]}"
fi

if [[ ${#directories[@]} -gt 0 ]]; then
    echo
    echo "⚠️ Directories referenced as files (${#directories[@]}):"
    printf '   %s\n' "${directories[@]}"
fi

echo

if [[ "$STRICT" == true ]]; then
    if [[ ${#missing[@]} -gt 0 || ${#directories[@]} -gt 0 ]]; then
        echo "STRICT MODE: failing due to errors."
        exit 1
    fi
fi

echo "Done."