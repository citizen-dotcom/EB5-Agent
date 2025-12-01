# Purpose: OCR fallback for extracting passport name if not already indexed.
import re
from PIL import Image
import pytesseract
from typing import Tuple

def extract_passport_name(image_path: str) -> Tuple[str, str]:
    """Run OCR on a passport image and try to extract the government name."""
    text = pytesseract.image_to_string(Image.open(image_path))
    match = re.search(r"(?:Surname|Name|Given Names)\s*[:\-]?\s*([A-Z\s]+)", text, re.IGNORECASE)
    return (match.group(1).strip() if match else "UNKNOWN", text)