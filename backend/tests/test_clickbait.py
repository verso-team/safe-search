import json

import httpx
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


def test_skax_openai_compatible_adapter(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            content = {
                "label": "clickbait",
                "score": 0.82,
                "confidence": 0.9,
                "summary": "A.X 모델이 클릭 유도 표현을 확인했습니다.",
                "evidence": [
                    {
                        "indicator": "즉각적인 클릭 유도",
                        "excerpt": "지금 확인",
                        "weight": 0.4,
                    }
                ],
                "requires_human_review": False,
                "human_review_reason": None,
                "limitations": ["기사 사실 여부는 별도 확인이 필요합니다."],
            }
            return {"choices": [{"message": {"content": json.dumps(content)}}]}

    def fake_post(url, **kwargs):
        assert url == "http://skax.test/v1/chat/completions"
        assert kwargs["json"]["model"] == "skt/A.X-4.0-Light"
        return FakeResponse()

    monkeypatch.setenv("CLICKBAIT_MODEL_PROVIDER", "skax")
    monkeypatch.setenv("SKAX_BASE_URL", "http://skax.test/v1")
    monkeypatch.setattr("app.services.clickbait_analysis.httpx.post", fake_post)

    response = client.post(
        "/api/v1/clickbait/analyze",
        json={"title": "충격! 지금 확인하세요"},
    )

    assert response.status_code == 200
    result = response.json()
    assert result["model_provider"] == "skax"
    assert result["model_name"] == "skt/A.X-4.0-Light"
    assert result["fallback_used"] is False


def test_skax_failure_uses_auditable_fallback(monkeypatch):
    def failing_post(*args, **kwargs):
        raise httpx.ConnectError("offline")

    monkeypatch.setenv("CLICKBAIT_MODEL_PROVIDER", "skax")
    monkeypatch.setattr("app.services.clickbait_analysis.httpx.post", failing_post)

    response = client.post(
        "/api/v1/clickbait/analyze",
        json={"title": "서울시, 폭염 대응 계획 발표"},
    )

    assert response.status_code == 200
    result = response.json()
    assert result["model_provider"] == "heuristic"
    assert result["fallback_used"] is True
    assert any("skax" in limitation for limitation in result["limitations"])


def test_skax_removes_ungrounded_evidence(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            content = {
                "label": "suspicious",
                "score": 0.4,
                "confidence": 0.7,
                "summary": "추가 확인이 필요합니다.",
                "evidence": [
                    {
                        "indicator": "모델이 만든 허위 근거",
                        "excerpt": "입력에 존재하지 않는 문장",
                        "weight": 0.4,
                    }
                ],
                "requires_human_review": False,
                "human_review_reason": None,
                "limitations": [],
            }
            return {"choices": [{"message": {"content": json.dumps(content)}}]}

    monkeypatch.setenv("CLICKBAIT_MODEL_PROVIDER", "skax")
    monkeypatch.setattr(
        "app.services.clickbait_analysis.httpx.post",
        lambda *args, **kwargs: FakeResponse(),
    )

    response = client.post(
        "/api/v1/clickbait/analyze",
        json={"title": "서울시, 폭염 대응 계획 발표"},
    )

    result = response.json()
    assert result["evidence"] == []
    assert result["requires_human_review"] is True
    assert any("근거를 제거" in limitation for limitation in result["limitations"])
