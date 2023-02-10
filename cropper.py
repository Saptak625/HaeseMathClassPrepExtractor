import tkinter as tk
from PIL import Image, ImageTk
import os


class ImageCropper:
    def __init__(self, root, classprepPages):
        print('\nImage Cropper Started')
        self.saveNumber = 1
        self.pageNumber = 0
        self.assignmentNumber = 0

        self.classprepPages = classprepPages
        self.root = root
        self.get_image()
        self.canvas = tk.Canvas(root, width=self.image.width, height=self.image.height)
        self.canvas.pack()
        self.set_image(delete=False)
        self.rect = None

        self.next_page_button = tk.Button(root, text="Page >>", command=self.next_page)
        self.next_page_button.config(height=5, width=15)
        self.next_page_button.pack(side="right")

        self.previous_page_button = tk.Button(root, text="<< Page", command=self.previous_page)
        self.previous_page_button.config(height=5, width=15)
        self.previous_page_button.pack(side="left")

        self.next_assignment_button = tk.Button(root, text="Assignment >>", command=self.next_assignment)
        self.next_assignment_button.config(height=5, width=15)
        self.next_assignment_button.pack(side="right")

        self.previous_assignment_button = tk.Button(root, text="<< Assignment", command=self.previous_assignment)
        self.previous_assignment_button.config(height=5, width=15)
        self.previous_assignment_button.pack(side="left")

        self.start_x, self.start_y = 0, 0
        self.end_x, self.end_y = 0, 0

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Setup Files
        # Remove old files
        if os.path.exists('cropped'):
            for file in os.listdir('cropped'):
                os.remove(os.path.join('cropped', file))
        else:
            os.makedirs('cropped')

    def on_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.rect = self.canvas.create_rectangle(0, 0, 0, 0, outline="red", width=2)

    def on_motion(self, event):
        self.end_x, self.end_y = event.x, event.y
        x1, y1 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
        x2, y2 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)
        if self.rect:
            self.canvas.coords(self.rect, x1, y1, x2, y2)

    def on_release(self, event):
        self.end_x, self.end_y = event.x, event.y
        if (self.start_x < 0 or self.start_x > self.image.width) or (
                self.end_x < 0 or self.end_x > self.image.width) or (
                self.start_y < 0 or self.start_y > self.image.height) or (
                self.start_y < 0 or self.start_y > self.image.height):
            self.on_escape(event)
        else:
            self.crop_image()

    def on_escape(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
            self.rect = None

    def on_closing(self):
        self.root.destroy()

    def crop_image(self):
        x1, y1 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
        x2, y2 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)
        cropped_image = self.image.crop((x1, y1, x2, y2))
        cropped_image.save(f'cropped/{self.assignment}_{self.saveNumber}.png')
        print('Saved Cropped Image', self.saveNumber)
        self.saveNumber += 1

    def next_page(self):
        self.pageNumber += 1
        self.update()

    def previous_page(self):
        self.pageNumber -= 1
        self.update()

    def next_assignment(self):
        self.assignmentNumber += 1
        self.pageNumber = 0
        self.update()

    def previous_assignment(self):
        self.assignmentNumber -= 1
        self.pageNumber = 0
        self.update()

    def update(self, delete=True):
        self.get_image()
        self.set_image(delete=delete)

    def get_image(self):
        self.assignment = self.assignmentNumber % len(self.classprepPages)
        self.page = self.pageNumber % len(self.classprepPages[self.assignment][1])
        self.exercise, self.pages, self.questions = self.classprepPages[self.assignment]

        self.root.title(
            f"Pg {self.pages[self.page]} --- {self.exercise} (pg. {self.pages}) - {', '.join(self.questions)}")
        self.image = Image.open(f'pages/{self.pages[self.page]}.png')
        self.tk_image = ImageTk.PhotoImage(self.image)

    def set_image(self, delete=True):
        if delete:
            self.canvas.delete(self.image_id)
        self.image_id = self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")
