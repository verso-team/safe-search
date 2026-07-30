from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


class AnalyzeResponse(BaseModel):
    crime_type: str
    urgency: str
    confidence: float
    safe_queries: list[str]
    recommended_agencies: list[str]
    requires_human_review: bool
