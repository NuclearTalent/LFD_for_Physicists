#!/usr/bin/env bash
#
# Advanced TOC validator for Jupyter Book
#
# Checks:
#   ✔ Missing files
#   ✔ Duplicate references (should be referenced exactly once)
#   ✔ Orphan files not listed in _toc.yml
#   ✔ Heading match (Markdown/IPYNB)
#   ✔ Output JSON + CSV summaries
#

set -euo pipefail

TOC_FILE=""
ROOT_DIR="content"
OUT_JSON="toc_validation.json"
OUT_CSV="toc_validation.csv"

usage() {
    echo "Usage:"
    echo "  $0 --toc _toc.yml [--root content] [--json out.json] [--csv out.csv]"
    echo "  On Mac OS X Silicon run with newer bash via homebrew:"
    echo "  /opt/homebrew/bin/bash $0"
    exit 1
}

# -------------------------------
# Parse arguments
# -------------------------------
while [[ $# -gt 0 ]]; do
    case "$1" in
        --toc)
            TOC_FILE="$2"; shift 2 ;;
        --root)
            ROOT_DIR="$2"; shift 2 ;;
        --json)
            OUT_JSON="$2"; shift 2 ;;
        --csv)
            OUT_CSV="$2"; shift 2 ;;
        *)
            usage ;;
    esac
done

[[ -z "$TOC_FILE" ]] && usage
[[ ! -f "$TOC_FILE" ]] && { echo "ERROR: TOC not found: $TOC_FILE"; exit 1; }

echo "🔍 Validating: $TOC_FILE"
echo "📁 Content root: $ROOT_DIR"
echo


# -------------------------------
# Extract file paths from TOC
# -------------------------------
toc_paths=$(grep -E "^[[:space:]]*file:[[:space:]]*" "$TOC_FILE" \
    | grep -v "^[[:space:]]*#" \
    | sed 's/^[[:space:]]*file:[[:space:]]*//' \
    | tr -d '\r' \
    | xargs -L1 echo)

declare -A count_refs
missing_files=()
directories=()
headings_mismatch=()


# -------------------------------
# Function to extract h1 from MD
# -------------------------------
extract_md_heading() {
    local f="$1"
    grep -m 1 "^# " "$f" | sed 's/^# //'
}

# -------------------------------
# Function to extract heading from IPYNB
# -------------------------------
extract_ipynb_heading() {
    local f="$1"
    # extract first markdown cell, first heading
    jq -r '
        .cells[] 
        | select(.cell_type=="markdown") 
        | .source[] 
        | select(startswith("# "))
        ' "$f" 2>/dev/null | head -n 1 | sed 's/^# //'
}


# -------------------------------
# Validate TOC entries
# -------------------------------
all_project_files=$(find "$ROOT_DIR" -type f | sort)


for p in $toc_paths; do
    path=$(echo "$p" | xargs)

    # Safe increment: treat undefined as 0
    count_refs["$path"]=$(( ${count_refs["$path"]:-0} + 1 ))

    if [[ ! -e "$path" ]]; then
        echo "❌ Missing: $path"
        missing_files+=("$path")
        continue
    fi

    if [[ -d "$path" ]]; then
        echo "⚠️ Directory referenced as file: $path"
        directories+=("$path")
        continue
    fi

    # -----------------------------------------
    # Heading check (only MD & IPYNB)
    # -----------------------------------------
    declared_title=$(grep -A1 "file:[[:space:]]*$path" -n "$TOC_FILE" \
        | grep -E "title:" \
        | sed 's/.*title:[[:space:]]*//; s/"//g' \
        || true)

    if [[ -n "$declared_title" ]]; then
        if [[ "$path" == *.md ]]; then
            h=$(extract_md_heading "$path")
        elif [[ "$path" == *.ipynb ]]; then
            h=$(extract_ipynb_heading "$path")
        else
            continue
        fi

        # normalize case for comparison
        h_norm=$(echo "$h" | tr '[:upper:]' '[:lower:]')
        t_norm=$(echo "$declared_title" | tr '[:upper:]' '[:lower:]')

        if [[ "$t_norm" != "$h_norm" ]]; then
            echo "⚠️ Heading mismatch: $path"
            echo "   TOC:     $declared_title"
            echo "   Heading: $h"
            headings_mismatch+=("$path|$declared_title|$h")
        fi
    fi
done


# -------------------------------
# Find orphan files
# -------------------------------
declare -A toc_map
for p in $toc_paths; do toc_map["$p"]=1; done

orphans=()
while IFS= read -r f; do
    [[ -n "${toc_map[$f]:-}" ]] && continue
    # ignore hidden files, checkpoint dirs, etc.
    case "$f" in
        *.py|*.txt|*.csv|*/.ipynb_checkpoints/*)
            continue;;
    esac
    orphans+=("$f")
done <<< "$all_project_files"


# -------------------------------
# Write JSON summary
# -------------------------------
{
    echo "{"
