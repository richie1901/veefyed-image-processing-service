from fastapi import Header, HTTPException, status
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)
def verify_api_key(x_api_key: str = Header(..., description="API Key for authentication")):
    if x_api_key != settings.SECRET_API_KEY:
        logger.warning("Unauthorized access attempt with invalid API Key")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    return x_api_key