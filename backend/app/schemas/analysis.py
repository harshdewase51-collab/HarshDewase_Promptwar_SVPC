from typing import List, Optional, Union
from pydantic import BaseModel, Field

class AnalysisRequest(BaseModel):
    decision: str = Field(..., min_length=3, max_length=2000, description="The decision you are considering")
    context: Optional[str] = Field(default="", max_length=5000, description="Context, constraints, background")
    reasoning: str = Field(..., min_length=5, max_length=5000, description="Why you think this is right / your rationale")

class BlindSpotItem(BaseModel):
    finding: str
    evidence: str
    why_it_matters: str

class AssumptionItem(BaseModel):
    assumption: str
    evidence: str
    needs_verification: bool = True

class VerificationItem(BaseModel):
    assumption: str
    verification: str

class ConflictItem(BaseModel):
    conflict: str
    evidence: str
    question: str

class AnalysisResult(BaseModel):
    blind_spots: List[BlindSpotItem] = []
    assumptions: List[AssumptionItem] = []
    verification: List[VerificationItem] = []
    potential_conflicts: List[ConflictItem] = []
    missing_factors: List[str] = []
    critical_questions: List[str] = []
    summary_grounding: Optional[str] = None
