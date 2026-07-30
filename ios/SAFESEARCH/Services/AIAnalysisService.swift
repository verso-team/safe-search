import Foundation

protocol AIAnalysisServing {
    func analyze(_ input: String) async throws -> SafetyAnalysisResult
}

enum AnalysisError: LocalizedError {
    case emptyInput
    var errorDescription: String? { "상황을 한 문장 이상 입력해주세요." }
}

struct AIAnalysisService: AIAnalysisServing {
    private let policy = SafetyPolicyEngine()

    func analyze(_ input: String) async throws -> SafetyAnalysisResult {
        guard !input.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else {
            throw AnalysisError.emptyInput
        }
        try await Task.sleep(nanoseconds: 650_000_000)
        let sample = MockSafetyAnalysis.result(matching: input)
        return policy.validate(sample)
    }
}

