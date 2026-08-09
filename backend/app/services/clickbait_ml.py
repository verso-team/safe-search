from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


REQUIRED_COLUMNS = {
    "title",
    "snippet",
    "is_clickbait",
}


@dataclass(frozen=True)
class ClickbaitPrediction:
    is_clickbait: bool
    probability: float


def load_dataset(path: str | Path) -> pd.DataFrame:
    """Load and validate a binary clickbait dataset."""

    dataframe = pd.read_csv(path, encoding="utf-8-sig")

    missing = REQUIRED_COLUMNS - set(dataframe.columns)
    if missing:
        raise ValueError(
            f"Missing required dataset columns: {sorted(missing)}"
        )

    dataframe = dataframe.copy()

    try:
        dataframe["is_clickbait"] = (
            pd.to_numeric(
                dataframe["is_clickbait"],
                errors="raise",
            )
            .astype(int)
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "is_clickbait must contain only 0 or 1."
        ) from exc

    labels = set(dataframe["is_clickbait"].unique())

    if labels != {0, 1}:
        raise ValueError(
            "Dataset must contain both binary labels 0 and 1."
        )

    dataframe["title"] = dataframe["title"].fillna("").astype(str)
    dataframe["snippet"] = dataframe["snippet"].fillna("").astype(str)

    return dataframe


def combine_text(
    title: str,
    snippet: str,
) -> str:
    return f"{title.strip()} [SEP] {snippet.strip()}".strip()


def _prepare_features(
    dataframe: pd.DataFrame,
) -> pd.Series:
    return dataframe.apply(
        lambda row: combine_text(
            row["title"],
            row["snippet"],
        ),
        axis=1,
    )


def build_baseline() -> Pipeline:
    """Build a Korean-friendly lightweight baseline.

    Character n-grams are used so the baseline does not depend on
    a separate Korean morphological analyzer.
    """

    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    analyzer="char_wb",
                    ngram_range=(2, 5),
                    min_df=1,
                    sublinear_tf=True,
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )


def train_baseline(
    dataframe: pd.DataFrame,
) -> Pipeline:
    model = build_baseline()

    model.fit(
        _prepare_features(dataframe),
        dataframe["is_clickbait"],
    )

    return model


def predict_clickbait(
    model: Pipeline,
    title: str,
    snippet: str,
    threshold: float = 0.5,
) -> ClickbaitPrediction:
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must be between 0 and 1.")

    text = combine_text(title, snippet)
    probabilities = model.predict_proba([text])[0]

    classes = list(model.classes_)
    positive_index = classes.index(1)

    probability = float(probabilities[positive_index])

    return ClickbaitPrediction(
        is_clickbait=probability >= threshold,
        probability=round(probability, 6),
    )


def evaluate_holdout(
    dataframe: pd.DataFrame,
    test_size: float = 0.25,
    random_state: int = 42,
) -> tuple[Pipeline, dict[str, Any]]:
    """Train on one split and evaluate on an unseen holdout split.

    Metrics generated from the bundled seed dataset are development
    smoke-test evidence only. They must not be presented as real-world
    model performance.
    """

    features = _prepare_features(dataframe)
    labels = dataframe["is_clickbait"]

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=test_size,
        random_state=random_state,
        stratify=labels,
    )

    model = build_baseline()
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)

    tn, fp, fn, tp = confusion_matrix(
        y_test,
        predictions,
        labels=[0, 1],
    ).ravel()

    clickbait_false_negative_rate = (
        fn / (fn + tp)
        if (fn + tp)
        else 0.0
    )

    metrics: dict[str, Any] = {
        "dataset_scope": "synthetic_seed_only",
        "train_rows": int(len(x_train)),
        "test_rows": int(len(x_test)),
        "precision": round(
            float(
                precision_score(
                    y_test,
                    predictions,
                    zero_division=0,
                )
            ),
            6,
        ),
        "recall": round(
            float(
                recall_score(
                    y_test,
                    predictions,
                    zero_division=0,
                )
            ),
            6,
        ),
        "f1": round(
            float(
                f1_score(
                    y_test,
                    predictions,
                    zero_division=0,
                )
            ),
            6,
        ),
        "confusion_matrix": {
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp),
        },
        "clickbait_false_negative_rate": round(
            float(clickbait_false_negative_rate),
            6,
        ),
    }

    return model, metrics


def save_model(
    model: Pipeline,
    path: str | Path,
) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, destination)


def load_model(
    path: str | Path,
) -> Pipeline:
    return joblib.load(path)
