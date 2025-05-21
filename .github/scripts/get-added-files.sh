#!/bin/bash

# Get the base branch from the first argument
BASE_BRANCH=$1

# Fetch the base branch
git fetch origin $BASE_BRANCH

# Get list of added markdown files
ADDED_FILES=$(git diff --diff-filter=A --name-only origin/$BASE_BRANCH... | grep '\.md$' || true)

echo "Added files: $ADDED_FILES"

# Set environment variable for added files
if [ -n "$ADDED_FILES" ]; then
  echo "files<<EOF" >> $GITHUB_ENV
  echo "$ADDED_FILES" >> $GITHUB_ENV
  echo "EOF" >> $GITHUB_ENV
else
  echo "files=" >> $GITHUB_ENV
fi 