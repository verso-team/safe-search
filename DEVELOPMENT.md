# SAFE:SEARCH 개발 시작 가이드

이 문서는 개발 경험이 적은 팀원도 같은 환경에서 프로젝트를 실행하고 작업 결과를 남길 수 있도록 만든 안내서입니다.

## 가장 쉬운 실행 방법: Docker

### 1. 준비

- Git 설치
- Docker Desktop 설치 및 실행
- 저장소 복제

```bash
git clone https://github.com/verso-team/safe-search.git
cd safe-search
```

### 2. 환경변수 파일 만들기

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

처음 실행할 때는 `.env`에 실제 API 키를 넣지 않아도 됩니다. 실제 키가 들어간 `.env`는 절대 GitHub에 올리지 않습니다.

### 3. 전체 서비스 실행

```bash
docker compose up --build
```

- 화면: http://localhost:3000
- API 상태 확인: http://localhost:8000/health
- API 문서: http://localhost:8000/docs

종료할 때는 실행 중인 터미널에서 `Ctrl+C`를 누릅니다. 컨테이너까지 정리하려면 다음을 실행합니다.

```bash
docker compose down
```

데이터베이스 데이터까지 삭제하는 `docker compose down -v`는 개발 PM과 확인한 뒤 사용합니다.

## 백엔드만 실행하기

Python 3.12가 필요합니다.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
python -m uvicorn app.main:app --app-dir backend --reload
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
python -m uvicorn app.main:app --app-dir backend --reload
```

## 작업 전후 확인

작업을 시작할 때:

```bash
git checkout main
git pull origin main
git checkout -b feature/짧은-작업명
```

코드 작업을 마쳤을 때:

```bash
python -m ruff check backend
python -m pytest
git status
```

문서만 수정했다면 Python 검사는 생략할 수 있습니다. Pull Request를 만들면 GitHub가 백엔드 검사와 Docker 설정 검사를 자동 실행합니다.

## 비전공자 팀원용 안전 체크리스트

- 실제 피해자의 이름, 연락처, 대화, 사진을 테스트에 사용하지 않습니다.
- `.env`와 API 키를 GitHub에 올리지 않습니다.
- `main`에서 직접 작업하지 않습니다.
- 파일을 삭제하거나 새 폴더를 만들기 전 담당 Workspace를 확인합니다.
- `git push --force`, `git reset --hard`, `git rebase`는 사용하지 않습니다.
- 오류가 나면 화면 전체와 실행한 명령을 복사해 이슈 또는 팀 채널에 남깁니다.

## TRAITHON Evidence 기록

대회에서는 결과뿐 아니라 계획, 수행, 확인, 개선의 근거가 중요합니다. PR에는 아래 내용을 남깁니다.

1. 해결하려는 사용자 또는 신뢰성 문제
2. 변경한 내용
3. 실행한 시험과 결과
4. 발견한 위험 또는 한계
5. 인간 검토가 필요한 조건
6. 다음 개선 항목

실제 피해정보 대신 가상·비식별화·공개 데이터를 사용하고, 시험 명령과 결과 파일 위치를 함께 기록합니다.
