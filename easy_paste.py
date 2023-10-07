import pyperclip
import tkinter as tk
from tkinter import filedialog
from pynput import keyboard
from pynput.keyboard import Listener

def newline_remove(raw_lines):
    new_lines = []
    for i in raw_lines:
        if not i.rstrip() == "":
            new_lines.append(i.rstrip())
    
    return new_lines

file_path = filedialog.askopenfilename(initialdir="/home/adam178/scanlations/texts/", filetypes=(('text files', '.txt'),))  # Provide the actual path to your text file

with open(file_path, 'r', encoding='utf-8') as f:
    raw_lines = f.readlines()

lines = newline_remove(raw_lines)

i = 0
ctrl_pressed = False

def copy_line():
    pyperclip.copy(lines[i].strip())
    line = f"({i + 1}): {lines[i]}"
    text_display.delete("1.0", tk.END)
    text_display.insert("1.0", line)


def choose_file():
    global lines, i
    lines = []  # Clear the old lines
    i = 0  # Reset the index
    
    new_file_path = filedialog.askopenfilename(initialdir="/home/adam178/scanlations/texts/", filetypes=(('text files', '.txt'),))
    
    with open(new_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Clear the text display
    text_display.delete("1.0", tk.END)
    
    copy_line()


def check_eol():
    global i
    if i < 0:
        i = len(lines) - 1
    elif i > len(lines) - 1:
        i = 0

def on_press(key):
    global i, ctrl_pressed
    if key == keyboard.Key.ctrl:
        ctrl_pressed = True

    elif key == keyboard.Key.up and ctrl_pressed:
        i -= 1
        check_eol()
        copy_line()
        print("-1")

    elif key == keyboard.Key.down and ctrl_pressed or key == keyboard.KeyCode.from_char('v') and ctrl_pressed:
        i += 1
        check_eol()
        copy_line()
        print("+1")

    elif key == keyboard.Key.left and ctrl_pressed:
        i -= 2
        check_eol()
        copy_line()
        print("-2")
    
    elif key == keyboard.Key.right and ctrl_pressed:
        i += 2
        check_eol()
        copy_line()
        print("+2")


def on_release(key):
    global ctrl_pressed
    if key == keyboard.Key.ctrl:
        ctrl_pressed = False


# GUI setup
root = tk.Tk()
root.title("Easy Paste Developed By AD178")
root.config(bg="#303841")
root.attributes('-topmost', 1)
root.resizable(0, 0)

# font
display_font = ("pyidaungsu", 10)

text_display = tk.Text(root, font=display_font, height=2, width=50)
text_display.pack()

choose_file_button = tk.Button(root, text='choose another file', command=choose_file)
choose_file_button.pack()

# copy the first line
copy_line()

# Set up the listener
with Listener(on_press=on_press, on_release=on_release) as listener:
    # Start GUI main loop
    root.mainloop()
