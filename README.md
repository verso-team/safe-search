# SAFE:SEARCH

> 디지털 범죄 피해자를 위한 AI 안전검색 서비스

SAFE:SEARCH는 디지털 범죄 피해자가 자신의 피해 상황을 입력하면, AI가 사건 유형과 긴급도를 분석하고 안전한 검색어와 공공기관의 공식 대응 정보를 안내하는 서비스입니다.

프로젝트의 목표는 AI가 피해자를 대신해 법적·행정적 판단을 내리는 것이 아니라, 위험도를 분석하고 필요한 정보를 구조화하여 **사람의 최종 판단과 관계기관 연계를 지원하는 Human-in-the-Loop 기반 시스템**을 구현하는 것입니다.

---

## 빠른 실행

Docker가 설치된 환경에서는 다음 명령으로 프론트엔드, API, PostgreSQL을 함께
실행할 수 있습니다.

```bash
docker compose up
```

- 사용자 화면: http://localhost:5173
- API 문서: http://localhost:8000/docs
- 상태 확인: http://localhost:8000/health

---

## Core Flow

```text
사용자 입력
  ↓
개인정보 / 민감정보 검사
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
Human Review / 관계기관 연계
```

---

# 🛠 Tech Stack

## Frontend

- Next.js
- TypeScript
- Tailwind CSS
- shadcn/ui

## Backend

- FastAPI
- Python
- Pydantic
- REST API

## AI / ML

- OpenAI API
- Scikit-learn
- Pandas
- Prompt Engineering
- Rule-based Risk Classification

## Database

- PostgreSQL

## AI Safety

- PII Detection & Masking
- Input Validation
- Risk / Urgency Classification
- Confidence Thresholding
- Human-in-the-Loop
- Output Safety Validation

## Security

- Authentication / Authorization
- Role-Based Access Control (RBAC)
- Rate Limiting
- Environment Variable Management
- Audit Logging
- HTTPS / TLS

## Infrastructure / DevOps

- GitHub
- GitHub Actions
- Docker
- Vercel

## Testing / Quality

- Pytest
- ESLint
- Prettier

## Design / Collaboration

- Figma
- GitHub
- Notion

---

# 🔬 Planned / Under Review

아래 기술은 프로젝트 진행 과정에서 실제 필요성을 검토한 뒤 도입합니다.

- Supabase
- pgvector
- Hugging Face Transformers
- Sentence Transformers
- SQLAlchemy
- Alembic
- Redis
- Sentry
- Playwright

> README에 작성된 모든 기술을 무조건 사용하는 것이 목표는 아닙니다.  
> SAFE:SEARCH의 기능과 안전성을 위해 실제로 필요한 기술만 선택합니다.

---

# 🤖 AI Pipeline

SAFE:SEARCH의 AI 기능은 하나의 LLM 응답에 모든 판단을 맡기지 않고 단계별 파이프라인으로 구성합니다.

```text
1. User Input
2. PII / Sensitive Information Check
3. Crime Type Classification
4. Urgency Detection
5. Search Risk Analysis
6. Safe Query Generation
7. Official Institution Recommendation
8. Confidence Check
9. Human Review Escalation
10. Final Guidance
```

주요 기능:

- Crime Type Classification
- Urgency Detection
- Search Risk Analysis
- Safe Query Generation
- Official Institution Recommendation
- Confidence Scoring
- Human Review Escalation

---

# 📂 Repository Structure

```text
safe-search/
│
├─ frontend/
├─ backend/
├─ ai/
├─ data/
├─ scripts/
│
├─ docs/
│  ├─ development/
│  ├─ ai-planning/
│  ├─ operations/
│  ├─ professor-materials/
│  └─ presentation/
│
├─ design/
├─ .github/
│
├─ README.md
├─ CONTRIBUTING.md
└─ DIRECTORY_GUIDE.md
```

---

# 👥 Team Workspaces

## 1. 개발팀

기본 Workspace:

```text
frontend/
backend/
ai/
data/
scripts/
docs/development/
```

### 이영준 — AI Engineer / Development PM / 컴퓨터공학과

담당:

- 전체 자문자료 총괄
- 프로젝트 개요
- 서비스 전체 흐름도
- 현재 개발된 시연 화면 정리
- AI 분석 결과 예시
- 교수님 자문자료 취합
- 이혁우 교수님 질문 작성
- 개발 일정 작성

권장 작업 위치:

```text
docs/development/project-overview/
docs/development/deliverables-0729/
docs/professor-materials/
ai/
```

예:

```text
docs/development/project-overview/project-overview.md
docs/development/project-overview/service-flow.md
docs/development/project-overview/development-roadmap.md
```

### 정한빈 — Prototype / Security / 게임공학과

담당:

- 시연 화면 캡처
- 사용자 화면 설명
- 관리자 화면 설명
- 시스템 구조도
- 보안 및 개인정보 보호 방안 초안

권장 작업 위치:

```text
docs/development/prototype/
docs/development/security/
backend/app/security/
```

예:

```text
docs/development/prototype/current-demo/
docs/development/prototype/user-screen/
docs/development/prototype/admin-screen/
docs/development/prototype/system-architecture/

docs/development/security/privacy-and-security-draft.md
```

화면 캡처 원본:

```text
design/screenshots/
```

### 임준호 — Data Scientist / AI Model / 컴퓨터공학과

담당:

- AI 학습 구조
- 데이터셋 구성
- AI 분석 결과 예시
- 검색 결과 위험도 분석 기준
- AI 신뢰도 및 한계 작성

권장 작업 위치:

```text
ai/
data/
docs/development/ai/
```

예:

```text
docs/development/ai/ai-model-plan.md

ai/classifier/
ai/risk-analysis/
ai/evaluation/

data/scenarios/
data/processed/
```

> 실제 피해자의 개인정보가 포함된 데이터는 업로드하지 않습니다.

---

## 2. AI 기획팀

기본 Workspace:

```text
docs/ai-planning/
```

### 이원주 — Psychology / 심리상담학과

담당:

- 피해자 심리 분석
- 사용자 입력 문구 검토
- 안내 문구 검토
- 심리적으로 안전한 UX 제안
- 임선영 교수님 질문 정리

기본 위치:

```text
docs/ai-planning/psychology/
```

논문, 보고서, HWPX, PDF 등 원본 조사자료:

```text
docs/ai-planning/psychology/research/
```

예:

```text
docs/ai-planning/psychology/research/
└─ 이원주_디지털범죄_피해자_심리행동분석.hwpx
```

정리된 결과:

```text
docs/ai-planning/psychology/victim-behavior/
docs/ai-planning/psychology/victim-input-examples/
docs/ai-planning/psychology/safe-guidance/
```

### 이혜성 — Crime Scenario / 경찰법학과

담당:

- 디지털 범죄 시나리오 작성
- 피해자 입력 예시
- 위험·정상 콘텐츠 사례
- 김동건 교수님 자문 질문 작성

기본 위치:

```text
docs/ai-planning/crime-scenario/
```

예:

```text
docs/ai-planning/crime-scenario/scenario-template.md
docs/ai-planning/crime-scenario/victim-input-examples/
docs/ai-planning/crime-scenario/risk-normal-boundary/
```

### 심주연 — Crime / Legal Scenario / 경찰법학과

담당:

- 범죄 유형 정리
- 신고 및 증거보존 절차
- 공식기관 안내 기준
- 인간 검토 기준 초안
- 김은기 교수님 자문 질문 작성

기본 위치:

```text
docs/ai-planning/legal/
```

예:

```text
docs/ai-planning/legal/crime-types/
docs/ai-planning/legal/reporting-procedure/
docs/ai-planning/legal/evidence-preservation/
docs/ai-planning/legal/official-agency-guidelines/
docs/ai-planning/legal/human-review-criteria-draft.md
```

---

## 3. 운영팀

기본 Workspace:

```text
docs/operations/
design/
docs/presentation/
```

### 문시우 — Business / 경영학과

담당:

- 유사 서비스 조사
- 시장 분석
- 사업화 가능성
- 서비스 차별성

기본 위치:

```text
docs/operations/market/
```

원본 조사 보고서 PDF/HWPX:

```text
docs/operations/market/reports/
```

예:

```text
docs/operations/market/reports/
└─ 문시우_유사서비스_시장분석_보고서.pdf
```

내용을 분리해서 정리할 때:

```text
docs/operations/market/similar-services/
docs/operations/market/market-analysis/
docs/operations/market/business-model/
docs/operations/market/differentiation/
```

### 주하린 — Public Operations / 행정학과

담당:

- 공공기관 운영 조사
- 경찰청·KISA 등 기관 연계
- 관리자 운영 프로세스

기본 위치:

```text
docs/operations/public-operation/
```

예:

```text
docs/operations/public-operation/police/
docs/operations/public-operation/kisa/
docs/operations/public-operation/agency-linkage/
docs/operations/public-operation/admin-operation-process/
```

### 손지원 — Content / Presentation / 미디어콘텐츠학과

담당:

- 9월 21일 팀 소개 제출 영상 제작
- 발표자료 구성

기본 위치:

```text
docs/operations/content/
docs/presentation/
```

예:

```text
docs/operations/content/team-intro-video/
docs/operations/content/presentation-structure/

docs/presentation/slides/
docs/presentation/images/
docs/presentation/diagrams/
docs/presentation/final/
```

> 영상 파일처럼 용량이 큰 파일은 GitHub에 바로 업로드하기 전에 개발 PM과 먼저 상의해주세요.

### 김은솔 — UI / UX / 컴퓨터공학과

담당:

- 최종 핵심 화면 1종 검수
- 색상·가독성에 대한 간단한 피드백

> 업무 부담을 최소화하기 위해 UI 구현, 디자인 시스템, 화면 배치,
> 다이어그램, 캡처 및 발표자료 편집은 개발팀과 콘텐츠 담당자가 수행합니다.
> 김은솔은 새 시안을 직접 제작하지 않고 완성본 검수만 담당합니다.

기본 위치:

```text
design/
docs/operations/design/
```

예:

```text
design/ui/
design/color-system/
design/exports/
```

---

# 📚 교수 자문자료

교수님께 보여드릴 자료:

```text
docs/professor-materials/
```

## 공통 자료

```text
docs/professor-materials/common/
```

공통 자료에는 다음 내용을 정리합니다.

- 프로젝트 개요
- 서비스 흐름
- 현재 시연 화면
- AI 분석 예시
- 안전 검색어 추천
- 검색 결과 위험도 분석
- Human-in-the-Loop 구조
- 시스템 구조
- 개인정보 및 보안
- 주요 쟁점
- 향후 개발 일정

## 교수님별 질문

```text
docs/professor-materials/lee-hyeokwoo/
docs/professor-materials/lim-seonyoung/
docs/professor-materials/kim-donggun/
docs/professor-materials/kim-eunki/
```

예:

```text
docs/professor-materials/kim-eunki/questions.md
```

> 원본 조사자료를 교수 자문 폴더에 다시 복사하지 않습니다.

예를 들어 심리상담 관련 원본 조사자료는:

```text
docs/ai-planning/psychology/
```

에 보관하고, 교수님께 실제로 질문할 내용만:

```text
docs/professor-materials/lim-seonyoung/questions.md
```

에 정리합니다.

---

# 📦 7/29 Deliverables

`deliverables-0729`는 모든 작업물을 넣는 장소가 아니라 **7월 29일 기준으로 팀이 확인할 수 있는 정리된 결과물**을 모으는 폴더입니다.

## 개발팀

```text
docs/development/deliverables-0729/
├─ project-overview/
├─ current-demo/
├─ ai-analysis-example/
├─ safe-search-query/
├─ search-risk-analysis/
├─ human-review-admin/
└─ development-schedule/
```

산출물:

- 프로젝트 개요
- 현재 개발된 시연 화면
- AI 분석 결과 예시
- 안전 검색어 추천 화면
- 검색 결과 위험도 분석 화면
- 인간 검토 관리자 화면
- 개발 일정

## AI 기획팀

```text
docs/ai-planning/deliverables-0729/
├─ victim-input-examples/
├─ crime-scenarios/
├─ risk-normal-boundary/
├─ police-law-questions/
├─ psychology-questions/
└─ ai-message-review/
```

산출물:

- 피해자 입력 예시
- 범죄 시나리오
- 위험·정상 콘텐츠 경계 사례
- 경찰법학 질문
- 심리상담 질문
- AI 안내 문구 검토

## 운영팀

```text
docs/operations/deliverables-0729/
├─ market-analysis/
├─ public-agency-research/
├─ operation-process/
├─ presentation-design/
└─ final-consulting-material/
```

산출물:

- 시장 분석
- 공공기관 운영 조사
- 운영 프로세스
- 발표자료 디자인
- 최종 자문자료 편집

---

# 📁 팀원 자료 업로드 가이드

SAFE:SEARCH 저장소는 코드뿐 아니라 조사자료, 교수 자문자료, 디자인, 발표자료도 함께 관리합니다.

팀원은 파일을 올리기 전에 **자신의 팀과 자료 성격에 맞는 폴더**를 먼저 확인해주세요.

> 같은 파일을 여러 폴더에 중복 업로드하지 않습니다.  
> 원본 자료는 담당 Workspace에 보관하고, 교수 자문자료나 발표자료에서는 필요한 내용을 정리하여 사용합니다.

---

# 📝 파일 이름 규칙

파일명을 보고 담당자와 내용을 알 수 있도록 작성합니다.

추천:

```text
문시우_유사서비스_시장분석_보고서.pdf
이원주_디지털범죄_피해자_심리분석.hwpx
이혜성_디지털범죄_시나리오.md
심주연_신고절차_증거보존.md
정한빈_시스템구조도.png
김은솔_관리자화면_UI.png
```

피하기:

```text
최종.pdf
진짜최종.pdf
최종수정2.pdf
새문서.hwpx
자료.pdf
```

Git이 파일 변경 이력을 관리하기 때문에 파일명에 `최종`, `진짜최종`, `최종2` 등을 반복해서 붙이지 않습니다.

---

# 📄 문서 작성 권장 형식

Markdown 문서를 작성할 경우 가능하면 아래 구조를 사용합니다.

```text
# 제목

## 목적

## 조사 내용

## 근거 / 출처

## SAFE:SEARCH에 반영할 내용

## 추가 확인 필요 사항
```

조사자료는 가능하면 출처를 함께 기록해주세요.

---

# 🔄 GitHub에 자료 올리는 방법

## 1. 작업 시작 전 최신 코드 받기

```bash
git checkout main
git pull origin main
```

## 2. 자기 작업 브랜치 생성

문서 작업:

```bash
git checkout -b docs/작업이름
```

예:

```bash
git checkout -b docs/market-analysis
git checkout -b docs/victim-psychology
git checkout -b docs/crime-scenario
```

디자인 작업:

```bash
git checkout -b design/작업이름
```

예:

```bash
git checkout -b design/admin-screen
```

개발 작업:

```bash
git checkout -b feature/작업이름
```

예:

```bash
git checkout -b feature/safe-query
git checkout -b feature/risk-analysis
```

오류 수정:

```bash
git checkout -b fix/작업이름
```

## 3. 자신의 Workspace에 파일 추가

예:

```text
docs/operations/market/reports/
docs/ai-planning/psychology/research/
docs/ai-planning/crime-scenario/
design/screenshots/
```

## 4. 변경사항 확인

```bash
git status
```

## 5. 변경사항 등록

전체 변경사항:

```bash
git add .
```

특정 파일만:

```bash
git add docs/ai-planning/crime-scenario/scenario.md
```

## 6. Commit

Commit 형식:

```text
feat: 새로운 기능
fix: 오류 수정
docs: 문서 추가 또는 수정
design: UI/UX 변경
refactor: 코드 구조 개선
test: 테스트 추가
chore: 설정 및 기타 작업
```

예:

```bash
git commit -m "docs: add market analysis report"
git commit -m "docs: add victim psychology research"
git commit -m "design: add admin review screen"
git commit -m "feat: add safe query API"
```

## 7. GitHub에 Push

처음 올리는 브랜치:

```bash
git push -u origin 브랜치이름
```

예:

```bash
git push -u origin docs/market-analysis
```

같은 브랜치에서 이후 작업:

```bash
git push
```

## 8. Pull Request 생성

```text
내 작업 브랜치
    ↓
Pull Request
    ↓
팀원 또는 개발 PM 확인
    ↓
main merge
```

PR 제목 예:

```text
[Docs] 시장 분석 보고서 추가
[Docs] 디지털 범죄 시나리오 추가
[Design] 관리자 검토 화면 추가
[Feature] 안전 검색어 추천 기능 구현
```

PR 설명 예:

```text
## 작업 내용

- 유사 서비스 조사 추가
- 시장 분석 자료 추가
- 서비스 차별성 정리

## 확인이 필요한 부분

- 공공기관 관련 통계 추가 확인 필요

## 관련 폴더

- docs/operations/market/
```

---

# 🚫 main 브랜치 직접 작업 금지

가능하면 `main` 브랜치에서 직접 파일을 수정하거나 Push하지 않습니다.

기본 작업 흐름:

```text
main 최신화
    ↓
개인 작업 브랜치 생성
    ↓
작업
    ↓
Commit
    ↓
Push
    ↓
Pull Request
    ↓
Review
    ↓
Merge
```

---

# 🔐 Security Rules

## API Key 업로드 금지

다음 정보는 절대 GitHub에 Commit하지 않습니다.

```text
OpenAI API Key
Database Password
Supabase Secret
JWT Secret
기타 서비스 Secret
```

환경변수는 `.env`를 사용합니다.

예:

```env
OPENAI_API_KEY=실제키
DATABASE_URL=실제DB주소
JWT_SECRET=실제시크릿
```

실제 `.env`는 Git에 올리지 않습니다.

저장소에는 값이 비어있는 `.env.example`만 공유합니다.

```env
OPENAI_API_KEY=
DATABASE_URL=
JWT_SECRET=
```

---

# 🔒 개인정보 및 데이터 업로드 규칙

다음 자료는 GitHub에 업로드하지 않습니다.

- 실제 피해자의 이름
- 실제 전화번호
- 주민등록번호
- 실제 계정 정보
- 비밀번호
- 실제 피해자의 비공개 대화
- 실제 피해자의 사진 및 영상
- 동의 없이 수집한 개인정보
- 공개가 허용되지 않은 교수님 또는 외부인의 개인정보

AI 테스트에는 다음 자료를 사용합니다.

- 가상 데이터
- 비식별화 데이터
- 공개된 공식 자료

---

# 📚 외부 자료 업로드 주의

논문, 기사, 외부 보고서 등은 저작권 및 이용조건을 확인합니다.

가능하면 원문 파일 전체를 저장소에 그대로 업로드하기보다 다음 내용을 Markdown으로 정리하는 방식을 우선합니다.

```text
출처
링크
핵심 내용
SAFE:SEARCH 반영점
```

팀에서 직접 작성한 조사 보고서나 정리자료는 담당 Workspace에 보관할 수 있습니다.

---

# 🖼 이미지 / 디자인 자료

UI 캡처:

```text
design/screenshots/
```

UI 설계:

```text
design/ui/
```

UX:

```text
design/ux/
```

색상:

```text
design/color-system/
```

정보 위계:

```text
design/information-hierarchy/
```

서비스 구조도:

```text
design/diagrams/
```

발표용 이미지:

```text
docs/presentation/images/
```

---

# 🎬 영상 및 대용량 파일

영상 원본처럼 용량이 큰 파일은 GitHub 저장소에 바로 업로드하지 않습니다.

예:

```text
.mp4
.mov
.psd
대용량 원본 디자인 파일
```

대용량 자료는 필요 시 별도 저장공간을 사용하고, GitHub에는 다음 정도만 보관합니다.

```text
영상 기획안
대본
스토리보드
썸네일
최종 영상 위치
```

---

# 🤔 어디에 올릴지 모르겠다면

아래 기준으로 판단합니다.

```text
코드인가?
→ frontend / backend / ai

개발 설명이나 시스템 구조인가?
→ docs/development

피해자 심리인가?
→ docs/ai-planning/psychology

범죄 시나리오인가?
→ docs/ai-planning/crime-scenario

범죄 유형 / 신고 / 증거보존 / Human Review 기준인가?
→ docs/ai-planning/legal

시장 / 사업화 / 유사 서비스인가?
→ docs/operations/market

경찰청 / KISA / 공공기관 운영인가?
→ docs/operations/public-operation

UI / UX 디자인인가?
→ design

팀 소개 영상이나 콘텐츠인가?
→ docs/operations/content

교수님께 실제로 보여드릴 질문인가?
→ docs/professor-materials

발표용인가?
→ docs/presentation

7/29 기준 정리된 결과물인가?
→ 각 팀의 deliverables-0729
```

그래도 애매하면 임의로 새 폴더를 만들기 전에 개발 PM에게 확인해주세요.

---

# ⚠️ Git 사용 시 주의

Git이 익숙하지 않은 팀원은 아래 명령을 임의로 사용하지 않습니다.

```text
git push --force
git reset --hard
git rebase
```

충돌이나 오류가 발생하면 파일을 삭제하거나 저장소를 다시 Clone하기 전에 개발 PM에게 먼저 확인해주세요.

Git에서 발생한 대부분의 실수는 복구할 수 있습니다.

---

# ✅ 기본 작업 흐름 요약

```text
1. git checkout main
2. git pull origin main
3. git checkout -b 내브랜치
4. 파일 작업
5. git status
6. git add .
7. git commit
8. git push
9. Pull Request
10. Review / Merge
```

---

# 🛡 Project Principles

SAFE:SEARCH는 다음 원칙을 기준으로 개발합니다.

1. **AI가 최종 법적 판단을 하지 않는다.**
2. **긴급하거나 불확실한 상황은 사람 또는 관계기관으로 연결한다.**
3. **공식적이고 검증 가능한 기관 정보를 우선한다.**
4. **피해자의 개인정보와 민감정보를 최소한으로 처리한다.**
5. **AI의 신뢰도가 낮은 경우 이를 숨기지 않는다.**
6. **피해자에게 추가적인 위험을 유발할 수 있는 검색어를 그대로 제공하지 않는다.**
7. **Human-in-the-Loop를 핵심 안전장치로 설계한다.**

---

# 📌 Status

🚧 SAFE:SEARCH is currently under active development.

프로젝트 구조, AI Pipeline, 기술 스택 및 운영 기준은 프로토타입 개발과 전문가 자문 결과에 따라 변경될 수 있습니다.
