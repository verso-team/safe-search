from typing import List
from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)

class AnalyzeResponse(BaseModel):
    crime_type: str
    urgency: str
    confidence: float
    safe_queries: List[str]
    recommended_agencies: List[str]
    requires_human_review: bool
