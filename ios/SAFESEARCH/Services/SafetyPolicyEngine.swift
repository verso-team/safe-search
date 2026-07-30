import Foundation

struct SafetyPolicyEngine {
    func validate(_ result: SafetyAnalysisResult) -> SafetyAnalysisResult {
        let mustEscalate = result.urgency >= .high || result.confidence < 0.65
        let urgentNotice = result.urgency == .critical
            ? "지금 생명이나 신체가 위험하다면 안전한 장소로 이동하고 112에 연락하세요."
            : result.safetyNotice

        return SafetyAnalysisResult(
            id: result.id,
            primaryIntent: result.primaryIntent,
            secondaryIntents: result.secondaryIntents,
            emotionalState: result.emotionalState,
            urgency: result.urgency,
            confidence: result.confidence,
            suspectedHarmType: result.suspectedHarmType,
            emotionalSupportMessage: result.emotionalSupportMessage,
            situationSummary: result.situationSummary,
            immediateActions: result.immediateActions,
            safeSearchQueries: result.safeSearchQueries,
            recommendedAgencies: result.recommendedAgencies,
            requiresHumanReview: result.requiresHumanReview || mustEscalate,
            safetyNotice: urgentNotice
        )
    }
}

