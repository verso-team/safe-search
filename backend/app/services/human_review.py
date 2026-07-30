import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from uuid import uuid4

from app.schemas.clickbait import (
    HumanReviewRequest,
    HumanReviewResponse,
    HumanReviewSummary,
)


_write_lock = Lock()
STORED_FIELDS = [
    "review_id",
    "created_at",
    "trace_id",
    "input_sha256",
    "ai_label",
    "final_label",
    "reason",
    "reviewer_role",
    "disagrees_with_ai",
]


def _log_path() -> Path:
    configured = os.getenv("HUMAN_REVIEW_LOG_PATH")
    if configured:
        return Path(configured)
    return Path(__file__).resolve().parents[2] / "runtime" / "human-reviews.jsonl"


def record_human_review(request: HumanReviewRequest) -> HumanReviewResponse:
    created_at = datetime.now(timezone.utc).isoformat()
    review_id = uuid4().hex
    disagrees = request.ai_label != request.final_label
    record = {
        "review_id": review_id,
        "created_at": created_at,
        **request.model_dump(),
        "disagrees_with_ai": disagrees,
    }
    path = _log_path()
    with _write_lock:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as output:
            output.write(json.dumps(record, ensure_ascii=False) + "\n")

    return HumanReviewResponse(
        review_id=review_id,
        created_at=created_at,
        disagrees_with_ai=disagrees,
        stored_fields=STORED_FIELDS,
    )


def summarize_human_reviews() -> HumanReviewSummary:
    path = _log_path()
    if not path.exists():
        return HumanReviewSummary(
            total=0,
            agreement_count=0,
            disagreement_count=0,
            agreement_rate=0,
            final_label_counts={},
        )

    records = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    disagreement_count = sum(record["disagrees_with_ai"] for record in records)
    agreement_count = len(records) - disagreement_count
    labels = Counter(record["final_label"] for record in records)
    return HumanReviewSummary(
        total=len(records),
        agreement_count=agreement_count,
        disagreement_count=disagreement_count,
        agreement_rate=round(agreement_count / len(records), 4) if records else 0,
        final_label_counts=dict(labels),
    )
