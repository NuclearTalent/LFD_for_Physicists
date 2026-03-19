#!/usr/bin/env bash

CSV="rename-map.csv"
TOC="_toc_new.yml"

# Detect macOS vs Linux sed
if sed --version >/dev/null 2>&1; then
    # GNU sed
    SED="sed -i"
else
    # macOS BSD sed
    SED="sed -i ''"
fi

while IFS=, read -r old new; do
    # Skip header
    if [[ "$old" == "\"old\"" ]]; then
        continue
    fi

    # Skip empty lines
    [[ -z "$old" ]] && continue

    # Remove surrounding quotes from CSV fields
    old="${old%\"}"
    old="${old#\"}"
    new="${new%\"}"
    new="${new#\"}"

    # Skip if any field accidentally becomes empty
    [[ -z "$old" || -z "$new" ]] && continue

    echo "Updating TOC: $old → $new"

    # Escape characters for sed
    old_esc=$(printf '%s' "$old" | sed -e 's/[\/&]/\\&/g')
    new_esc=$(printf '%s' "$new" | sed -e 's/[\/&]/\\&/g')

    # Replace inside _toc.yml
    eval $SED "\"s/$old_esc/$new_esc/g\"" "$TOC"

done < "$CSV"