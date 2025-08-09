"""
process_new_macros_for_config_file.py

This script reads in LaTeX macros from a macros.sty file and inserts them
into a Jupyter Book _config.yml, removing the previous macros.

The macro filename is hardwired as macros.sty.

The script can handle \newcommand and \renewcommand definitions. 

Author: Dick Furnstahl
Date: 2025-01-28
"""

# imports
import os
import regex
import pathlib
import json
import uuid

# --------------------------------------------------------------------
# Define a recursive regex for (re)newcommand with multi-level braces
# --------------------------------------------------------------------
# Version from 28-Jan-2025 12:15am --> Works on all examples from Christian F.
#  iterated with chatGPT to get this version.
macro_pattern = regex.compile(
    r'''
    \\(?:newcommand|renewcommand)\s*
    \{\s*\\(\w+)\s*\}               # \newcommand{\macroName} --> saves macro name
    (?:\s*\[\s*(\d+)\s*\])?         # optional [n] --> if number of arguments
    \{\s*
    (?P<brace_content>                  # recursive matching of pattern
        (?:
            \\[{}]                      # \{ or \}
          | \\[a-zA-Z@]+[^\s{}\\]*      # multi-letter commands: \left(, \boldsymbol, etc.
          | \\[^a-zA-Z@\s{}\\]          # single-char punctuation commands: \, \%, \!, etc.
          | [^{}\\]                     # normal chars (not a brace/backslash)
          | \{(?&brace_content)\}       # recurse for nested braces
        )*
    )
    \s*\}
    ''',
    flags=regex.MULTILINE | regex.DOTALL | regex.VERBOSE
)

def parse_macros(file_path):
    """
    Parse LaTeX macros from file_path using the recursive macro_pattern.
    Returns a dict: { macro_name: definition_or_list }.
    If a macro takes arguments, store as [definition, arg_count].
    Otherwise store just the definition string.
    """
    file_path = pathlib.Path(file_path)
    if not file_path.is_file():
        return {}

    content = file_path.read_text(encoding='utf-8')
    macros = {}

    for match in macro_pattern.finditer(content):
        name = match.group(1)               # e.g. "data"
        arg_count_s = match.group(2)        # e.g. "1" or "2", or None
        definition = match.group('brace_content')  # the entire (possibly nested) definition

        if arg_count_s is None:
            macros[name] = definition
        else:
            macros[name] = [definition, int(arg_count_s)]

    return macros

def top_level_newlines(obj):
    """
    Return a JSON string with:
      - each top-level key-value pair on its own line
      - nested objects/arrays kept compact (no extra newlines)
    """
    # Build lines for each key-value pair at the top level
    lines = []
    for i, (k, v) in enumerate(obj.items()):
        # Dump the value alone (compact) so it doesn't contain newlines
        val_str = json.dumps(v, separators=(',', ':'))
        # Combine into `"key":value` format with appropriate spaces
        lines.append(f'        "{k}": {val_str}')
    
    # Join each key-value on its own line, with indentation if you like
    # and wrap in braces to form a valid JSON object
    inner = ",\n  ".join(lines)
    return f"{{\n  {inner}\n}}"

# --------------------------------------------------------------------
# Read and parse macros from an external file (e.g., macros.sty)
# --------------------------------------------------------------------
MACROS_FILE = "macros.sty"  # Adjust to the actual macro file
macros = parse_macros(MACROS_FILE)

# Append-adds at last
in_macros_block = False
in_preamble_block = False
input_config = '_config.yml'            # current _config.yml file
output_config = '_config_new_test.yml'  # temporary new _config.yml file

with open(input_config, 'r', encoding='utf-8') as fin, \
     open(output_config, 'w', encoding='utf-8') as fout:

    for line in fin:
        # Detect start of macros block
        # - Check for a line that (after optional indentation) has "macros:"
        if regex.match(r'^\s*macros:', line):
            in_macros_block = True
            fout.write(line)  # Write the line as is
            continue

        # Detect start of preamble block
        # - Check for a line that (after optional indentation) has "preamble: |"
        if regex.match(r'^\s*preamble:', line):
            in_preamble_block = True
            fout.write(line)  # Write the line as is
            continue

        if in_macros_block:
            # If line starts with '#', consider that the end of the macros block
            #  Print the html macros to the file, flattening and removing commas
            if line.strip().startswith('#'):
                in_macros_block = False
                temp = top_level_newlines(macros)
                new_temp = "\n".join(myline.rstrip(",") for myline in temp.splitlines())
                fout.writelines(new_temp[2:-2])
                fout.write("\n")
                fout.write(line)  # put back the line starting with '#'
                continue

            # If line starts with a double quote after whitespace, don't copy the line;
            #  these are the definitions to be removed.
            if regex.match(r'^\s*"', line):
                continue
            else:
                # Otherwise just keep writing the lines unmodified:
                fout.write(line)
                continue

        elif in_preamble_block:
            # if any line doesn't start with \newcommand or \renewcommand, end of block
            if not line.strip().startswith(r'\newcommand') and \
               not line.strip().startswith(r'\renewcommand'):
                in_preamble_block = False
                if os.path.isfile(MACROS_FILE):
                    with open(MACROS_FILE, "r", encoding="utf-8") as f:
                        for myline in f:
                            fout.write(f"          {myline}")
                fout.write("\n")
                fout.write(line)

        else:
            # Outside of macros block, just write lines unchanged
            fout.write(line)

# Save the old file with a unique id, at least for now (to avoid accidents)
# Rename the new file to be the configuration file.
unique_id = uuid.uuid4().hex
unique_config = f"{unique_id}{input_config}"
os.rename(input_config, unique_config)
os.rename(output_config, input_config)

