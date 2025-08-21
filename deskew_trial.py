# def fix_orientation(image):
#     if image is None:
#         raise ValueError("Image not loaded or is empty.")

#     rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     results = pytesseract.image_to_osd(rgb, output_type=pytesseract.Output.DICT)
#     rotated_image = imutils.rotate_bound(image, angle=results["rotate"])
#     return rotated_image


import os
import cv2
import pytesseract
import imutils

def fix_orientation(image):
    if image is None:
        raise ValueError("Image not loaded or is empty.")
    
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pytesseract.image_to_osd(rgb, output_type=pytesseract.Output.DICT)
    rotated_image = imutils.rotate_bound(image, angle=results["rotate"])
    return rotated_image

def process_images_in_dir(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            image_path = os.path.join(input_dir, filename)
            image = cv2.imread(image_path)
            
            if image is not None:
                fixed_image = fix_orientation(image)
                output_path = os.path.join(output_dir, filename)
                cv2.imwrite(output_path, fixed_image)
                print(f"Processed: {filename}")
            else:
                print(f"Failed to load: {filename}")

# Example usage
input_directory = "/home/aventior_sant/Desktop/CPV.20/pdf_to_png/A032100243 Executed batch record Compound 29A"
output_directory = "result"
process_images_in_dir(input_directory, output_directory)
