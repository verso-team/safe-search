# SAFE:SEARCH

> 디지털 범죄 피해자를 위한 AI 안전검색 서비스

SAFE:SEARCH는 디지털 범죄 피해자가 자신의 피해 상황을 입력하면, AI가 사건 유형과 긴급도를 분석하고 안전한 검색어와 공공기관의 공식 대응 정보를 안내하는 서비스입니다.

AI가 법적 판단을 대신하는 것이 아니라, 위험도 분석과 정보 구조화를 통해 **Human-in-the-Loop 기반의 안전한 의사결정 지원**을 목표로 합니다.

## Core Flow

```text
사용자 입력
  ↓
개인정보/민감정보 검사
  ↓
범죄 유형 분류
  ↓
긴급도 및 위험도 분석
  ↓
안전 검색어 생성
  ↓
공식기관 정보 연결
  ↓
AI 안내
  ↓
필요 시 인간 검토 / 관계기관 연계
```

## Tech Stack

### Current / Initial
- Frontend: Next.js, TypeScript, Tailwind CSS, shadcn/ui
- Backend: FastAPI, Python, Pydantic, REST API
- AI / ML: OpenAI API, Scikit-learn, Pandas, Prompt Engineering, Rule-based Risk Classification
- Database: PostgreSQL
- DevOps: GitHub, GitHub Actions, Docker, Vercel
- Quality: Pytest, ESLint, Prettier
- Collaboration: Figma, GitHub, Notion

### Planned / Under Review
- Supabase
- pgvector
- Hugging Face Transformers
- Sentence Transformers
- SQLAlchemy
- Alembic
- Redis
- Sentry
- Playwright

> 기술은 실제 필요성이 확인될 때 도입합니다. README에 적기 위해 불필요한 기술을 추가하지 않습니다.

## Team Workspaces

### 개발팀
- `frontend/`
- `backend/`
- `ai/`
- `data/`
- `scripts/`
- `docs/development/`

### AI 기획팀
- `docs/ai-planning/`

### 운영팀
- `docs/operations/`
- `design/`
- `docs/presentation/`

### 교수 자문
- `docs/professor-materials/`

## 꼭 먼저 읽기
1. [`CONTRIBUTING.md`](./CONTRIBUTING.md)
2. [`DIRECTORY_GUIDE.md`](./DIRECTORY_GUIDE.md)
3. 자기 팀 폴더의 `README.md`

## 7/29 산출물
- 개발팀: `docs/development/deliverables-0729/`
- AI 기획팀: `docs/ai-planning/deliverables-0729/`
- 운영팀: `docs/operations/deliverables-0729/`

## Project Principles
1. AI가 최종 법적 판단을 하지 않는다.
2. 긴급하거나 불확실한 상황은 사람 또는 관계기관으로 연결한다.
3. 공식적이고 검증 가능한 기관 정보를 우선한다.
4. 개인정보와 민감정보를 최소한으로 처리한다.
5. AI의 신뢰도가 낮은 경우 이를 숨기지 않는다.
6. 피해자에게 추가 위험을 만들 수 있는 검색어를 그대로 제공하지 않는다.
7. Human-in-the-Loop를 핵심 안전장치로 설계한다.

## Status
🚧 Under active development.
