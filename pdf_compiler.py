from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import landscape

from PIL import Image
import os

def png_to_pdf(title, classprepPages):
    png_files = os.listdir('cropped')
    png_files = sorted([os.path.join('cropped', png) for png in png_files])
    header = None

    c = canvas.Canvas(f'{title}.pdf', pagesize=letter)
    y = 792
    y -= 50
    c.setFont('Helvetica-Bold', 20)
    c.drawString(40, y, title)
    text_width = c.stringWidth(title)
    c.setLineWidth(3)
    c.line(40, y-5, 40 + text_width, y-5)
    y -= 30
    for i, png in enumerate(png_files):
        if int(png.split('_')[0].replace('/', '\\').split('\\')[1]) != header:
            if header is not None:
                c.showPage()
                y = 792
                y -= 50
            header = int(png.split('_')[0].replace('/', '\\').split('\\')[1])
            c.setFont('Helvetica', 16)
            header_title = f'{classprepPages[header][0]} (pg. {", ".join([str(i) for i in classprepPages[header][1]])}) - #{", ".join(classprepPages[header][2])}'
            c.drawString(40, y, header_title)
            text_width = c.stringWidth(header_title)
            c.setLineWidth(1.5)
            c.line(40, y-5, 40 + text_width, y-5)
            y -= 30
        image = Image.open(png)
        width, height = image.size
        x = 40
        y -= height
        if y - height < 0:
            c.showPage()
            y = 792 - height - 50
        c.drawImage(png, x, y, width=width, height=height)
        y -= 120
    c.save()
    print('Saved PDF')
