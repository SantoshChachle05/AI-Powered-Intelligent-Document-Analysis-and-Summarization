✅ Modified Code Snippet (insert inside your existing function):
First, at the top of the script, add a way to load the bounding box JSON:

python
Copy
Edit
with open("bounding_box_data.json") as bbox_file:  # Replace with actual path if needed
    bbox_data = json.load(bbox_file)
Then, update the loop where you append questions_with_responses like so:

python
Copy
Edit
        questions_with_responses = []
        for (question_key, question_description), response in zip(all_questions, responses):
            description = question_description.get("Description", "").strip()
            
            # Get bbox using helper function
            bbox = get_bounding_box(bbox_data, actual_page_number, response)

            questions_with_responses.append({
                question_key: {
                    "value": response,
                    "actual_page_number": actual_page_number,
                    "Description": description,
                    "bbox": bbox if bbox else []
                }
            })
✅ Helper Function (add outside process_images_and_questions()):
python
Copy
Edit
def get_bounding_box(json_data, actual_page_number, matched_response):
    for entry in json_data:
        pages = entry.get("pages", [])
        for page in pages:
            try:
                page_no = int(page.get("pageNo", -1))
            except ValueError:
                continue

            if page_no == actual_page_number:
                for area in page.get("areas", []):
                    if area.get("name", "").strip().lower() == matched_response.strip().lower():
                        return area.get("coords", [])
    return None
✅ Output Sample (final structure):
Your output JSON will now look like this:

json
Copy
Edit
{
  "questions": [
    {
      "DrugName": {
        "value": "COGNATE",
        "actual_page_number": 0,
        "Description": "The name of the drug",
        "bbox": [346.0, 282.0, 558.0, 358.0]
      }
    }
  ]
}
