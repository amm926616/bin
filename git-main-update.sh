#!/bin/bash

# Check if a commit message was provided
if [ -z "$1" ]; then
  echo "Usage: ./git-main-update.sh \"commit message\""
  exit 1
fi

# Get current branch name
branch=$(git rev-parse --abbrev-ref HEAD)

# Run the git commands
git add .
git commit -m "$1"
git push -u origin "$branch"

