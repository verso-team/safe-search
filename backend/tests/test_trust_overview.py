from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_trust_overview_exposes_reproducible_baseline(tmp_path, monkeypatch):
    monkeypatch.setenv("HUMAN_REVIEW_LOG_PATH", str(tmp_path / "reviews.jsonl"))

    response = client.get("/api/v1/trust/overview")

    assert response.status_code == 200
    overview = response.json()
    assert overview["status"] == "ready"
    assert overview["policy_version"] == "clickbait-policy-2026.07.30-v2"
    assert overview["baseline_sample_count"] == 12
    assert overview["baseline_accuracy"] == 1
    assert overview["evidence_dataset_sha256"]
    assert overview["human_reviews"]["total"] == 0
    assert overview["cautions"]
