import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, Text, ttk

class ImageTagger:
    def __init__(self):
        self.image_index = 0
        self.images = []
        self.root = tk.Tk()
        self.root.configure(background='black')
        self.root.title("Image Tagger")
        self.root.geometry("800x600")
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.textbox = Text(self.root, bg='white', fg='black')
        self.panel = tk.Label(self.root, background='black')

    def open_folder(self):
        folder_path = filedialog.askdirectory()
        if not folder_path:
            return
        self.images = []
        self.image_index = 0
        for file in os.listdir(folder_path):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.images.append(os.path.join(folder_path, file))
        if self.images:
            self.show_image()

    def save_annotation(self):
        if self.images:
            txt_filename = os.path.splitext(self.images[self.image_index])[0] + '.txt'
            with open(txt_filename, 'w') as txt_file:
                txt_file.write(self.textbox.get("1.0", "end-1c"))
            self.textbox.delete("1.0", "end")

    def next_image(self):
        self.save_annotation()
        self.image_index += 1
        if self.image_index < len(self.images):
            self.show_image()

    def previous_image(self):
        self.save_annotation()
        if self.image_index > 0:
            self.image_index -= 1
            self.show_image()

    def load_annotation(self):
        txt_filename = os.path.splitext(self.images[self.image_index])[0] + '.txt'
        if os.path.isfile(txt_filename):
            with open(txt_filename, 'r') as txt_file:
                self.textbox.insert("1.0", txt_file.read())
        else:
            self.textbox.delete("1.0", "end")

    def show_image(self):
        image = Image.open(self.images[self.image_index])
        w_ratio = image.width / self.root.winfo_width()
        h_ratio = image.height / (self.root.winfo_height() // 2)
        ratio = max(w_ratio, h_ratio)

        image = image.resize((int(image.width / ratio), int(image.height / ratio)), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.panel.config(image=photo)
        self.panel.image = photo
        self.load_annotation()

    def run(self):
        open_button = ttk.Button(self.root, text="Open Folder", command=self.open_folder)
        next_button = ttk.Button(self.root, text="Next Image", command=self.next_image)
        prev_button = ttk.Button(self.root, text="Previous Image", command=self.previous_image)

        open_button.grid(row=0, column=0, pady=10, padx=10, sticky="ew")
        prev_button.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        next_button.grid(row=1, column=1, pady=10, padx=10, sticky="ew")
        self.panel.grid(row=2, column=0, columnspan=2, pady=10, padx=10)
        self.textbox.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        # Configure the row and column weights
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.root.mainloop()

if __name__ == "__main__":
    tagger = ImageTagger()
    tagger.run()
