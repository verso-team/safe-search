# SAFE:SEARCH

> **Team Verso**  
> 디지털 범죄 피해자를 위한 AI 안전검색 서비스

SAFE:SEARCH는 디지털 범죄 피해자가 불안한 상황에서 위험한 정보, 과장 광고, 공식기관 사칭 콘텐츠에 노출되지 않도록 돕는 AI 기반 안전검색 서비스입니다.

사용자가 피해 상황을 자연어로 입력하면 AI가 사건 유형과 긴급도를 분석하고, 안전한 검색어와 공식기관 정보를 우선 추천합니다. 검색 결과에 포함된 클릭베이트, 과장 표현, 결제 유도, 신고 방해 신호를 탐지하며, 신뢰도가 낮거나 영향이 큰 사례는 Human-in-the-Loop 검토로 전환합니다.

본 프로젝트는 **제2회 TRAITHON** 참가를 위해 Team Verso가 개발합니다.

---

## Core Features

- 피해 상황 자연어 입력 및 유형 분석
- AI 기반 위험도·긴급도·신뢰도 분류
- 상황별 안전 검색어 추천
- 공식기관 정보 우선 안내
- 검색 결과 내 위험 표현 탐지
- 정상·주의·위험 콘텐츠 분류
- 저신뢰·고위험 사례 Human-in-the-Loop 전환
- 관리자 승인·수정·반려 및 감사 로그
- 전문가 자문 결과 기반 법률·심리·운영 기준 개선

---

## Service Flow

```text
피해 상황 입력
    ↓
AI 사건 유형·위험 신호·긴급도 분석
    ↓
안전 검색어 추천
    ↓
공식기관 중심 정보 안내
    ↓
검색 결과 위험도 분석
    ↓
저신뢰·고위험 사례 인간 검토
```

---

## Team Verso

### 개발팀

| 이름 | 역할 | 전공 |
|---|---|---|
| 이영준 | AI Engineer · Development PM | 컴퓨터공학과 |
| 정한빈 | Prototype · Security | 게임공학과 |
| 임준호 | Data Scientist · AI Model Training | 컴퓨터공학과 |

### AI 기획팀

| 이름 | 역할 | 전공 |
|---|---|---|
| 이원주 | Psychology Planning · 안전 문구 검토 | 심리상담학과 |
| 이혜성 | Crime Scenario Planning | 경찰법학과 |
| 심주연 | Crime Scenario · 대응 기준 기획 | 경찰법학과 |

### 운영팀

| 이름 | 역할 | 전공 |
|---|---|---|
| 문시우 | Market Analysis · Business Research | 경영학과 |
| 주하린 | Public Institution Operations Research | 행정학과 |
| 손지원 | Content Editing · Presentation | 콘텐츠미디어학과 |
| 김은솔 | UI/UX Design | 컴퓨터공학과 |

---

## Repository Structure

```text
safe-search/
├── frontend/                   # 사용자·관리자 웹 화면
├── backend/                    # API, 서비스 로직, 데이터 저장
├── ai/                         # 모델 학습·추론·평가
├── data/                       # 원천·가공·샘플 데이터
├── docs/
│   ├── scenario/               # 피해자 입력 및 범죄 시나리오
│   ├── psychology/             # 심리적 안전 기준과 문구
│   ├── legal/                  # 범죄·법률·신고 기준
│   ├── presentation/           # 발표자료와 시연 대본
│   └── professor-materials/    # 교수님 자문자료
├── design/                     # UI/UX, 와이어프레임, 디자인 자산
├── research/
│   ├── market/                 # 시장·유사 서비스·사업화 조사
│   └── public-operation/       # 공공기관 연계·운영 조사
├── scripts/                    # 실행·데이터 처리 자동화
├── CONTRIBUTING.md
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

## Team Workspaces

### 개발팀

- `frontend/`
- `backend/`
- `ai/`
- `data/`
- `scripts/`

### AI 기획팀

- `docs/scenario/`
- `docs/psychology/`
- `docs/legal/`

### 운영팀

- `research/market/`
- `research/public-operation/`
- `design/`
- `docs/presentation/`
- `docs/professor-materials/`

---

## Branch Strategy

| 브랜치 | 용도 |
|---|---|
| `main` | 최종 제출·안정 버전 |
| `develop` | 통합 개발 브랜치 |
| `feature/frontend` | 사용자 화면 개발 |
| `feature/backend` | API·백엔드 개발 |
| `feature/ai-model` | AI 모델 학습·평가 |
| `feature/scenario` | 피해 시나리오·기획 문서 |
| `feature/admin` | 인간 검토 관리자 기능 |
| `feature/design` | UI/UX 및 디자인 |
| `docs/professor-materials` | 교수님 자문자료 |

기능별 세부 작업은 다음 형식을 권장합니다.

```text
feature/<기능명>
fix/<오류명>
docs/<문서명>
design/<화면명>
research/<조사명>
```

---
## 🛠 Tech Stack

### Frontend
- Next.js
- TypeScript
- Tailwind CSS
- shadcn/ui

### Backend
- FastAPI
- Python
- Pydantic

### AI / NLP
- OpenAI API
- LangChain
- Sentence Transformers
- Scikit-learn

### Data
- PostgreSQL
- pgvector

### Security
- Input Validation & Sanitization
- PII Detection / Masking
- Prompt Injection Defense
- Rate Limiting

### Infrastructure
- Docker
- GitHub Actions
- Vercel
- Supabase

### Collaboration
- GitHub
- Figma
- Notion
---

---

## Collaboration Rules

1. 작업 전 GitHub Issue를 생성합니다.
2. `develop`에서 작업 브랜치를 생성합니다.
3. 한 브랜치에는 하나의 목적만 담습니다.
4. 커밋 메시지는 변경 목적이 드러나게 작성합니다.
5. 작업 완료 후 `develop` 대상 Pull Request를 생성합니다.
6. 최소 1명의 리뷰 후 병합합니다.
7. `main`은 발표·제출 가능한 상태에서만 갱신합니다.
8. `.env`, API 키, 비밀번호, 개인정보는 커밋하지 않습니다.

### Commit Convention

```text
feat: 새로운 기능 추가
fix: 오류 수정
docs: 문서 추가 또는 수정
design: UI/UX 및 디자인 변경
data: 데이터 추가·정제
test: 테스트 추가 또는 수정
refactor: 기능 변경 없는 코드 개선
chore: 설정·빌드·환경 작업
```

예시:

```text
feat: 피해 상황 분석 API 추가
docs: 경찰법학 교수님 자문 질문 정리
data: 클릭베이트 경계 사례 데이터 추가
design: 위험도 분석 화면 정보 위계 수정
fix: 관리자 승인 상태 저장 오류 수정
```

---

## Quick Start

### 1. 저장소 복제

```bash
git clone https://github.com/verso-team/safe-search.git
cd safe-search
```

### 2. 환경변수 준비

```bash
cp .env.example .env
```

### 3. Docker 실행

```bash
docker compose up --build
```

### 4. 서비스 종료

```bash
docker compose down
```

> 현재 저장소는 프로젝트 초기 구조입니다. 실제 실행 환경과 서비스별 Dockerfile은 개발 진행에 맞춰 추가합니다.

---

## Development Principles

- 피해자를 비난하거나 책임을 돌리는 표현을 사용하지 않습니다.
- AI 결과를 확정적인 법률 판단으로 표현하지 않습니다.
- 공식기관과 검증된 정보원을 우선합니다.
- 고위험·저신뢰 사례는 인간 검토로 전환합니다.
- 판단 근거와 불확실성을 가능한 범위에서 설명합니다.
- 개인정보는 최소한으로 수집하고 안전하게 관리합니다.
- 공포와 조급함을 과도하게 자극하는 문구를 피합니다.
- 전문가 자문 내용을 화면·정책·데이터 기준에 추적 가능하게 반영합니다.

---

## Current Goals

- 사용자 피해 상황 입력 화면
- AI 피해 유형 및 위험 신호 분석
- 안전 검색어 추천 화면
- 공식기관 우선 안내
- 검색 결과 위험도 분석
- 정상·주의·위험 분류
- 인간 검토 관리자 화면
- 감사 로그 및 수정 이력
- 경찰법학·심리상담·행정 분야 전문가 자문 반영
- TRAITHON 최종 발표 및 시연

---

## Documentation

| 문서 | 위치 |
|---|---|
| 피해자 입력 및 범죄 시나리오 | `docs/scenario/` |
| 심리적 안전 기준 | `docs/psychology/` |
| 법률·신고·증거 보존 기준 | `docs/legal/` |
| 교수님 자문자료 | `docs/professor-materials/` |
| 발표자료와 시연 대본 | `docs/presentation/` |
| 시장·사업화 조사 | `research/market/` |
| 공공기관 운영 조사 | `research/public-operation/` |
| UI/UX 자료 | `design/` |

---

## Security

보안 취약점이나 개인정보 관련 문제는 공개 Issue에 민감한 정보를 작성하지 말고, 팀 내부 채널을 통해 개발 PM에게 전달합니다.

- 실제 피해자의 개인정보를 테스트 데이터에 사용하지 않습니다.
- 모든 샘플 데이터는 비식별·가상 데이터로 작성합니다.
- 비밀정보는 `.env`에서 관리합니다.
- 민감한 로그는 최소한으로 저장합니다.

---

## License

본 프로젝트는 TRAITHON 참가 및 교육·연구 목적의 프로젝트입니다.  
라이선스는 팀 협의 후 확정할 예정입니다.

---

## Contact

**Team Verso**

프로젝트 관련 작업과 제안은 GitHub Issue와 Pull Request를 통해 관리합니다.
