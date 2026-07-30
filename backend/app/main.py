from fastapi import FastAPI

from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse
from app.services.mock_analysis import analyze_safely

app = FastAPI(title="SAFE:SEARCH API", version="0.1.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/v1/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """Mock 기반 구조화 분석. 실제 AI 연결 전 UX 계약을 고정한다."""
    return analyze_safely(request.text)
