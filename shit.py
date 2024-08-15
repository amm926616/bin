import tkinter as tk 
from tkinter import messagebox

def show_popup():
    # Create a new Tkinter window
    root = tk.Tk()
    # Hide the root window
    root.withdraw()
    # Show a pop-up message box
    messagebox.showinfo("Pop-up Title", "This is your pop-up message!")
    # Destroy the root window after the pop-up is closed
    root.destroy()

# Call the function to show the pop-up
show_popup()