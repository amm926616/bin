#!/usr/bin/env python 

import os

def remove_dash_from_files():
    # Get the current folder path
    folder_path = os.getcwd()

    # Get a list of all text files in the folder
    text_files = [file for file in os.listdir(folder_path) if file.endswith(".txt")]

    # Process each text file
    for file in text_files:
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'r') as f:
            lines = f.readlines()

        modified_lines = [line.lstrip('-') for line in lines]

        # Overwrite the original file with modified content
        with open(file_path, 'w') as f:
            f.writelines(modified_lines)

        print(f"Modified content saved to '{file_path}'.")

# Usage: simply call the function
remove_dash_from_files()

