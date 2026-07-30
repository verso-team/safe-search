import SwiftUI

struct SafeQueryChip: View {
    let query: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Label(query, systemImage: "magnifyingglass")
                .font(.subheadline.weight(.medium))
                .multilineTextAlignment(.leading)
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding(12)
        }
        .buttonStyle(.plain)
        .foregroundStyle(.indigo)
        .background(Color.indigo.opacity(0.08), in: RoundedRectangle(cornerRadius: 12))
    }
}

#Preview { SafeQueryChip(query: "사이버범죄 신고 절차", action: {}).padding() }

