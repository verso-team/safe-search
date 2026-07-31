# Backend

FastAPI 기반 구조화 안전 분석 API입니다. 현재는 실제 AI 대신 결정론적 Mock
서비스를 사용해 프론트엔드와 iOS의 UX 계약을 검증합니다.

## 로컬 실행

```bash
python -m venv .venv
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API

- `GET /health`: 서비스 상태 및 버전
- `POST /api/v1/analyze`: 피해 상황 구조화 분석

## 환경 변수

- `CORS_ORIGINS`: 허용할 프론트엔드 Origin의 쉼표 구분 목록
- `DATABASE_URL`: 향후 Human Review 저장소 연결
- `OPENAI_API_KEY`: 실제 AI 분석 연결 전까지 사용하지 않음

API는 범죄 여부나 법률 결론을 확정하지 않습니다. 긴급 신호 또는 낮은 신뢰도는
Human Review 대상으로 전달하도록 응답합니다.
