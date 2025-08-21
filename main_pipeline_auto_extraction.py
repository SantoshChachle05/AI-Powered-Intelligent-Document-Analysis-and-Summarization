import os
import json
import pyAesCrypt
import shutil
from boto3 import client as boto_client
from boto3.s3.transfer import S3Transfer
from dotenv import load_dotenv
from PIL import Image
from transformers import AutoModel, AutoTokenizer
import pandas as pd
from difflib import SequenceMatcher
import fitz
import torch
dir = '/home/server4/Documents/AWS_EC2_docs/Model_o'

model = AutoModel.from_pretrained(dir, trust_remote_code=True,
                                           attn_implementation='sdpa', torch_dtype=torch.bfloat16)
model = model.eval().cuda()
tokenizer = AutoTokenizer.from_pretrained(dir, trust_remote_code=True)
# Load environment variables
load_dotenv()

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_REGION = os.getenv("S3_REGION", "us-west-2")

def check_connection_s3():
    """Check connection with S3 bucket."""
    client = None
    transfer = None
    try:
        client = boto_client('s3', aws_access_key_id=S3_ACCESS_KEY, 
                             aws_secret_access_key=S3_SECRET_KEY,
                             region_name=S3_REGION)
        transfer = S3Transfer(client)
    except Exception as e:
        print(f"Error connecting to S3: {e}")
    return client, transfer

def load_file_paths_from_json(json_path):
    """Load file paths and decryption keys from the JSON input file."""
    with open(json_path, 'r') as file:
        return json.load(file)

# def download_file(file_key, local_path):
#     """
#     Download a file from S3 to a local path.
#     """
#     try:
#         client.download_file(S3_BUCKET_NAME, file_key, local_path)
#         print(f"Downloaded {file_key} to {local_path}")
#     except Exception as e:
#         print(f"Failed to download {file_key}: {e}")

# def process_files(input_json_path):
#     """
#     Process the files by downloading, decrypting, and unpacking them as needed.
#     Returns the directories where the decrypted files are stored.
#     """
#     file_data = load_file_paths_from_json(input_json_path)

#     # Assuming the first item in the list contains the relevant data
#     if isinstance(file_data, list) and len(file_data) > 0:
#         file_data = file_data[0]  # Get the first (and only) dict from the list
#     else:
#         print("Error: Input JSON does not contain valid data.")
#         return {}

#     base_path = "/home/server4/Documents/AWS_EC2_docs/decpt_data"
#     pdf_dir = os.path.join(base_path, "data_to_download_searchable_pdf")
#     deskew_dir = os.path.join(base_path, "data_to_download_Deskew_folder")

#     os.makedirs(pdf_dir, exist_ok=True)
#     os.makedirs(deskew_dir, exist_ok=True)

#     result_paths = {"searchable_pdf": [], "zip_data": []}  # Dictionary to store results

#     for file_info in file_data.get("data_to_download_searchable_pdf", []):
#         file_key = file_info["file_key"]
#         encrypted_file = os.path.join("/home/server4/Documents/AWS_EC2_docs", os.path.basename(file_key))

#         private_key = file_info.get("decryption_key")
#         if not private_key:
#             print(f"Decryption key not found for file: {file_key}")
#             continue
#         # print(f"Downloading {file_key} to {encrypted_file}")
#         download_file(file_key, encrypted_file)

#         decrypted_file = os.path.join(pdf_dir, os.path.basename(file_key))  # Save in searchable PDF directory
#         buffer_size = 64 * 2048

#         # print(f"Decrypting {encrypted_file} to {decrypted_file}")
#         private_key = private_key.replace('\n', '\\n')
#         pyAesCrypt.decryptFile(encrypted_file, decrypted_file, private_key, buffer_size)
#         # print(f"Decrypted searchable PDF: {decrypted_file}")

#         result_paths["searchable_pdf"].append(decrypted_file)
#     print("20% - Download and decryption of searchable PDFs complete.")
        

#     for file_info in file_data.get("data_to_download_Deskew_folder", []):
#         file_key = file_info["file_key"]
#         encrypted_file = os.path.join("/home/server4/Documents/AWS_EC2_docs", os.path.basename(file_key))
#         decrypted_file = os.path.join(deskew_dir, os.path.basename(file_key).replace('.zip', '.pdf'))  # Save in Deskew folder
#         buffer_size = 64 * 2048

#         private_key = file_info.get("decryption_key")
#         if not private_key:
#             print(f"Decryption key not found for file: {file_key}")
#             continue

#         # print(f"Downloading {file_key} to {encrypted_file}")
#         download_file(file_key, encrypted_file)
#         # print(f"Decrypting {encrypted_file} to {decrypted_file}")
#         private_key = private_key.replace('\n', '\\n')
#         pyAesCrypt.decryptFile(encrypted_file, decrypted_file, private_key, buffer_size)
#         # print(f"Decrypted Deskew file: {decrypted_file}")

#         f_name = os.path.splitext(os.path.basename(file_key))[0]
#         # zip_folder = os.path.join('/home/server4/Documents/AWS_EC2_docs/zip_data', f_name)
#         zip_folder = os.path.join('/home/server4/Documents/AWS_EC2_docs/zip_data', f_name.replace('_zip_encrypt', ''))
#         os.makedirs(zip_folder, exist_ok=True)
#         shutil.unpack_archive(decrypted_file, zip_folder, 'zip')

#         result_paths["zip_data"].append(zip_folder)
#         # print('zip_folder',zip_folder)
#     print("40% - Download and decryption of Deskew files complete.")
#     return {
#         "searchable_pdf": pdf_dir,
#         "zip_data": os.path.dirname(zip_folder)
#     }


def calculate_similarity(text1, text2):
    return SequenceMatcher(None, text1, text2).ratio()

def content_similarity_main(pdf1_path, pdf2_path):
    
    try:
        pdf2_filename = os.path.splitext(os.path.basename(pdf2_path))[0]
        folder_name = os.path.join(os.getcwd(), 'content_similarity')
        os.makedirs(folder_name, exist_ok=True)
        output_json_path = os.path.join(folder_name, f'{pdf2_filename}_content_similarity.json')

        pdf1_doc = fitz.open(pdf1_path)
        pdf2_doc = fitz.open(pdf2_path)

        data = []  # List to store the data for JSON

        for pdf1_page_num in range(len(pdf1_doc)):
            pdf1_page = pdf1_doc[pdf1_page_num]
            pdf1_text = pdf1_page.get_text()

            similarities = []  # Store the similarity scores for the top N pages
            for pdf2_page_num in range(len(pdf2_doc)):
                pdf2_page = pdf2_doc[pdf2_page_num]
                pdf2_text = pdf2_page.get_text()

                similarity = calculate_similarity(pdf1_text, pdf2_text)
                similarities.append((pdf2_page_num, similarity))

            similarities.sort(key=lambda x: x[1], reverse=True)
            top_similar_page = similarities[:1]  # Only get the top similar page

            for page_num, similarity in top_similar_page:
                data.append({'Actual_Batch_Record_Page': pdf1_page_num, 
                              'Sample_Batch_Record_Page': page_num,
                              'Similarity Score': similarity})

        pdf1_doc.close()
        pdf2_doc.close()

        df = pd.DataFrame(data)
        df.to_json(output_json_path, orient='split', index=False)
        print("60% - Content similarity algorithm complete.")
        return output_json_path
    except Exception as e:
        print(f"An error occurred: {e}")



def process_images_and_questions(input_json_path, searchable_pdf_path, deskew_folder_path):
    """Process the images and questions using already available local paths."""
    
    data = load_file_paths_from_json(input_json_path)
    results = {
        "data_to_download_searchable_pdf": data[0]["data_to_download_searchable_pdf"],
        "data_to_download_Deskew_folder": data[0]["data_to_download_Deskew_folder"],
        "mapping_detail": []
    }

    for mapping in data[0]['mapping_detail']:
        sample_pdf_name = mapping['sample_pdf_name']
        actual_pdf_name = mapping['actual_pdf_name']
        questions_list = mapping['questions']
        first_page_number = mapping['sample_page_number']

        pdf1_path = os.path.join(searchable_pdf_path, sample_pdf_name)
        pdf2_path = os.path.join(searchable_pdf_path, actual_pdf_name)

        if not os.path.exists(pdf1_path) or not os.path.exists(pdf2_path):
            print(f"PDF not found: {pdf1_path} or {pdf2_path}")
            continue

        content_sim = content_similarity_main(pdf1_path, pdf2_path)

        with open(content_sim) as f:
            page_info = json.load(f)

        actual_page_number = None
        for record in page_info['data']:
            if record[0] == first_page_number:
                actual_page_number = record[1]
                break

        if actual_page_number is None:
            print(f"No match found for page {first_page_number}")
            continue

        # Initialize model
        image_directory = os.path.join(deskew_folder_path, os.path.splitext(actual_pdf_name)[0])
        if not os.path.exists(image_directory):
            print(f"Image directory not found: {image_directory}")
            continue

        image_files = [f for f in os.listdir(image_directory) if f.endswith('.png')]
        image_file = None
        for img_file in image_files:
            try:
                page_number_from_filename = int(img_file.split('_')[-1].replace('.png', ''))
                if page_number_from_filename == actual_page_number:
                    image_file = img_file
                    break
            except ValueError:
                print(f"Skipping improperly named file: {img_file}")

        if image_file is None:
            print(f"No image file found for page {actual_page_number}")
            continue

        image_path = os.path.join(image_directory, image_file)
        try:
            image = Image.open(image_path).convert('RGB')
        except Exception as e:
            print(f"Failed to open image {image_path}: {e}")
            continue

        all_questions = []
        for questions in questions_list:
            all_questions.extend(questions.items())

        msgs = []
        for question_key, question_description in all_questions:
            description = question_description.get("Description", "").strip()
            dynamic_part = f"Extract only the value for the parameter '{question_key} {description} from the given Image'"
            static_part = ("The output should strictly contain the extracted values for the specified parameters, "
                           "presented without any additional information, explanations, or formatting...")
            question_prompt = f"{dynamic_part}. {static_part}"
            msgs.append({'role': 'user', 'content': [image, question_prompt]})

        responses = inference_model(model, tokenizer, image, msgs)
        if len(responses) != len(all_questions):
            print(f"Expected {len(all_questions)} responses, got {len(responses)}. Padding...")
            responses += [''] * (len(all_questions) - len(responses))

        questions_with_responses = []
        for (question_key, question_description), response in zip(all_questions, responses):
            description = question_description.get("Description", "").strip()
            questions_with_responses.append({
                question_key: {
                    "value": response,
                    "actual_page_number": actual_page_number,
                    "Description": description
                }
            })

        results["mapping_detail"].append({
            "sample_pdf_name": sample_pdf_name,
            "sample_page_number": first_page_number,
            "actual_pdf_name": actual_pdf_name,
            "questions": questions_with_responses
        })

    with open('results_auto_extraction.json', 'w') as outfile:
        json.dump(results, outfile, indent=4)
    print("100% - Image and question processing complete.")


def inference_model(model, tokenizer, image, msgs):
    """Run the model inference and return responses for all questions."""
    responses = []
    for msg in msgs:
        response = model.chat(
            image=None,
            msgs=[msg],
            tokenizer=tokenizer
        )
        responses.append(response)  
    return responses

if __name__ == "__main__":
    input_json_path = "/home/server4/Documents/CPV-QC-2.0/test/input_alynlym.json"
    searchable_pdf_path = "/home/server4/Documents/CPV-QC-2.0/test/searchable_pdf"
    deskew_folder_path = "/home/server4/Documents/CPV-QC-2.0/test/deskew_data"
    
    process_images_and_questions(input_json_path, searchable_pdf_path, deskew_folder_path)

    
    
