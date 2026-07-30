import Foundation

struct InstitutionService {
    static let shared = InstitutionService()

    let police = Agency(
        id: "police", name: "경찰청", role: "긴급 신고 및 사이버범죄 신고",
        phone: "112", website: URL(string: "https://ecrm.police.go.kr")!, isOfficial: true
    )
    let kisa = Agency(
        id: "kisa", name: "KISA 118", role: "사이버 침해·불법스팸 상담",
        phone: "118", website: URL(string: "https://www.kisa.or.kr/118")!, isOfficial: true
    )
    let d4u = Agency(
        id: "d4u", name: "디지털성범죄피해자지원센터",
        role: "상담, 삭제 지원, 수사·법률·의료 연계",
        phone: "02-735-8994", website: URL(string: "https://d4u.stop.or.kr")!, isOfficial: true
    )

    func agencies(for intent: UserIntent) -> [Agency] {
        switch intent {
        case .secondaryDamage: [d4u, police]
        case .emergency, .reporting, .evidence: [police, kisa]
        default: [kisa, police]
        }
    }
}

