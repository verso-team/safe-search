# SAFE:SEARCH iOS

SwiftUI로 구현한 Mock 기반 AI Safety Guide 프로토타입입니다.

## 실행

1. Xcode에서 iOS App 프로젝트 `SAFESEARCH`를 생성합니다(iOS 16 이상).
2. 기본으로 생성된 Swift 파일을 삭제하고 `SAFESEARCH/` 아래 폴더를 프로젝트에 추가합니다.
3. `SAFESEARCHApp.swift`를 앱 진입점으로 사용합니다.

현재 단계는 실제 AI API를 호출하지 않습니다. `MockSafetyAnalysis`와
`SafetyPolicyEngine`으로 전체 UX, 긴급도 우선순위, Human Review 흐름을 검증합니다.

## 구조

- `Models`: 구조화된 분석 결과와 도메인 타입
- `Views`: 입력, 분석 중, 결과 및 각 결과 섹션
- `Components`: 재사용 가능한 작은 UI
- `Services`: 분석 인터페이스, 안전 정책, 공식기관 카탈로그
- `Mock`: Preview 및 시나리오 테스트 데이터

