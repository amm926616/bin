import pyperclip
from pynput import keyboard
from pynput.keyboard import Listener
from tkinter import filedialog 
import sys

file_path = filedialog.askopenfilename(initialdir="~/Documents/scanlations/texts/", filetypes=(('text files', '.txt'),))

with open(file_path, 'r') as f:
    lines = f.readlines()

i = 0
ctrl_pressed = False

def copy_line():
    if i < len(lines):
        pyperclip.copy(lines[i].strip())  # Remove newline characters
    else:
        print("Out of lines")

def check_eol():
    if i < len(lines):
        print(f"Copied line {i}: {lines[i]}")
    else:
        print("End of file.")
        sys.exit()

def on_press(key):
    global i, ctrl_pressed
    if key == keyboard.Key.ctrl:
        ctrl_pressed = True

    elif key == keyboard.Key.up and ctrl_pressed:
        i += 1
        copy_line()
        print("+1")
        check_eol()

    elif key == keyboard.Key.down and ctrl_pressed:
        i -= 1
        copy_line()
        print("-1")
        check_eol()

    elif key == keyboard.Key.left and ctrl_pressed:
        i -= 2
        copy_line()
        print("-2")
        check_eol()
    
    elif key == keyboard.Key.right and ctrl_pressed or key == keyboard.KeyCode.from_char('v') and ctrl_pressed:
        i += 2
        copy_line()
        print("+2")
        check_eol()
    
    elif key == keyboard.Key.ctrl:
        ctrl_pressed = False

# start copying the first line
copy_line()

# Set up the listener
with Listener(on_press=on_press) as listener:
    print("Press 'Ctrl + V' to copy the next line.")
    listener.join()
