import os
import random
import tkinter as tk
from PIL import Image, ImageTk
import pillow_heif

# Register HEIF opener for Pillow
pillow_heif.register_heif_opener()


class ImageViewerApp:
    def __init__(self, root):
        self.root = root
        self.geometry = self.root.geometry()
        self.root.configure(bg='black')

        # Keyboard shortcuts for toggling fullscreen and exiting
        self.root.bind("<F11>", self.toggle_screen)
        self.root.bind("q", self.exit_app)

        # Label for displaying images
        self.image_label = tk.Label(root, bg='black')
        self.image_label.pack(expand=True)

        self.image_paths = []
        self.current_image = None

        # Select directory and load images
        self.select_directory()
        if self.image_paths:
            self.show_random_image()

        # Automatically switch images every 5 seconds
        self.root.after(10000, self.show_next_image)
        self.full_screen = False

    def toggle_screen(self, event):
        if self.full_screen:
            self.exit_fullscreen()
        else:
            self.toggle_fullscreen()
        self.full_screen = not self.full_screen

    def select_directory(self):
        """Sets the image directory directly in the code."""
        directory = r"C:\Users\stefa\OneDrive\Pictures\Jonas"  # Replace with your desired directory path
        if directory and os.path.exists(directory):
            # Supported image formats
            extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".heic")
            self.image_paths = [os.path.join(directory, f) for f in os.listdir(directory) if
                                f.lower().endswith(extensions)]

    def show_random_image(self):
        """Displays a randomly selected image from the directory."""
        if not self.image_paths:
            return
        random_image_path = random.choice(self.image_paths)
        self.display_image(random_image_path)

    def show_next_image(self):
        """Displays the next image after a delay."""
        self.show_random_image()
        self.root.after(5000, self.show_next_image)

    def display_image(self, image_path):
        """Displays an image in the GUI while keeping its original aspect ratio."""
        img = Image.open(image_path)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        img.thumbnail((screen_width, screen_height), Image.LANCZOS)  # Maintain aspect ratio
        self.current_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.current_image)

    def toggle_fullscreen(self):
        """Enables or disables fullscreen mode."""
        #self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))
        # Store geometry for reset
        self.geometry = self.root.geometry()
        self.root.overrideredirect(True)
        self.root.state("zoomed")

    def exit_fullscreen(self):
        """Exits fullscreen mode if active."""
        #self.root.attributes("-fullscreen", False)
        self.root.state("normal")
        self.root.geometry(self.geometry)
        self.root.overrideredirect(False)

    def minimize_window(self, event=None):
        """Minimizes the window."""
        self.root.iconify()

    def exit_app(self, event=None):
        """Exits the application."""
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewerApp(root)
    root.mainloop()