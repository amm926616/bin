import pyperclip
import tkinter as tk
from tkinter import filedialog
import pyxhook

file_path = filedialog.askopenfilename(initialdir="/home/adam178/scanlations/texts/", filetypes=(('text files', '.txt'),))  # Provide the actual path to your text file

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

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

def on_key_event(event):
    global i, ctrl_pressed

    if event.Ascii == 29:  # ASCII value for Ctrl key
        ctrl_pressed = True
    elif event.Ascii == 17:  # ASCII value for Ctrl+Q
        hookman.cancel()
    else:
        if event.Ascii == 38 and ctrl_pressed:  # ASCII value for 'up' arrow key
            i -= 1
            check_eol()
            copy_line()
            print("-1")
        elif event.Ascii == 40 and ctrl_pressed:  # ASCII value for 'down' arrow key
            i += 1
            check_eol()
            copy_line()
            print("+1")
        elif event.Ascii == 37 and ctrl_pressed:  # ASCII value for 'left' arrow key
            i -= 2
            check_eol()
            copy_line()
            print("-2")
        elif (event.Ascii == 39 and ctrl_pressed) or (event.Ascii == 22 and ctrl_pressed):  # ASCII value for 'right' arrow key or 'v' key
            i += 2
            check_eol()
            copy_line()
            print("+2")

def on_key_release(event):
    global ctrl_pressed

    if event.Ascii == 29:  # ASCII value for Ctrl key
        ctrl_pressed = False

hookman = pyxhook.HookManager()
hookman.KeyDown = on_key_event
hookman.KeyUp = on_key_release
hookman.HookKeyboard()

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

# Start GUI main loop
root.mainloop()

hookman.cancel()  # Stop the hook manager after GUI main loop exits
