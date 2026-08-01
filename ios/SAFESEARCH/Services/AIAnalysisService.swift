import Foundation
#if canImport(FoundationNetworking)
import FoundationNetworking
#endif

protocol AIAnalysisServing {
    func analyze(_ input: String) async throws -> SafetyAnalysisResult
}

enum AnalysisError: LocalizedError {
    case emptyInput

    var errorDescription: String? {
        switch self {
        case .emptyInput:
            "상황을 한 문장 이상 입력해주세요."
        }
    }
}

enum AnalysisAPIError: LocalizedError {
    case invalidResponse
    case server(statusCode: Int)
    case invalidPayload
    case invalidAgencyWebsite
    case transport(URLError)

    var errorDescription: String? {
        switch self {
        case .invalidResponse:
            "분석 서버의 응답을 확인할 수 없습니다."
        case let .server(statusCode):
            "분석 서버에서 오류가 발생했습니다. (HTTP \(statusCode))"
        case .invalidPayload:
            "분석 결과 형식이 앱과 맞지 않습니다."
        case .invalidAgencyWebsite:
            "공식기관 주소 형식이 올바르지 않습니다."
        case .transport:
            "분석 서버에 연결할 수 없습니다."
        }
    }
}

struct AIAnalysisService: AIAnalysisServing {
    private let policy: SafetyPolicyEngine
    private let session: URLSession
    private let endpoint: URL
    private let allowsMockFallback: Bool

    init(
        policy: SafetyPolicyEngine = SafetyPolicyEngine(),
        session: URLSession = .shared,
        endpoint: URL = APIConfiguration.analyzeURL,
        allowsMockFallback: Bool = APIConfiguration.allowsMockFallback
    ) {
        self.policy = policy
        self.session = session
        self.endpoint = endpoint
        self.allowsMockFallback = allowsMockFallback
    }

    func analyze(_ input: String) async throws -> SafetyAnalysisResult {
        let normalizedInput = input.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !normalizedInput.isEmpty else {
            throw AnalysisError.emptyInput
        }

        do {
            let remoteResult = try await requestAnalysis(for: normalizedInput)
            return policy.validate(remoteResult)
        } catch let transportError as URLError {
            guard allowsMockFallback else {
                throw AnalysisAPIError.transport(transportError)
            }

            return makeTransparentMockFallback(for: normalizedInput)
        }
    }

    private func requestAnalysis(for input: String) async throws -> SafetyAnalysisResult {
        var request = URLRequest(url: endpoint)
        request.httpMethod = "POST"
        request.timeoutInterval = APIConfiguration.requestTimeout
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        request.httpBody = try JSONEncoder().encode(AnalyzeRequestDTO(text: input))

        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw AnalysisAPIError.invalidResponse
        }

        guard (200..<300).contains(httpResponse.statusCode) else {
            throw AnalysisAPIError.server(statusCode: httpResponse.statusCode)
        }

        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase

        do {
            let responseDTO = try decoder.decode(AnalyzeResponseDTO.self, from: data)
            return try responseDTO.toDomain()
        } catch let mappingError as AnalysisAPIError {
            throw mappingError
        } catch {
            throw AnalysisAPIError.invalidPayload
        }
    }

    /// 네트워크 장애 때만 사용하는 개발용 fallback이다.
    /// 실제 서버 결과가 아님을 safetyNotice에 명확히 남긴다.
    private func makeTransparentMockFallback(for input: String) -> SafetyAnalysisResult {
        let sample = policy.validate(MockSafetyAnalysis.result(matching: input))
        let fallbackNotice = "개발 서버에 연결하지 못해 시연용 Mock 결과를 표시합니다."
        let combinedNotice = [sample.safetyNotice, fallbackNotice]
            .compactMap { $0 }
            .joined(separator: "\n")

        return SafetyAnalysisResult(
            id: sample.id,
            primaryIntent: sample.primaryIntent,
            secondaryIntents: sample.secondaryIntents,
            emotionalState: sample.emotionalState,
            urgency: sample.urgency,
            confidence: sample.confidence,
            suspectedHarmType: sample.suspectedHarmType,
            emotionalSupportMessage: sample.emotionalSupportMessage,
            situationSummary: sample.situationSummary,
            immediateActions: sample.immediateActions,
            safeSearchQueries: sample.safeSearchQueries,
            recommendedAgencies: sample.recommendedAgencies,
            requiresHumanReview: sample.requiresHumanReview,
            safetyNotice: combinedNotice
        )
    }
}
