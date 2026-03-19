#!/usr/bin/env bash
outfile="rename-map.csv"
echo "\"old\",\"new\"" > "$outfile"

files=$(git ls-files "content/**/sec-[0-9][0-9]-*.md" "content/**/sec-[0-9][0-9]-*.ipynb")

for f in $files; do
    new=$(echo "$f" | sed -E 's/sec-[0-9][0-9]-/sec-/')
    printf "\"%s\",\"%s\"\n" "$f" "$new" >> "$outfile"
done

echo "Generated $outfile"