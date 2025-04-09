#!/bin/bash

# Check if project name is provided
if [ -z "$1" ]; then
  echo "Usage: ./create_project.sh <project-name>"
  exit 1
fi

PROJECT_NAME="$1"

# Create Vite project using Bun
bun create vite@latest "$PROJECT_NAME" && cd "$PROJECT_NAME"

# Create symbolic link for node_modules
ln -s $NODE_MODULES node_modules

echo "Project '$PROJECT_NAME' created and linked successfully."

