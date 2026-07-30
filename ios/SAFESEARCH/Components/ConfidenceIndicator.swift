import SwiftUI

struct ConfidenceIndicator: View {
    let confidence: Double

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack {
                Text("분석 신뢰도")
                Spacer()
                Text(confidence, format: .percent.precision(.fractionLength(0))).bold()
            }
            .font(.subheadline)
            ProgressView(value: confidence).tint(.indigo)
            Text("신뢰도가 낮거나 상황이 긴급하면 전문가 검토로 연결합니다.")
                .font(.caption).foregroundStyle(.secondary)
        }
    }
}

#Preview { ConfidenceIndicator(confidence: 0.87).padding() }

