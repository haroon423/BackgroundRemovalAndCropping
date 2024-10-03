import cv2
import pytesseract
from pytesseract import Output
import numpy as np
from rembg import remove
from PIL import Image

def correct_orientation_and_remove_background(image_path, output_path):
    # Step 1: Load the image using OpenCV
    print(f"Attempting to load image from: {image_path}")
    image = cv2.imread(image_path)

    if image is None:
        print("Error: Image not loaded. Check the file path and integrity.")
        return

    # Step 2: Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 3: Use pytesseract to detect text orientation
    results = pytesseract.image_to_osd(gray, output_type=Output.DICT)
    angle = results.get("rotate", 0)
    print(f"Detected angle: {angle}")

    # Step 4: Rotate the image to correct orientation if necessary
    if angle != 0:
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, -angle, 1.0)

        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))

        M[0, 2] += (new_w / 2) - center[0]
        M[1, 2] += (new_h / 2) - center[1]

        rotated = cv2.warpAffine(image, M, (new_w, new_h))
        print(f"Rotated image by {angle} degrees.")
    else:
        rotated = image
        print("No rotation needed.")

    # Step 5: Convert the rotated image to a PIL image
    rotated_pil = Image.fromarray(cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB))

    # Step 6: Remove the background using rembg
    output_image = remove(rotated_pil)

    # Step 7: Ensure the output image has an alpha channel (RGBA)
    output_image = output_image.convert('RGBA')

    # Step 8: Convert the image to a numpy array for processing
    data = np.array(output_image)

    # Step 9: Extract the alpha channel
    alpha_channel = data[:, :, 3]

    # Step 10: Define an alpha threshold to ignore faint edges (adjust as needed)
    alpha_threshold = 10  # Pixels with alpha > 10 are considered opaque

    # Step 11: Create a binary mask where alpha > threshold
    mask = alpha_channel > alpha_threshold

    # Step 12: Find the bounding box coordinates where mask is True
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)

    if not rows.any() or not cols.any():
        # Step 13: If no content is found, save the original output image
        output_image.save(output_path)
    else:
        # Step 14: Find the min and max indices where mask is True
        ymin, ymax = np.where(rows)[0][[0, -1]]
        xmin, xmax = np.where(cols)[0][[0, -1]]

        # Step 15: Crop the image using the bounding box
        # Adding +1 to xmax and ymax to include the last pixel
        cropped_image = output_image.crop((xmin, ymin, xmax + 1, ymax + 1))

        # Step 16: Save the cropped image
        cropped_image.save(output_path)
        print(f"Cropped image saved to {output_path}")

# Example usage
correct_orientation_and_remove_background('testing.jpg', '0998877output.png')