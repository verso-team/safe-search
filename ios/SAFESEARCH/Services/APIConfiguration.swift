import Foundation

enum APIConfiguration {
    /// Xcode Scheme 환경변수 `SAFESEARCH_API_URL`로 덮어쓸 수 있다.
    /// 예: http://192.168.0.20:8000
    static var baseURL: URL {
        if let rawValue = ProcessInfo.processInfo.environment["SAFESEARCH_API_URL"],
           let configuredURL = URL(string: rawValue),
           configuredURL.scheme != nil,
           configuredURL.host != nil {
            return configuredURL
        }

        return URL(string: "http://127.0.0.1:8000")!
    }

    static var analyzeURL: URL {
        baseURL
            .appendingPathComponent("api")
            .appendingPathComponent("v1")
            .appendingPathComponent("analyze")
    }

    static var searchRiskURL: URL {
        baseURL
            .appendingPathComponent("api")
            .appendingPathComponent("v1")
            .appendingPathComponent("search-risk")
    }

    static let requestTimeout: TimeInterval = 12

    /// 개발 시연 중 서버가 꺼져 있어도 기존 Analyze 화면 흐름을 확인한다.
    /// Search Risk는 위험 provenance를 흐리지 않기 위해 Mock fallback을 사용하지 않는다.
    static var allowsMockFallback: Bool {
        #if DEBUG
        true
        #else
        false
        #endif
    }
}
