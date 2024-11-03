import PyPDF2
import google.generativeai as genai
from typing import Dict, Any, Tuple, Optional

## This function reads the text from a PDF file and returns it as a string, this is not needed for the functionality of the API and was used for testing with the given pdf files
def read_pdf_text(pdf_path:str)-> str:
    text = ""
    # Open the PDF file
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        # Iterate through all the pages
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()  # Append page text to the main text string
    return text

## This function calls the gemini API to generate a summary based on the given prompt
def call_model_api(prompt:str)-> str:
    genai.configure(api_key='your_api_key')
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

## generates summary for a given transcript based on the category and details provided

def generate_summary(transcript:str, category:str, details:str)-> str:
    prompt = f"""
    Given the following transcript, provide a concise summary specifically focused on {category}. The summary should contain:
    - {details}
    
    If there is no information related to {category} in the transcript, return only "NA".

    Only output the summary text or "NA" without any additional formatting.
    
    Transcript: "{transcript}"
    """

    response = call_model_api(prompt)
    return response.strip() # Stripping extra whitespace, if any

## Binds all of the functions together to generate a summary for each category based on the transcript provided
def summarize_transcript(transcript:str, company_name:str = 'Not provided') -> Dict[str, Any]:
    categories = {
        "Financial Performance": "key financial metrics or statements about the company’s recent performance",
        "Market Dynamics": "any commentary on market trends, demand shifts, competition, etc.",
        "Expansion Plans": "information on the company’s plans for growth or expansion",
        "Environmental Risks": "references to environmental issues, sustainability, or ESG concerns",
        "Regulatory or Policy Changes": "information on recent or upcoming regulatory or policy changes affecting the company"
    }
    summary_json = {}
    
    # Loop through each category and generate its summary
    for category, details in categories.items():
        try:
            summary_json[category.lower().replace(" ", "_")] = generate_summary(transcript, category, details)
        except Exception as e:
            summary_json[category.lower().replace(" ", "_")] = "Error in generating summary"
        

    
    return {
        "company_name": company_name,  
        **summary_json
    }