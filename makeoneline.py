#!/usr/bin/env python

import os

def join_lines_in_paragraphs(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        paragraphs = file.read().split('\n\n')  # Split text into paragraphs using double newline as separator

    lines = []
    for paragraph in paragraphs:
        paragraph_lines = paragraph.split('\n')  # Split each paragraph into lines
        joined_line = ' '.join(paragraph_lines)  # Join lines with a space separator
        lines.append(joined_line)  # Add joined line to the list

    return '\n\n'.join(lines)  # Join lines with double newline separator

def process_files_in_folder(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):  # Process only text files
            file_path = os.path.join(folder_path, file_name)
            modified_text = join_lines_in_paragraphs(file_path)

            # Save the modified text back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(modified_text)

# Example usage
folder_path = os.getcwd()
process_files_in_folder(folder_path)




