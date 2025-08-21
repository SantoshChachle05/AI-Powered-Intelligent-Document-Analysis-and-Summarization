from PIL import Image
import os

def images_to_pdf(image_folder, output_pdf):
    # Get all image files in the directory
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif'))]
    image_files.sort()  # Optional: Sort files to maintain order

    if not image_files:
        print("No images found in the directory.")
        return

    image_list = []

    # Open images and convert them to RGB mode (necessary for PDF)
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        with Image.open(image_path) as img:
            img = img.convert('RGB')
            image_list.append(img)

    # Save all images as a single PDF
    if image_list:
        image_list[0].save(output_pdf, save_all=True, append_images=image_list[1:])
        print(f"PDF created successfully: {output_pdf}")
    else:
        print("No valid images to save.")

if __name__ == "__main__":
    image_folder = input("Enter the folder path containing images: ")
    output_pdf = input("Enter the output PDF file path (e.g., output.pdf): ")
    images_to_pdf(image_folder, output_pdf)

