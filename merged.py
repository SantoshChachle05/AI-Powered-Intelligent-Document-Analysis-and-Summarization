import os
import shutil

# Define folder paths
folder1 = "/home/aventior_sant/Desktop/CPV.20/pdf_to_png/A012330090-BMR"
folder2 = "/home/aventior_sant/Desktop/CPV.20/latest_pdf_to_png"
output_folder = "merged"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Get sorted list of images from both folders
images1 = sorted(os.listdir(folder1))
images2 = sorted(os.listdir(folder2))

# Merge and rename images sequentially
counter = 1

# Process first folder
for img in images1:
    ext = os.path.splitext(img)[1]  # Get file extension
    new_name = f"{counter}{ext}"
    shutil.copy(os.path.join(folder1, img), os.path.join(output_folder, new_name))
    counter += 1

# Process second folder
for img in images2:
    ext = os.path.splitext(img)[1]  # Get file extension
    new_name = f"{counter}{ext}"
    shutil.copy(os.path.join(folder2, img), os.path.join(output_folder, new_name))
    counter += 1

print("Merging complete! Check the output folder.")
