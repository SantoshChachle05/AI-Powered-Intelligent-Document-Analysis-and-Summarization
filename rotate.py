import cv2
import os
import numpy as np

# Input and output directory
input_dir = "test_png"  # Change to your input directory path
output_dir = "90_dum"  # Change to your output directory path
angle = 180  # Rotation angle in degrees (clockwise)

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

def rotate_image_without_cropping(image, angle):
    """ Rotates an image while ensuring no cropping occurs. """
    (h, w) = image.shape[:2]
    
    # Compute the rotation matrix
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Compute the sine and cosine of rotation angle
    cos = np.abs(rotation_matrix[0, 0])
    sin = np.abs(rotation_matrix[0, 1])

    # Compute new bounding dimensions after rotation
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))

    # Adjust rotation matrix to account for translation
    rotation_matrix[0, 2] += (new_w / 2) - center[0]
    rotation_matrix[1, 2] += (new_h / 2) - center[1]

    # Perform rotation
    rotated_image = cv2.warpAffine(image, rotation_matrix, (new_w, new_h))
    return rotated_image

# Process each image in the directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff")):
        image_path = os.path.join(input_dir, filename)

        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Skipping {filename}: Unable to read image.")
            continue

        # Rotate without cropping
        rotated_image = rotate_image_without_cropping(image, angle)

        # Save the rotated image
        output_path = os.path.join(output_dir, "180_"+filename)
        cv2.imwrite(output_path, rotated_image)
        print(f"Rotated {filename} and saved to {output_path}")

print("Rotation process completed!")
