from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class UserIntent(str, Enum):
    information = "information"
    emotional_support = "emotional_support"
    reporting = "reporting"
    evidence = "evidence"
    emergency = "emergency"
    legal_question = "legal_question"
    institution = "institution"
    secondary_damage = "secondary_damage"
    unknown = "unknown"


class EmotionalState(str, Enum):
    stable = "stable"
    anxious = "anxious"
    confused = "confused"
    fearful = "fearful"
    panic = "panic"
    high_distress = "high_distress"


class UrgencyLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class ActionItem(BaseModel):
    title: str
    detail: str
    priority: int = Field(ge=1, le=3)


class Agency(BaseModel):
    id: str
    name: str
    role: str
    phone: Optional[str] = None
    website: str
    is_official: bool = True

class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


class AnalyzeResponse(BaseModel):
    primary_intent: UserIntent
    secondary_intents: List[UserIntent]
    emotional_state: EmotionalState
    urgency: UrgencyLevel
    confidence: float = Field(ge=0, le=1)
    suspected_harm_type: str
    emotional_support_message: str
    situation_summary: str
    immediate_actions: List[ActionItem] = Field(max_length=3)
    safe_search_queries: List[str]
    recommended_agencies: List[Agency]
    requires_human_review: bool
    safety_notice: Optional[str] = None
