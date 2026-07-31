import Foundation

@MainActor
final class SafeJourneyStore: ObservableObject {
    @Published private(set) var session: SafeJourneySession? {
        didSet { persist() }
    }

    private let defaults: UserDefaults
    private let key = "safe-search.active-safe-journey"

    init(defaults: UserDefaults = .standard) {
        self.defaults = defaults
        if let data = defaults.data(forKey: key),
           let saved = try? JSONDecoder().decode(SafeJourneySession.self, from: data),
           saved.expectedArrivalAt > .now.addingTimeInterval(-3_600) {
            session = saved
        }
    }

    func start(destination: String, durationMinutes: Int, startCoordinate: String?) {
        let now = Date.now
        let newSession = SafeJourneySession(
            destination: destination,
            startedAt: now,
            expectedArrivalAt: now.addingTimeInterval(TimeInterval(durationMinutes * 60)),
            startCoordinate: startCoordinate
        )
        session = newSession

        Task {
            await SafetyNotificationService.scheduleJourneyReminder(session: newSession)
        }
    }

    func finish() {
        guard let session else { return }
        SafetyNotificationService.cancelJourneyReminder(sessionID: session.id)
        self.session = nil
    }

    func remainingSeconds(at date: Date = .now) -> TimeInterval {
        guard let session else { return 0 }
        return max(0, session.expectedArrivalAt.timeIntervalSince(date))
    }

    private func persist() {
        guard let session else {
            defaults.removeObject(forKey: key)
            return
        }
        if let data = try? JSONEncoder().encode(session) {
            defaults.set(data, forKey: key)
        }
    }
}
