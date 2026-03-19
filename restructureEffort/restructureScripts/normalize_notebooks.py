#!/usr/bin/env python3
import glob
import uuid
import nbformat as nbf
from pathlib import Path

def ensure_ids(nb):
    added = 0
    for c in nb.cells:
        if "id" not in c:
            c["id"] = uuid.uuid4().hex
            added += 1
    return added

def normalize_notebook(path):
    nb = nbf.read(path, as_version=4)

    # nbformat may already have inserted some IDs invisibly
    added_by_us = ensure_ids(nb)

    # ALWAYS write back: this saves nbformat’s silent fixes too
    nbf.write(nb, path)

    return added_by_us

def main():
    notebooks = glob.glob("content/**/*.ipynb", recursive=True)
    print(f"Found {len(notebooks)} notebooks…")

    total = 0
    for p in notebooks:
        added = normalize_notebook(Path(p))
        if added > 0:
            print(f"[normalized] {p} (+{added} ids)")
        total += added

    print(f"\nDone. Total IDs added explicitly: {total}")
    print("Note: Some IDs may have been added indirectly by nbformat during read().")

if __name__ == "__main__":
    main()
