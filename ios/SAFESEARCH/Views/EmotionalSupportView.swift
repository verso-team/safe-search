import SwiftUI

struct EmotionalSupportView: View {
    let message: String
    var body: some View { NasumiGuideView(message: message) }
}

#Preview { EmotionalSupportView(message: MockSafetyAnalysis.highRisk.emotionalSupportMessage).padding() }

