import csv
import os
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog
from colorama import init, Fore
from termcolor import colored
import pyfiglet

# Initialize colorama
init()

# Global variables for coordinates
x, y = None, None

# Icons for logs
ICONS = {
    'info': colored('[ ℹ ]', 'blue'),
    'success': colored('[ ✔ ]', 'green'),
    'warning': colored('[ ⚠ ]', 'yellow'),
    'error': colored('[ ✖ ]', 'red'),
}

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
    get_user_coordinates(Image.open(input_file))  # Call once to get coordinates
    confirmed = False
    
    while not confirmed:
        with open(csv_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                name = row['name']
                output_image_path = os.path.join(output_folder, f"{name}{os.path.splitext(image_path)[1]}")
                image = Image.open(image_path)
                draw = ImageDraw.Draw(image)
                draw.text((x, y), name.title(), fill="black", font=ImageFont.truetype("arial.ttf", size=30))
                image.save(output_image_path)
                print(f"{ICONS['success']} {colored(f'Name {name} placed on image {os.path.basename(output_image_path)}', 'green')}")

        # Show preview and ask for confirmation
        preview_image = Image.open(output_image_path)
        preview_image.show()
        confirmed = tk.messagebox.askyesno("Confirmation", "Is the location correct?")
        
        if not confirmed:
            get_user_coordinates(Image.open(input_file))

    print(f"{ICONS['info']} {colored('Task completed successfully!', 'blue')}")



banner = pyfiglet.figlet_format("CertifyD", font="slant")
print(banner)

# Default files
input_file = 'data/template.png'
csv_file = 'data/names.csv'

if not (os.path.exists(input_file) or os.path.exists(csv_file)):
    print(f"{ICONS['info']} {colored('Default files template.png or names.csv not found. Please select files.', 'blue')}")
    input_file = filedialog.askopenfilename(title="Select input image file")
    csv_file = filedialog.askopenfilename(title="Select CSV file")


output_folder = "certificates"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)


print(f"{ICONS['info']} {colored('Writing names on images...', 'blue')}")
write_names_on_image(input_file, csv_file, output_folder)
print(f"{ICONS['info']} {colored('Task completed successfully!', 'blue')}")
