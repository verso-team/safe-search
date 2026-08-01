# iOS ↔ FastAPI 분석 API 계약

## Endpoint

```http
POST /api/v1/analyze
Content-Type: application/json
```

## Request

```json
{
  "text": "피해 상황 설명"
}
```

- 최소 1자
- 최대 5,000자
- 공백만 포함된 입력은 `422`로 거부
- 서버에서 앞뒤 공백을 제거한 뒤 분석

## Response

iOS `AnalyzeResponseDTO`가 기대하는 snake_case 필드:

- `primary_intent`
- `secondary_intents`
- `emotional_state`
- `urgency`
- `confidence`
- `suspected_harm_type`
- `emotional_support_message`
- `situation_summary`
- `immediate_actions`
- `safe_search_queries`
- `recommended_agencies`
- `requires_human_review`
- `safety_notice`

### 행동 가이드

- 최대 3개
- `priority`는 1~3
- 낮은 숫자가 먼저 표시됨

### 공식기관

각 기관은 다음 필드를 제공한다.

- `id`
- `name`
- `role`
- `phone`
- `website`
- `is_official`

`website`는 iOS의 `URL`로 변환 가능한 HTTP 또는 HTTPS 주소여야 한다.

## 검증

```bash
cd backend
python -m pytest
```

실행 중인 서버를 Windows PowerShell에서 확인:

```powershell
.\scripts\smoke-test-ios-api.ps1
```

이 테스트는 실제 AI 성능을 검증하지 않는다. iOS와 백엔드 사이의
구조·유효성·안전 출력 계약이 깨지지 않았는지를 확인한다.
