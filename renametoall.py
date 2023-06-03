#!/usr/bin/env python
import os

def rename_folder_entries(folder_path):
    # Get the list of elements in the folder
    elements = os.listdir(folder_path)
    
    # Sort the elements to maintain consistency
    elements.sort()
    
    # Iterate over each element
    for index, element in enumerate(elements):
        # Generate the new name with leading zeros
        new_name = str(index + 1).zfill(4)
        
        # Split the element into name and extension
        name, extension = os.path.splitext(element)
        
        # Get the current path of the element
        current_path = os.path.join(folder_path, element)
        
        # Generate the new name with the original extension
        new_name_with_extension = new_name + extension
        
        # Get the new path with the renamed element
        new_path = os.path.join(folder_path, new_name_with_extension)
        
        # Rename the element by moving it to the new path
        os.rename(current_path, new_path)
        
        print(f"Renamed {element} to {new_name_with_extension}")
        
# Specify the folder path
folder_path = os.getcwd()

# Call the function to rename the entries in the folder
rename_folder_entries(folder_path)

