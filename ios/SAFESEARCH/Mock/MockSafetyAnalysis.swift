import Foundation

enum MockSafetyAnalysis {
    static func result(matching input: String) -> SafetyAnalysisResult {
        let isCritical = ["죽", "흉기", "찾아왔", "위협"].contains { input.contains($0) }
        return isCritical ? critical : highRisk
    }

    static let highRisk = SafetyAnalysisResult(
        primaryIntent: .reporting,
        secondaryIntents: [.information, .evidence],
        emotionalState: .anxious,
        urgency: .high,
        confidence: 0.87,
        suspectedHarmType: "디지털 성범죄·유포 위협 가능성",
        emotionalSupportMessage: "혼자 해결하려고 하지 않아도 됩니다.\n지금 할 수 있는 안전한 조치부터 확인해볼게요.",
        situationSummary: "영상 유포가 진행 중이거나 임박했을 가능성이 있어 신속한 증거 보존과 공식기관 상담이 필요합니다.",
        immediateActions: [
            ActionItem(title: "추가 요구에 응하지 않기", detail: "송금하거나 새로운 사진·정보를 보내지 마세요.", priority: 1),
            ActionItem(title: "대화와 계정 정보 보존하기", detail: "메시지, URL, 계정명, 송금 내역을 삭제하지 말고 캡처하세요.", priority: 2),
            ActionItem(title: "공식기관에 상담·신고하기", detail: "지원센터 또는 경찰에 현재 상황을 알려주세요.", priority: 3)
        ],
        safeSearchQueries: ["디지털 성범죄 피해자 지원센터", "영상 유포 피해 신고 방법", "사이버범죄 신고 절차"],
        recommendedAgencies: InstitutionService.shared.agencies(for: .secondaryDamage),
        requiresHumanReview: true,
        safetyNotice: "분석은 법률적 판단이나 범죄 확정을 의미하지 않습니다."
    )

    static let critical = SafetyAnalysisResult(
        primaryIntent: .emergency,
        secondaryIntents: [.reporting],
        emotionalState: .panic,
        urgency: .critical,
        confidence: 0.93,
        suspectedHarmType: "즉각적인 신체 안전 위협 가능성",
        emotionalSupportMessage: "지금은 안전을 확보하는 것이 가장 중요합니다.",
        situationSummary: "즉각적인 대응이 필요한 신체 위험 신호가 감지되었습니다.",
        immediateActions: [
            ActionItem(title: "안전한 장소로 이동하기", detail: "가능하면 주변 사람이나 열린 공공장소로 이동하세요.", priority: 1),
            ActionItem(title: "112에 연락하기", detail: "직접 통화하기 어렵다면 주변 사람에게 도움을 요청하세요.", priority: 2),
            ActionItem(title: "위치 공유하기", detail: "신뢰할 수 있는 사람에게 현재 위치를 알리세요.", priority: 3)
        ],
        safeSearchQueries: ["경찰청 긴급 신고", "범죄피해자 안전 지원"],
        recommendedAgencies: [InstitutionService.shared.police],
        requiresHumanReview: true,
        safetyNotice: nil
    )
}

