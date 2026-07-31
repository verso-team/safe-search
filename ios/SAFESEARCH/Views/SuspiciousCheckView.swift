import SwiftUI

struct SuspiciousCheckView: View {
    let kind: ArtifactKind
    @State private var input: String
    @State private var result: ArtifactRiskResult?

    @EnvironmentObject private var evidenceStore: EvidenceStore
    @EnvironmentObject private var locationService: LocationSafetyService

    private let analyzer = SuspiciousArtifactAnalyzer()

    init(kind: ArtifactKind, initialText: String = "") {
        self.kind = kind
        _input = State(initialValue: initialText)
    }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                GuardianTigerGuideView(message: "\(kind.displayName)만 보고 범죄를 확정하지는 않아. 의심 패턴을 찾고, 공식 확인 방법을 먼저 안내할게.")

                VStack(alignment: .leading, spacing: 12) {
                    Label("\(kind.displayName) 확인", systemImage: kind.systemImage)
                        .font(.title3.bold())
                    TextField(placeholder, text: $input, axis: .vertical)
                        .lineLimit(5...10)
                        .textFieldStyle(.roundedBorder)

                    Button {
                        result = analyzer.analyze(kind: kind, text: input)
                    } label: {
                        Label("위험 신호 확인", systemImage: "shield.checkered")
                            .font(.headline).frame(maxWidth: .infinity).padding()
                    }
                    .buttonStyle(.borderedProminent)
                    .tint(.indigo)
                }
                .padding(18)
                .background(.background, in: RoundedRectangle(cornerRadius: 20))

                if let result {
                    resultView(result)
                }
            }
            .padding()
        }
        .background(Color(red: 0.96, green: 0.98, blue: 1.0))
        .navigationTitle("\(kind.displayName) 위험 확인")
    }

    private var placeholder: String {
        switch kind {
        case .message: "받은 문자나 통화 내용을 붙여넣어줘"
        case .link: "https://example.com/..."
        case .phone: "전화번호와 상대가 말한 소속·요구사항을 같이 적어줘"
        }
    }

    @ViewBuilder
    private func resultView(_ result: ArtifactRiskResult) -> some View {
        VStack(alignment: .leading, spacing: 16) {
            VStack(alignment: .leading, spacing: 8) {
                Text(result.risk.displayName)
                    .font(.caption.bold())
                    .foregroundStyle(riskColor(result.risk))
                    .padding(.horizontal, 9).padding(.vertical, 5)
                    .background(riskColor(result.risk).opacity(0.10), in: Capsule())
                Text(result.title).font(.title3.bold())
                Text(result.summary).font(.subheadline).foregroundStyle(.secondary)
            }
            .padding(16)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(.background, in: RoundedRectangle(cornerRadius: 18))

            VStack(alignment: .leading, spacing: 8) {
                Text("확인된 신호").font(.headline)
                ForEach(result.reasons, id: \.self) { reason in
                    Label(reason, systemImage: "circle.fill")
                        .font(.subheadline)
                        .symbolRenderingMode(.hierarchical)
                }
            }

            VStack(alignment: .leading, spacing: 8) {
                Text("지금 먼저 해줘").font(.headline)
                ForEach(Array(result.recommendedActions.enumerated()), id: \.offset) { index, action in
                    HStack(alignment: .top, spacing: 10) {
                        Text("\(index + 1)")
                            .font(.caption.bold()).foregroundStyle(.white)
                            .frame(width: 24, height: 24)
                            .background(.indigo, in: Circle())
                        Text(action).font(.subheadline)
                    }
                }
            }

            VStack(alignment: .leading, spacing: 8) {
                Text("Safe Query").font(.headline)
                SafeQueryView(queries: result.safeQueries)
            }

            Button {
                evidenceStore.add(
                    kind: evidenceKind,
                    title: "의심 \(kind.displayName) 보존",
                    content: input,
                    coordinate: locationService.coordinateText
                )
            } label: {
                Label("이 내용을 증거 보존함에 저장", systemImage: "externaldrive.badge.checkmark")
                    .frame(maxWidth: .infinity)
            }
            .buttonStyle(.bordered)

            NavigationLink { SupportHubView() } label: {
                Label("공식기관 확인", systemImage: "building.columns.fill")
                    .frame(maxWidth: .infinity)
            }
            .buttonStyle(.bordered)
        }
    }

    private var evidenceKind: EvidenceKind {
        switch kind {
        case .message: .message
        case .link: .link
        case .phone: .phone
        }
    }

    private func riskColor(_ risk: RiskBand) -> Color {
        switch risk {
        case .low: .green
        case .caution: .orange
        case .high, .critical: .red
        }
    }
}
