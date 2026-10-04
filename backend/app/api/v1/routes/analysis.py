from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.analysis import AnalysisRequest
from app.schemas.response import APIResponse
from app.services.analysis_service import analysis_service
from app.core.security import get_current_user_optional
from app.models.user import User

router = APIRouter(tags=["analysis"])

@router.post("/analysis", response_model=APIResponse[dict])
async def analyze_decision(
    request_data: AnalysisRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    result = await analysis_service.process_analysis(
        request_data=request_data,
        current_user=current_user,
        db=db
    )
    return APIResponse.ok(
        data=result,
        message="Reasoning audit generated successfully"
    )
