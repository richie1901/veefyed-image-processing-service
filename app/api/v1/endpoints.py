from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from app.schemas.image import ImageUploadResponse, AnalysisResponse, AnalysisRequest
from app.services.image_service import ImageService
from app.core.security import verify_api_key

router = APIRouter()

@router.post(
    "/upload", 
    response_model=ImageUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload an image",
    description="Uploads a JPEG or PNG image (max 5MB) and returns a unique image_id."
)
async def upload_image(
    file: UploadFile = File(...), 
    _ = Depends(verify_api_key)
):
    image_id = await ImageService.validate_and_save(file)
    return ImageUploadResponse(image_id=image_id)


@router.post(
    "/analyze", 
    response_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze an image",
    description="Performs mock skin analysis logic on a previously uploaded image_id."
)
async def analyze_image(
    request: AnalysisRequest, 
    _ = Depends(verify_api_key)
):
    result = ImageService.analyze_mock(request.image_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Image with ID {request.image_id} not found or could not be processed."
        )
    
    return AnalysisResponse(**result)