import json
import sys
from collections import Counter
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

from app.schemas.clickbait import ClickbaitAnalyzeRequest
from app.services.clickbait_analysis import analyze_clickbait


ROOT = BACKEND_ROOT.parent
DATASET = ROOT / "data" / "evaluation" / "clickbait-seed.jsonl"


def main() -> None:
    records = [
        json.loads(line)
        for line in DATASET.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    confusion: Counter[tuple[str, str]] = Counter()
    review_count = 0

    for record in records:
        result = analyze_clickbait(ClickbaitAnalyzeRequest(title=record["title"]))
        confusion[(record["label"], result.label)] += 1
        review_count += int(result.requires_human_review)
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


if __name__ == "__main__":
    main()
