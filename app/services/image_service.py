import os
import uuid
import shutil
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings
import logging
import hashlib

logger = logging.getLogger(__name__)

class ImageService:
    #Using pool of mock data for analysis
    SKIN_TYPES = ["Oily", "Dry", "Combination", "Sensitive", "Normal"]
    CONCERNS = ["Hyperpigmentation", "Acne", "Fine Lines", "Redness", "Enlarged Pores"]

    @staticmethod
    def _format_file_size(size_in_bytes: int) -> str:
        """Converts bytes to a human-readable string (KB or MB)."""
        if size_in_bytes < 1024:
            return f"{size_in_bytes} Bytes"
        elif size_in_bytes < 1024 * 1024:
            return f"{round(size_in_bytes / 1024, 2)} KB"
        else:
            return f"{round(size_in_bytes / (1024 * 1024), 2)} MB"

    @staticmethod
    async def validate_and_save(file: UploadFile) -> str:
        logger.info(f"Received upload request: {file.filename} ({file.content_type})")

        if file.content_type not in settings.ALLOWED_CONTENT_TYPES:
            logger.warning(f"Rejected file {file.filename}: Allowed content type {settings.ALLOWED_CONTENT_TYPES} not with file content {file.content_type}")
            raise HTTPException(status_code=400, detail="Unsupported file type.")

        content = await file.read()
        if len(content) > settings.MAX_FILE_SIZE:
            logger.warning(f"Rejected file {file.filename}: Size {len(content)} exceeds limit {settings.MAX_FILE_SIZE}")
            raise HTTPException(status_code=413, detail="File too large.")
        await file.seek(0)

        image_id = str(uuid.uuid4())
        file_ext = "jpg" if file.content_type == "image/jpeg" else "png"
        file_path = os.path.join(settings.UPLOAD_DIR, f"{image_id}.{file_ext}")

        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            logger.info(f"Image saved successfully: {image_id} at {file_path}")
        except Exception as e:
            logger.error(f"Failed to save image {image_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal storage error")
        
        return image_id

    @staticmethod
    def analyze_mock(image_id: str):
        logger.info(f"Attempting analysis for image_id: {image_id}")
        path_exists = False
        file_size = 0
        for f in os.listdir(settings.UPLOAD_DIR):
            if f.startswith(image_id):
                full_path = os.path.join(settings.UPLOAD_DIR, f)
                file_size = os.path.getsize(full_path)
                path_exists = True
                break
        
        if not path_exists:
            logger.error(f"Analysis failed: Image ID {image_id} not found on disk")
            return None
        seed = int(hashlib.sha256(image_id.encode()).hexdigest(), 16)
        skin_index = seed % len(ImageService.SKIN_TYPES)
    
        confidence = round(min(0.99, 0.80 + (file_size / 5242880) * 0.19), 2)

        logger.info(f"Analysis complete for {image_id}")
        return {
            "image_id": image_id,
            "skin_type": ImageService.SKIN_TYPES[skin_index],
            "issues": [ImageService.CONCERNS[seed % len(ImageService.CONCERNS)]],
            "confidence": confidence,
            "metadata": {
                "processed_file_size": ImageService._format_file_size(file_size),
                "analysis_engine": "Image Processing Service-v1-Mock"
            }
        }