import os
import json
import re

# Set the directory to your book content
TARGET_DIR = "./content"

def check_line_for_glue(file_path, line_num, line_text):
    """Checks if a string line contains a vulnerable glue call."""
    if "glue(" in line_text:
        # Simple regex to see if it uses string formatting or float casting
        # Safely ignores things like: f"{var}", str(var), float(var), or literal strings '...' / "..."
        is_safe = re.search(r'glue\s*\(\s*["\'][^"\']+["\']\s*,\s*(f["\']|str\(|float\(|int\(|["\'])', line_text)
        
        status = "✅ SAFE (Looks formatted/casted)" if is_safe else "⚠️  SUSPECT (Check if NumPy type)"
        print(f"[{status}] {file_path}:{line_num}")
        print(f"    Code: {line_text.strip()}\n")

def scan_notebook(file_path):
    """Parses .ipynb JSON structure to find glue calls in code cells."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for cell_idx, cell in enumerate(data.get('cells', []), 1):
            if cell.get('cell_type') == 'code':
                source = cell.get('source', [])
                # Source can be a list of strings or a single string
                if isinstance(source, str):
                    source = source.splitlines()
                
                for line_idx, line in enumerate(source, 1):
                    if "glue(" in line:
                        # Map to notebook-friendly location notation
                        check_line_for_glue(f"{file_path} (Cell {cell_idx})", line_idx, line)
    except Exception as e:
        print(f"Error reading notebook {file_path}: {e}")

def run_scanner(directory):
    print(f"Scanning target directory: {os.path.abspath(directory)}\n" + "="*60 + "\n")
    
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Check Markdown/MyST files
            if file.endswith('.md'):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            check_line_for_glue(file_path, line_num, line)
                except Exception as e:
                    print(f"Error reading markdown {file_path}: {e}")
            
            # Check Jupyter Notebooks
            elif file.endswith('.ipynb'):
                scan_notebook(file_path)

if __name__ == "__main__":
    run_scanner(TARGET_DIR)
