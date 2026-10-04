from fastapi import APIRouter
from app.schemas.response import APIResponse

router = APIRouter()

@router.get("/health", response_model=APIResponse[dict])
def health_check():
    return APIResponse(
        success=True,
        message="Backend is running",
        data={"status": "healthy", "version": "1.0.0"}
    )
