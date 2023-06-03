#!/usr/bin/env python
import os 

def remove_numbering(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    with open(filename, 'w') as file:
        for line in lines:
            # Remove numbering from each line
            line = line.lstrip('1234567890. ')
            file.write(line)

folder = os.getcwd()
folder = os.listdir(folder)
for filename in folder:
    remove_numbering(filename)

