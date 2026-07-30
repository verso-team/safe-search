from typing import Literal

from pydantic import BaseModel, Field


class ClickbaitAnalyzeRequest(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    body: str = Field(default="", max_length=5000)
    source_url: str | None = Field(default=None, max_length=2000)


class ClickbaitEvidence(BaseModel):
    indicator: str
    excerpt: str
    weight: float = Field(ge=0, le=1)


class ClickbaitAnalyzeResponse(BaseModel):
    trace_id: str
    input_sha256: str
    policy_version: str
    label: Literal["normal", "suspicious", "clickbait"]
    score: float = Field(ge=0, le=1)
    confidence: float = Field(ge=0, le=1)
    summary: str
    evidence: list[ClickbaitEvidence]
    model_provider: Literal["heuristic", "ollama", "skax"]
    model_name: str
    fallback_used: bool = False
    decision_thresholds: dict[str, float]
    requires_human_review: bool
    human_review_reason: str | None = None
    limitations: list[str]


class HumanReviewRequest(BaseModel):
    trace_id: str = Field(min_length=16, max_length=16)
    input_sha256: str = Field(min_length=64, max_length=64)
    ai_label: Literal["normal", "suspicious", "clickbait"]
    final_label: Literal["normal", "suspicious", "clickbait"]
    reason: str = Field(min_length=5, max_length=1000)
    reviewer_role: Literal["user", "operator", "expert"] = "user"


class HumanReviewResponse(BaseModel):
    review_id: str
    created_at: str
    disagrees_with_ai: bool
    stored_fields: list[str]


class HumanReviewSummary(BaseModel):
    total: int
    agreement_count: int
    disagreement_count: int
    agreement_rate: float = Field(ge=0, le=1)
    final_label_counts: dict[str, int]
