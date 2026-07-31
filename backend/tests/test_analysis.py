from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_analysis_returns_structured_safety_response():
    response = client.post(
        "/api/v1/analyze",
        json={"text": "영상이 퍼지고 있는데 어디로 신고해야 할지 모르겠어요."},
    )

    assert response.status_code == 200
    result = response.json()
    assert result["primary_intent"] == "reporting"
    assert "information" in result["secondary_intents"]
    assert len(result["immediate_actions"]) <= 3
    assert all(agency["is_official"] for agency in result["recommended_agencies"])
    assert result["requires_human_review"] is True


def test_critical_signal_prioritizes_emergency_guidance():
    response = client.post(
        "/api/v1/analyze",
        json={"text": "상대가 흉기를 들고 집 앞에 찾아왔어요."},
    )

    assert response.status_code == 200
    result = response.json()
    assert result["urgency"] == "critical"
    assert result["primary_intent"] == "emergency"
    assert "112" in result["safety_notice"]
    assert result["immediate_actions"][0]["priority"] == 1


def test_empty_input_is_rejected():
    response = client.post("/api/v1/analyze", json={"text": ""})
    assert response.status_code == 422


def test_health_exposes_service_metadata():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "safe-search-api",
        "version": "0.1.0",
    }


def test_cors_allows_local_frontend():
    response = client.options(
        "/api/v1/analyze",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
