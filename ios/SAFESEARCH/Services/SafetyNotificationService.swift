import Foundation
import UserNotifications

enum SafetyNotificationService {
    static func scheduleJourneyReminder(session: SafeJourneySession) async {
        let center = UNUserNotificationCenter.current()
        let granted = (try? await center.requestAuthorization(options: [.alert, .sound])) ?? false
        guard granted else { return }

        let content = UNMutableNotificationContent()
        content.title = "안심 귀가 확인"
        content.body = "\(session.destination)에 도착했는지 확인해주세요. 아직 이동 중이면 보호자에게 상태를 알려주세요."
        content.sound = .default

        let interval = max(5, session.expectedArrivalAt.timeIntervalSinceNow)
        let trigger = UNTimeIntervalNotificationTrigger(timeInterval: interval, repeats: false)
        let request = UNNotificationRequest(
            identifier: "safe-journey-\(session.id.uuidString)",
            content: content,
            trigger: trigger
        )
        try? await center.add(request)
    }

    static func cancelJourneyReminder(sessionID: UUID) {
        UNUserNotificationCenter.current().removePendingNotificationRequests(
            withIdentifiers: ["safe-journey-\(sessionID.uuidString)"]
        )
    }
}
