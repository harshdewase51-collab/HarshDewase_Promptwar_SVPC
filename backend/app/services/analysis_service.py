import logging
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.analysis import AnalysisRequest, AnalysisResult
from app.services.ai_service import ai_service
from app.models.user import User

logger = logging.getLogger("blindspot.analysis")

class AnalysisService:
    @staticmethod
    async def process_analysis(
        request_data: AnalysisRequest,
        current_user: Optional[User] = None,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        """Audits the decision reasoning and optionally persists to DB."""
        # Validate minimum inputs
        if len(request_data.decision.strip()) < 3:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Please specify a concrete decision you are considering."
            )
        if len(request_data.reasoning.strip()) < 5:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Please explain your reasoning behind this choice."
            )

        # Execute AI reasoning audit
        try:
            raw_audit = await ai_service.generate_audit(
                decision=request_data.decision.strip(),
                context=request_data.context.strip() if request_data.context else "",
                reasoning=request_data.reasoning.strip()
            )
        except Exception as e:
            logger.error(f"Error invoking AI reasoning engine: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="The reasoning audit engine is temporarily unavailable. Please try again."
            )

        # Validate with Pydantic model
        validated_result = AnalysisResult(**raw_audit)

        decision_id = None
        # If user is authenticated and DB is available, persist the record
        if current_user and db:
            try:
                from app.services.decision_service import decision_service
                saved_decision = decision_service.create_decision_with_analysis(
                    db=db,
                    user_id=current_user.id,
                    decision=request_data.decision.strip(),
                    context=request_data.context.strip() if request_data.context else "",
                    reasoning=request_data.reasoning.strip(),
                    analysis_data=validated_result.model_dump()
                )
                decision_id = saved_decision.id
            except Exception as db_err:
                logger.warning(f"Unable to save analysis to database: {db_err}")
                # Do not block the user response if database fails
                pass

        return {
            "decision_id": decision_id,
            "decision": request_data.decision.strip(),
            "context": request_data.context.strip() if request_data.context else "",
            "reasoning": request_data.reasoning.strip(),
            "analysis": validated_result.model_dump()
        }

analysis_service = AnalysisService()
