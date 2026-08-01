from fastapi import FastAPI

from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse
from app.services.pii_redaction import (
    build_redaction_notice,
    log_redaction_summary,
    redact_sensitive_text,
)
from app.services.rule_based_analysis import analyze_safely

app = FastAPI(title="SAFE:SEARCH API", version="0.3.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/v1/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """민감정보를 마스킹한 뒤 규칙 기반 안전 분석을 수행한다.

    요청 원문은 분석 함수나 애플리케이션 로그로 전달하지 않는다.
    범죄 여부를 확정하지 않고 안전 대응의 우선순위와 공식기관 정보를 반환한다.
    """

    redaction = redact_sensitive_text(request.text)
    log_redaction_summary(redaction)

    result = analyze_safely(redaction.redacted_text)
    redaction_notice = build_redaction_notice(redaction)

    if redaction_notice is None:
        return result

    combined_notice = "\n".join(
        part
        for part in (
            result.safety_notice,
            redaction_notice,
        )
        if part
    )

    return result.model_copy(
        update={"safety_notice": combined_notice}
    )
