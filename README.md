# Summary API Documentation - Rishit Chugh QNEXT

## Overview
The Earnings Transcript Summary API processes earnings call transcripts and generates concise summaries across multiple categories using the Gemini AI model. The API analyzes transcripts for key information about financial performance, market dynamics, expansion plans, environmental risks, and regulatory changes.

 NOTE: To run the code in this repository please add your own Gemini api key in helper_functions.py
## API Endpoint
```
POST https://rishitchugh.pythonanywhere.com/earnings_transcript_summary
```

## Request Format
The API accepts POST requests with JSON payloads containing the following fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| company_name | string | Yes | Name of the company whose transcript is being analyzed |
| transcript_text | string | Yes | The earnings call transcript text to be summarized |

### Example Request Body
```json
{
    "company_name": "Reliance Industries",
    "transcript_text": "Your transcript text here..."
}
```

## Response Format
The API returns a JSON response with the following structure:

```json
{
    "company_name": "Reliance Industries",
    "financial_performance": "Summary of financial metrics...",
    "market_dynamics": "Summary of market trends...",
    "expansion_plans": "Summary of growth plans...",
    "environmental_risks": "Summary of environmental concerns...",
    "regulatory_or_policy_changes": "Summary of regulatory updates..."
}
```

## Categories Analyzed
1. **Financial Performance**: Key financial metrics and statements about recent performance
2. **Market Dynamics**: Commentary on market trends, demand shifts, and competition
3. **Expansion Plans**: Information on growth and expansion strategies
4. **Environmental Risks**: References to environmental issues, sustainability, and ESG concerns
5. **Regulatory or Policy Changes**: Information about regulatory or policy changes affecting the company

## Response Codes
- 200: Success
- 400: Bad Request (missing fields or invalid input)
- 500: Internal Server Error

## Limitations
- Maximum transcript length: 20,000 tokens
- Transcript text must be non-empty
- All requests must include both required fields

## Testing Script
Here's a complete script to test the API with various scenarios:

```python
import requests
import json

def test_earnings_api():
    # Define the API URL
    url = "https://rishitchugh.pythonanywhere.com/earnings_transcript_summary"
    
    # Test cases
    test_cases = {
        "valid_request": {
            "company_name": "Sample Corp",
            "transcript_text": """
            In Q4 2023, we achieved revenue growth of 15% year-over-year, reaching $2.5 billion.
            Our market share in key segments expanded by 3 percentage points.
            We plan to open 50 new locations in emerging markets next year.
            We've reduced our carbon footprint by 20% and are on track for our 2025 sustainability goals.
            New regulations in the EU market will require additional compliance measures starting next quarter.
            """
        },
        "missing_field": {
            "company_name": "Sample Corp"
        },
        "empty_transcript": {
            "company_name": "Sample Corp",
            "transcript_text": ""
        },
        "too_long": {
            "company_name": "Sample Corp",
            "transcript_text": "word " * 20001
        }
    }
    
    for test_name, payload in test_cases.items():
        print(f"\nTesting: {test_name}")
        print("-" * 50)
        
        response = requests.post(url, json=payload)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response:")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)
        
        print("-" * 50)

if __name__ == "__main__":
    test_earnings_api()
```

## Example Usage with cURL
```bash
curl -X POST \
  https://rishitchugh.pythonanywhere.com/earnings_transcript_summary \
  -H 'Content-Type: application/json' \
  -d '{
    "company_name": "Sample Corp",
    "transcript_text": "Your transcript text here..."
}'
```

## Example Usage with Python Requests
```python
import requests

url = "https://rishitchugh.pythonanywhere.com/earnings_transcript_summary"
payload = {
    "company_name": "Sample Corp",
    "transcript_text": "Your transcript text here..."
}

response = requests.post(url, json=payload)
summary = response.json()
```

## Error Handling
The API returns detailed error messages for common issues:

```json
{
    "error": "Request must be in JSON format"
}
```
```json
{
    "error": "Both 'company_name' and 'transcript_text' fields are required"
}
```
```json
{
    "error": "The 'transcript_text' must be non-empty and under 20,000 tokens"
}
```
## Decisions Taken:
I took some decisions and assumptions while making the code:
- I did not use tokenisation to check for the 20,000 limit, i used the word count instead. in a production environment we would tokenise and count the number of tokens instead.
- While generating the summary I chose to create summaries for each part in a separate request to make it more robust to failure, from my previous experiences, while asking for the entire thing at once works most of the time, certain updates pushed to the model make the engineered prompt that was used to get the json back, outdated. To solve this I used a more robust approach of collecting each summary seperately and combining them on my own instead. This allows me to return a json without relying on Gemini to provide me incorrect or extra words such as 'Sure Here is'. This obviously increases the time to response.
- When certain data is not given, the summary is prompt engineered to be returned as 'NA' for future parsing consistency and saving tokens.

## Dependencies
The API uses the following key dependencies:
- Flask for the web framework
- Google's Generative AI (Gemini) for text summarization



