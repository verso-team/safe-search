from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum


class SupportMode(str, Enum):
    """사용자가 어떤 방식으로 도움을 받을지 표현한다."""

    information_first = "information_first"
    support_first = "support_first"
    user_choice = "user_choice"


class ToneStyle(str, Enum):
    """말투는 사용자가 명시적으로 선택할 수 있도록 분리한다."""

    soft_polite = "soft_polite"
    casual = "casual"


class PsychologicalSafetyIssue(str, Enum):
    coercive_language = "coercive_language"
    emotion_assumption = "emotion_assumption"
    over_reassurance = "over_reassurance"
    victim_blaming = "victim_blaming"
    overly_authoritative_tone = "overly_authoritative_tone"
    search_burden = "search_burden"


@dataclass(frozen=True)
class PsychologicalSafetyAudit:
    """AI 응답 문장의 심리적 안전성 점검 결과."""

    passed: bool
    issues: tuple[PsychologicalSafetyIssue, ...]
    recommendations: tuple[str, ...]


PSYCHOLOGICAL_SAFETY_PRINCIPLES = (
    "사용자의 감정을 AI가 사실처럼 단정하지 않는다.",
    "피해자에게 책임을 돌리거나 비난하지 않는다.",
    "안전이나 해결 가능성을 근거 없이 보장하지 않는다.",
    "신고나 특정 행동을 강압적으로 지시하지 않는다.",
    "필요한 공식기관 정보를 다시 직접 검색하도록 떠넘기지 않는다.",
    "기본 말투는 부드럽고 정중하게 유지한다.",
    "정보 우선과 대화 우선 중 사용자가 선택할 수 있게 한다.",
    "AI의 감정 추론은 참고 신호일 뿐 최종 판단으로 사용하지 않는다.",
)


ISSUE_RECOMMENDATIONS = {
    PsychologicalSafetyIssue.coercive_language: (
        "명령·재촉 표현 대신 선택 가능한 행동과 공식기관 연결 방법을 제시하세요."
    ),
    PsychologicalSafetyIssue.emotion_assumption: (
        "사용자가 직접 표현하지 않은 감정을 AI가 확정하지 마세요."
    ),
    PsychologicalSafetyIssue.over_reassurance: (
        "안전·해결을 보장하지 말고 현재 확인 가능한 사실과 한계를 설명하세요."
    ),
    PsychologicalSafetyIssue.victim_blaming: (
        "피해자의 행동을 원인이나 책임으로 돌리는 표현을 제거하세요."
    ),
    PsychologicalSafetyIssue.overly_authoritative_tone: (
        "권위적인 극존칭보다 부드럽고 정중한 질문형 표현을 사용하세요."
    ),
    PsychologicalSafetyIssue.search_burden: (
        "피해자에게 직접 검색을 요구하기보다 확인된 공식기관 정보를 우선 제공하세요."
    ),
}


ISSUE_PATTERNS: tuple[
    tuple[PsychologicalSafetyIssue, tuple[str, ...]],
    ...
] = (
    (
        PsychologicalSafetyIssue.coercive_language,
        (
            "반드시 신고",
            "무조건 신고",
            "당장 신고",
            "꼭 신고",
            "하셔야 합니다",
            "해야 합니다",
            "해야만 합니다",
        ),
    ),
    (
        PsychologicalSafetyIssue.emotion_assumption,
        (
            "많이 무서우셨",
            "무서우셨겠",
            "불안하시겠",
            "많이 불안하",
            "힘드시겠",
            "많이 놀라셨",
            "괴로우시겠",
            "충격이 크셨",
        ),
    ),
    (
        PsychologicalSafetyIssue.over_reassurance,
        (
            "안전합니다",
            "걱정하지 마세요",
            "괜찮을 거예요",
            "괜찮아질 거예요",
            "해결될 거예요",
            "문제없습니다",
            "반드시 해결",
        ),
    ),
    (
        PsychologicalSafetyIssue.victim_blaming,
        (
            "왜 보내셨어요",
            "왜 믿으셨어요",
            "왜 클릭하셨어요",
            "본인 잘못",
            "당신 잘못",
            "당신 책임",
            "피해자 책임",
        ),
    ),
    (
        PsychologicalSafetyIssue.overly_authoritative_tone,
        (
            "하시겠습니까",
            "주시겠습니까",
            "알려주시겠습니까",
            "진행하시겠습니까",
        ),
    ),
    (
        PsychologicalSafetyIssue.search_burden,
        (
            "직접 검색해",
            "직접 찾아보",
            "인터넷에서 찾아보",
            "검색해서 확인",
            "포털에서 검색",
        ),
    ),
)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def recommend_support_mode(
    primary_intent: str,
    user_selected_mode: SupportMode | None = None,
) -> SupportMode:
    """사용자가 명시적으로 선택한 방식이 있으면 그 선택을 우선한다.

    선택이 없는 경우:
    - 정서적 지지를 명시적으로 원하는 경우 support_first
    - 정보/신고/증거/기관/긴급 대응은 information_first
    - 의도가 불명확하면 user_choice

    이 함수는 사용자의 감정상태를 진단하지 않는다.
    """

    if user_selected_mode is not None:
        return user_selected_mode

    normalized_intent = primary_intent.strip().lower()

    if normalized_intent == "emotional_support":
        return SupportMode.support_first

    if normalized_intent in {
        "information",
        "reporting",
        "evidence",
        "emergency",
        "legal_question",
        "institution",
        "secondary_damage",
    }:
        return SupportMode.information_first

    return SupportMode.user_choice


def build_opening_message(
    mode: SupportMode,
    tone: ToneStyle = ToneStyle.soft_polite,
) -> str:
    """감정을 단정하지 않는 초기 안내 문장을 생성한다."""

    messages = {
        ToneStyle.soft_polite: {
            SupportMode.information_first: (
                "필요한 대응 정보를 먼저 정리해드릴게요. "
                "원하시면 공식기관 안내도 바로 확인할 수 있어요."
            ),
            SupportMode.support_first: (
                "원하시면 지금 상황을 이야기하면서 정리할 수 있어요. "
                "필요한 정보는 준비되면 함께 확인할 수 있어요."
            ),
            SupportMode.user_choice: (
                "필요한 정보를 먼저 확인하거나, "
                "이야기하면서 상황을 정리할 수 있어요. "
                "어떤 방식이 편한가요?"
            ),
        },
        ToneStyle.casual: {
            SupportMode.information_first: (
                "필요한 대응 정보를 먼저 정리해줄게. "
                "원하면 공식기관 안내도 바로 확인할 수 있어."
            ),
            SupportMode.support_first: (
                "원하면 지금 상황을 이야기하면서 정리할 수 있어. "
                "필요한 정보는 준비되면 같이 확인할 수 있어."
            ),
            SupportMode.user_choice: (
                "필요한 정보를 먼저 확인하거나, "
                "이야기하면서 상황을 정리할 수 있어. "
                "어떤 방식이 편해?"
            ),
        },
    }

    return messages[tone][mode]


def audit_response_text(
    text: str,
) -> PsychologicalSafetyAudit:
    """AI가 생성한 최종 응답에 위험 표현이 있는지 점검한다.

    v0.1은 설명 가능한 lexical guardrail이다.
    문맥을 완전히 이해하는 모델이 아니므로 탐지 결과 자체를
    임상적 판단이나 사용자 감정 판정으로 사용해서는 안 된다.
    """

    normalized = _normalize(text)

    if not normalized:
        raise ValueError("response text must not be blank")

    issues: list[PsychologicalSafetyIssue] = []

    for issue, patterns in ISSUE_PATTERNS:
        if any(pattern in normalized for pattern in patterns):
            issues.append(issue)

    issues = list(dict.fromkeys(issues))

    recommendations = tuple(
        ISSUE_RECOMMENDATIONS[issue]
        for issue in issues
    )

    return PsychologicalSafetyAudit(
        passed=not issues,
        issues=tuple(issues),
        recommendations=recommendations,
    )