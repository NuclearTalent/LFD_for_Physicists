import json
import re
import argparse
from pathlib import Path

def find_imports(search_path):
    imports = set()
    pattern = re.compile(r"^\s*(import\s+\S+|from\s+\S+\s+import\s+\S+)")

    for path in Path(search_path).rglob("*.ipynb"):
        nb = json.loads(path.read_text(encoding="utf-8"))
        for cell in nb.get("cells", []):
            for line in cell.get("source", []):
                m = pattern.match(line)
                if m:
                    imports.add(m.group(0).strip())

    return imports

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find all unique import statements in Jupyter notebooks."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Directory to search recursively (default: current directory)",
    )
    args = parser.parse_args()

    imports = find_imports(args.path)
    if imports:
        print("\n".join(sorted(imports)))
    else:
        print("No import statements found.")
        
