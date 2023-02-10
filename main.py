import tkinter as tk

from scraper import scrape
from cropper import ImageCropper

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
        questions = s[1].split(', ')
        classprepPages.append((exercise, page, questions))

# Scrape pages
scrape(classprepPages)

# Start Image Cropper to get Questions
root = tk.Tk()
app = ImageCropper(root, classprepPages)
root.mainloop()