from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Image Processing Service API"
    API_V1_STR: str = "/api/v1"
    SECRET_API_KEY: str = "imageProcessingService@2026"
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 5 * 1024 * 1024
    ALLOWED_CONTENT_TYPES: list = ["image/jpeg", "image/png"]

    class Config:
        env_file = ".env"

settings = Settings()