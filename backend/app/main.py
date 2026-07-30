import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse
from app.schemas.clickbait import (
    ClickbaitAnalyzeRequest,
    ClickbaitAnalyzeResponse,
    HumanReviewRequest,
    HumanReviewResponse,
    HumanReviewSummary,
)
from app.services.clickbait_analysis import analyze_clickbait
from app.services.human_review import record_human_review, summarize_human_reviews
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


@app.post("/api/v1/clickbait/analyze", response_model=ClickbaitAnalyzeResponse)
def analyze_clickbait_content(request: ClickbaitAnalyzeRequest) -> ClickbaitAnalyzeResponse:
    """클릭베이트 위험도와 재현 가능한 판단 근거를 반환한다."""
    return analyze_clickbait(request)


@app.post("/api/v1/clickbait/reviews", response_model=HumanReviewResponse)
def create_human_review(request: HumanReviewRequest) -> HumanReviewResponse:
    """원문 없이 AI 판단에 대한 인간의 최종 검토를 감사 로그로 남긴다."""
    return record_human_review(request)


@app.get("/api/v1/clickbait/reviews/summary", response_model=HumanReviewSummary)
def get_human_review_summary() -> HumanReviewSummary:
    """개별 원문을 노출하지 않고 인간 검토 집계만 반환한다."""
    return summarize_human_reviews()


frontend_dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
assets_dir = frontend_dist / "assets"

if assets_dir.is_dir():
    app.mount("/assets", StaticFiles(directory=assets_dir), name="frontend-assets")

    @app.get("/", include_in_schema=False)
    def frontend_index() -> FileResponse:
        return FileResponse(frontend_dist / "index.html")
