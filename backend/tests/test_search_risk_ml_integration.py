from app.schemas.search_risk import SearchRiskRequest
from app.services.clickbait_ml import ClickbaitPrediction
from app.services.clickbait_runtime import (
    CLICKBAIT_MODEL_NAME,
    get_clickbait_model,
)
from app.services import search_risk as search_risk_service


def analyze(title: str, snippet: str = ""):
    return search_risk_service.analyze_search_result(
        SearchRiskRequest(
            title=title,
            snippet=snippet,
            url="https://example.com",
        )
    )


def test_runtime_model_is_cached():
    get_clickbait_model.cache_clear()

    first = get_clickbait_model()
    second = get_clickbait_model()

    assert first is second


def test_ml_only_prediction_does_not_overwrite_rule_confidence(
    monkeypatch,
):
    monkeypatch.setattr(
        search_risk_service,
        "predict_runtime_clickbait",
        lambda **kwargs: ClickbaitPrediction(
            is_clickbait=True,
            probability=0.91,
        ),
    )

    result = analyze(
        "Account recovery guide",
        "Neutral procedural information.",
    )

    assert result.is_clickbait is True
    assert result.risk_types == []
    assert result.risk_level == "medium"
    assert result.confidence == 0.76
    assert result.clickbait_probability == 0.91
    assert result.clickbait_model == CLICKBAIT_MODEL_NAME
    assert result.clickbait_decision_source == "ml"
    assert result.requires_human_review is False


def test_rule_only_prediction_source(
    monkeypatch,
):
    monkeypatch.setattr(
        search_risk_service,
        "predict_runtime_clickbait",
        lambda **kwargs: ClickbaitPrediction(
            is_clickbait=False,
            probability=0.10,
        ),
    )

    result = analyze("WOW!!")

    assert result.is_clickbait is True
    assert result.clickbait_decision_source == "rule"
    assert result.clickbait_probability == 0.10


def test_rule_and_ml_prediction_source(
    monkeypatch,
):
    monkeypatch.setattr(
        search_risk_service,
        "predict_runtime_clickbait",
        lambda **kwargs: ClickbaitPrediction(
            is_clickbait=True,
            probability=0.88,
        ),
    )

    result = analyze("WOW!!")

    assert result.is_clickbait is True
    assert result.clickbait_decision_source == "rule+ml"
    assert result.clickbait_probability == 0.88


def test_negative_agreement_has_no_positive_source(
    monkeypatch,
):
    monkeypatch.setattr(
        search_risk_service,
        "predict_runtime_clickbait",
        lambda **kwargs: ClickbaitPrediction(
            is_clickbait=False,
            probability=0.12,
        ),
    )

    result = analyze("Account recovery guide")

    assert result.is_clickbait is False
    assert result.clickbait_decision_source == "none"
    assert result.clickbait_probability == 0.12
