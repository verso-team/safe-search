import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

from app.schemas.clickbait import ClickbaitAnalyzeRequest
from app.services.clickbait_analysis import analyze_clickbait


ROOT = BACKEND_ROOT.parent
DATASET = ROOT / "data" / "evaluation" / "clickbait-seed.jsonl"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    records = [
        json.loads(line)
        for line in DATASET.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    confusion: Counter[tuple[str, str]] = Counter()
    review_count = 0
    predictions = []

    for record in records:
        result = analyze_clickbait(ClickbaitAnalyzeRequest(title=record["title"]))
        confusion[(record["label"], result.label)] += 1
        review_count += int(result.requires_human_review)
        predictions.append(
            {
                "id": record["id"],
                "expected": record["label"],
                "predicted": result.label,
                "score": result.score,
                "requires_human_review": result.requires_human_review,
                "trace_id": result.trace_id,
                "input_sha256": result.input_sha256,
                "policy_version": result.policy_version,
                "evidence": [item.model_dump() for item in result.evidence],
            }
        )
        print(
            f'{record["id"]}: expected={record["label"]:<10} '
            f"predicted={result.label:<10} score={result.score:.3f} "
            f"review={result.requires_human_review}"
        )

    correct = sum(
        count for (expected, predicted), count in confusion.items() if expected == predicted
    )
    print()
    print(f"accuracy={correct / len(records):.3f} ({correct}/{len(records)})")
    print(f"human_review_rate={review_count / len(records):.3f}")
    print("confusion=")
    for (expected, predicted), count in sorted(confusion.items()):
        print(f"  {expected} -> {predicted}: {count}")

    if args.output:
        evidence_package = {
            "schema_version": "1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "dataset": str(DATASET.relative_to(ROOT)).replace("\\", "/"),
            "dataset_sha256": sha256(DATASET.read_bytes()).hexdigest(),
            "model_provider": "heuristic",
            "model_name": "safe-search-rules-v1",
            "policy_version": predictions[0]["policy_version"] if predictions else None,
            "sample_count": len(records),
            "accuracy": correct / len(records),
            "human_review_rate": review_count / len(records),
            "confusion": [
                {"expected": expected, "predicted": predicted, "count": count}
                for (expected, predicted), count in sorted(confusion.items())
            ],
            "predictions": predictions,
            "limitations": [
                "수작업으로 만든 소규모 기능 검증용 데이터입니다.",
                "독립적인 라벨 검수 전이므로 성능 주장에 단독 사용하지 않습니다.",
            ],
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(evidence_package, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"evidence_output={args.output.resolve()}")


if __name__ == "__main__":
    main()
