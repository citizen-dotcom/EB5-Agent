# Purpose: Wrapper functions for Lucidchart API (create document, add shapes, add connectors).
import requests
from .config import settings

def _headers():
    """Authorization headers using env-provided Lucidchart API key."""
    return {"Authorization": f"Bearer {settings.LUCID_API_KEY}"}

def create_document(title: str, description: str = "EB-5 Flow of Funds") -> str:
    """Create a new Lucidchart document and return its ID."""
    url = "https://api.lucidchart.com/v1/documents"
    resp = requests.post(url, headers=_headers(), json={"title": title, "description": description})
    resp.raise_for_status()
    return resp.json().get("id")

def add_shape(doc_id: str, text: str, category: str, x: int, y: int, width: int = 240, height: int = 100) -> str:
    """Add a rectangle shape with text, color-coded by category (unknowns = no color)."""
    color = settings.get_color(category)
    url = f"https://api.lucidchart.com/v1/documents/{doc_id}/shapes"
    payload = {
        "type": "rectangle",
        "text": text,
        "x": x, "y": y,
        "width": width, "height": height,
        "style": {"fillColor": color, "strokeColor": "#000000", "fontSize": 12}
    }
    resp = requests.post(url, headers=_headers(), json=payload)
    resp.raise_for_status()
    return resp.json().get("id")

def add_connector(doc_id: str, from_id: str, to_id: str):
    """Draw an arrow connector between two shapes."""
    url = f"https://api.lucidchart.com/v1/documents/{doc_id}/connectors"
    payload = {"fromShapeId": from_id, "toShapeId": to_id, "style": {"strokeColor": "#000000", "arrowHead": "filled"}}
    resp = requests.post(url, headers=_headers(), json=payload)
    resp.raise_for_status()