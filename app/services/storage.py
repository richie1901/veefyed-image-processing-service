import os
import uuid
import shutil

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_file(file) -> str:
    image_id = str(uuid.uuid4())
    extension = file.filename.split(".")[-1]
    path = os.path.join(UPLOAD_DIR, f"{image_id}.{extension}")
    
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return image_id
