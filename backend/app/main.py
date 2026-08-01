from fastapi import FastAPI

from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse
from app.services.rule_based_analysis import analyze_safely

app = FastAPI(title="SAFE:SEARCH API", version="0.2.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/v1/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """규칙 기반 안전 분석.

    범죄 여부를 확정하지 않고 안전 대응의 우선순위와 공식기관 정보를 반환한다.
    """
    return analyze_safely(request.text)
