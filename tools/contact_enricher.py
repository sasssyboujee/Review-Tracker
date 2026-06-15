import os
import json

def extract_contacts(domain: str, mock_mode: bool = True) -> str:
    """Uses Apollo.io to find the decision-maker email addresses associated with a business domain.
    
    Args:
        domain: The domain of the business.
        mock_mode: If True, returns a deterministic mock JSON response.
    """
    if mock_mode:
        mock_response = {
            "domain": domain,
            "decision_maker": "John Doe",
            "title": "Owner",
            "email": f"john.doe@{domain}"
        }
        return json.dumps(mock_response)
        
    api_key = os.environ.get("APOLLO_API_KEY")
    if not api_key:
        raise ValueError("APOLLO_API_KEY environment variable not set.")
    return json.dumps({"status": "real_mode_not_implemented"})
