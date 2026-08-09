import Foundation

enum SearchRiskLevel: String, Codable {
    case low
    case medium
    case high

    var displayName: String {
        switch self {
        case .low:
            "뚜렷한 고위험 신호 적음"
        case .medium:
            "주의해서 확인 필요"
        case .high:
            "고위험 신호 확인"
        }
    }
}

enum SearchRiskType: String, Codable, Identifiable {
    case sensational
    case misleading
    case institutionImpersonation = "institution_impersonation"
    case financialLure = "financial_lure"
    case personalInformationRequest = "personal_information_request"

    var id: String { rawValue }

    var displayName: String {
        switch self {
        case .sensational:
            "과장·선정 표현"
        case .misleading:
            "오해 유도 표현"
        case .institutionImpersonation:
            "기관 사칭 위험"
        case .financialLure:
            "금전 유도 위험"
        case .personalInformationRequest:
            "개인정보 요구 위험"
        }
    }
}

enum ClickbaitDecisionSource: String, Codable {
    case none
    case rule
    case ml
    case ruleAndML = "rule+ml"

    var displayName: String {
        switch self {
        case .none:
            "탐지 신호 없음"
        case .rule:
            "규칙 기반"
        case .ml:
            "ML baseline"
        case .ruleAndML:
            "규칙 + ML"
        }
    }
}

struct SearchRiskResult: Identifiable {
    let id = UUID()

    let isClickbait: Bool
    let riskLevel: SearchRiskLevel
    let riskTypes: [SearchRiskType]

    /// 범죄 확률이 아니라 백엔드 규칙 일치 강도다.
    let ruleConfidence: Double

    let riskSignals: [String]
    let explanation: String
    let requiresHumanReview: Bool

    /// 클릭베이트 모델의 binary classification probability다.
    /// 범죄 또는 불법성 확률이 아니다.
    let clickbaitProbability: Double
    let clickbaitModel: String
    let clickbaitDecisionSource: ClickbaitDecisionSource
}
