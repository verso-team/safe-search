# Contributing to SAFE:SEARCH

Git/GitHub가 처음인 팀원을 위한 최소 협업 가이드입니다.

## 가장 중요한 규칙
1. `main`에서 직접 작업하지 않습니다.
2. 작업 전에 최신 `main`을 받습니다.
3. 내 브랜치를 만들고 작업합니다.
4. 작업 후 Pull Request를 만듭니다.

## 처음 한 번
```bash
git clone https://github.com/verso-team/safe-search.git
cd safe-search
```

## 매번 작업 시작
```bash
git checkout main
git pull origin main
git checkout -b 브랜치이름
```

브랜치 예시:
```text
feature/safe-query
feature/admin-review
docs/crime-scenario
docs/psychology-review
design/result-screen
fix/input-validation
```

## 작업 후
```bash
git status
git add .
git commit -m "docs: add crime scenario"
git push -u origin 브랜치이름
```

## Commit 규칙
```text
feat: 기능 추가
fix: 버그 수정
docs: 문서 추가/수정
design: UI/UX 변경
refactor: 코드 구조 개선
test: 테스트
chore: 설정/패키지/기타
```

## Pull Request 예시
```md
## 작업 내용
- 보이스피싱 시나리오 3개 추가
- 피해자 입력 예시 추가

## 확인이 필요한 부분
- 긴급도 기준 검토 필요

## 관련 폴더
- docs/ai-planning/crime-scenario/
```

## 절대 올리면 안 되는 것
- API Key
- Database Password
- JWT Secret
- 실제 피해자의 개인정보
- 실제 피해자의 비공개 대화
- 주민등록번호, 전화번호, 계정 비밀번호

`.env`는 Git에 올리지 않습니다. `.env.example`만 공유합니다.

## 위험한 Git 명령
```text
git push --force
git reset --hard
git rebase
```
익숙하지 않다면 사용하지 말고 개발 PM에게 물어보세요.

## 한 줄 요약
```text
main 최신화 → 내 브랜치 → 작업 → commit → push → PR → review → merge
```
