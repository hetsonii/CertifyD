import csv
import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont

def write_names_on_file(input_file, csv_path, output_folder):
    name, ext = os.path.splitext(input_file)
    if ext.lower() == '.pdf':
        write_names_on_pdf(input_file, csv_path, output_folder)
    elif ext.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
        write_names_on_image(input_file, csv_path, output_folder)
    else:
        print(f"Unsupported file type: {ext}")

def get_middle_coordinates(width, height, text, font_size):
    text_width = font_size * len(text) * 0.6  # Rough approximation of text width
    x = (width - text_width) / 2
    y = (height - font_size) / 2
    return x, y

def write_names_on_pdf(pdf_path, csv_path, output_folder):
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            name = row['name']
            output_pdf_path = os.path.join(output_folder, f"{name}.pdf")
            reader = PdfReader(pdf_path)
            writer = PdfWriter()

            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                writer.add_page(page)

                width, height = letter
                x, y = get_middle_coordinates(width, height, name, 12)  # Adjust font size as needed
                packet = canvas.Canvas("temp.pdf", pagesize=letter)
                # packet.drawString(x-200, y-40, ' '.join(name.split()[:2]), fontName="Helvetica", fontSize=12)
                packet.setFont("Helvetica", 12)  # Setting font to Helvetica with size 12
                packet.drawString(x-200, y-40, ' '.join(name.split()[:2]))
                packet.save()

                overlay = PdfReader("temp.pdf")
                page.merge_page(overlay.pages[0])

            with open(output_pdf_path, 'wb') as output_pdf:
                writer.write(output_pdf)

            os.remove("temp.pdf")  # Remove temporary file

def write_names_on_image(image_path, csv_path, output_folder):
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            name = row['name']
            output_image_path = os.path.join(output_folder, f"{name}{os.path.splitext(image_path)[1]}")
            image = Image.open(image_path)
            draw = ImageDraw.Draw(image)
            width, height = image.size
            x, y = get_middle_coordinates(width, height, ' '.join(name.split()[:2]), 40)  # Adjust font size as needed
            draw.text((x-200, y-40), name.title(), fill="black", font=ImageFont.truetype("arial.ttf", size=30))
            image.save(output_image_path)


input_file = "data/template.png"
csv_file = "data/names.csv"
output_folder = "certificates"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

write_names_on_file(input_file, csv_file, output_folder)
