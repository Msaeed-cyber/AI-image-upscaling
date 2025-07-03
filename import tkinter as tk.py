import tkinter as tk
from tkinter import filedialog, DISABLED, NORMAL, simpledialog
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageEnhance, ImageTk, ImageFilter
import numpy as np
import cv2

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Image Editor")
        self.root.geometry("1000x700")
        self.dark_mode = False

        self.img = None
        self.processed_img = None
        self.before_img = None

        self.create_widgets()

    def create_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=5)

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop_image)

        tk.Button(top_frame, text="Open Image", command=self.open_image).pack(side=tk.LEFT, padx=5)
        self.save_btn = tk.Button(top_frame, text="Save Image", command=self.save_image, state=DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Reset", command=self.reset_image).pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Dark/Light Mode", command=self.toggle_mode).pack(side=tk.LEFT, padx=5)

        slider_frame = tk.LabelFrame(self.root, text="Adjustments")
        slider_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        self.sliders = {}
        effects = {
            "Brightness": (0.0, 3.0, 1.0),
            "Contrast": (0.0, 3.0, 1.0),
            "Sharpness": (0.0, 5.0, 1.0),
            "Saturation": (0.0, 3.0, 1.0),
            "Highlights": (0, 100, 0),
            "Blur": (0, 10, 0),
            "Noise Reduction": (0, 100, 0)
        }

        for name, (min_val, max_val, default) in effects.items():
            var = tk.DoubleVar(value=default)
            slider = tk.Scale(slider_frame, label=name, from_=min_val, to=max_val, orient=tk.HORIZONTAL,
                              resolution=0.1, variable=var, length=200, command=self.update_image)
            slider.pack()
            self.sliders[name] = var

        display_frame = tk.Frame(self.root)
        display_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.image_label = tk.Label(display_frame)
        self.image_label.pack(expand=True)

        tool_frame = tk.LabelFrame(self.root, text="Advanced Tools")
        tool_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        tk.Button(tool_frame, text="Upscale 2x", command=self.upscale_image).pack(pady=2)
        tk.Button(tool_frame, text="Custom Resolution", command=self.custom_resolution).pack(pady=2)
        tk.Button(tool_frame, text="Crop", command=self.crop_image).pack(pady=2)
        tk.Button(tool_frame, text="Rotate", command=self.rotate_image).pack(pady=2)
        tk.Button(tool_frame, text="Flip", command=self.flip_image).pack(pady=2)
        tk.Button(tool_frame, text="Remove Background", command=self.remove_background).pack(pady=2)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", ".png;.jpg;.jpeg;.bmp")])
        if file_path:
            self.load_image(file_path)

    def drop_image(self, event):
        file_path = event.data.strip('{}')
        self.load_image(file_path)

    def load_image(self, file_path):
        try:
            self.img = Image.open(file_path).convert("RGB")
            self.before_img = self.img.copy()
            self.processed_img = self.img.copy()
            self.enable_controls()
            self.update_image()
        except Exception as e:
            print(f"Failed to load image: {e}")

    def enable_controls(self):
        self.save_btn.config(state=NORMAL)

    def update_image(self, _=None):
        if self.img:
            img = self.img.copy()

            img = ImageEnhance.Brightness(img).enhance(self.sliders["Brightness"].get())
            img = ImageEnhance.Contrast(img).enhance(self.sliders["Contrast"].get())
            img = ImageEnhance.Sharpness(img).enhance(self.sliders["Sharpness"].get())
            img = ImageEnhance.Color(img).enhance(self.sliders["Saturation"].get())

            highlight_val = self.sliders["Highlights"].get()
            if highlight_val:
                img = img.point(lambda p: p + highlight_val if p > 200 else p)

            blur_val = self.sliders["Blur"].get()
            if blur_val:
                img = img.filter(ImageFilter.GaussianBlur(blur_val))

            noise_val = self.sliders["Noise Reduction"].get()
            if noise_val:
                size = int(noise_val // 10 + 1)
                if size % 2 == 0:
                    size += 1
                size = max(3, size)
                img = img.filter(ImageFilter.MedianFilter(size))

            self.processed_img = img
            self.display_image(img)

    def display_image(self, img):
        max_size = (600, 400)
        img.thumbnail(max_size, Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
        self.image_label.config(image=tk_img)
        self.image_label.image = tk_img

    def reset_image(self):
        if self.before_img:
            self.img = self.before_img.copy()
            self.update_image()

    def toggle_mode(self):
        self.dark_mode = not self.dark_mode
        bg_color = "#2e2e2e" if self.dark_mode else "white"
        fg_color = "white" if self.dark_mode else "black"
        self.root.configure(bg=bg_color)
        for widget in self.root.winfo_children():
            try:
                widget.configure(bg=bg_color, fg=fg_color)
            except:
                try:
                    widget.configure(bg=bg_color)
                except:
                    pass

    def save_image(self):
        if self.processed_img:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", ".png"), ("JPEG", ".jpg")])
            if file_path:
                self.processed_img.save(file_path)

    def upscale_image(self):
        if self.processed_img:
            new_size = (self.processed_img.width * 2, self.processed_img.height * 2)
            self.processed_img = self.processed_img.resize(new_size, Image.LANCZOS)
            self.display_image(self.processed_img)

    def custom_resolution(self):
        if self.processed_img:
            w = simpledialog.askinteger("Custom Width", "Enter width:")
            h = simpledialog.askinteger("Custom Height", "Enter height:")
            if w and h:
                self.processed_img = self.processed_img.resize((w, h), Image.LANCZOS)
                self.display_image(self.processed_img)

    def crop_image(self):
        if self.processed_img:
            left = simpledialog.askinteger("Crop", "Left:")
            upper = simpledialog.askinteger("Crop", "Upper:")
            right = simpledialog.askinteger("Crop", "Right:")
            lower = simpledialog.askinteger("Crop", "Lower:")
            if None not in (left, upper, right, lower):
                self.processed_img = self.processed_img.crop((left, upper, right, lower))
                self.display_image(self.processed_img)

    def rotate_image(self):
        if self.processed_img:
            angle = simpledialog.askinteger("Rotate", "Angle:")
            if angle:
                self.processed_img = self.processed_img.rotate(angle)
                self.display_image(self.processed_img)

    def flip_image(self):
        if self.processed_img:
            self.processed_img = self.processed_img.transpose(Image.FLIP_LEFT_RIGHT)
            self.display_image(self.processed_img)

    def remove_background(self):
        if self.processed_img:
            img_cv = cv2.cvtColor(np.array(self.processed_img), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
            img_cv[mask == 0] = (0, 0, 0)
            img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
            self.processed_img = img_pil
            self.display_image(self.processed_img)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
