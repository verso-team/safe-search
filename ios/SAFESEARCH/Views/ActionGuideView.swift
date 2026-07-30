import SwiftUI

struct ActionGuideView: View {
    let actions: [ActionItem]

    var body: some View {
        VStack(spacing: 10) {
            ForEach(Array(actions.prefix(3).enumerated()), id: \.element.id) { index, action in
                HStack(alignment: .top, spacing: 12) {
                    Text("\(index + 1)").font(.subheadline.bold()).foregroundStyle(.white)
                        .frame(width: 28, height: 28).background(.indigo, in: Circle())
                    VStack(alignment: .leading, spacing: 4) {
                        Text(action.title).font(.headline)
                        Text(action.detail).font(.subheadline).foregroundStyle(.secondary)
                    }
                    Spacer()
                }
                .padding(14)
                .background(.background, in: RoundedRectangle(cornerRadius: 16))
            }
        }
    }
}

#Preview { ActionGuideView(actions: MockSafetyAnalysis.highRisk.immediateActions).padding().background(Color(.systemGroupedBackground)) }

