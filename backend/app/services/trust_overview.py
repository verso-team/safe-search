import json
from pathlib import Path

from app.schemas.clickbait import TrustOverview
from app.services.clickbait_analysis import POLICY_VERSION
from app.services.human_review import summarize_human_reviews


EVIDENCE_PATH = (
    Path(__file__).resolve().parents[3]
    / "data"
    / "evaluation"
    / "baseline-evidence.json"
)


def get_trust_overview() -> TrustOverview:
    reviews = summarize_human_reviews()
    if not EVIDENCE_PATH.exists():
        return TrustOverview(
            policy_version=POLICY_VERSION,
            model_name="safe-search-rules-v1",
            model_provider="heuristic",
            baseline_sample_count=0,
            baseline_accuracy=0,
            baseline_human_review_rate=0,
            human_reviews=reviews,
            status="needs_evidence",
            cautions=["기준선 Evidence 파일을 생성해야 합니다."],
        )

    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    return TrustOverview(
        policy_version=evidence.get("policy_version", POLICY_VERSION),
        model_name=evidence.get("model_name", "safe-search-rules-v1"),
        model_provider=evidence.get("model_provider", "heuristic"),
        baseline_sample_count=evidence["sample_count"],
        baseline_accuracy=evidence["accuracy"],
        baseline_human_review_rate=evidence["human_review_rate"],
        human_reviews=reviews,
        evidence_generated_at=evidence.get("generated_at"),
        evidence_dataset_sha256=evidence.get("dataset_sha256"),
        status="ready",
        cautions=evidence.get("limitations", []),
    )
