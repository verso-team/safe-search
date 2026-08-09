from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"

sys.path.insert(0, str(BACKEND))

from app.services.clickbait_ml import (  # noqa: E402
    evaluate_holdout,
    load_dataset,
    save_model,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train and evaluate the SAFE:SEARCH clickbait baseline."
    )

    parser.add_argument(
        "--data",
        type=Path,
        default=ROOT / "data" / "clickbait" / "seed_v0.csv",
    )
    parser.add_argument(
        "--save-model",
        type=Path,
        default=None,
    )
    parser.add_argument(
        "--metrics-json",
        type=Path,
        default=None,
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    dataframe = load_dataset(args.data)
    model, metrics = evaluate_holdout(dataframe)

    if args.save_model is not None:
        save_model(model, args.save_model)

    if args.metrics_json is not None:
        args.metrics_json.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        args.metrics_json.write_text(
            json.dumps(
                metrics,
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    print(
        json.dumps(
            metrics,
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
