#!/usr/bin/env python

import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Connect to the SQLite database
conn = sqlite3.connect('korean_characters.db')
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS korean_characters (
    id INTEGER PRIMARY KEY,
    character TEXT NOT NULL,
    meaning TEXT NOT NULL
)
''')

class KoreanDictionaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Korean Dictionary")
        self.create_widgets()

    def create_widgets(self):
        self.character_label = tk.Label(self.root, text="Character:")
        self.character_label.grid(row=0, column=0, padx=10, pady=10)
        self.character_entry = tk.Entry(self.root)
        self.character_entry.grid(row=0, column=1, padx=10, pady=10)

        self.meaning_label = tk.Label(self.root, text="Meaning:")
        self.meaning_label.grid(row=1, column=0, padx=10, pady=10)
        self.meaning_entry = tk.Entry(self.root)
        self.meaning_entry.grid(row=1, column=1, padx=10, pady=10)

        self.add_button = tk.Button(self.root, text="Add", command=self.add_character)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.search_label = tk.Label(self.root, text="Search Character:")
        self.search_label.grid(row=3, column=0, padx=10, pady=10)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=3, column=1, padx=10, pady=10)

        self.search_button = tk.Button(self.root, text="Search", command=self.search_character)
        self.search_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.tree = ttk.Treeview(self.root, columns=("Character", "Meaning"), show='headings')
        self.tree.heading("Character", text="Character")
        self.tree.heading("Meaning", text="Meaning")
        self.tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.load_data()

    def add_character(self):
        character = self.character_entry.get()
        meaning = self.meaning_entry.get()
        if character and meaning:
            cursor.execute('INSERT INTO korean_characters (character, meaning) VALUES (?, ?)', (character, meaning))
            conn.commit()
            messagebox.showinfo("Success", "Character added successfully!")
            self.character_entry.delete(0, tk.END)
            self.meaning_entry.delete(0, tk.END)
            self.load_data()
        else:
            messagebox.showwarning("Input Error", "Please fill in both fields.")

    def search_character(self):
        character = self.search_entry.get()
        cursor.execute('SELECT meaning FROM korean_characters WHERE character = ?', (character,))
        result = cursor.fetchone()
        if result:
            self.result_label.config(text=f"Meaning of {character}: {result[0]}")
        else:
            self.result_label.config(text=f"{character} not found in the database.")

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        cursor.execute('SELECT character, meaning FROM korean_characters')
        rows = cursor.fetchall()
        for row in rows:
            self.tree.insert("", tk.END, values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = KoreanDictionaryApp(root)
    root.mainloop()

# Close the database connection when the application is closed
conn.close()
