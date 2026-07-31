import SwiftUI

struct SupportHubView: View {
    private let agencies = [
        InstitutionService.shared.d4u,
        InstitutionService.shared.police,
        InstitutionService.shared.kisa
    ]

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                GuardianTigerGuideView(message: "기관 이름이 비슷해도 링크나 전화번호가 다를 수 있어. 공식기관 정보인지 먼저 확인해줘.")

                VStack(alignment: .leading, spacing: 12) {
                    Text("도움을 받을 수 있는 곳").font(.title3.bold())
                    ForEach(agencies) { agency in
                        VStack(alignment: .leading, spacing: 7) {
                            HStack {
                                Label("공식기관 인증", systemImage: "checkmark.seal.fill")
                                    .font(.caption.bold()).foregroundStyle(.blue)
                                Spacer()
                            }
                            AgencyCard(agency: agency)
                        }
                    }
                }

                HumanReviewView(isRequired: true)

                NavigationLink { EmergencySOSView() } label: {
                    Label("긴급 SOS / 위치 공유", systemImage: "sos.circle.fill")
                        .font(.headline).frame(maxWidth: .infinity).padding()
                }
                .buttonStyle(.borderedProminent)
                .tint(.red)
            }
            .padding()
        }
        .background(Color(red: 0.96, green: 0.98, blue: 1.0))
        .navigationTitle("공식 지원기관")
    }
}
