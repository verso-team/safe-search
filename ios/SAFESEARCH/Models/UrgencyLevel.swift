import SwiftUI

enum UrgencyLevel: String, Codable, CaseIterable, Comparable {
    case low, medium, high, critical

    private var rank: Int {
        switch self {
        case .low: 0
        case .medium: 1
        case .high: 2
        case .critical: 3
        }
    }

    static func < (lhs: Self, rhs: Self) -> Bool { lhs.rank < rhs.rank }

    var displayName: String {
        switch self {
        case .low: "낮음"
        case .medium: "주의"
        case .high: "높음"
        case .critical: "긴급"
        }
    }

    var tint: Color {
        switch self {
        case .low: .green
        case .medium: .orange
        case .high: Color(red: 0.91, green: 0.36, blue: 0.20)
        case .critical: .red
        }
    }
}

