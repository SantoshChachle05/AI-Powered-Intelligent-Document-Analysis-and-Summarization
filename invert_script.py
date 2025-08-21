from PIL import Image
import os

# Directories
input_directory = "/home/aventior_sant/Desktop/CPV.20/pdf_to_png/A012330090-BMR"
output_directory = "latest_pdf_to_png"

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

# Process each image
for filename in os.listdir(input_directory):
    input_path = os.path.join(input_directory, filename)
    output_path = os.path.join(output_directory, filename[:-2]+'.png')
    
    # Check if it's an image
    if filename.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
        with Image.open(input_path) as img:
            # Rotate 180 degrees and save
            inverted_img = img.rotate(180)
            inverted_img.save(output_path)
            print(f"Inverted: {filename}")

print("All images inverted and saved.")
