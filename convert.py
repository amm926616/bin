#!/usr/bin/env python

import os
import img2pdf

# Specify the path to the folder containing the images
folder_path = os.getcwd()
images = os.listdir(folder_path)
images.sort()

# Get the current folder's chapter name and parent folder name
chapter_name = os.getcwd()
parent_folder_name = os.path.basename(os.path.dirname(chapter_name))
chapter_name = os.path.basename(chapter_name)
print(chapter_name)
print(parent_folder_name)
pdf_name = parent_folder_name + " - " + chapter_name + ".pdf"
# Create a list to store the image files
image_files = []

# Iterate through the files in the folder and add the image files to the list
for filename in images:
    if filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")):
        image_files.append(os.path.join(folder_path, filename))

# Create a PDF file and open it in binary write mode
with open(pdf_name, "wb") as f:
    f.write(img2pdf.convert(image_files))

print("PDF file generated successfully!")

