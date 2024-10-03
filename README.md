# Background Removal and Cropping

## Project Description
This project provides a Python script that automates the process of correcting the orientation of images, removing backgrounds, and cropping unnecessary whitespace. It leverages the capabilities of OpenCV, Tesseract OCR, and the rembg library to ensure clean and usable output images.

### Features
- **Orientation Correction**: Automatically detects and corrects the orientation of images based on text analysis.
- **Background Removal**: Utilizes the `rembg` library to remove backgrounds from images, leaving only the main subject.
- **Cropping**: Eliminates excess whitespace around the subject, resulting in a well-cropped image.

## Installation Instructions
To set up the project locally, clone the repository and install the required packages:

```bash
git clone git@github.com:haroon423/BackgroundRemovalAndCropping.git
cd BackgroundRemovalAndCropping
pip install -r requirements.txt
