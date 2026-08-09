from urllib.parse import urlparse

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


EXPECTED_RESPONSE_KEYS = {
    "primary_intent",
    "secondary_intents",
    "emotional_state",
    "urgency",
    "confidence",
    "suspected_harm_type",
    "emotional_support_message",
    "situation_summary",
    "immediate_actions",
    "safe_search_queries",
    "recommended_agencies",
    "requires_human_review",
    "safety_notice",
    "support_mode",
    "tone_style",
    "opening_message",
    "psychological_safety_passed",
    "psychological_safety_issues",
}

EXPECTED_ACTION_KEYS = {
    "title",
    "detail",
    "priority",
}

EXPECTED_AGENCY_KEYS = {
    "id",
    "name",
    "role",
    "phone",
    "website",
    "is_official",
}


def test_ios_contract_has_expected_snake_case_shape():
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": (
                "상대가 내 영상을 유포하겠다고 "
                "협박하고 있어요."
            )
        },
    )

    assert response.status_code == 200
    result = response.json()

    assert set(result) == EXPECTED_RESPONSE_KEYS

    assert 0 <= result["confidence"] <= 1
    assert len(result["immediate_actions"]) <= 3
    assert result["safe_search_queries"]
    assert result["recommended_agencies"]

    assert result["support_mode"] in {
        "information_first",
        "support_first",
        "user_choice",
    }

    assert result["tone_style"] in {
        "soft_polite",
        "casual",
    }

    assert result["opening_message"]
    assert isinstance(
        result["psychological_safety_passed"],
        bool,
    )

    assert isinstance(
        result["psychological_safety_issues"],
        list,
    )

    priorities = [
        item["priority"]
        for item in result["immediate_actions"]
    ]

    assert priorities == sorted(priorities)

    assert all(
        set(item) == EXPECTED_ACTION_KEYS
        for item in result["immediate_actions"]
    )

    for agency in result["recommended_agencies"]:
        assert set(agency) == EXPECTED_AGENCY_KEYS
        assert agency["is_official"] is True

        parsed = urlparse(
            agency["website"]
        )

        assert parsed.scheme in {
            "http",
            "https",
        }

        assert parsed.netloc


def test_whitespace_only_input_is_rejected():
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": "   \n\t  ",
        },
    )

    assert response.status_code == 422


def test_overlong_input_is_rejected():
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": "가" * 5001,
        },
    )

    assert response.status_code == 422


def test_input_is_trimmed_before_analysis():
    response = client.post(
        "/api/v1/analyze",
        json={
            "text": (
                "   상대가 흉기를 들고 "
                "찾아왔어요.   "
            )
        },
    )

    assert response.status_code == 200

    assert (
        response.json()["urgency"]
        == "critical"
    )