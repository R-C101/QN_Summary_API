from flask import Flask, request, jsonify
from helper_functions import summarize_transcript 
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
## Main API, recieves POST requests in json format with company_name and transcript_text fields
@app.route('/earnings_transcript_summary', methods=['POST'])
def earnings_transcript_summary():
    logger.info("Received transcript summary request")
    # Ensure the request has JSON data
    if not request.is_json:
        return jsonify({"error": "Request must be in JSON format"}), 400
    
    # Get JSON data from the request
    data = request.get_json()
    
    #edge cases and error handling
    
    # Check for required fields
    if 'company_name' not in data or 'transcript_text' not in data:
        return jsonify({"error": "Both 'company_name' and 'transcript_text' fields are required"}), 400

    company_name = data.get("company_name")
    transcript_text = data.get("transcript_text")

    # CHECK for 20,000 token limit(Ideally you would want to check for the number of tokens in the transcript_text, but here for simplicity i'm just using the number of words)
    if not transcript_text or len(transcript_text.split()) > 20000:
        return jsonify({"error": "The 'transcript_text' must be non-empty and under 20,000 tokens"}), 400


    try:
        summary = summarize_transcript(transcript_text, company_name)
        logger.info(f"Successfully processed transcript for {company_name}")
        
        return jsonify(summary), 200
    #any other error handling
    except Exception as e:
        logger.error(f"Error processing transcript: {str(e)}")
        return jsonify({"error": "An error occurred while processing the transcript", "details": str(e)}), 500
    
## Test API
@app.route('/test', methods=['GET'])
def test():
    return "API is working!"

if __name__ == '__main__':
    app.run()