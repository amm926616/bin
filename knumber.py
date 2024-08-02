#! /usr/bin/env python

import tkinter as tk 
import random

root = tk.Tk()

screen = tk.Text(root, height=2, width=20)
screen.pack()

def next_num():
    num = random.randint(1, 99)
    screen.delete("1.0", tk.END)
    screen.insert("1.0", num)

button = tk.Button(root, text="click me!", command=next_num)
button.pack()

root.title("Korean the number!")
root.attributes('-topmost', True)
root.mainloop()

