#!/usr/bin/env python

import os
from PIL import Image

# Directory containing the images
image_directory = os.getcwd()

# Output directory for resized images
output_directory = "processed_" + os.path.basename(image_directory)
os.makedirs(output_directory)

# Target width for resizing
target_width = 720

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Get a list of all files in the image directory
image_files = os.listdir(image_directory)

# Loop through each file in the directory
for file_name in image_files:
    # Check if the file is an image
    if file_name.endswith(('.png', '.jpg', '.jpeg')):
        # Open the image using Pillow
        image_path = os.path.join(image_directory, file_name)
        image = Image.open(image_path)

        # Calculate the new height while maintaining aspect ratio
        width, height = image.size
        aspect_ratio = width / height
        new_height = int(target_width / aspect_ratio)

        # Resize the image
        resized_image = image.resize((target_width, new_height), Image.LANCZOS)

        # Save the resized image to the output directory
        output_path = os.path.join(output_directory, file_name)
        resized_image.save(output_path)

        print(f"Resized {file_name} to {target_width}x{new_height} pixels.")

print("Image resizing complete.")
