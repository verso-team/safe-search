from fastapi.testclient import TestClient

from app.main import app
from app.schemas.search_risk import (
    RiskType,
    SearchRiskRequest,
)
from app.services.search_risk import analyze_search_result


client = TestClient(app)


def analyze(
    title: str,
    snippet: str,
    url: str = "https://example.com",
):
    return analyze_search_result(
        SearchRiskRequest(
            title=title,
            snippet=snippet,
            url=url,
        )
    )


def test_normal_official_police_result_is_low_risk():
    result = analyze(
        "사이버범죄 신고시스템 안내",
        "경찰청 공식 사이버범죄 신고 및 상담 안내",
        "https://ecrm.police.go.kr",
    )

    assert result.is_clickbait is False
    assert result.risk_level == "low"
    assert result.risk_types == []
    assert result.requires_human_review is False


def test_normal_kisa_result_is_low_risk():
    result = analyze(
        "KISA 118 상담 안내",
        "해킹, 스미싱, 개인정보 침해 상담 정보를 확인하세요.",
        "https://www.kisa.or.kr/118",
    )

    assert result.is_clickbait is False
    assert result.risk_level == "low"
    assert RiskType.institution_impersonation not in result.risk_types


def test_sensational_title_is_clickbait():
    result = analyze(
        "충격!! 경찰이 절대 알려주지 않는 피해 대처법",
        "지금 확인하세요.",
    )

    assert result.is_clickbait is True
    assert RiskType.sensational in result.risk_types
    assert result.risk_level == "medium"


def test_misleading_secret_language_is_clickbait():
    result = analyze(
        "아무도 알려주지 않는 보이스피싱 비밀",
        "곧 사라질 정보입니다.",
    )

    assert result.is_clickbait is True
    assert RiskType.misleading in result.risk_types


def test_fake_police_refund_site_requires_human_review():
    result = analyze(
        "경찰청 피해금 환급센터",
        "피해금 환급을 위해 안전계좌로 수수료를 입금하세요.",
        "https://police-refund.example.com",
    )

    assert RiskType.institution_impersonation in result.risk_types
    assert RiskType.financial_lure in result.risk_types
    assert result.risk_level == "high"
    assert result.requires_human_review is True


def test_fake_financial_supervisory_service_is_high_risk():
    result = analyze(
        "금융감독원 보이스피싱 환급 안내",
        "본인확인을 위해 계좌번호를 입력하고 수수료를 입금하세요.",
        "https://fss-help.example.com",
    )

    assert RiskType.institution_impersonation in result.risk_types
    assert RiskType.financial_lure in result.risk_types
    assert RiskType.personal_information_request in result.risk_types
    assert result.requires_human_review is True


def test_financial_lure_without_institution_name_is_detected():
    result = analyze(
        "피해금 바로 돌려받는 방법",
        "환급을 위해 수수료를 입금하세요.",
        "https://refund.example.com",
    )

    assert RiskType.financial_lure in result.risk_types
    assert result.risk_level == "high"


def test_advance_payment_lure_is_detected():
    result = analyze(
        "긴급 지원금 신청",
        "선입금 후 지원금 지급이 진행됩니다.",
        "https://support-money.example.com",
    )

    assert RiskType.financial_lure in result.risk_types
    assert result.requires_human_review is True


def test_resident_number_request_is_detected():
    result = analyze(
        "피해 확인 서비스",
        "피해 여부 확인을 위해 주민번호를 입력해주세요.",
        "https://check.example.com",
    )

    assert RiskType.personal_information_request in result.risk_types
    assert result.risk_level == "high"
    assert result.requires_human_review is True


def test_otp_request_is_detected():
    result = analyze(
        "계정 복구 안내",
        "복구 확인을 위해 OTP 인증번호를 보내주세요.",
        "https://account-help.example.com",
    )

    assert RiskType.personal_information_request in result.risk_types
    assert result.requires_human_review is True


def test_official_domain_is_not_marked_as_impersonation():
    result = analyze(
        "경찰청 공식 신고 안내",
        "공식 신고 절차를 확인할 수 있습니다.",
        "https://www.police.go.kr",
    )

    assert RiskType.institution_impersonation not in result.risk_types


def test_search_risk_api_contract():
    response = client.post(
        "/api/v1/search-risk",
        json={
            "title": "충격! 검찰 피해금 환급센터",
            "snippet": "안전계좌로 수수료를 송금하세요.",
            "url": "https://prosecution-refund.example.com",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert set(body) == {
        "is_clickbait",
        "risk_level",
        "risk_types",
        "confidence",
        "risk_signals",
        "explanation",
        "requires_human_review",
        "clickbait_probability",
        "clickbait_model",
        "clickbait_decision_source",
    }

    assert body["is_clickbait"] is True
    assert body["risk_level"] == "high"
    assert body["requires_human_review"] is True
    assert "institution_impersonation" in body["risk_types"]
    assert "financial_lure" in body["risk_types"]
