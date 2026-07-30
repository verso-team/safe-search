import Foundation

enum EmotionalState: String, Codable, CaseIterable {
    case stable, anxious, confused, fearful, panic
    case highDistress = "high_distress"

    var displayName: String {
        switch self {
        case .stable: "안정"
        case .anxious: "불안"
        case .confused: "혼란"
        case .fearful: "두려움"
        case .panic: "매우 불안"
        case .highDistress: "높은 고통"
        }
    }
}

