import json

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_human_review_log_excludes_raw_input(tmp_path, monkeypatch):
    log_path = tmp_path / "reviews.jsonl"
    monkeypatch.setenv("HUMAN_REVIEW_LOG_PATH", str(log_path))
    payload = {
        "trace_id": "0123456789abcdef",
        "input_sha256": "a" * 64,
        "ai_label": "suspicious",
        "final_label": "clickbait",
        "reason": "과장된 표현과 원문 불일치가 확인됨",
        "reviewer_role": "expert",
    }

    response = client.post("/api/v1/clickbait/reviews", json=payload)

    assert response.status_code == 200
    assert response.json()["disagrees_with_ai"] is True
    stored = json.loads(log_path.read_text(encoding="utf-8"))
    assert stored["final_label"] == "clickbait"
    assert "title" not in stored
    assert "body" not in stored


def test_human_review_summary_counts_agreement(tmp_path, monkeypatch):
    log_path = tmp_path / "reviews.jsonl"
    monkeypatch.setenv("HUMAN_REVIEW_LOG_PATH", str(log_path))
    base = {
        "trace_id": "0123456789abcdef",
        "input_sha256": "b" * 64,
        "ai_label": "normal",
        "reason": "기사 원문과 표현을 함께 확인함",
        "reviewer_role": "operator",
    }
    client.post("/api/v1/clickbait/reviews", json={**base, "final_label": "normal"})
    client.post("/api/v1/clickbait/reviews", json={**base, "final_label": "suspicious"})

    response = client.get("/api/v1/clickbait/reviews/summary")

    assert response.status_code == 200
    summary = response.json()
    assert summary["total"] == 2
    assert summary["agreement_count"] == 1
    assert summary["disagreement_count"] == 1
    assert summary["agreement_rate"] == 0.5
