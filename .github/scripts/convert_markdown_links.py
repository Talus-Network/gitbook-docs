#!/usr/bin/env python3
import sys
import re
import os
from pathlib import Path

# Regex patterns
REF_DEF_RE = re.compile(r"^\[([^\]]+)\]:\s*(\S.*)$")
EXPLICIT_LINK_RE = re.compile(r"\[([^\]]+)\]\[([^\]]+)\]")
IMPLICIT_LINK_RE = re.compile(r"\[([^\]]+)\]\[\]")
BARE_LINK_RE = re.compile(r"\[([^\]]+)\](?!\()")

def convert_markdown_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # First pass: collect reference definitions
    refs = {}
    content_lines = []
    for line in lines:
        m = REF_DEF_RE.match(line.strip())
        if m:
            ref_id, url = m.groups()
            refs[ref_id] = url.strip()
        else:
            content_lines.append(line)

    content = ''.join(content_lines)

    # Replace [text][ref]
    def repl_explicit(match):
        text, ref = match.groups()
        url = refs.get(ref)
        return f'[{text}]({url})' if url else match.group(0)
    content = EXPLICIT_LINK_RE.sub(repl_explicit, content)

    # Replace [text][]
    def repl_implicit(match):
        text = match.group(1)
        url = refs.get(text)
        return f'[{text}]({url})' if url else match.group(0)
    content = IMPLICIT_LINK_RE.sub(repl_implicit, content)

    # Replace [text] (bare, not followed by '(')
    def repl_bare(match):
        text = match.group(1)
        url = refs.get(text)
        return f'[{text}]({url})' if url else match.group(0)
    content = BARE_LINK_RE.sub(repl_bare, content)

    # Remove trailing blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Write back if changed
    new_content = content.rstrip() + '\n'
    if new_content != ''.join(lines):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file_path}")
    else:
        print(f"No changes in {file_path}")

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for name in files:
            if name.endswith('.md'):
                convert_markdown_links(os.path.join(root, name))

def main():
    if len(sys.argv) < 2:
        print("Usage: python convert-markdown-links.py <directory1> [directory2] ...")
        sys.exit(1)
    for directory in sys.argv[1:]:
        if os.path.isdir(directory):
            print(f"Processing directory: {directory}")
            process_directory(directory)
        else:
            print(f"Warning: Directory '{directory}' does not exist, skipping...")

if __name__ == "__main__":
    main() 