from pathlib import Path

import pandas as pd
import pytest

from app.services.clickbait_ml import (
    evaluate_holdout,
    load_dataset,
    load_model,
    predict_clickbait,
    save_model,
    train_baseline,
)


ROOT = Path(__file__).resolve().parents[2]
SEED_DATASET = ROOT / "data" / "clickbait" / "seed_v0.csv"


def test_seed_dataset_encoding_preserves_korean():
    raw = SEED_DATASET.read_text(encoding="utf-8-sig")

    assert "경찰청" in raw
    assert "충격" in raw
    assert "보이스피싱" in raw
    assert "???" not in raw


def test_seed_dataset_contract():
    dataframe = load_dataset(SEED_DATASET)

    assert len(dataframe) == 60

    counts = dataframe["is_clickbait"].value_counts().to_dict()

    assert counts[0] == 30
    assert counts[1] == 30

    high_impact = dataframe["safety_flags"].str.contains(
        "institution_impersonation"
        "|financial_lure"
        "|personal_information_request",
        regex=True,
    )

    assert int(high_impact.sum()) >= 20

    risky_non_clickbait = dataframe[
        (dataframe["is_clickbait"] == 0)
        & high_impact
    ]

    assert len(risky_non_clickbait) >= 10


def test_train_and_predict_probability():
    dataframe = load_dataset(SEED_DATASET)
    model = train_baseline(dataframe)

    result = predict_clickbait(
        model,
        title="충격! 아무도 알려주지 않는 피해 대응 비밀",
        snippet="지금 바로 확인해야 합니다.",
    )

    assert isinstance(result.is_clickbait, bool)
    assert 0.0 <= result.probability <= 1.0


def test_holdout_metrics_have_expected_fields():
    dataframe = load_dataset(SEED_DATASET)

    _, metrics = evaluate_holdout(dataframe)

    assert metrics["dataset_scope"] == "synthetic_seed_only"
    assert metrics["train_rows"] == 45
    assert metrics["test_rows"] == 15

    for metric_name in (
        "precision",
        "recall",
        "f1",
        "clickbait_false_negative_rate",
    ):
        assert 0.0 <= metrics[metric_name] <= 1.0

    assert set(metrics["confusion_matrix"]) == {
        "tn",
        "fp",
        "fn",
        "tp",
    }


def test_model_save_and_load_roundtrip(tmp_path):
    dataframe = load_dataset(SEED_DATASET)
    model = train_baseline(dataframe)

    destination = tmp_path / "baseline.joblib"
    save_model(model, destination)

    restored = load_model(destination)

    before = predict_clickbait(
        model,
        "단독! 피해자가 꼭 알아야 할 비밀",
        "지금 확인하세요.",
    )
    after = predict_clickbait(
        restored,
        "단독! 피해자가 꼭 알아야 할 비밀",
        "지금 확인하세요.",
    )

    assert before == after


def test_dataset_rejects_missing_required_columns(tmp_path):
    path = tmp_path / "invalid.csv"

    pd.DataFrame(
        {
            "title": ["sample"],
            "is_clickbait": [1],
        }
    ).to_csv(
        path,
        index=False,
        encoding="utf-8-sig",
    )

    with pytest.raises(
        ValueError,
        match="Missing required dataset columns",
    ):
        load_dataset(path)
