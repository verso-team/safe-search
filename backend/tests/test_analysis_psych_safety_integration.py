from fastapi.testclient import TestClient

from app.main import app
from app.services.analysis_response_policy import (
    PSYCHOLOGICAL_STATE_NOTICE,
    apply_psychological_safety_policy,
)
from app.services.psychological_safety import (
    PsychologicalSafetyIssue,
    SupportMode,
)
from app.services.rule_based_analysis import (
    analyze_safely,
)


client = TestClient(app)


def test_information_intent_uses_information_first():
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": (
                "사이버범죄 신고 방법과 "
                "지원 기관을 알고 싶어요."
            )
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert (
        body["support_mode"]
        == "information_first"
    )

    assert body["opening_message"]


def test_unknown_intent_uses_user_choice():
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": "이상한 일이 있었어요.",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert (
        body["support_mode"]
        == "user_choice"
    )

    assert "어떤 방식이 편한가요?" in (
        body["opening_message"]
    )


def test_explicit_support_mode_overrides_intent():
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": (
                "사이버범죄 신고 기관을 "
                "알고 싶어요."
            ),
            "support_mode": "support_first",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert (
        body["support_mode"]
        == "support_first"
    )

    assert (
        "상황을 이야기하면서 정리"
        in body["opening_message"]
    )


def test_casual_tone_is_respected():
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": (
                "사이버범죄 신고 기관을 "
                "알고 싶어요."
            ),
            "tone_style": "casual",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert (
        body["tone_style"]
        == "casual"
    )

    assert (
        "정리해줄게"
        in body["opening_message"]
    )


def test_unsafe_generated_text_escalates_human_review():
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

    assert (
        processed.psychological_safety_passed
        is False
    )

    assert (
        PsychologicalSafetyIssue.emotion_assumption.value
        in processed.psychological_safety_issues
    )

    assert (
        PsychologicalSafetyIssue.coercive_language.value
        in processed.psychological_safety_issues
    )

    assert (
        processed.requires_human_review
        is True
    )


def test_emotional_state_notice_is_always_added():
    result = analyze_safely(
        "사이버범죄 신고 방법을 알고 싶어요."
    )

    processed = apply_psychological_safety_policy(
        result
    )

    assert (
        PSYCHOLOGICAL_STATE_NOTICE
        in processed.safety_notice
    )


def test_invalid_support_mode_is_rejected():
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": "도움이 필요해요.",
            "support_mode": "force_information",
        },
    )

    assert response.status_code == 422


def test_invalid_tone_style_is_rejected():
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": "도움이 필요해요.",
            "tone_style": "authoritative",
        },
    )

    assert response.status_code == 422