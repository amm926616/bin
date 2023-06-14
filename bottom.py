import pyperclip as clip 

with open("bottom.txt", "r") as f:
    lines = f.read()

clip.copy(lines)
