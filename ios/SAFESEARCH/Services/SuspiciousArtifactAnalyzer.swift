import Foundation

struct SuspiciousArtifactAnalyzer {
    private let rewriter = SafeQueryRewriter()

    func analyze(kind: ArtifactKind, text: String) -> ArtifactRiskResult {
        let normalized = text.lowercased().trimmingCharacters(in: .whitespacesAndNewlines)
        guard !normalized.isEmpty else {
            return ArtifactRiskResult(
                risk: .caution,
                title: "확인할 내용이 필요해요",
                summary: "문자 내용, 링크 또는 전화 상황을 입력하면 위험 신호를 확인할 수 있어요.",
                reasons: [],
                recommendedActions: ["개인정보나 인증번호를 먼저 제공하지 마세요."],
                safeQueries: rewriter.rewrite(text)
            )
        }

        var score = 0
        var reasons: [String] = []

        let institutions = ["검찰", "경찰", "금감원", "금융감독원", "국세청", "법원", "카드사", "은행"]
        let moneyTerms = ["송금", "입금", "계좌", "안전계좌", "보증금", "수수료", "벌금"]
        let credentialTerms = ["인증번호", "비밀번호", "보안카드", "주민번호", "원격제어", "앱 설치"]
        let urgencyTerms = ["즉시", "오늘까지", "지금", "정지", "압류", "체포", "미납", "긴급"]

        if containsAny(normalized, institutions) && (containsAny(normalized, moneyTerms) || containsAny(normalized, credentialTerms)) {
            score += 4
            reasons.append("기관을 언급하면서 금전 또는 개인정보 제공을 요구하는 패턴이 있어요.")
        }
        if containsAny(normalized, moneyTerms) {
            score += 2
            reasons.append("송금·계좌 관련 요구가 포함되어 있어요.")
        }
        if containsAny(normalized, credentialTerms) {
            score += 3
            reasons.append("인증정보 또는 원격제어를 요구하는 표현이 있어요.")
        }
        if containsAny(normalized, urgencyTerms) {
            score += 1
            reasons.append("빠른 행동을 압박하는 표현이 있어요.")
        }

        if kind == .link {
            let linkRisk = inspectURL(normalized)
            score += linkRisk.score
            reasons += linkRisk.reasons
        }

        if kind == .phone && !containsAny(normalized, institutions + moneyTerms + credentialTerms) {
            reasons.append("전화번호만으로는 사기 여부를 확정할 수 없어요. 통화에서 소속·목적·금전 요구 여부를 함께 확인해야 해요.")
            score = max(score, 1)
        }

        let risk: RiskBand
        switch score {
        case 7...: risk = .high
        case 3...6: risk = .caution
        default: risk = .low
        }

        let title: String
        let summary: String
        switch risk {
        case .high, .critical:
            title = "사기·기관 사칭 위험 신호가 보여요"
            summary = "입력 내용만으로 범죄를 확정할 수는 없지만, 추가 행동 전에 공식 경로로 다시 확인하는 게 안전해요."
        case .caution:
            title = "주의해서 확인할 필요가 있어요"
            summary = "바로 링크를 열거나 정보를 제공하지 말고, 발신자가 주장한 기관의 공식 대표번호를 직접 찾아 확인하세요."
        case .low:
            title = "뚜렷한 고위험 신호는 적어요"
            summary = "안전 판정을 의미하지는 않아요. 모르는 발신자라면 공식 채널로 한 번 더 확인하세요."
        }

        return ArtifactRiskResult(
            risk: risk,
            title: title,
            summary: summary,
            reasons: reasons.isEmpty ? ["현재 입력에서 대표적인 고위험 패턴이 많이 발견되지는 않았어요."] : reasons,
            recommendedActions: [
                "문자나 통화에 포함된 번호가 아니라 기관 공식 대표번호를 직접 찾아 확인하기",
                "인증번호·비밀번호·원격제어 권한을 제공하지 않기",
                "송금 전 대화·발신번호·링크를 증거로 보존하기"
            ],
            safeQueries: rewriter.rewrite(text)
        )
    }

    private func containsAny(_ text: String, _ terms: [String]) -> Bool {
        terms.contains { text.contains($0) }
    }

    private func inspectURL(_ text: String) -> (score: Int, reasons: [String]) {
        var score = 0
        var reasons: [String] = []
        let candidate = text.hasPrefix("http") ? text : "https://\(text)"

        guard let url = URL(string: candidate), let host = url.host?.lowercased() else {
            return (2, ["정상적인 URL 형식인지 확인하기 어려워요."])
        }

        if url.scheme == "http" {
            score += 1
            reasons.append("암호화되지 않은 http 링크예요.")
        }
        if host.contains("xn--") {
            score += 3
            reasons.append("국제화 도메인(Punycode)이 포함되어 있어 유사 도메인 여부를 확인해야 해요.")
        }
        if host.range(of: #"^\d{1,3}(\.\d{1,3}){3}$"#, options: .regularExpression) != nil {
            score += 3
            reasons.append("도메인 이름 대신 IP 주소를 직접 사용하는 링크예요.")
        }
        let shorteners = ["bit.ly", "tinyurl.com", "t.co", "url.kr"]
        if shorteners.contains(where: { host == $0 || host.hasSuffix(".\($0)") }) {
            score += 1
            reasons.append("최종 목적지를 바로 확인하기 어려운 단축 URL이에요.")
        }

        return (score, reasons)
    }
}
