from typing import List, Optional
from pydantic import BaseModel, Field

class AnalysisRequest(BaseModel):
    decision: str = Field(..., min_length=3, max_length=2000, description="The decision you are considering")
    context: Optional[str] = Field(default="", max_length=5000, description="Context, constraints, background")
    reasoning: str = Field(..., min_length=5, max_length=5000, description="Why you think this is right / your rationale")

class ReasoningTrace(BaseModel):
    trigger: str = Field(..., description="Exact quote or cue in the user's reasoning that triggered this finding")
    considered_factor: Optional[str] = Field(None, description="What factor the user already evaluated")
    missing_or_weak_factor: Optional[str] = Field(None, description="What relevant factor was overlooked or weakly supported")
    first_reasoning_point: Optional[str] = Field(None, description="First point in tension (for conflicts)")
    second_reasoning_point: Optional[str] = Field(None, description="Second point in tension (for conflicts)")
    why_relevant: str = Field(..., description="Why this finding matters to this specific decision")

class BlindSpotItem(BaseModel):
    finding: str
    evidence: Optional[str] = ""
    why_it_matters: Optional[str] = ""
    trace: Optional[ReasoningTrace] = None

class AssumptionItem(BaseModel):
    assumption: str
    evidence: Optional[str] = ""
    needs_verification: bool = True
    trace: Optional[ReasoningTrace] = None
    verification: Optional[str] = None

class VerificationItem(BaseModel):
    assumption: str
    verification: str

class ConflictItem(BaseModel):
    conflict: str
    evidence: Optional[str] = ""
    question: Optional[str] = ""
    trace: Optional[ReasoningTrace] = None

class AnalysisResult(BaseModel):
    blind_spots: List[BlindSpotItem] = []
    assumptions: List[AssumptionItem] = []
    verification: List[VerificationItem] = []
    potential_conflicts: List[ConflictItem] = []
    missing_factors: List[str] = []
    critical_questions: List[str] = []
    summary_grounding: Optional[str] = None
