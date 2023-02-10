import tkinter as tk

from scraper import scrape
from cropper import ImageCropper
from pdf_compiler import png_to_pdf

# Read classprep.txt
classprepPages = []
with open('classprep.txt', 'r') as f:
    for line in f:
        if line == '\n':
            continue
        s = line.split(' - ')
        exercise_page = s[0].split('(pg')
        exercise = exercise_page[0].strip(' ')
        page = exercise_page[1].strip('). ')
        if '-' in page:
            page = page.split('-')
            page = [int(i) for i in page]
            page = list(range(page[0], page[1] + 1))
        else:
            page = [int(page)]
        questions = s[1].replace('#', '').replace('\n', '').split(', ')
        classprepPages.append((exercise, page, questions))

# Scrape pages
# scrape(classprepPages)

# Start Image Cropper to get Questions
root = tk.Tk()
app = ImageCropper(root, classprepPages)
root.mainloop()

# Convert pngs to pdf
# Read all png files in the cropped directory
# png_to_pdf(input('Class Prep Unit Title: '), classprepPages)