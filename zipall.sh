#!/bin/bash

# Create a "zips" directory if it doesn't exist
mkdir -p zips

# Loop through each subdirectory in the current directory
for folder in */; do
    # Remove the trailing slash to get the folder name
    folder_name="${folder%/}"
    
    # Create a zip file with the folder name in the "zips" directory
    zip -r "zips/${folder_name}.zip" "$folder_name"
    
    # Optionally, you can remove the original folder after zipping
    # Uncomment the following line to remove the original folder
    # rm -r "$folder_name"
done

echo "All folders zipped and placed in the 'zips' directory."

