import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse
from app.services.mock_analysis import analyze_safely

app = FastAPI(title="SAFE:SEARCH API", version="0.1.0")

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "safe-search-api", "version": app.version}


@app.post("/api/v1/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """Mock 기반 구조화 분석. 실제 AI 연결 전 UX 계약을 고정한다."""
    return analyze_safely(request.text)
