import Foundation

/// Preview와 사용자 테스트에서 정보 품질(AIMQ)과 정서적 지지(SRS)를
/// 서로 독립적으로 기록하기 위한 평가 모델입니다.
struct ResponseQualityRubric {
    enum AIMQItem: String, CaseIterable, Identifiable {
        case accessibility = "정보 접근성"
        case amount = "정보량"
        case reliability = "신뢰성"
        case scope = "정보 범위"
        case conciseness = "간결성"
        case format = "정보 형식"
        case findability = "검색 용이성"
        case accuracy = "정확성"
        case interpretability = "해석 용이성"
        case objectivity = "객관성"
        case usefulness = "유용성"
        case timeliness = "시의성"
        case understandability = "이해 용이성"
        var id: String { rawValue }
    }

    enum SRSItem: String, CaseIterable, Identifiable {
        case nonBlaming = "피해자를 비난하지 않음"
        case understanding = "상황을 이해하려 함"
        case organizing = "피해 내용 정리를 도움"
        case nonJudgmental = "판단하지 않음"
        case natural = "기계적인 위로가 아님"
        case considerate = "감정을 고려함"
        case nonAssumptive = "감정을 과도하게 추측하지 않음"
        case actionable = "다음 행동으로 이동하도록 도움"
        var id: String { rawValue }
    }

    /// 1(매우 부족)~5(매우 우수). 두 척도를 합산하지 않는다.
    var aimqScores: [AIMQItem: Int]
    var srsScores: [SRSItem: Int]
}

