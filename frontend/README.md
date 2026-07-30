# Frontend

SAFE:SEARCH 사용자 입력, 구조화된 분석 결과, 안전 검색어 및 Human Review
화면을 담당합니다.

## 실행

```bash
npm install
npm run dev
```

개발 서버는 `/api` 요청을 `http://localhost:8000`으로 전달합니다.
다른 API 주소를 사용할 때는 `VITE_API_BASE_URL`을 설정합니다.

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

## 현재 구현

- 피해 상황 입력과 개인정보 최소화 안내
- `POST /api/v1/analyze` 구조화 응답 연결
- 긴급 안내, 정서적 지지, 최대 3개 즉시 행동
- 안전 검색어 및 공식기관 카드
- Human Review 상태
- 모바일 반응형 레이아웃
