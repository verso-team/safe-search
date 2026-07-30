import SwiftUI

struct NasumiGuideView: View {
    let message: String

    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            ZStack {
                Circle().fill(Color.indigo.opacity(0.12))
                Text("나").font(.headline).foregroundStyle(.indigo)
            }
            .frame(width: 44, height: 44)
            .accessibilityLabel("나섬이")

            Text(message)
                .font(.body.weight(.medium))
                .lineLimit(3)
                .frame(maxWidth: .infinity, alignment: .leading)
        }
        .padding(16)
        .background(Color.indigo.opacity(0.07), in: RoundedRectangle(cornerRadius: 18))
    }
}

#Preview {
    NasumiGuideView(message: "필요한 것부터 하나씩 확인해볼게요.")
        .padding()
}

