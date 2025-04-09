#!/bin/bash

# Default to the current directory or use the first argument as the folder path
folder="${1:-$(pwd)}"

# Check if the folder exists
if [ ! -d "$folder" ]; then
  echo "Error: '$folder' is not a valid directory."
  exit 1
fi

# Find all files in the folder (non-recursive), shuffle, and pick the first one
random_file=$(find "$folder" -maxdepth 1 -type f | shuf -n 1)

if [ -z "$random_file" ]; then
  echo "No files found in the folder."
  exit 1
fi

echo "Opening: $random_file"

# Open the file with the default application
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  xdg-open "$random_file" &>/dev/null
elif [[ "$OSTYPE" == "darwin"* ]]; then
  open "$random_file" &>/dev/null
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  start "$random_file"
else
  echo "Unsupported operating system."
  exit 1
fi

