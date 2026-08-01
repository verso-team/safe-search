import Foundation

struct AnalyzeRequestDTO: Encodable {
    let text: String
}

struct AnalyzeResponseDTO: Decodable {
    let primaryIntent: UserIntent
    let secondaryIntents: [UserIntent]
    let emotionalState: EmotionalState
    let urgency: UrgencyLevel
    let confidence: Double
    let suspectedHarmType: String
    let emotionalSupportMessage: String
    let situationSummary: String
    let immediateActions: [ActionItemDTO]
    let safeSearchQueries: [String]
    let recommendedAgencies: [AgencyDTO]
    let requiresHumanReview: Bool
    let safetyNotice: String?

    func toDomain() throws -> SafetyAnalysisResult {
        SafetyAnalysisResult(
            primaryIntent: primaryIntent,
            secondaryIntents: secondaryIntents,
            emotionalState: emotionalState,
            urgency: urgency,
            confidence: confidence,
            suspectedHarmType: suspectedHarmType,
            emotionalSupportMessage: emotionalSupportMessage,
            situationSummary: situationSummary,
            immediateActions: immediateActions.map {
                ActionItem(
                    title: $0.title,
                    detail: $0.detail,
                    priority: $0.priority
                )
            },
            safeSearchQueries: safeSearchQueries,
            recommendedAgencies: try recommendedAgencies.map { try $0.toDomain() },
            requiresHumanReview: requiresHumanReview,
            safetyNotice: safetyNotice
        )
    }
}

struct ActionItemDTO: Decodable {
    let title: String
    let detail: String
    let priority: Int
}

struct AgencyDTO: Decodable {
    let id: String
    let name: String
    let role: String
    let phone: String?
    let website: String
    let isOfficial: Bool

    func toDomain() throws -> Agency {
        guard let websiteURL = URL(string: website),
              let scheme = websiteURL.scheme,
              ["http", "https"].contains(scheme.lowercased()) else {
            throw AnalysisAPIError.invalidAgencyWebsite
        }

        return Agency(
            id: id,
            name: name,
            role: role,
            phone: phone,
            website: websiteURL,
            isOfficial: isOfficial
        )
    }
}
