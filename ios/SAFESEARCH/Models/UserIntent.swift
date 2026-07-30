import Foundation

enum UserIntent: String, Codable, CaseIterable, Identifiable {
    case information, emotionalSupport = "emotional_support", reporting, evidence
    case emergency, legalQuestion = "legal_question", institution
    case secondaryDamage = "secondary_damage", unknown

    var id: String { rawValue }
}

