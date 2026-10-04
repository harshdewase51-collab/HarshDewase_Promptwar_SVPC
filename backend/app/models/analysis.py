import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.session import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    decision_id = Column(String(36), ForeignKey("decisions.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    blind_spots = Column(JSON, nullable=False)
    assumptions = Column(JSON, nullable=False)
    verification = Column(JSON, nullable=False)
    potential_conflicts = Column(JSON, nullable=False)
    missing_factors = Column(JSON, nullable=False)
    critical_questions = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    decision = relationship("Decision", back_populates="analysis")
