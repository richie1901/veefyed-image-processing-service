import os
import uuid
import shutil

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def perform_mock_analysis(image_id: str):
    exists = any(f.startswith(image_id) for f in os.listdir(UPLOAD_DIR))
    if not exists:
        return None
    
    return {
        "image_id": image_id,
        "skin_type": "Oily",
        "issues": ["Hyperpigmentation", "Minor Acne"],
        "confidence": 0.87
    }