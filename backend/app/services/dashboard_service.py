from sqlalchemy.orm import Session
from app.models.decision import Decision
from app.schemas.decision import DashboardData, DecisionSummary

class DashboardService:
    @staticmethod
    def get_dashboard_data(db: Session, user_id: str) -> DashboardData:
        total = db.query(Decision).filter(Decision.user_id == user_id).count()
        recent = (
            db.query(Decision)
            .filter(Decision.user_id == user_id)
            .order_by(Decision.created_at.desc())
            .limit(5)
            .all()
        )
        recent_summaries = [
            DecisionSummary(
                id=d.id,
                decision=d.decision,
                context=d.context or "",
                reasoning=d.reasoning,
                created_at=d.created_at
            )
            for d in recent
        ]
        return DashboardData(
            total_decisions=total,
            recent_decisions=recent_summaries
        )

dashboard_service = DashboardService()
