from __future__ import annotations

import re
from urllib.parse import urlparse

from app.schemas.search_risk import (
    RiskLevel,
    RiskType,
    SearchRiskRequest,
    SearchRiskResponse,
)
from app.services.clickbait_runtime import (
    CLICKBAIT_MODEL_NAME,
    predict_runtime_clickbait,
)


SENSATIONAL_TERMS = (
    "충격",
    "경악",
    "단독",
    "절대",
    "아무도 알려주지 않는",
    "지금 당장",
    "무조건",
    "100%",
    "소름",
    "대박",
)

MISLEADING_TERMS = (
    "숨긴",
    "숨겨진",
    "비밀",
    "삭제되기 전",
    "곧 사라질",
    "공개하지 않는",
    "알려주지 않는",
)

INSTITUTION_TERMS = (
    "경찰",
    "경찰청",
    "검찰",
    "검찰청",
    "금융감독원",
    "금감원",
    "kisa",
    "한국인터넷진흥원",
    "정부",
    "피해자지원센터",
)

SUSPICIOUS_INSTITUTION_ACTIONS = (
    "안전계좌",
    "송금",
    "입금",
    "수수료",
    "환급",
    "본인인증",
    "인증번호",
    "otp",
    "주민번호",
    "주민등록번호",
    "계좌번호",
    "개인정보",
)

FINANCIAL_LURE_TERMS = (
    "안전계좌",
    "선입금",
    "수수료 입금",
    "수수료를 입금",
    "송금하세요",
    "송금해",
    "입금하세요",
    "입금해",
    "피해금 환급",
    "환급금",
    "보상금 지급",
    "지원금 지급",
)

PII_TERMS = (
    "주민번호",
    "주민등록번호",
    "인증번호",
    "인증코드",
    "otp",
    "계좌번호",
    "카드번호",
    "개인정보",
)

PII_ACTION_TERMS = (
    "입력",
    "제출",
    "보내",
    "알려",
    "기입",
    "등록",
    "확인",
)

OFFICIAL_DOMAINS = (
    "police.go.kr",
    "kisa.or.kr",
    "fss.or.kr",
    "stop.or.kr",
    "women1366.kr",
)

RISK_LABELS = {
    RiskType.sensational: "과장·자극적 표현",
    RiskType.misleading: "오해를 유도할 수 있는 표현",
    RiskType.institution_impersonation: "공공기관 사칭 가능성",
    RiskType.financial_lure: "송금·금전 유도",
    RiskType.personal_information_request: "개인정보 또는 인증정보 요구",
}


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term.lower() in text for term in terms)


def _hostname(url: str) -> str:
    candidate = url.strip()

    if "://" not in candidate:
        candidate = f"https://{candidate}"

    return (urlparse(candidate).hostname or "").lower().rstrip(".")


def _is_official_domain(url: str) -> bool:
    host = _hostname(url)

    if host.endswith(".go.kr") or host == "go.kr":
        return True

    return any(
        host == domain or host.endswith(f".{domain}")
        for domain in OFFICIAL_DOMAINS
    )


def _append_unique(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)


def analyze_search_result(
    request: SearchRiskRequest,
) -> SearchRiskResponse:
    """검색결과의 클릭베이트 및 추가 피해 위험 신호를 규칙과 ML baseline으로 분석한다.

    이 결과는 사이트의 불법성이나 범죄 여부를 확정하지 않는다.
    confidence는 실제 범죄 확률이 아니라 현재 규칙이 입력과 얼마나
    강하게 일치하는지 표현하기 위한 초기 지표다.
    """

    title = _normalize(request.title)
    snippet = _normalize(request.snippet)
    combined = f"{title} {snippet}".strip()
    official_domain = _is_official_domain(request.url)

    ml_prediction = predict_runtime_clickbait(
        title=request.title,
        snippet=request.snippet,
    )

    risk_types: list[RiskType] = []
    signals: list[str] = []

    sensational = (
        _contains_any(title, SENSATIONAL_TERMS)
        or bool(re.search(r"[!?]{2,}", request.title))
    )

    if sensational:
        risk_types.append(RiskType.sensational)
        _append_unique(
            signals,
            "제목에 과장되거나 긴급 행동을 유도하는 표현이 포함되어 있습니다.",
        )

    if _contains_any(combined, MISLEADING_TERMS):
        risk_types.append(RiskType.misleading)
        _append_unique(
            signals,
            "정보를 숨기거나 곧 사라질 것처럼 표현하는 문구가 탐지되었습니다.",
        )

    has_institution_name = _contains_any(combined, INSTITUTION_TERMS)
    has_suspicious_action = _contains_any(
        combined,
        SUSPICIOUS_INSTITUTION_ACTIONS,
    )

    if (
        has_institution_name
        and has_suspicious_action
        and not official_domain
    ):
        risk_types.append(RiskType.institution_impersonation)
        _append_unique(
            signals,
            "공공기관을 언급하면서 비공식 도메인에서 민감한 행동을 요구합니다.",
        )

    if (
        _contains_any(combined, FINANCIAL_LURE_TERMS)
        and not official_domain
    ):
        risk_types.append(RiskType.financial_lure)
        _append_unique(
            signals,
            "송금·입금·환급·수수료와 관련된 금전 유도 표현이 탐지되었습니다.",
        )

    has_pii_term = _contains_any(combined, PII_TERMS)
    has_pii_action = _contains_any(combined, PII_ACTION_TERMS)

    if has_pii_term and has_pii_action and not official_domain:
        risk_types.append(RiskType.personal_information_request)
        _append_unique(
            signals,
            "개인정보 또는 인증정보 입력·제출을 요구하는 표현이 탐지되었습니다.",
        )

    # 중복 가능성을 방어하면서 순서는 유지한다.
    risk_types = list(dict.fromkeys(risk_types))

    rule_is_clickbait = any(
        risk_type in (
            RiskType.sensational,
            RiskType.misleading,
        )
        for risk_type in risk_types
    )

    ml_is_clickbait = ml_prediction.is_clickbait

    is_clickbait = (
        rule_is_clickbait
        or ml_is_clickbait
    )

    if rule_is_clickbait and ml_is_clickbait:
        clickbait_decision_source = "rule+ml"
    elif rule_is_clickbait:
        clickbait_decision_source = "rule"
    elif ml_is_clickbait:
        clickbait_decision_source = "ml"
    else:
        clickbait_decision_source = "none"

    if ml_is_clickbait:
        _append_unique(
            signals,
            "TF-IDF baseline에서 클릭베이트 신호가 탐지되었습니다.",
        )

    high_impact_types = {
        RiskType.institution_impersonation,
        RiskType.financial_lure,
        RiskType.personal_information_request,
    }

    has_high_impact_risk = any(
        risk_type in high_impact_types
        for risk_type in risk_types
    )

    if has_high_impact_risk:
        risk_level = RiskLevel.high
    elif risk_types or ml_is_clickbait:
        risk_level = RiskLevel.medium
    else:
        risk_level = RiskLevel.low

    if risk_types:
        confidence = round(
            min(0.70 + (0.06 * len(risk_types)), 0.94),
            2,
        )
    else:
        confidence = 0.76

    requires_human_review = (
        has_high_impact_risk
        or len(risk_types) >= 3
    )

    if risk_types:
        labels = ", ".join(
            RISK_LABELS[risk_type]
            for risk_type in risk_types
        )
        explanation = (
            f"현재 규칙에서 {labels} 신호가 탐지되었습니다. "
            "이 결과는 사이트의 범죄 여부를 확정하는 판단이 아닙니다."
        )
    elif ml_is_clickbait:
        explanation = (
            "TF-IDF 클릭베이트 baseline에서 클릭베이트 신호가 "
            "탐지되었습니다. 모델 확률은 범죄 또는 불법성의 "
            "확률을 의미하지 않습니다."
        )
    else:
        explanation = (
            "현재 규칙에서 뚜렷한 클릭베이트 또는 추가 피해 위험 신호가 "
            "탐지되지 않았습니다. 이는 해당 검색결과의 안전을 보장하지 않습니다."
        )

    return SearchRiskResponse(
        is_clickbait=is_clickbait,
        risk_level=risk_level,
        risk_types=risk_types,
        confidence=confidence,
        risk_signals=signals,
        explanation=explanation,
        requires_human_review=requires_human_review,
        clickbait_probability=ml_prediction.probability,
        clickbait_model=CLICKBAIT_MODEL_NAME,
        clickbait_decision_source=clickbait_decision_source,
    )
