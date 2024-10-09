#!/bin/bash

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "ffmpeg could not be found. Please install ffmpeg first."
    exit 1
fi

# Loop through all .m4a files in the current directory
for file in *.m4a; do
    # Check if the file exists
    if [[ -f "$file" ]]; then
        # Extract the base filename without extension
        base="${file%.m4a}"
        # Convert .m4a to .ogg using ffmpeg
        ffmpeg -i "$file" "${base}.ogg"
        echo "Converted: $file -> ${base}.ogg"
    else
        echo "No .m4a files found in the directory."
        exit 0
    fi
done

echo "Batch conversion completed!"
