from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.schemas.analysis import AnalysisResult

class DecisionSummary(BaseModel):
    id: str
    decision: str
    context: Optional[str] = ""
    reasoning: str
    created_at: datetime

    class Config:
        from_attributes = True

class DecisionResponse(BaseModel):
    id: str
    decision: str
    context: Optional[str] = ""
    reasoning: str
    created_at: datetime
    analysis: Optional[AnalysisResult] = None

    class Config:
        from_attributes = True

class DashboardData(BaseModel):
    total_decisions: int
    recent_decisions: List[DecisionSummary] = []
