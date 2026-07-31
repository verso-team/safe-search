import Foundation

@MainActor
final class EvidenceStore: ObservableObject {
    @Published private(set) var records: [EvidenceRecord] = []

    private let fileURL: URL

    init(fileManager: FileManager = .default) {
        let directory = fileManager.urls(for: .documentDirectory, in: .userDomainMask).first!
        fileURL = directory.appendingPathComponent("safe-search-evidence.json")
        load()
    }

    func add(kind: EvidenceKind, title: String, content: String, coordinate: String?) {
        let record = EvidenceRecord(
            kind: kind,
            title: title.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty ? kind.displayName : title,
            content: content,
            coordinate: coordinate
        )
        records.insert(record, at: 0)
        save()
    }

    func delete(_ record: EvidenceRecord) {
        records.removeAll { $0.id == record.id }
        save()
    }

    func exportText() -> String {
        records.map { record in
            var lines = [
                "[\(record.createdAt.formatted(date: .numeric, time: .shortened))] \(record.kind.displayName) - \(record.title)",
                record.content
            ]
            if let coordinate = record.coordinate { lines.append("위치: \(coordinate)") }
            return lines.joined(separator: "\n")
        }
        .joined(separator: "\n\n---\n\n")
    }

    private func load() {
        guard let data = try? Data(contentsOf: fileURL),
              let saved = try? JSONDecoder().decode([EvidenceRecord].self, from: data) else { return }
        records = saved.sorted { $0.createdAt > $1.createdAt }
    }

    private func save() {
        guard let data = try? JSONEncoder().encode(records) else { return }
        try? data.write(to: fileURL, options: [.atomic])
    }
}
