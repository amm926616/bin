#!/bin/bash

# Create 'zips' folder if it doesn't exist
mkdir -p zips

# Loop through the provided folder names as arguments
for folder in "$@"; do
    # Check if the folder exists
    if [ -d "$folder" ]; then
        # Create a zip file using the folder name
        zip_file="$folder.zip"
        # Zip the folder
        zip -r "$zip_file" "$folder"
        # Move the zip file to the 'zips' folder
        mv "$zip_file" zips/
        echo "Folder '$folder' has been zipped and moved to 'zips' folder."
    else
        echo "Error: Folder '$folder' does not exist. Skipping..."
    fi
done

