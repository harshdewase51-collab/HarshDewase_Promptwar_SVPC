from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.decision import Decision
from app.models.analysis import Analysis
from app.schemas.decision import DecisionSummary, DecisionResponse
from app.schemas.analysis import AnalysisResult

class DecisionService:
    @staticmethod
    def create_decision_with_analysis(
        db: Session,
        user_id: str,
        decision: str,
        context: Optional[str],
        reasoning: str,
        analysis_data: Dict[str, Any]
    ) -> Decision:
        # Create Decision record
        decision_record = Decision(
            user_id=user_id,
            decision=decision,
            context=context or "",
            reasoning=reasoning
        )
        db.add(decision_record)
        db.flush()

        # Create Analysis record
        analysis_record = Analysis(
            decision_id=decision_record.id,
            blind_spots=analysis_data.get("blind_spots", []),
            assumptions=analysis_data.get("assumptions", []),
            verification=analysis_data.get("verification", []),
            potential_conflicts=analysis_data.get("potential_conflicts", []),
            missing_factors=analysis_data.get("missing_factors", []),
            critical_questions=analysis_data.get("critical_questions", [])
        )
        db.add(analysis_record)
        db.commit()
        db.refresh(decision_record)
        return decision_record

    @staticmethod
    def get_user_decisions(db: Session, user_id: str) -> List[DecisionSummary]:
        decisions = (
            db.query(Decision)
            .filter(Decision.user_id == user_id)
            .order_by(Decision.created_at.desc())
            .all()
        )
        return [
            DecisionSummary(
                id=d.id,
                decision=d.decision,
                context=d.context or "",
                reasoning=d.reasoning,
                created_at=d.created_at
            )
            for d in decisions
        ]

    @staticmethod
    def get_decision_by_id(db: Session, decision_id: str, user_id: str) -> DecisionResponse:
        decision = db.query(Decision).filter(Decision.id == decision_id).first()
        if not decision:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Decision not found"
            )

        # Enforce that user can only access their own decision
        if decision.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view this decision audit"
            )

        analysis_obj = None
        if decision.analysis:
            analysis_obj = AnalysisResult(
                blind_spots=decision.analysis.blind_spots or [],
                assumptions=decision.analysis.assumptions or [],
                verification=decision.analysis.verification or [],
                potential_conflicts=decision.analysis.potential_conflicts or [],
                missing_factors=decision.analysis.missing_factors or [],
                critical_questions=decision.analysis.critical_questions or []
            )

        return DecisionResponse(
            id=decision.id,
            decision=decision.decision,
            context=decision.context or "",
            reasoning=decision.reasoning,
            created_at=decision.created_at,
            analysis=analysis_obj
        )

decision_service = DecisionService()
