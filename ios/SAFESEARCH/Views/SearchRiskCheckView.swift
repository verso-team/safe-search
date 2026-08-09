import SwiftUI

struct SearchRiskCheckView: View {
    @State private var title = ""
    @State private var snippet = ""
    @State private var url = ""

    @State private var result: SearchRiskResult?
    @State private var isLoading = false
    @State private var errorMessage: String?

    private let service = SearchRiskService()

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                GuardianTigerGuideView(
                    message: (
                        "검색결과의 클릭베이트·기관 사칭·금전 유도 "
                        + "신호를 확인해볼게. 결과만으로 범죄 여부를 "
                        + "확정하지는 않아."
                    )
                )

                inputCard

                if isLoading {
                    HStack(spacing: 10) {
                        ProgressView()
                        Text("검색결과 위험 신호를 확인하고 있어요.")
                            .font(.subheadline)
                    }
                    .frame(
                        maxWidth: .infinity,
                        alignment: .leading
                    )
                    .padding()
                }

                if let errorMessage {
                    errorCard(errorMessage)
                }

                if let result {
                    resultCard(result)
                }
            }
            .padding()
        }
        .background(
            Color(
                red: 0.96,
                green: 0.98,
                blue: 1.0
            )
        )
        .navigationTitle("검색결과 위험 확인")
    }

    private var inputCard: some View {
        VStack(alignment: .leading, spacing: 12) {
            Label(
                "검색결과 입력",
                systemImage: "magnifyingglass"
            )
            .font(.title3.bold())

            TextField(
                "제목",
                text: $title,
                axis: .vertical
            )
            .textFieldStyle(.roundedBorder)

            TextField(
                "검색결과 설명 또는 미리보기",
                text: $snippet,
                axis: .vertical
            )
            .lineLimit(3...6)
            .textFieldStyle(.roundedBorder)

            TextField(
                "https://example.com/...",
                text: $url
            )
            .textInputAutocapitalization(.never)
            .autocorrectionDisabled()
            .textFieldStyle(.roundedBorder)

            Button {
                Task {
                    await analyze()
                }
            } label: {
                Label(
                    "위험 신호 분석",
                    systemImage: "shield.checkered"
                )
                .font(.headline)
                .frame(maxWidth: .infinity)
                .padding()
            }
            .buttonStyle(.borderedProminent)
            .tint(.indigo)
            .disabled(isLoading)
        }
        .padding(18)
        .background(
            .background,
            in: RoundedRectangle(cornerRadius: 20)
        )
    }

    @ViewBuilder
    private func resultCard(
        _ result: SearchRiskResult
    ) -> some View {
        VStack(alignment: .leading, spacing: 18) {
            VStack(alignment: .leading, spacing: 8) {
                Text(result.riskLevel.displayName)
                    .font(.caption.bold())
                    .foregroundStyle(
                        riskColor(result.riskLevel)
                    )
                    .padding(.horizontal, 10)
                    .padding(.vertical, 5)
                    .background(
                        riskColor(result.riskLevel)
                            .opacity(0.10),
                        in: Capsule()
                    )

                Text(
                    result.isClickbait
                    ? "클릭베이트 신호가 확인됐어요"
                    : "뚜렷한 클릭베이트 신호는 적어요"
                )
                .font(.title3.bold())

                Text(result.explanation)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
            }
            .padding(16)
            .frame(
                maxWidth: .infinity,
                alignment: .leading
            )
            .background(
                .background,
                in: RoundedRectangle(cornerRadius: 18)
            )

            if !result.riskTypes.isEmpty {
                VStack(alignment: .leading, spacing: 9) {
                    Text("확인된 위험 유형")
                        .font(.headline)

                    ForEach(result.riskTypes) { type in
                        Label(
                            type.displayName,
                            systemImage: "exclamationmark.shield"
                        )
                        .font(.subheadline)
                    }
                }
            }

            if !result.riskSignals.isEmpty {
                VStack(alignment: .leading, spacing: 9) {
                    Text("탐지 근거")
                        .font(.headline)

                    ForEach(
                        result.riskSignals,
                        id: \.self
                    ) { signal in
                        Label(
                            signal,
                            systemImage: "circle.fill"
                        )
                        .font(.subheadline)
                        .symbolRenderingMode(
                            .hierarchical
                        )
                    }
                }
            }

            modelEvidenceCard(result)

            HumanReviewView(
                isRequired: result.requiresHumanReview
            )

            NavigationLink {
                SupportHubView()
            } label: {
                Label(
                    "공식기관 확인",
                    systemImage: "building.columns.fill"
                )
                .frame(maxWidth: .infinity)
            }
            .buttonStyle(.bordered)
        }
    }

    private func modelEvidenceCard(
        _ result: SearchRiskResult
    ) -> some View {
        VStack(alignment: .leading, spacing: 8) {
            Label(
                "AI 탐지 근거",
                systemImage: "waveform.path.ecg"
            )
            .font(.headline)

            HStack {
                Text("판단 출처")
                    .foregroundStyle(.secondary)

                Spacer()

                Text(
                    result.clickbaitDecisionSource
                        .displayName
                )
                .fontWeight(.semibold)
            }

            HStack {
                Text("클릭베이트 모델 점수")
                    .foregroundStyle(.secondary)

                Spacer()

                Text(
                    "\(Int(result.clickbaitProbability * 100))%"
                )
                .fontWeight(.semibold)
            }

            Text(
                "이 점수는 클릭베이트 분류 모델의 출력이며 "
                + "범죄·사기·불법성의 확률을 의미하지 않습니다."
            )
            .font(.caption)
            .foregroundStyle(.secondary)

            Text(
                "model: \(result.clickbaitModel)"
            )
            .font(.caption2.monospaced())
            .foregroundStyle(.secondary)
        }
        .padding(16)
        .background(
            Color.indigo.opacity(0.06),
            in: RoundedRectangle(cornerRadius: 18)
        )
    }

    private func errorCard(
        _ message: String
    ) -> some View {
        Label(
            message,
            systemImage: "wifi.exclamationmark"
        )
        .font(.subheadline)
        .foregroundStyle(.red)
        .padding(16)
        .frame(
            maxWidth: .infinity,
            alignment: .leading
        )
        .background(
            Color.red.opacity(0.08),
            in: RoundedRectangle(cornerRadius: 18)
        )
    }

    @MainActor
    private func analyze() async {
        isLoading = true
        errorMessage = nil
        result = nil

        defer {
            isLoading = false
        }

        do {
            result = try await service.analyze(
                title: title,
                snippet: snippet,
                url: url
            )
        } catch {
            errorMessage = (
                error as? LocalizedError
            )?.errorDescription
                ?? "검색결과 위험 분석에 실패했습니다."
        }
    }

    private func riskColor(
        _ level: SearchRiskLevel
    ) -> Color {
        switch level {
        case .low:
            .green
        case .medium:
            .orange
        case .high:
            .red
        }
    }
}

#Preview {
    NavigationStack {
        SearchRiskCheckView()
    }
}
