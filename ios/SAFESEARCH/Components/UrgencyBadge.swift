import SwiftUI

struct UrgencyBadge: View {
    let urgency: UrgencyLevel

    var body: some View {
        Text(urgency.displayName)
            .font(.caption.bold())
            .foregroundStyle(urgency.tint)
            .padding(.horizontal, 10).padding(.vertical, 6)
            .background(urgency.tint.opacity(0.12), in: Capsule())
            .accessibilityLabel("긴급도 \(urgency.displayName)")
    }
}

#Preview { UrgencyBadge(urgency: .high) }

