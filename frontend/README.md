# Frontend

SAFE:SEARCH 사용자 입력, 구조화된 분석 결과, 안전 검색어 및 Human Review
화면을 담당합니다.

## 현재 상태

`index.html`은 초기 시연을 위해 CSS와 JavaScript를 한 파일에 포함한 레거시
프로토타입입니다. 실행 가능한 참고 자료로 유지하지만 실제 제품 코드와 GitHub
언어 통계에서는 생성된 산출물로 취급합니다.

새 기능은 `src/` 아래 TypeScript 코드로 작성합니다.

## 목표 구조

```text
src/
├─ app/
├─ components/
│  ├─ common/
│  ├─ result/
│  └─ admin/
├─ features/
│  ├─ risk-analysis/
│  ├─ safe-query/
│  ├─ report/
│  └─ human-review/
├─ lib/
└─ types/
```

## 다음 단계

1. Next.js 또는 Vite 기반 TypeScript 실행 환경을 확정합니다.
2. 인라인 스타일을 디자인 토큰과 컴포넌트 스타일로 분리합니다.
3. 인라인 JavaScript 상태를 React 상태와 API 클라이언트로 이전합니다.
4. `POST /api/v1/analyze` 구조화 응답을 결과 컴포넌트에 연결합니다.
