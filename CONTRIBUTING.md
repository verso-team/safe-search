# Contributing to SAFE:SEARCH

Team Verso의 협업 규칙입니다.

## 1. 작업 시작

1. 담당 작업에 대한 GitHub Issue를 생성합니다.
2. 담당자, 마감일, 관련 폴더, 완료 조건을 작성합니다.
3. `develop` 브랜치에서 새 브랜치를 생성합니다.

```bash
git checkout develop
git pull origin develop
git checkout -b feature/example
```

## 2. 담당 폴더

- 개발팀: `frontend/`, `backend/`, `ai/`, `data/`, `scripts/`
- AI 기획팀: `docs/scenario/`, `docs/psychology/`, `docs/legal/`
- 운영팀: `research/`, `design/`, `docs/presentation/`, `docs/professor-materials/`

다른 팀 폴더를 수정할 때는 해당 담당자와 먼저 공유합니다.

## 3. 커밋 메시지

```text
feat: 기능 추가
fix: 오류 수정
docs: 문서 수정
design: 디자인 수정
data: 데이터 작업
test: 테스트 작업
refactor: 코드 구조 개선
chore: 환경·설정 작업
```

## 4. Pull Request

Pull Request에는 아래 내용을 포함합니다.

- 작업 목적
- 주요 변경 내용
- 확인 방법
- 화면 캡처 또는 결과 예시
- 남아 있는 문제
- 관련 Issue

`main`으로 직접 Push하지 않습니다. 일반 작업은 `develop`에 병합하고, 검증된 버전만 `main`에 병합합니다.

## 5. 문서 작성 원칙

- 확정된 내용과 검토 중인 내용을 구분합니다.
- 출처가 있는 내용은 기관명과 자료명을 기록합니다.
- 피해자 비난, 과도한 공포 유발, 법률적 단정 표현을 피합니다.
- 교수님 자문 반영 사항은 변경 전·후를 기록합니다.

## 6. 데이터 및 개인정보

- 실제 피해자의 개인정보를 저장하지 않습니다.
- 이름, 전화번호, 계좌번호 등은 가상 정보만 사용합니다.
- API 키와 비밀번호를 Git에 올리지 않습니다.
- 원천 데이터의 이용 조건과 출처를 기록합니다.
