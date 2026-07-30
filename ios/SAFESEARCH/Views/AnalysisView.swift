import SwiftUI

struct AnalysisView: View {
    let input: String
    let service: any AIAnalysisServing
    @State private var result: SafetyAnalysisResult?
    @State private var errorMessage: String?

    init(input: String, service: any AIAnalysisServing = AIAnalysisService()) {
        self.input = input
        self.service = service
    }

    var body: some View {
        Group {
            if let result {
                AnalysisResultView(result: result)
            } else if let errorMessage {
                VStack(spacing: 12) {
                    Image(systemName: "exclamationmark.arrow.triangle.2.circlepath")
                        .font(.largeTitle).foregroundStyle(.secondary)
                    Text("분석을 완료하지 못했어요").font(.headline)
                    Text(errorMessage).font(.subheadline).foregroundStyle(.secondary)
                }
                .multilineTextAlignment(.center).padding()
            } else {
                VStack(spacing: 20) {
                    ProgressView().controlSize(.large).tint(.indigo)
                    Text("위험 신호와 필요한 지원을 확인하고 있어요").font(.headline)
                    Text("입력 내용은 Mock 분석에만 사용됩니다.")
                        .font(.subheadline).foregroundStyle(.secondary)
                }
                .multilineTextAlignment(.center).padding()
            }
        }
        .task {
            guard result == nil else { return }
            do { result = try await service.analyze(input) }
            catch { errorMessage = error.localizedDescription }
        }
    }
}

#Preview { NavigationStack { AnalysisView(input: "영상이 퍼지고 있는데 신고 방법을 모르겠어요.") } }
