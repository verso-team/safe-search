from app.schemas.analysis import ActionItem
from app.services.analysis_response_policy import (
    PSYCHOLOGICAL_SAFETY_FALLBACK_NOTICE,
    apply_psychological_safety_policy,
)
from app.services.psychological_safety import (
    PsychologicalSafetyIssue,
    audit_response_text,
)
from app.services.rule_based_analysis import analyze_safely


def _returned_user_text(result) -> str:
    parts = [
        result.opening_message,
        result.emotional_support_message,
        result.situation_summary,
    ]

    for action in result.immediate_actions:
        parts.append(action.title)
        parts.append(action.detail)

    return "\n".join(parts)


def test_unsafe_candidate_is_replaced_with_safe_fallback():
    result = analyze_safely(
        "사이버범죄 신고 방법을 알고 싶어요."
    )

    unsafe_result = result.model_copy(
        update={
            "emotional_support_message": (
                "많이 무서우셨겠어요. "
                "반드시 신고하셔야 합니다."
            ),
            "requires_human_review": False,
        }
    )

    processed = apply_psychological_safety_policy(
        unsafe_result
    )

    assert processed.psychological_safety_passed is False
    assert processed.requires_human_review is True

    assert (
        PsychologicalSafetyIssue.emotion_assumption.value
        in processed.psychological_safety_issues
    )
    assert (
        PsychologicalSafetyIssue.coercive_language.value
        in processed.psychological_safety_issues
    )

    returned_text = _returned_user_text(processed)

    assert "많이 무서우셨" not in returned_text
    assert "반드시 신고" not in returned_text

    assert (
        PSYCHOLOGICAL_SAFETY_FALLBACK_NOTICE
        in processed.safety_notice
    )

    assert audit_response_text(
        returned_text
    ).passed is True


def test_unsafe_action_is_removed_but_safe_action_is_preserved():
    result = analyze_safely(
        "사이버범죄 신고 방법을 알고 싶어요."
    )

    safe_action = ActionItem(
        title="공식기관 정보 확인",
        detail=(
            "원하시면 확인된 공식기관 정보를 "
            "안내할 수 있어요."
        ),
        priority=1,
    )

    unsafe_action = ActionItem(
        title="즉시 신고",
        detail="반드시 신고하셔야 합니다.",
        priority=2,
    )

    candidate = result.model_copy(
        update={
            "immediate_actions": [
                safe_action,
                unsafe_action,
            ],
            "requires_human_review": False,
        }
    )

    processed = apply_psychological_safety_policy(
        candidate
    )

    titles = [
        action.title
        for action in processed.immediate_actions
    ]

    assert "공식기관 정보 확인" in titles
    assert "즉시 신고" not in titles
    assert processed.requires_human_review is True

    assert audit_response_text(
        _returned_user_text(processed)
    ).passed is True
