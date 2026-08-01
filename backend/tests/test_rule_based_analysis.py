from app.schemas.analysis import UrgencyLevel, UserIntent
from app.services.rule_based_analysis import analyze_safely


def test_physical_threat_overrides_other_scenarios():
    result = analyze_safely(
        "검찰을 사칭한 사람이 송금하라고 했고 지금 흉기를 들고 집 앞에 찾아왔어요."
    )

    assert result.urgency == UrgencyLevel.critical
    assert result.primary_intent == UserIntent.emergency
    assert result.recommended_agencies[0].id == "police"
    assert "112" in result.safety_notice


def test_digital_sexual_harm_scenario():
    result = analyze_safely(
        "상대가 나체 사진을 유포하겠다고 협박해서 신고 방법과 증거 보존 방법을 알고 싶어요."
    )

    assert result.urgency == UrgencyLevel.high
    assert result.primary_intent == UserIntent.reporting
    assert "디지털 성범죄" in result.suspected_harm_type
    assert {agency.id for agency in result.recommended_agencies} >= {
        "d4u",
        "police",
    }
    assert UserIntent.evidence in result.secondary_intents


def test_phishing_impersonation_scenario():
    result = analyze_safely(
        "검찰 사칭 전화가 안전계좌로 송금하고 원격제어 앱을 설치하라고 해요."
    )

    assert result.urgency == UrgencyLevel.high
    assert "기관 사칭" in result.suspected_harm_type
    assert {agency.id for agency in result.recommended_agencies} == {
        "police",
        "kisa-118",
        "fss-1332",
    }


def test_account_takeover_scenario():
    result = analyze_safely(
        "모르는 기기 로그인 알림이 왔고 복구 이메일과 비밀번호가 변경됐어요."
    )

    assert result.urgency == UrgencyLevel.medium
    assert "계정 탈취" in result.suspected_harm_type
    assert result.immediate_actions[0].priority == 1
    assert result.recommended_agencies[0].id == "kisa-118"


def test_stalking_scenario():
    result = analyze_safely(
        "전 애인이 계속 미행하고 회사 앞에서 기다려서 너무 무서워요."
    )

    assert result.urgency == UrgencyLevel.high
    assert result.primary_intent == UserIntent.emergency
    assert "스토킹" in result.suspected_harm_type
    assert result.requires_human_review is True
    assert result.emotional_state.value in {"fearful", "high_distress"}


def test_information_request_stays_low_urgency():
    result = analyze_safely(
        "사이버범죄는 어디로 신고하고 어떤 지원 기관에서 상담받는지 알고 싶어요."
    )

    assert result.urgency == UrgencyLevel.low
    assert result.primary_intent == UserIntent.information
    assert result.requires_human_review is False


def test_unknown_input_does_not_claim_safety():
    result = analyze_safely("이상한 일이 있었어요.")

    assert result.primary_intent == UserIntent.unknown
    assert result.urgency == UrgencyLevel.medium
    assert result.confidence < 0.5
    assert result.requires_human_review is True
    assert "안전하다는 뜻이 아닙니다" in result.safety_notice


def test_analysis_is_deterministic():
    text = "택배 링크를 눌렀고 인증번호를 입력해 달라는 문자가 왔어요."

    first = analyze_safely(text)
    second = analyze_safely(text)

    assert first.model_dump() == second.model_dump()


def test_all_outputs_preserve_ios_contract_limits():
    samples = (
        "상대가 흉기를 들고 찾아왔어요.",
        "몸캠 영상을 유포하겠다고 협박해요.",
        "금융감독원 사칭 전화가 안전계좌로 송금하래요.",
        "모르는 기기에서 로그인했고 비밀번호가 바뀌었어요.",
        "누군가 계속 미행하고 집 주변을 맴돌아요.",
        "어디에 신고하는지 알고 싶어요.",
        "설명하기 어려운 일이 있었어요.",
    )

    for sample in samples:
        result = analyze_safely(sample)

        assert len(result.immediate_actions) <= 3
        assert all(
            action.priority in {1, 2, 3}
            for action in result.immediate_actions
        )
        assert all(
            agency.is_official
            for agency in result.recommended_agencies
        )
        assert 0 <= result.confidence <= 1
        assert "범죄 확정" in result.safety_notice or "112" in result.safety_notice
