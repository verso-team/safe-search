import SwiftUI

struct AnalysisView: View {
    let input: String
    let service: any AIAnalysisServing

    @State private var result: SafetyAnalysisResult?
    @State private var errorMessage: String?
    @State private var requestID = UUID()

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
                        .font(.largeTitle)
                        .foregroundStyle(.secondary)

                    Text("분석을 완료하지 못했어요")
                        .font(.headline)

                    Text(errorMessage)
                        .font(.subheadline)
                        .foregroundStyle(.secondary)

                    Button("다시 시도") {
                        self.errorMessage = nil
                        requestID = UUID()
                    }
                    .buttonStyle(.borderedProminent)
                    .tint(.indigo)
                }
                .multilineTextAlignment(.center)
                .padding()
            } else {
                VStack(spacing: 20) {
                    ProgressView()
                        .controlSize(.large)
                        .tint(.indigo)

                    Text("위험 신호와 필요한 지원을 확인하고 있어요")
                        .font(.headline)

                    Text("개인정보·인증번호·전체 계좌번호는 입력하지 마세요.")
                        .font(.subheadline)
                        .foregroundStyle(.secondary)

                    #if DEBUG
                    Text("개발 빌드에서는 서버 연결 실패 시 시연용 Mock 결과로 전환됩니다.")
                        .font(.caption)
                        .foregroundStyle(.secondary)
                    #endif
                }
                .multilineTextAlignment(.center)
                .padding()
            }
        }
        .task(id: requestID) {
            await runAnalysis()
        }
    }

    @MainActor
    private func runAnalysis() async {
        guard result == nil else { return }

        do {
            result = try await service.analyze(input)
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}

#Preview {
    NavigationStack {
        AnalysisView(input: "영상이 퍼지고 있는데 신고 방법을 모르겠어요.")
    }
}
