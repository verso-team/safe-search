import Foundation

@MainActor
final class SafetyContactStore: ObservableObject {
    @Published var contact: SafetyContact {
        didSet { save() }
    }

    private let defaults: UserDefaults
    private let key = "safe-search.primary-safety-contact"

    init(defaults: UserDefaults = .standard) {
        self.defaults = defaults
        if let data = defaults.data(forKey: key),
           let saved = try? JSONDecoder().decode(SafetyContact.self, from: data) {
            contact = saved
        } else {
            contact = SafetyContact()
        }
    }

    private func save() {
        guard let data = try? JSONEncoder().encode(contact) else { return }
        defaults.set(data, forKey: key)
    }
}
