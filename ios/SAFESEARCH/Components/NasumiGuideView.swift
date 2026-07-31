import SwiftUI

/// SAFE:SEARCH의 AI 안내 페르소나.
/// 실제 전문가와 혼동되지 않도록 화면에서 항상 "AI 안전 가이드" 역할을 표시한다.
struct GuardianTigerGuideView: View {
    let message: String

    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Image("GuardianTiger")
                .resizable()
                .scaledToFill()
                .frame(width: 54, height: 54)
                .clipShape(Circle())
                .overlay(Circle().stroke(Color.indigo.opacity(0.12), lineWidth: 1))
                .accessibilityHidden(true)

            VStack(alignment: .leading, spacing: 5) {
                Text("가디 · AI 안전 가이드")
                    .font(.caption.bold())
                    .foregroundStyle(.indigo)
                Text(message)
                    .font(.body.weight(.medium))
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
        }
        .padding(16)
        .background(Color.indigo.opacity(0.07), in: RoundedRectangle(cornerRadius: 18))
        .accessibilityElement(children: .combine)
        .accessibilityLabel("가디, AI 안전 가이드. \(message)")
    }
}

/// 기존 호출부 호환용. 후속 리팩터링에서 제거할 수 있다.
typealias NasumiGuideView = GuardianTigerGuideView

#Preview {
    GuardianTigerGuideView(message: "필요한 것부터 안전하게 확인해볼게.")
        .padding()
}
