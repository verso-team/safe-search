from functools import lru_cache
from pathlib import Path

from sklearn.pipeline import Pipeline

from app.services.clickbait_ml import (
    ClickbaitPrediction,
    load_dataset,
    predict_clickbait,
    train_baseline,
)


CLICKBAIT_MODEL_NAME = "tfidf_logreg_seed_v0"
CLICKBAIT_THRESHOLD = 0.5

REPO_ROOT = Path(__file__).resolve().parents[3]
SEED_DATASET = (
    REPO_ROOT
    / "data"
    / "clickbait"
    / "seed_v0.csv"
)


@lru_cache(maxsize=1)
def get_clickbait_model() -> Pipeline:
    """Train the bundled seed baseline once per worker process."""

    dataframe = load_dataset(SEED_DATASET)

    return train_baseline(dataframe)


def predict_runtime_clickbait(
    title: str,
    snippet: str,
) -> ClickbaitPrediction:
    """Return the cached baseline prediction."""

    return predict_clickbait(
        model=get_clickbait_model(),
        title=title,
        snippet=snippet,
        threshold=CLICKBAIT_THRESHOLD,
    )
