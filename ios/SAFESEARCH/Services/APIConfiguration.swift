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

    static let requestTimeout: TimeInterval = 12

    /// 개발 시연 중 서버가 꺼져 있어도 화면 흐름을 확인할 수 있도록 한다.
    /// Release 빌드에서는 자동으로 비활성화된다.
    static var allowsMockFallback: Bool {
        #if DEBUG
        true
        #else
        false
        #endif
    }
}
