from enum import Enum

from pydantic import BaseModel, Field, field_validator


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class RiskType(str, Enum):
    sensational = "sensational"
    misleading = "misleading"
    institution_impersonation = "institution_impersonation"
    financial_lure = "financial_lure"
    personal_information_request = "personal_information_request"


class SearchRiskRequest(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    snippet: str = Field(default="", max_length=3000)
    url: str = Field(min_length=1, max_length=2048)

    @field_validator("title", "url")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("value must contain non-whitespace characters")
        return normalized

    @field_validator("snippet")
    @classmethod
    def strip_optional_text(cls, value: str) -> str:
        return value.strip()


class SearchRiskResponse(BaseModel):
    is_clickbait: bool
    risk_level: RiskLevel
    risk_types: list[RiskType]
    confidence: float = Field(ge=0, le=1)
    risk_signals: list[str]
    explanation: str
    requires_human_review: bool
