from fastapi import FastAPI
from app.api.v1.endpoints import router as api_v1_router
from app.core.config import settings
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.on_event("startup")
def startup_event():
    logger.info(f"Starting {settings.PROJECT_NAME}...")
    logger.info(f"Upload directory set to: {settings.UPLOAD_DIR}")
    if not os.path.exists(settings.UPLOAD_DIR):
        os.makedirs(settings.UPLOAD_DIR)

app.include_router(api_v1_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Health"])
def root():
    return {"message": "Image Processing Service API is running", "docs": "/docs"}