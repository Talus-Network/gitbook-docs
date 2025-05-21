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
COMMENT_LINE_RE = re.compile(r"^\s*<!--.*-->\s*$")

def convert_markdown_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # First pass: collect reference definitions and their line numbers
    refs = {}
    ref_lines = set()
    content_lines = []
    for i, line in enumerate(lines):
        m = REF_DEF_RE.match(line.strip())
        if m:
            ref_id, url = m.groups()
            refs[ref_id] = url.strip()
            ref_lines.add(i)
        else:
            content_lines.append((i, line))

    # Convert content lines to string
    content = ''.join(line for _, line in content_lines)

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

    # Split content back into lines
    new_lines = content.splitlines(True)

    # Remove reference lines and clean up trailing empty/comment lines
    final_lines = []
    in_reference_section = False
    for i, line in enumerate(new_lines):
        if i in ref_lines:
            in_reference_section = True
            continue
        if in_reference_section:
            if line.strip() and not COMMENT_LINE_RE.match(line):
                in_reference_section = False
                final_lines.append(line)
        else:
            final_lines.append(line)

    # Remove trailing empty lines and comments
    while final_lines and (not final_lines[-1].strip() or COMMENT_LINE_RE.match(final_lines[-1])):
        final_lines.pop()

    # Add a single newline at the end
    final_content = ''.join(final_lines).rstrip() + '\n'

    # Write back if changed
    if final_content != ''.join(lines):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        print(f"Updated {file_path}")
    else:
        print(f"No changes in {file_path}")

def process_path(path):
    path = Path(path)
    if path.is_file():
        if path.suffix == '.md':
            convert_markdown_links(path)
        else:
            print(f"Skipping non-markdown file: {path}")
    elif path.is_dir():
        print(f"Processing directory: {path}")
        for md_file in path.rglob('*.md'):
            convert_markdown_links(md_file)
    else:
        print(f"Warning: Path '{path}' does not exist, skipping...")

def main():
    if len(sys.argv) < 2:
        print("Usage: python convert-markdown-links.py <path1> [path2] ...")
        sys.exit(1)
    for path in sys.argv[1:]:
        process_path(path)

if __name__ == "__main__":
    main() 