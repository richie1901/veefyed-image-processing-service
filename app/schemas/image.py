from pydantic import BaseModel, Field
from typing import List,Dict, Any, Union

class ImageUploadResponse(BaseModel):
    image_id: str

class AnalysisRequest(BaseModel):
    image_id: str = Field(..., example="abc123")

class AnalysisResponse(BaseModel):
    image_id: str
    skin_type: str
    issues: List[str]
    confidence: float
    metadata: Dict[str, Any]