import tkinter as tk
from PIL import Image, ImageTk

# Create a window
root = tk.Tk()
root.title("Image Viewer")

# Load the image
image_path = "/home/adam178/Pictures/. erotic pics/194511.jpg"  # Replace with your image path
image = Image.open(image_path)

# Convert the image to a format Tkinter can use
tk_image = ImageTk.PhotoImage(image)

# Create a Label widget to display the image
label = tk.Label(root, image=tk_image)
label.pack()

# Run the Tkinter event loop
root.mainloop()
