#!/usr/bin/env python

import os

folder_path = os.getcwd()

# List all files in the folder
files = os.listdir(folder_path)

name = 'Chapter '
# Iterate over the files
for filename in files:
    if filename.startswith(name):
        # Create the new name by removing the prefix '123'
        new_name = filename[len(name):]
        
        # Generate the full file paths
        current_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)
        
        # Rename the file
        os.rename(current_path, new_path)
        
        print(f'Renamed {filename} to {new_name}')

