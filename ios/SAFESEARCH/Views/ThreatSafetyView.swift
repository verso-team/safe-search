import SwiftUI

struct ThreatSafetyView: View {
    @State private var note = "누가 뒤에서 따라오는 것 같아"
    @Environment(\.openURL) private var openURL
    @EnvironmentObject private var locationService: LocationSafetyService

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                GuardianTigerGuideView(message: "누가 따라오는 것 같다는 느낌만으로 사실 여부를 단정하지 않을게. 대신 지금 안전을 확보하는 행동을 먼저 보여줄게.")

                VStack(alignment: .leading, spacing: 10) {
                    Text("지금 상황").font(.headline)
                    TextField("상황을 짧게 적어줘", text: $note, axis: .vertical)
                        .textFieldStyle(.roundedBorder)
                }
                .padding(16)
                .background(.background, in: RoundedRectangle(cornerRadius: 18))

                VStack(alignment: .leading, spacing: 12) {
                    Label("긴급도 높음으로 우선 대응", systemImage: "exclamationmark.triangle.fill")
                        .font(.headline).foregroundStyle(.red)
                    action("밝고 사람이 있는 장소로 이동하기", icon: "figure.walk")
                    action("신뢰할 수 있는 사람에게 현재 위치 공유하기", icon: "location.fill")
                    action("실제 위협이 있거나 접근이 계속되면 112에 연락하기", icon: "phone.fill")
                }
                .padding(16)
                .background(Color.red.opacity(0.06), in: RoundedRectangle(cornerRadius: 18))

                NavigationLink { EmergencySOSView() } label: {
                    Label("SOS · 위치 공유 · 112", systemImage: "sos.circle.fill")
                        .font(.headline).frame(maxWidth: .infinity).padding()
                }
                .buttonStyle(.borderedProminent)
                .tint(.red)

                NavigationLink { SafeJourneyView() } label: {
                    Label("안심 귀가 모드 시작", systemImage: "figure.walk.motion")
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(.bordered)

                Button {
                    locationService.requestCurrentLocation()
                    var urlString = "https://maps.apple.com/?q=경찰서"
                    if let coordinate = locationService.lastLocation?.coordinate {
                        urlString += "&sll=\(coordinate.latitude),\(coordinate.longitude)"
                    }
                    if let url = URL(string: urlString) { openURL(url) }
                } label: {
                    Label("주변 경찰서·안전 장소 찾기", systemImage: "map.fill")
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(.bordered)

                Text("이 기능은 카메라·심박수로 '미행을 자동 판정'하지 않아. 사용자 입력을 안전 신호로 받아 즉시 대응 수단을 제공하는 구조야.")
                    .font(.footnote).foregroundStyle(.secondary)
            }
            .padding()
        }
        .background(Color(red: 0.96, green: 0.98, blue: 1.0))
        .navigationTitle("협박·미행 불안")
    }

    private func action(_ text: String, icon: String) -> some View {
        Label(text, systemImage: icon)
            .font(.subheadline)
            .frame(maxWidth: .infinity, alignment: .leading)
    }
}
