import Foundation

struct SafeQueryRewriter {
    func rewrite(_ input: String) -> [String] {
        let normalized = input.lowercased()
        var queries: [String] = []

        if containsAny(normalized, ["몸캠", "영상", "유포", "사진", "딥페이크"]) {
            queries += [
                "디지털성범죄 유포협박 증거보존 방법",
                "디지털성범죄 공식 피해지원기관",
                "사이버범죄 신고 절차"
            ]
        }

        if containsAny(normalized, ["해킹", "인스타", "계정", "로그인", "복구"]) {
            queries += [
                "SNS 계정 탈취 공식 복구 방법",
                "계정 탈취 피해 증거보존 방법",
                "사이버범죄 계정 탈취 신고 절차"
            ]
        }

        if containsAny(normalized, ["택배", "과태료", "범칙금", "문자", "스미싱", "링크"]) {
            queries += [
                "KISA 스미싱 확인 공식 서비스",
                "스미싱 피해 대응 공식 안내",
                "의심 링크 공식기관 확인 방법"
            ]
        }

        if containsAny(normalized, ["검찰", "경찰", "금감원", "기관", "사칭", "보이스피싱"]) {
            queries += [
                "기관 사칭 보이스피싱 공식 확인 방법",
                "경찰청 보이스피싱 신고 절차",
                "KISA 피싱 피해 상담"
            ]
        }

        if queries.isEmpty {
            queries = [
                "사이버범죄 피해 공식 신고 절차",
                "KISA 사이버 피해 상담",
                "경찰청 사이버범죄 신고"
            ]
        }

        return Array(NSOrderedSet(array: queries)) as? [String] ?? queries
    }

    private func containsAny(_ text: String, _ terms: [String]) -> Bool {
        terms.contains { text.contains($0) }
    }
}
