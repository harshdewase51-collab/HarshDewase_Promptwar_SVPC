from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.decision import DecisionSummary, DecisionResponse
from app.schemas.response import APIResponse
from app.services.decision_service import decision_service
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/decisions", tags=["decisions"])

@router.get("", response_model=APIResponse[List[DecisionSummary]])
def list_decisions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    decisions = decision_service.get_user_decisions(db=db, user_id=current_user.id)
    return APIResponse.ok(data=decisions, message="Decisions retrieved successfully")

@router.get("/{decision_id}", response_model=APIResponse[DecisionResponse])
def get_decision(
    decision_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    decision = decision_service.get_decision_by_id(
        db=db,
        decision_id=decision_id,
        user_id=current_user.id
    )
    return APIResponse.ok(data=decision, message="Decision audit retrieved successfully")
