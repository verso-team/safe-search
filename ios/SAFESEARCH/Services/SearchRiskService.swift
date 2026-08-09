import Foundation
#if canImport(FoundationNetworking)
import FoundationNetworking
#endif

protocol SearchRiskServing {
    func analyze(
        title: String,
        snippet: String,
        url: String
    ) async throws -> SearchRiskResult
}

enum SearchRiskAPIError: LocalizedError {
    case emptyTitle
    case invalidURL
    case invalidResponse
    case server(statusCode: Int)
    case invalidPayload
    case transport(URLError)

    var errorDescription: String? {
        switch self {
        case .emptyTitle:
            "검색결과 제목을 입력해주세요."
        case .invalidURL:
            "http 또는 https 형식의 주소를 입력해주세요."
        case .invalidResponse:
            "위험 분석 서버의 응답을 확인할 수 없습니다."
        case let .server(statusCode):
            "위험 분석 서버에서 오류가 발생했습니다. (HTTP \(statusCode))"
        case .invalidPayload:
            "위험 분석 결과 형식이 앱과 맞지 않습니다."
        case .transport:
            "위험 분석 서버에 연결할 수 없습니다."
        }
    }
}

struct SearchRiskService: SearchRiskServing {
    private let session: URLSession
    private let endpoint: URL

    init(
        session: URLSession = .shared,
        endpoint: URL = APIConfiguration.searchRiskURL
    ) {
        self.session = session
        self.endpoint = endpoint
    }

    func analyze(
        title: String,
        snippet: String,
        url: String
    ) async throws -> SearchRiskResult {
        let normalizedTitle = title.trimmingCharacters(
            in: .whitespacesAndNewlines
        )
        let normalizedSnippet = snippet.trimmingCharacters(
            in: .whitespacesAndNewlines
        )
        let normalizedURL = url.trimmingCharacters(
            in: .whitespacesAndNewlines
        )

        guard !normalizedTitle.isEmpty else {
            throw SearchRiskAPIError.emptyTitle
        }

        guard
            let parsedURL = URL(string: normalizedURL),
            let scheme = parsedURL.scheme?.lowercased(),
            ["http", "https"].contains(scheme),
            parsedURL.host != nil
        else {
            throw SearchRiskAPIError.invalidURL
        }

        var request = URLRequest(url: endpoint)
        request.httpMethod = "POST"
        request.timeoutInterval = APIConfiguration.requestTimeout
        request.setValue(
            "application/json",
            forHTTPHeaderField: "Content-Type"
        )
        request.setValue(
            "application/json",
            forHTTPHeaderField: "Accept"
        )

        request.httpBody = try JSONEncoder().encode(
            SearchRiskRequestDTO(
                title: normalizedTitle,
                snippet: normalizedSnippet,
                url: parsedURL.absoluteString
            )
        )

        do {
            let (data, response) = try await session.data(
                for: request
            )

            guard let httpResponse = response as? HTTPURLResponse else {
                throw SearchRiskAPIError.invalidResponse
            }

            guard (200..<300).contains(httpResponse.statusCode) else {
                throw SearchRiskAPIError.server(
                    statusCode: httpResponse.statusCode
                )
            }

            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase

            do {
                let dto = try decoder.decode(
                    SearchRiskResponseDTO.self,
                    from: data
                )

                return dto.toDomain()
            } catch {
                throw SearchRiskAPIError.invalidPayload
            }
        } catch let error as SearchRiskAPIError {
            throw error
        } catch let error as URLError {
            throw SearchRiskAPIError.transport(error)
        }
    }
}
