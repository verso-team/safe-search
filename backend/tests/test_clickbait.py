from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_clickbait_analysis_returns_evidence_and_trace():
    response = client.post(
        "/api/v1/clickbait/analyze",
        json={"title": "충격!! 아무도 모르는 비밀, 지금 확인하세요"},
    )

    assert response.status_code == 200
    result = response.json()
    assert result["label"] == "clickbait"
    assert result["score"] >= 0.45
    assert result["model_provider"] == "heuristic"
    assert len(result["trace_id"]) == 16
    assert len(result["input_sha256"]) == 64
    assert result["policy_version"] == "clickbait-policy-2026.07.30-v2"
    assert result["fallback_used"] is False
    assert result["decision_thresholds"]["clickbait"] == 0.45
    assert len(result["evidence"]) >= 3


def test_neutral_title_is_not_marked_clickbait():
    response = client.post(
        "/api/v1/clickbait/analyze",
        json={"title": "서울시, 여름철 폭염 대응 계획 발표"},
    )

    assert response.status_code == 200
    result = response.json()
    assert result["label"] == "normal"
    assert result["score"] < 0.28


def test_short_or_boundary_input_requests_human_review():
    response = client.post(
        "/api/v1/clickbait/analyze",
        json={"title": "충격"},
    )

    assert response.status_code == 200
    result = response.json()
    assert result["requires_human_review"] is True
    assert result["human_review_reason"]


def test_invalid_empty_title_is_rejected():
    response = client.post(
        "/api/v1/clickbait/analyze",
        json={"title": ""},
    )

    assert response.status_code == 422


def test_exaggerated_short_term_transformation_is_clickbait():
    response = client.post(
        "/api/v1/clickbait/analyze",
        json={"title": "단 3일 만에 인생이 바뀐 놀라운 방법"},
    )

    assert response.status_code == 200
    result = response.json()
    assert result["label"] == "clickbait"
    assert len(result["evidence"]) >= 3
