# import cv2
# import numpy as np

# def estimate_skew_angle(image_path):
#     # Load the image
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Apply edge detection
#     edges = cv2.Canny(gray, 50, 150, apertureSize=3)

#     # Use Hough Line Transform to detect lines
#     lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=5)
    
#     angles = []
#     if lines is not None:
#         for line in lines:
#             x1, y1, x2, y2 = line[0]
#             angle = np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi
#             angles.append(angle)
    
#     # Compute the median angle to reduce outliers
#     return np.median(angles) if angles else 0

# def rotate_image(image_path, output_path):
#     image = cv2.imread(image_path)
#     angle = estimate_skew_angle(image_path)
    
#     # Get image size and compute rotation matrix
#     (h, w) = image.shape[:2]
#     center = (w // 2, h // 2)
#     M = cv2.getRotationMatrix2D(center, angle, 1.0)
#     rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
#     # Save the deskewed image
#     cv2.imwrite(output_path, rotated)
#     print(f"Deskewed image saved at: {output_path}")

# # Example usage
# image_path = "/home/aventior_sant/Desktop/CPV.20/pdf_to_png/complex_images_1/complex_images_1_5.png"  # Replace with your image path
# output_path = "deskewed_image_3.png"
# rotate_image(image_path, output_path)

import os
import traceback
import io
import math
import numpy as np
import pandas as pd
import pytesseract
import imutils
import cv2
import img2pdf
import shutil
import glob
import json
import re
import multiprocessing as mp
from multiprocessing import cpu_count
from deskew import determine_skew
from functools import partial
from pdf2image import convert_from_path
from typing import Tuple, Union
from pytesseract import Output, TesseractError
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import argparse
import fitz  # PyMuPDF
from difflib import SequenceMatcher
import csv
import PyPDF2
from PIL import Image
# from paddleocr import PaddleOCR, draw_ocr
IMAGE_SHAPE = (224, 224)
from scipy.spatial import distance 
import imagehash
import tensorflow as tf
import tensorflow_hub as hub



def fix_orientation(image):
    if image is None:
        raise ValueError("Image not loaded or is empty.")

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pytesseract.image_to_osd(rgb, output_type=pytesseract.Output.DICT)
    rotated_image = imutils.rotate_bound(image, angle=results["rotate"])
    return rotated_image

def deskew_with_smaller_angle(images_save_path,pdf_name):
    print('\n********************************Commence Deskew processing****************************************')
    """
    Args:
        images_save_path: path to store rotated images
    """
    pdf_name_1=pdf_name
    # Create the output folder for rotated images
    rot_images_dir = os.path.join(os.getcwd(),'deskew/'+ pdf_name_1)
    try:
        os.makedirs(rot_images_dir, exist_ok=True)
    except FileExistsError:
        pass

    # Iterate through the images in the input folder
    for image_name in os.listdir(images_save_path):
        image_path = os.path.join(images_save_path, image_name)

        # Create the output path for each rotated image
        rot_img_path = os.path.join(rot_images_dir, image_name)

        # Load the image
        img = cv2.imread(image_path)

        # Check if the image is loaded successfully
        if img is None:
            print(f"Error loading image: {image_path}")
            continue

        try:
            final_deskewed_image = fix_orientation(img)
        except TesseractError:
            final_deskewed_image = img

        # Writing the rotated image
        try:
            cv2.imwrite(rot_img_path, final_deskewed_image)
        except TypeError:
            cv2.imwrite(rot_img_path, final_deskewed_image)

    print(f"Deskewing completed. Rotated images saved in: {rot_images_dir}")
    print('\n**************************** Conclude Deskew processing ***************************************')
    return rot_images_dir,pdf_name_1


if __name__ == "__main__":
    # Example usage
    images_directory = "/home/aventior_sant/Desktop/CPV.20/sample"
    pdf_name = "sample"

    deskew_with_smaller_angle(images_directory, pdf_name)