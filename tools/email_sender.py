import os
import json

def send_email(email: str, content: str, mock_mode: bool = True) -> str:
    """Sends an automated cold outreach email using Resend.
    
    Args:
        email: The target email address.
        content: The email content to send.
        mock_mode: If True, returns a deterministic mock JSON response.
    """
    if mock_mode:
        mock_response = {
            "status": "success",
            "to": email,
            "message_id": "mock_msg_12345",
            "content_snippet": content[:50] + "..."
        }
        return json.dumps(mock_response)
        
    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        raise ValueError("RESEND_API_KEY environment variable not set.")
    return json.dumps({"status": "real_mode_not_implemented"})
