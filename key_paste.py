import keyboard
from tkinter import filedialog
import pyperclip as clip

file_path = filedialog.askopenfilename(initialdir="~/Documents/scanlations/", filetypes=(('text files', '.txt'),))

lines = ''
with open(file_path, 'r') as f:
    lines = f.readlines()

key_pressed = False

def on_key_press(event):
    global key_pressed
    
    if event.name == 'v' and event.event_type == 'down' and keyboard.is_pressed('ctrl'):
        key_pressed = True

    print("Code processing...")
    key_pressed = False

keyboard.on_press(on_key_press)
keyboard.wait()
