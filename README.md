# AI-image-upscaling
# 🖼️ Interactive Image Editor

This is a desktop-based Image Editor built with Python using Tkinter, PIL (Pillow), OpenCV, and TkinterDnD2. It allows users to enhance and manipulate images with various built-in tools, including brightness, contrast, sharpness, saturation, cropping, rotation, flipping, blurring, noise reduction, and even background removal.

## 🌟 Features

- 📂 Drag-and-drop image loading
- 🔧 Basic image adjustments:
  - Brightness
  - Contrast
  - Sharpness
  - Saturation
  - Highlights
  - Blur
  - Noise Reduction
- 💡 Dark/Light mode toggle
- 🖼️ Image display with real-time updates
- 💾 Save edited image in PNG or JPEG format
- 🔄 Reset to original image
- ✂️ Advanced tools:
  - Upscale image by 2x
  - Resize to custom resolution
  - Crop with custom dimensions
  - Rotate with custom angle
  - Flip horizontally
  - Remove white background

## 🛠️ Technologies Used

- `Python 3.x`
- `Tkinter` – GUI framework
- `Pillow (PIL)` – Image processing
- `OpenCV (cv2)` – Background removal and filtering
- `tkinterDnD2` – Drag-and-drop support

## 📦 Installatio

pip install pillow opencv-python tkinterdnd2 numpy
📷 Screenshots
Light Mode	Dark Mode

📝 Usage
Click "Open Image" or drag-and-drop an image into the window.

Use the sliders in the left panel for basic adjustments.

Use the right panel for advanced tools like cropping, rotating, etc.

Save the edited image using "Save Image".

🧩 Supported Formats
JPG / JPEG

PNG

BMP

🚫 Limitations
Background removal is basic (uses thresholding on white backgrounds only).

No support for transparency layers or advanced masking.

📄 License
This project is licensed under the MIT License. See LICENSE for more details.
