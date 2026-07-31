import SwiftUI

struct AnalysisResultView: View {
    let result: SafetyAnalysisResult

    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 22) {
                GuardianTigerGuideView(message: "지금은 필요한 것부터 순서대로 확인해줘.")

                summaryCard

                section("지금 먼저 해줘") {
                    ActionGuideView(actions: result.immediateActions)
                }

                section("안전하게 검색하기") {
                    VStack(alignment: .leading, spacing: 10) {
                        Label("Safe Query", systemImage: "shield.lefthalf.filled")
                            .font(.caption.bold()).foregroundStyle(.indigo)
                        Text("가디가 검색어를 공식 정보 중심으로 다시 정리했어.")
                            .font(.subheadline).foregroundStyle(.secondary)
                        SafeQueryView(queries: result.safeSearchQueries)
                    }
                }

                section("도움을 받을 수 있는 곳") {
                    AgencyRecommendationView(agencies: result.recommendedAgencies)
                }

                HumanReviewView(isRequired: result.requiresHumanReview)

                if result.urgency >= .high {
                    NavigationLink { EmergencySOSView() } label: {
                        Label("긴급 안전 기능 열기", systemImage: "sos.circle.fill")
                            .font(.headline)
                            .frame(maxWidth: .infinity)
                            .padding()
                    }
                    .buttonStyle(.borderedProminent)
                    .tint(.red)
                }
            }
            .padding()
        }
        .background(Color(red: 0.96, green: 0.98, blue: 1.0))
        .navigationTitle("안전 분석 결과")
        .navigationBarTitleDisplayMode(.inline)
    }

    private var summaryCard: some View {
        VStack(alignment: .leading, spacing: 14) {
            if let notice = result.safetyNotice {
                Label(notice, systemImage: "exclamationmark.triangle.fill")
                    .font(.subheadline.bold())
                    .foregroundStyle(result.urgency.tint)
            }

            HStack(alignment: .top) {
                VStack(alignment: .leading, spacing: 6) {
                    Text("주의 필요")
                        .font(.caption.bold())
                        .foregroundStyle(.orange)
                        .padding(.horizontal, 9).padding(.vertical, 5)
                        .background(Color.orange.opacity(0.10), in: Capsule())
                    Text(result.suspectedHarmType)
                        .font(.title3.bold())
                }
                Spacer()
                UrgencyBadge(urgency: result.urgency)
            }

            Text(result.situationSummary)
                .font(.subheadline).foregroundStyle(.secondary)

            Divider()

            VStack(alignment: .leading, spacing: 8) {
                HStack {
                    Text("분석 신뢰도").font(.subheadline.bold())
                    Spacer()
                    Text(confidenceLabel).font(.subheadline.bold()).foregroundStyle(.indigo)
                }
                ProgressView(value: result.confidence)
                    .tint(.indigo)

                DisclosureGroup("내부 지표 자세히 보기") {
                    Text("내부 분석 신뢰도 \(result.confidence, format: .number.precision(.fractionLength(2))). 이 값은 범죄가 실제로 발생했을 확률을 의미하지 않고, 현재 분석 결과의 내부 일관성 지표로 사용해.")
                        .font(.caption).foregroundStyle(.secondary)
                        .padding(.top, 6)
                }
                .font(.caption)
            }
        }
        .padding(18)
        .background(.background, in: RoundedRectangle(cornerRadius: 20))
        .overlay(RoundedRectangle(cornerRadius: 20).stroke(result.urgency.tint.opacity(0.12)))
    }

    private var confidenceLabel: String {
        switch result.confidence {
        case 0.85...: "높음"
        case 0.65..<0.85: "보통"
        default: "낮음 · 추가 확인 필요"
        }
    }

    private func section<Content: View>(_ title: String, @ViewBuilder content: () -> Content) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            Text(title).font(.title3.bold())
            content()
        }
    }
}

#Preview {
    NavigationStack { AnalysisResultView(result: MockSafetyAnalysis.highRisk) }
}
