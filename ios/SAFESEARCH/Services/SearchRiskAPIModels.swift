import Foundation

struct SearchRiskRequestDTO: Encodable {
    let title: String
    let snippet: String
    let url: String
}

struct SearchRiskResponseDTO: Decodable {
    let isClickbait: Bool
    let riskLevel: SearchRiskLevel
    let riskTypes: [SearchRiskType]
    let confidence: Double
    let riskSignals: [String]
    let explanation: String
    let requiresHumanReview: Bool
    let clickbaitProbability: Double
    let clickbaitModel: String
    let clickbaitDecisionSource: ClickbaitDecisionSource

    func toDomain() -> SearchRiskResult {
        SearchRiskResult(
            isClickbait: isClickbait,
            riskLevel: riskLevel,
            riskTypes: riskTypes,
            ruleConfidence: confidence,
            riskSignals: riskSignals,
            explanation: explanation,
            requiresHumanReview: requiresHumanReview,
            clickbaitProbability: clickbaitProbability,
            clickbaitModel: clickbaitModel,
            clickbaitDecisionSource: clickbaitDecisionSource
        )
    }
}
