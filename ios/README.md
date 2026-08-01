# SAFE:SEARCH iOS

SwiftUI로 구현한 AI Safety Guide 프로토타입입니다.

## 현재 연결 구조

```text
사용자 입력
→ iOS `AIAnalysisService`
→ POST `/api/v1/analyze`
→ FastAPI 구조화 응답
→ `SafetyAnalysisResult`
→ 안전 정책 검증
→ 결과 UI
```

iOS는 실제 HTTP API를 호출하지만, 현재 백엔드 분석 로직은 아직
`mock_analysis.py`의 규칙 기반 Mock입니다. 즉 네트워크 계약은 연결됐지만
실제 LLM/ML 모델 연결은 후속 단계입니다.

개발 빌드에서는 서버에 연결할 수 없을 때만 시연용 Mock 결과로 전환하며,
결과의 `safetyNotice`에 Mock 결과임을 명시합니다. Release 빌드에서는
자동 fallback을 사용하지 않습니다.

## 실행

1. Xcode에서 iOS App 프로젝트 `SAFESEARCH`를 생성합니다(iOS 16 이상).
2. 기본으로 생성된 Swift 파일을 삭제하고 `SAFESEARCH/` 아래 폴더를 프로젝트에 추가합니다.
3. `SAFESEARCHApp.swift`를 앱 진입점으로 사용합니다.
4. FastAPI 서버를 실행합니다.
5. Xcode Scheme 환경변수에 API 주소를 설정합니다.

### API 주소 설정

Xcode에서:

`Product → Scheme → Edit Scheme → Run → Arguments → Environment Variables`

아래 값을 추가합니다.

```text
SAFESEARCH_API_URL=http://127.0.0.1:8000
```

Simulator에서는 Mac에서 실행 중인 FastAPI에 `127.0.0.1`로 접근할 수 있습니다.

실제 iPhone에서는 `127.0.0.1`이 iPhone 자신을 뜻하므로 같은 Wi-Fi에 연결된
Mac의 LAN 주소를 사용해야 합니다.

```text
SAFESEARCH_API_URL=http://192.168.x.x:8000
```

## Xcode 권한 설정

`TARGETS → SAFESEARCH → Info`에서 아래 항목을 추가합니다.

```text
Privacy - Location When In Use Usage Description
긴급 SOS와 안심 귀가 기능에서 현재 위치를 확인하기 위해 사용합니다.
```

로컬 HTTP 서버를 사용하는 개발 단계에서는 다음 설정도 검토합니다.

```text
App Transport Security Settings
└─ Allow Local Networking = YES
```

무분별한 `Allow Arbitrary Loads` 사용은 피합니다.

## 구조

- `Models`: 구조화된 분석 결과와 도메인 타입
- `Views`: 입력, 분석 중, 결과 및 각 결과 섹션
- `Components`: 재사용 가능한 작은 UI
- `Services`: HTTP 분석 서비스, 안전 정책, 위치·증거·공식기관 서비스
- `Mock`: Preview 및 네트워크 장애 시 개발 fallback 데이터
