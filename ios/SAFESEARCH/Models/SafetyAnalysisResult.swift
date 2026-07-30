import Foundation

struct SafetyAnalysisResult: Identifiable, Codable {
    let id: UUID
    let primaryIntent: UserIntent
    let secondaryIntents: [UserIntent]
    let emotionalState: EmotionalState
    let urgency: UrgencyLevel
    let confidence: Double
    let suspectedHarmType: String
    let emotionalSupportMessage: String
    let situationSummary: String
    let immediateActions: [ActionItem]
    let safeSearchQueries: [String]
    let recommendedAgencies: [Agency]
    let requiresHumanReview: Bool
    let safetyNotice: String?

    init(
        id: UUID = UUID(),
        primaryIntent: UserIntent,
        secondaryIntents: [UserIntent],
        emotionalState: EmotionalState,
        urgency: UrgencyLevel,
        confidence: Double,
        suspectedHarmType: String,
        emotionalSupportMessage: String,
        situationSummary: String,
        immediateActions: [ActionItem],
        safeSearchQueries: [String],
        recommendedAgencies: [Agency],
        requiresHumanReview: Bool,
        safetyNotice: String?
    ) {
        self.id = id
        self.primaryIntent = primaryIntent
        self.secondaryIntents = secondaryIntents
        self.emotionalState = emotionalState
        self.urgency = urgency
        self.confidence = min(max(confidence, 0), 1)
        self.suspectedHarmType = suspectedHarmType
        self.emotionalSupportMessage = emotionalSupportMessage
        self.situationSummary = situationSummary
        self.immediateActions = Array(immediateActions.sorted { $0.priority < $1.priority }.prefix(3))
        self.safeSearchQueries = safeSearchQueries
        self.recommendedAgencies = recommendedAgencies.filter(\.isOfficial)
        self.requiresHumanReview = requiresHumanReview
        self.safetyNotice = safetyNotice
    }
}

