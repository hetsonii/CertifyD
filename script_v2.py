import csv
import os
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog

# Global variables for coordinates
x, y = None, None

def get_user_coordinates(img):
    global x, y

    def on_click(event):
        global x, y
        x, y = event.x, event.y
        root.destroy()

    root = tk.Tk()
    root.title("Select Coordinates")
    root.geometry("+100+100")
    root.bind("<Button-1>", on_click)

    canvas = tk.Canvas(root, width=img.width, height=img.height)
    canvas.pack()
    photo_image = tk.PhotoImage(file=img.filename)
    canvas.create_image(0, 0, anchor=tk.NW, image=photo_image)

    root.mainloop()

def write_names_on_image(image_path, csv_path, output_folder):
    global x, y
    get_user_coordinates(Image.open(image_path))  # Call once to get coordinates
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            name = row['name']
            output_image_path = os.path.join(output_folder, f"{name}{os.path.splitext(image_path)[1]}")
            image = Image.open(image_path)
            draw = ImageDraw.Draw(image)
            draw.text((x, y), name.title(), fill="black", font=ImageFont.truetype("arial.ttf", size=30))
            image.save(output_image_path)

# Example usage:
input_file = filedialog.askopenfilename(title="Select input image file")
csv_file = filedialog.askopenfilename(title="Select CSV file")
output_folder = "certificates"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

write_names_on_image(input_file, csv_file, output_folder)
