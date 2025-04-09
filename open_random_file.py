#!/usr/bin/env python

import os
import random
import subprocess

def open_random_file(folder_path):
    # Get a list of all files in the folder

    # Collect all files, including those in subfolders
    files = []
    for root, _, filenames in os.walk(folder_path):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    
    if not files:
        print("No files found in the folder.")
        return

    # Choose a random file
    random_file = random.choice(files)
    file_path = os.path.join(folder_path, random_file)

    print(f"Opening: {file_path}")
    
    # Open the file using the default application
    if os.name == "nt":  # Windows
        os.startfile(file_path)
    elif os.name == "posix":  # Linux/Mac
        subprocess.run(["xdg-open", file_path])
    else:
        print("Unsupported operating system.")

if __name__ == "__main__":
    # Specify the folder path (current directory by default)
    folder = os.getcwd()  # Change this to a specific folder if needed
    open_random_file(folder)

