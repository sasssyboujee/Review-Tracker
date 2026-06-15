import os
import json

def run_scraping(location_query: str, mock_mode: bool = True) -> str:
    """Uses Apify to extract business metadata, domains, and historical review text for a location.
    
    Args:
        location_query: The location and industry, e.g., "Singapore + Plumber".
        mock_mode: If True, returns a deterministic mock JSON response.
    """
    if mock_mode:
        mock_response = {
            "business_name": "Example Plumber SG",
            "domain": "exampleplumber.sg",
            "reviews": [
                {"rating": 1, "text": "Terrible service, very bad.", "date": "2023-10-01"},
                {"rating": 1, "text": "Scam! Do not use.", "date": "2023-10-02"},
                {"rating": 1, "text": "Overpriced and rude.", "date": "2023-10-03"},
                {"rating": 5, "text": "Good work.", "date": "2023-09-15"}
            ]
        }
        return json.dumps(mock_response)
    
    api_key = os.environ.get("APIFY_API_KEY")
    if not api_key:
        raise ValueError("APIFY_API_KEY environment variable not set.")
    return json.dumps({"status": "real_mode_not_implemented"})
