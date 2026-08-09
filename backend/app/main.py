from fastapi import FastAPI

from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse
from app.schemas.search_risk import (
    SearchRiskRequest,
    SearchRiskResponse,
)
from app.services.analysis_response_policy import (
    apply_psychological_safety_policy,
)
from app.services.pii_redaction import (
    build_redaction_notice,
    log_redaction_summary,
    redact_sensitive_text,
)
from app.services.psychological_safety import (
    SupportMode,
    ToneStyle,
)
from app.services.rule_based_analysis import analyze_safely
from app.services.search_risk import analyze_search_result


app = FastAPI(
    title="SAFE:SEARCH API",
    version="0.6.1",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post(
    "/api/v1/analyze",
    response_model=AnalyzeResponse,
)
def analyze(
    request: AnalyzeRequest,
) -> AnalyzeResponse:
    """피해 상황을 분석하고 Psychological Safety 정책을 적용한다.

    처리 순서:
    1. PII / 민감정보 마스킹
    2. 사건 유형·긴급도·의도 분석
    3. 사용자 지원 방식 결정
    4. Psychological Safety Audit
    5. 필요 시 Human Review 활성화
    """

    redaction = redact_sensitive_text(request.text)
    log_redaction_summary(redaction)

    result = analyze_safely(
        redaction.redacted_text
    )

    redaction_notice = build_redaction_notice(
        redaction
    )

    if redaction_notice is not None:
        combined_notice = "\n".join(
            part
            for part in (
                result.safety_notice,
                redaction_notice,
            )
            if part
        )

        result = result.model_copy(
            update={
                "safety_notice": combined_notice,
            }
        )

    selected_mode = (
        SupportMode(request.support_mode)
        if request.support_mode is not None
        else None
    )

    tone = ToneStyle(request.tone_style)

    return apply_psychological_safety_policy(
        result=result,
        user_selected_mode=selected_mode,
        tone=tone,
    )


@app.post(
    "/api/v1/search-risk",
    response_model=SearchRiskResponse,
)
def search_risk(
    request: SearchRiskRequest,
) -> SearchRiskResponse:
    """검색결과의 클릭베이트 및 추가 피해 위험 신호를 분석한다.

    범죄 여부나 사이트의 불법성을 확정하지 않으며,
    고영향 위험 신호는 Human Review 대상으로 표시한다.
    """

    return analyze_search_result(request)