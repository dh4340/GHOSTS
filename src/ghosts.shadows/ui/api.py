from typing import Any
import requests
from .config import SHADOWS_URL

def query_api(input_text: str, model: str, token: str) -> Any | str:
    """Query the API with the given input text and model."""
    if not token:
        return "Please log in to access."
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{SHADOWS_URL}/{model}", json={"query": input_text}, headers=headers
    )
    if response.ok:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"
