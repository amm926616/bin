"""
Created on Fri Feb 24 13:34:08 2023

@author: adam178
"""

import tkinter as tk 
from tkinter import filedialog 
import pyperclip as clip
import os
from settings import Settings

class EasyPaste():
    def __init__(self, master):
        self.settings = Settings()
        self.master = master
        self.master.config(bg=self.settings.root_color)
        self.master.resizable(0, 0)
        self.master.title("Easy Paste")

        # Buttons
        self.next_two = tk.Button(self.master, text="(2xnext line)", fg=self.settings.fg_color, bg=self.settings.bg_color, height=2, command=self.next_line)
        self.previous_two = tk.Button(self.master, text="(2xprevious line)", fg=self.settings.fg_color, bg=self.settings.bg_color, height=2, command=self.back_line)
        self.next = tk.Button(self.master, text="next line", fg=self.settings.fg_color, bg=self.settings.bg_color, height=2, command=self.plusone)
        self.previous = tk.Button(self.master, text="previous line", fg=self.settings.fg_color, bg=self.settings.bg_color, height=2, command=self.minusone)
        self.restart = tk.Button(self.master, text='Choose another text file', fg=self.settings.fg_color, bg=self.settings.bg_color, height=2, command=self.restart_program)

        # packing the button
        self.previous.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        self.previous_two.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        self.next_two.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
        self.next.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        self.restart.grid(row=3, columnspan=2, padx=10, pady=10, sticky='ew')

        # Start asking for text file
        self.file = self.ask_dir()
        if self.file:
            # opening the text file and readlines, asign to "lines"
            with open(self.file, 'r', encoding='utf-8') as f:
                self.lines = f.readlines()
            self.text_display = tk.Text(self.master, height=2, width=50)
            self.text_display.grid(row=0, column=0, columnspan=2, sticky='ew')

            # Display the current line to text widget
            self.i = 0 
            if self.i > len(self.lines) or self.i < len(self.lines):
                self.i = 0
            self.line = self.lines[self.i]
            self.text_display.insert("1.0", self.line)
            self.master.attributes('-topmost', 1)
        else:
            self.master.destroy()

    # function to get the file location 
    def ask_dir(self):
        file_path = filedialog.askopenfilename(initialdir="~/Documents/", filetypes=(('text files', '.txt'),))
        return file_path

    def next_line(self):
        self.text_display.delete("1.0", tk.END)
        self.i += 2
        self.line = self.lines[self.i]
        self.text_display.insert("1.0", self.line)
        clip.copy(self.line)

    def back_line(self):
        self.text_display.delete("1.0", tk.END)
        self.i -= 2
        self.line = self.lines[self.i]
        self.text_display.insert("1.0", self.line)
        clip.copy(self.line)

    def minusone(self):
        self.text_display.delete("1.0", tk.END)
        self.i -= 1
        self.line = self.lines[self.i]
        self.text_display.insert("1.0", self.line)
        clip.copy(self.line)

    def plusone(self):
        self.text_display.delete("1.0", tk.END)
        self.i += 1
        self.line = self.lines[self.i]
        self.text_display.insert("1.0", self.line)
        clip.copy(self.line)

    def restart_program(self):
        self.master.destroy()
        root = tk.Tk()
        EasyPaste(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    EasyPaste(root)
    root.mainloop()



