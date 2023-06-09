#!/usr/bin/env python

import os
from PIL import Image

# Get the current working directory
folder_path = os.getcwd()

# Get the list of image files in the folder
image_files = [file for file in os.listdir(folder_path) if file.endswith('.jpg')]

# Sort the image files based on their names
image_files.sort()

# Set the number of images to join vertically
images_per_join = 5

# Calculate the total number of joined images
total_joined_images = len(image_files) // images_per_join

# Iterate over the image files and join them vertically
for i in range(0, len(image_files), images_per_join):
    # Create a list to store the image objects
    images_to_join = []

    # Iterate over the next `images_per_join` files and open them as images
    for j in range(images_per_join):
        if i + j < len(image_files):
            image_path = os.path.join(folder_path, image_files[i + j])
            image = Image.open(image_path)
            images_to_join.append(image)

    # Join the images vertically
    joined_image = Image.new('RGB', (images_to_join[0].width, sum(image.height for image in images_to_join)))
    y_offset = 0
    for image in images_to_join:
        joined_image.paste(image, (0, y_offset))
        y_offset += image.height

    # Save the joined image with the correct name
    joined_image_path = os.path.join(folder_path, f'{str(i // images_per_join + 1).zfill(4)}.jpg')
    joined_image.save(joined_image_path)

    # Delete the old images
    for j in range(images_per_join):
        if i + j < len(image_files):
            image_path = os.path.join(folder_path, image_files[i + j])
            os.remove(image_path)

