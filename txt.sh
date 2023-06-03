#!/bin/bash

# Check if docx2txt is installed
if ! command -v docx2txt &> /dev/null; then
    echo "Error: docx2txt is not installed. Please install docx2txt and try again."
    exit 1
fi

# Set the folder path where the .docx files are located
folder_path=$(pwd)

# Check if the folder exists
if [ ! -d "$folder_path" ]; then
    echo "Error: Folder $folder_path does not exist."
    exit 1
fi

# Convert .docx files to .txt and delete .docx files
for file in "$folder_path"/*.docx; do
    if [ -f "$file" ]; then
        # Get the file name without extension
        filename=$(basename "$file" .docx)
        
        # Convert .docx to .txt
        docx2txt "$file" "$folder_path/$filename.txt"
        
        if [ $? -eq 0 ]; then
            echo "Converted $file to $folder_path/$filename.txt"
            
            # Delete .docx file
            rm "$file"
            echo "Deleted $file"
        else
            echo "Error converting $file to $folder_path/$filename.txt"
        fi
    fi
done

