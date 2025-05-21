#!/bin/bash

SUMMARY_FILE="SUMMARY.md"
SECTION_TITLE="## Looking for a home"

if [ ! -f "$SUMMARY_FILE" ]; then
  echo "SUMMARY.md not found!"
  exit 1
fi

if [ -z "$files" ]; then
  echo "No new markdown files detected."
  exit 0
fi

# Track new entries
NEW_ENTRIES=""

# Find uncategorized files
UNLISTED_FILES=""
for file in $files; do
  if ! grep -q "($file)" "$SUMMARY_FILE"; then
    UNLISTED_FILES+="$file"$'\n'
  fi
done

# If there are uncategorized files, add them
if [ -n "$UNLISTED_FILES" ]; then
  # Add section if it does not already exist
  if ! grep -Fxq "$SECTION_TITLE" "$SUMMARY_FILE"; then
    echo -e "\n$SECTION_TITLE\n" >> "$SUMMARY_FILE"
  fi

  # Add new files under "Looking for a home"
  for file in $UNLISTED_FILES; do
    ENTRY="* [$file]($file)"
    echo "$ENTRY" >> "$SUMMARY_FILE"
    NEW_ENTRIES+="$ENTRY"$'\n'
  done
fi

echo "Updated SUMMARY.md:"
cat "$SUMMARY_FILE"

# Save new entries as environment variable for later
echo "new_entries<<EOF" >> $GITHUB_ENV
echo "$NEW_ENTRIES" >> $GITHUB_ENV
echo "EOF" >> $GITHUB_ENV 