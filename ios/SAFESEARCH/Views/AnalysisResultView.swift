import SwiftUI

struct AnalysisResultView: View {
    let result: SafetyAnalysisResult

    var body: some View {
        ScrollView {
            LazyVStack(alignment: .leading, spacing: 24) {
                if let notice = result.safetyNotice {
                    Label(notice, systemImage: "exclamationmark.triangle.fill")
                        .font(.subheadline.bold())
                        .foregroundStyle(result.urgency.tint)
                        .padding(14)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(result.urgency.tint.opacity(0.10), in: RoundedRectangle(cornerRadius: 14))
                }

                EmotionalSupportView(message: result.emotionalSupportMessage)

                section("지금 확인된 상황") {
                    VStack(alignment: .leading, spacing: 14) {
                        HStack {
                            VStack(alignment: .leading, spacing: 4) {
                                Text("예상 피해 유형").font(.caption).foregroundStyle(.secondary)
                                Text(result.suspectedHarmType).font(.headline)
                            }
                            Spacer()
                            UrgencyBadge(urgency: result.urgency)
                        }
                        Text(result.situationSummary).font(.subheadline).foregroundStyle(.secondary)
                        Divider()
                        ConfidenceIndicator(confidence: result.confidence)
                    }
                    .padding(16).background(.background, in: RoundedRectangle(cornerRadius: 18))
                }

                section("지금 먼저 해주세요") {
                    ActionGuideView(actions: result.immediateActions)
                }
                section("안전하게 검색하기") {
                    SafeQueryView(queries: result.safeSearchQueries)
                }
                section("도움을 받을 수 있는 곳") {
                    AgencyRecommendationView(agencies: result.recommendedAgencies)
                }
                HumanReviewView(isRequired: result.requiresHumanReview)
            }
            .padding()
        }
        .background(Color(.systemGroupedBackground))
        .navigationTitle("안전 분석 결과")
        .navigationBarTitleDisplayMode(.inline)
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

