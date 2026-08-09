from app.services.psychological_safety import (
    PsychologicalSafetyIssue,
    SupportMode,
    ToneStyle,
    audit_response_text,
    build_opening_message,
    recommend_support_mode,
)


def test_unknown_intent_defaults_to_user_choice():
    assert recommend_support_mode("unknown") == SupportMode.user_choice


def test_information_intent_prefers_information_first():
    assert (
        recommend_support_mode("information")
        == SupportMode.information_first
    )


def test_emotional_support_intent_prefers_support_first():
    assert (
        recommend_support_mode("emotional_support")
        == SupportMode.support_first
    )


def test_explicit_user_selection_is_respected():
    assert (
        recommend_support_mode(
            "information",
            user_selected_mode=SupportMode.support_first,
        )
        == SupportMode.support_first
    )


def test_user_choice_message_does_not_assume_emotion():
    message = build_opening_message(
        SupportMode.user_choice,
        ToneStyle.soft_polite,
    )

    audit = audit_response_text(message)

    assert audit.passed is True
    assert "어떤 방식이 편한가요?" in message


def test_casual_tone_is_available_only_when_selected():
    message = build_opening_message(
        SupportMode.user_choice,
        ToneStyle.casual,
    )

    assert message.endswith("어떤 방식이 편해?")
    assert "편한가요?" not in message


def test_detects_coercive_language():
    audit = audit_response_text(
        "이 경우 반드시 신고하셔야 합니다."
    )

    assert audit.passed is False
    assert (
        PsychologicalSafetyIssue.coercive_language
        in audit.issues
    )


def test_detects_emotion_assumption():
    audit = audit_response_text(
        "많이 무서우셨겠어요. 지금부터 도와드릴게요."
    )

    assert (
        PsychologicalSafetyIssue.emotion_assumption
        in audit.issues
    )


def test_detects_over_reassurance():
    audit = audit_response_text(
        "이제 안전합니다. 걱정하지 마세요."
    )

    assert (
        PsychologicalSafetyIssue.over_reassurance
        in audit.issues
    )


def test_detects_victim_blaming():
    audit = audit_response_text(
        "왜 그 링크를 클릭하셨어요? 본인 잘못도 있습니다."
    )

    assert (
        PsychologicalSafetyIssue.victim_blaming
        in audit.issues
    )


def test_detects_overly_authoritative_tone():
    audit = audit_response_text(
        "신고 절차를 진행하시겠습니까?"
    )

    assert (
        PsychologicalSafetyIssue.overly_authoritative_tone
        in audit.issues
    )


def test_detects_search_burden():
    audit = audit_response_text(
        "관련 기관은 인터넷에서 찾아보세요."
    )

    assert (
        PsychologicalSafetyIssue.search_burden
        in audit.issues
    )


def test_safe_information_message_passes():
    audit = audit_response_text(
        "원하시면 공식기관에 확인할 수 있는 방법을 "
        "바로 보여드릴게요."
    )

    assert audit.passed is True
    assert audit.issues == ()
    assert audit.recommendations == ()


def test_multiple_issues_are_reported_together():
    audit = audit_response_text(
        "많이 무서우셨겠어요. "
        "반드시 신고하셔야 합니다. "
        "이제 안전하니 걱정하지 마세요."
    )

    assert audit.passed is False

    assert (
        PsychologicalSafetyIssue.emotion_assumption
        in audit.issues
    )
    assert (
        PsychologicalSafetyIssue.coercive_language
        in audit.issues
    )
    assert (
        PsychologicalSafetyIssue.over_reassurance
        in audit.issues
    )