import logging

from fastapi.testclient import TestClient

from app.main import app
from app.services.pii_redaction import (
    PIICategory,
    build_redaction_notice,
    redact_sensitive_text,
)


client = TestClient(app)


def test_redacts_common_sensitive_values():
    source = (
        "주민번호 990101-1234567, "
        "이메일 victim@example.com, "
        "휴대폰 010-1234-5678, "
        "카드 1234-5678-9012-3456"
    )

    result = redact_sensitive_text(source)

    assert result.total_count == 4
    assert result.counts[PIICategory.resident_registration_number] == 1
    assert result.counts[PIICategory.email] == 1
    assert result.counts[PIICategory.phone] == 1
    assert result.counts[PIICategory.payment_card] == 1

    assert "990101-1234567" not in result.redacted_text
    assert "victim@example.com" not in result.redacted_text
    assert "010-1234-5678" not in result.redacted_text
    assert "1234-5678-9012-3456" not in result.redacted_text


def test_redacts_contextual_account_and_authentication_code():
    result = redact_sensitive_text(
        "검찰 사칭이 계좌번호 123-456-789012와 "
        "인증번호 654321을 요구했어요."
    )

    assert result.total_count == 2
    assert "계좌번호 [계좌번호]" in result.redacted_text
    assert "인증번호 [인증번호]" in result.redacted_text
    assert "123-456-789012" not in result.redacted_text
    assert "654321" not in result.redacted_text


def test_preserves_emergency_numbers_dates_and_unlabeled_digits():
    source = (
        "긴급번호 112, 상담번호 118과 1366, "
        "날짜 2026-08-01, 일반 숫자 123456"
    )

    result = redact_sensitive_text(source)

    assert result.total_count == 0
    assert result.redacted_text == source


def test_counts_repeated_values_without_retaining_them():
    result = redact_sensitive_text(
        "010-1111-2222와 010-3333-4444로 연락이 왔어요."
    )

    assert result.total_count == 2
    assert result.counts[PIICategory.phone] == 2
    assert "010-1111-2222" not in result.redacted_text
    assert "010-3333-4444" not in result.redacted_text


def test_notice_contains_only_count_and_category_names():
    result = redact_sensitive_text(
        "victim@example.com과 010-1234-5678"
    )

    notice = build_redaction_notice(result)

    assert notice is not None
    assert "민감정보 2건" in notice
    assert "이메일" in notice
    assert "전화번호" in notice
    assert "victim@example.com" not in notice
    assert "010-1234-5678" not in notice


def test_api_masks_pii_before_rule_analysis():
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": (
                "검찰 사칭 전화가 010-1234-5678로 왔고 "
                "안전계좌번호 123-456-789012로 송금한 뒤 "
                "인증번호 654321을 보내라고 해요."
            )
        },
    )

    assert response.status_code == 200
    result = response.json()

    assert result["urgency"] == "high"
    assert "기관 사칭" in result["suspected_harm_type"]
    assert "민감정보 3건" in result["safety_notice"]


def test_api_response_does_not_return_original_sensitive_values():
    sensitive_values = (
        "990101-1234567",
        "victim@example.com",
        "010-1234-5678",
        "1234-5678-9012-3456",
    )
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": (
                "영상 유포 협박을 받고 있습니다. "
                f"주민번호 {sensitive_values[0]}, "
                f"이메일 {sensitive_values[1]}, "
                f"전화 {sensitive_values[2]}, "
                f"카드 {sensitive_values[3]}"
            )
        },
    )

    assert response.status_code == 200

    for sensitive_value in sensitive_values:
        assert sensitive_value not in response.text


def test_log_contains_only_redaction_statistics(caplog):
    raw_input = (
        "검찰 사칭이 010-1234-5678로 연락해 "
        "계좌번호 123-456-789012를 요구해요."
    )

    with caplog.at_level(logging.INFO, logger="app.pii"):
        response = client.post(
            "/api/v1/analyze",
            json={"text": raw_input},
        )

    assert response.status_code == 200
    assert "PII redaction applied total=2" in caplog.text
    assert "010-1234-5678" not in caplog.text
    assert "123-456-789012" not in caplog.text
    assert raw_input not in caplog.text


def test_api_without_pii_does_not_add_redaction_notice():
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": "사이버범죄 신고 절차와 공식 지원기관을 알고 싶어요."
        },
    )

    assert response.status_code == 200
    assert "마스킹했습니다" not in response.json()["safety_notice"]
