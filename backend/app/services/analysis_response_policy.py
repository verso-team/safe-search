from __future__ import annotations

from app.schemas.analysis import (
    ActionItem,
    AnalyzeResponse,
)
from app.services.psychological_safety import (
    SupportMode,
    ToneStyle,
    audit_response_text,
    build_opening_message,
    recommend_support_mode,
)


PSYCHOLOGICAL_STATE_NOTICE = (
    "emotional_state는 키워드 기반 참고 신호이며 "
    "사용자의 실제 심리 상태를 확정하지 않습니다."
)

PSYCHOLOGICAL_SAFETY_FALLBACK_NOTICE = (
    "심리적 안전성 점검에서 검토가 필요한 표현이 탐지되어 "
    "일부 안내를 안전한 기본 문구로 대체했습니다."
)

FALLBACK_SITUATION_SUMMARY = (
    "일부 자동 생성 문구는 안전성 검토가 필요해 표시하지 않습니다. "
    "확인된 대응 정보와 공식기관 안내를 우선 제공합니다."
)


def _combine_notice(
    current_notice: str | None,
    additional_notice: str,
) -> str:
    return "\n".join(
        part
        for part in (
            current_notice,
            additional_notice,
        )
        if part
    )


def _collect_user_facing_text(
    result: AnalyzeResponse,
    opening_message: str,
) -> str:
    """사용자에게 직접 표시되는 주요 설명 문구를 Audit 대상으로 모은다."""

    parts = [
        opening_message,
        result.emotional_support_message,
        result.situation_summary,
    ]

    for action in result.immediate_actions:
        parts.append(action.title)
        parts.append(action.detail)

    return "\n".join(
        part.strip()
        for part in parts
        if part and part.strip()
    )


def _safe_fallback_opening(
    tone: ToneStyle,
) -> str:
    if tone == ToneStyle.casual:
        return (
            "확인된 정보와 선택 가능한 대응 방법을 "
            "중심으로 안내해줄게."
        )

    return (
        "확인된 정보와 선택 가능한 대응 방법을 "
        "중심으로 안내해드릴게요."
    )


def _safe_fallback_support(
    tone: ToneStyle,
) -> str:
    if tone == ToneStyle.casual:
        return "확인된 정보만 기준으로 정리해줄게."

    return "확인된 정보만 기준으로 정리해드릴게요."


def _filter_safe_actions(
    actions: list[ActionItem],
) -> list[ActionItem]:
    safe_actions: list[ActionItem] = []

    for action in actions:
        audit = audit_response_text(
            f"{action.title}\n{action.detail}"
        )

        if audit.passed:
            safe_actions.append(action)

    return safe_actions


def apply_psychological_safety_policy(
    result: AnalyzeResponse,
    user_selected_mode: SupportMode | None = None,
    tone: ToneStyle = ToneStyle.soft_polite,
) -> AnalyzeResponse:
    """기존 사건 분석 결과에 Psychological Safety 정책을 적용한다.

    핵심 원칙:
    - 사용자의 명시적 선택을 우선한다.
    - 감정 추론값만으로 응답 방식을 결정하지 않는다.
    - 최종 사용자 노출 문구를 Psychological Safety Audit으로 검사한다.
    - Audit 실패 시 위험 후보 문구를 그대로 반환하지 않는다.
    - 안전한 기본 문구로 대체하고 Human Review를 활성화한다.
    """

    mode = recommend_support_mode(
        primary_intent=result.primary_intent.value,
        user_selected_mode=user_selected_mode,
    )

    opening_message = build_opening_message(
        mode=mode,
        tone=tone,
    )

    audit_target = _collect_user_facing_text(
        result=result,
        opening_message=opening_message,
    )

    audit = audit_response_text(audit_target)

    safety_notice = _combine_notice(
        result.safety_notice,
        PSYCHOLOGICAL_STATE_NOTICE,
    )

    updates = {
        "support_mode": mode.value,
        "tone_style": tone.value,
        "opening_message": opening_message,
        "psychological_safety_passed": audit.passed,
        "psychological_safety_issues": [
            issue.value
            for issue in audit.issues
        ],
        "requires_human_review": (
            result.requires_human_review
            or not audit.passed
        ),
        "safety_notice": safety_notice,
    }

    if not audit.passed:
        updates.update(
            {
                "opening_message": _safe_fallback_opening(tone),
                "emotional_support_message": (
                    _safe_fallback_support(tone)
                ),
                "situation_summary": FALLBACK_SITUATION_SUMMARY,
                "immediate_actions": _filter_safe_actions(
                    result.immediate_actions
                ),
                "safety_notice": _combine_notice(
                    safety_notice,
                    PSYCHOLOGICAL_SAFETY_FALLBACK_NOTICE,
                ),
            }
        )

    return result.model_copy(update=updates)
