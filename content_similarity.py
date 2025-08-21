import os
import fitz
from difflib import SequenceMatcher
import pandas as pd
import json



def calculate_similarity(text1, text2):
    # Calculate the similarity ratio between two texts
    return SequenceMatcher(None, text1, text2).ratio()

def identify_outliers(group):
    q1 = group["Similarity Score"].quantile(0.25)
    q3 = group["Similarity Score"].quantile(0.75)
    iqr = q3 - q1
#     lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = group[(group["Similarity Score"] > upper_bound)]
    if outliers.empty:
        outliers = group.nlargest(3, "Similarity Score")
    return outliers

def content_similarity_main(pdf1_path, pdf2_path):
    '''
    The function compares each pages of MBR with all test sample pages of both searchable pdf 
    and return a json having content similarty score of each pages among two pdfs 
    '''
    print('\n ******************Commence Content Similarity Processing********************************')
    try:
        pdf2_filename = os.path.splitext(os.path.basename(pdf2_path))[0]
        folder_name = os.path.join(os.getcwd(), 'content_similarity')
        os.makedirs(folder_name, exist_ok=True)
        output_json_path = os.path.join(folder_name, f'{pdf2_filename}_content_similarity.json')

        top_n = 5

        pages_to_compare = None

        pdf1_doc = fitz.open(pdf1_path)
        pdf2_doc = fitz.open(pdf2_path)

        if pages_to_compare:
            pages_to_compare = [int(page) for page in pages_to_compare.split(',')]
        else:
            pages_to_compare = range(1, len(pdf1_doc) + 1)

        data = []  # List to store the data for JSON

        for pdf1_page_num in pages_to_compare:
            if pdf1_page_num < 1 or pdf1_page_num > len(pdf1_doc):
                print(f"Page {pdf1_page_num} is out of range. Skipping this page.")
                continue

            pdf1_page = pdf1_doc[pdf1_page_num - 1]
            pdf1_text = pdf1_page.get_text()

            similarities = []  # Store the similarity scores for the top N pages
            for pdf2_page_num in range(len(pdf2_doc)):
                pdf2_page = pdf2_doc[pdf2_page_num]
                pdf2_text = pdf2_page.get_text()

                similarity = calculate_similarity(pdf1_text, pdf2_text)
                similarities.append((pdf2_page_num + 1, similarity))

            similarities.sort(key=lambda x: x[1], reverse=True)
            top_similar_pages = similarities[:top_n]

            for page_num, similarity in top_similar_pages:
                 data.append({'Actual_Batch_Record_Page': pdf1_page_num, 'Sample_Batch_Record_Page': page_num,
                            'Similarity Score': similarity})


        pdf1_doc.close()
        pdf2_doc.close()
        
        df = pd.DataFrame(data)

        # Use the provided logic to identify outliers and add them to a separate DataFrame
        outlier_df = df.groupby('Actual_Batch_Record_Page').apply(identify_outliers).reset_index(drop=True)

        # Save the outliers to the output JSON file
        outlier_df.to_json(output_json_path, orient='split', index=False)
        return output_json_path
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    pdf1 = "/home/aventior_sant/Desktop/CPV.20/Sample-9690.pdf"
    pdf2 = "/home/aventior_sant/Desktop/CPV.20/Sample-9700.pdf"
    content_similarity_main(pdf1, pdf2)

if __name__ == "__main__":
    main()
