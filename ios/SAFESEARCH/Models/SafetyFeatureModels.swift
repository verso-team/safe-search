import Foundation

enum ArtifactKind: String, CaseIterable, Identifiable, Codable {
    case message
    case link
    case phone

    var id: String { rawValue }

    var displayName: String {
        switch self {
        case .message: "문자"
        case .link: "링크"
        case .phone: "전화번호"
        }
    }

    var systemImage: String {
        switch self {
        case .message: "message.fill"
        case .link: "link"
        case .phone: "phone.fill"
        }
    }
}

enum RiskBand: Int, Comparable, Codable {
    case low = 0
    case caution = 1
    case high = 2
    case critical = 3

    static func < (lhs: RiskBand, rhs: RiskBand) -> Bool {
        lhs.rawValue < rhs.rawValue
    }

    var displayName: String {
        switch self {
        case .low: "뚜렷한 고위험 신호 적음"
        case .caution: "주의 필요"
        case .high: "위험 신호 높음"
        case .critical: "즉시 안전 확인 필요"
        }
    }
}

struct ArtifactRiskResult: Identifiable {
    let id = UUID()
    let risk: RiskBand
    let title: String
    let summary: String
    let reasons: [String]
    let recommendedActions: [String]
    let safeQueries: [String]
}

struct SafetyContact: Codable, Equatable {
    var name: String = ""
    var phone: String = ""

    var isConfigured: Bool {
        !name.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty &&
        !phone.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
    }
}

struct SafeJourneySession: Identifiable, Codable, Equatable {
    let id: UUID
    let destination: String
    let startedAt: Date
    let expectedArrivalAt: Date
    let startCoordinate: String?

    init(
        id: UUID = UUID(),
        destination: String,
        startedAt: Date = .now,
        expectedArrivalAt: Date,
        startCoordinate: String?
    ) {
        self.id = id
        self.destination = destination
        self.startedAt = startedAt
        self.expectedArrivalAt = expectedArrivalAt
        self.startCoordinate = startCoordinate
    }
}

enum EvidenceKind: String, CaseIterable, Identifiable, Codable {
    case note
    case message
    case link
    case phone
    case account

    var id: String { rawValue }

    var displayName: String {
        switch self {
        case .note: "메모"
        case .message: "문자/대화"
        case .link: "링크"
        case .phone: "전화번호"
        case .account: "계정 정보"
        }
    }
}

struct EvidenceRecord: Identifiable, Codable, Equatable {
    let id: UUID
    let kind: EvidenceKind
    let title: String
    let content: String
    let createdAt: Date
    let coordinate: String?

    init(
        id: UUID = UUID(),
        kind: EvidenceKind,
        title: String,
        content: String,
        createdAt: Date = .now,
        coordinate: String? = nil
    ) {
        self.id = id
        self.kind = kind
        self.title = title
        self.content = content
        self.createdAt = createdAt
        self.coordinate = coordinate
    }
}
