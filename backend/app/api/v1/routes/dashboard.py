from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.decision import DashboardData
from app.schemas.response import APIResponse
from app.services.dashboard_service import dashboard_service
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("", response_model=APIResponse[DashboardData])
def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    stats = dashboard_service.get_dashboard_data(db=db, user_id=current_user.id)
    return APIResponse.ok(data=stats, message="Dashboard metrics retrieved")
