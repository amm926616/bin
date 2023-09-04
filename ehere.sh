#!/bin/bash

# Set the folder path
folder=$(pwd)

# Change to the specified folder
cd "$folder"

# Find all .cbz files and extract them
for file in *.cbz; do
    # Extract the file to its folder name
    foldername="${file%.cbz}"
    mkdir -p "$foldername"
    unzip "$file" -d "$foldername"
done

