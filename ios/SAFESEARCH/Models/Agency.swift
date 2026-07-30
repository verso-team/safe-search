import Foundation

struct Agency: Identifiable, Codable, Hashable {
    let id: String
    let name: String
    let role: String
    let phone: String?
    let website: URL
    let isOfficial: Bool
}

struct ActionItem: Identifiable, Codable, Hashable {
    let id: UUID
    let title: String
    let detail: String
    let priority: Int

    init(id: UUID = UUID(), title: String, detail: String, priority: Int) {
        self.id = id
        self.title = title
        self.detail = detail
        self.priority = priority
    }
}

