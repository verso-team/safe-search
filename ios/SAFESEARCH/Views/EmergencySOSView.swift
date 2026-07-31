import MessageUI
import SwiftUI

struct EmergencySOSView: View {
    @EnvironmentObject private var locationService: LocationSafetyService
    @EnvironmentObject private var contactStore: SafetyContactStore
    @Environment(\.openURL) private var openURL

    @State private var isActivated = false
    @State private var showContactSettings = false
    @State private var showMessageComposer = false

    var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                GuardianTigerGuideView(message: "실제 위험이면 앱 분석보다 안전한 장소로 이동하고 112에 연락하는 게 먼저야.")

                VStack(spacing: 14) {
                    Image(systemName: isActivated ? "checkmark.shield.fill" : "sos.circle.fill")
                        .font(.system(size: 56))
                        .foregroundStyle(isActivated ? .green : .red)

                    Text(isActivated ? "긴급 안전 모드 준비 완료" : "SOS 버튼을 길게 눌러")
                        .font(.title2.bold())

                    Text(isActivated
                         ? "현재 위치 확인, 보호자 메시지, 112 연결을 바로 사용할 수 있어."
                         : "실수로 눌리는 걸 막기 위해 1.2초 동안 길게 눌러야 해.")
                        .font(.subheadline).foregroundStyle(.secondary)
                        .multilineTextAlignment(.center)

                    if !isActivated {
                        Text("SOS 길게 누르기")
                            .font(.headline).foregroundStyle(.white)
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(.red, in: RoundedRectangle(cornerRadius: 16))
                            .onLongPressGesture(minimumDuration: 1.2) {
                                isActivated = true
                                locationService.requestCurrentLocation()
                            }
                            .accessibilityHint("1.2초 동안 길게 누르면 긴급 안전 기능을 준비합니다")
                    }
                }
                .padding(20)
                .background(.background, in: RoundedRectangle(cornerRadius: 22))

                if isActivated {
                    locationCard
                    actionButtons
                }

                Text("SAFE:SEARCH는 경찰에 위치를 자동 전송하지 않아. 112 통화와 보호자 메시지는 사용자가 직접 최종 실행해야 해.")
                    .font(.footnote).foregroundStyle(.secondary)
            }
            .padding()
        }
        .background(Color(red: 0.96, green: 0.98, blue: 1.0))
        .navigationTitle("긴급 SOS")
        .sheet(isPresented: $showContactSettings) {
            NavigationStack {
                EmergencyContactSettingsView()
                    .toolbar {
                        ToolbarItem(placement: .confirmationAction) {
                            Button("완료") { showContactSettings = false }
                        }
                    }
            }
            .environmentObject(contactStore)
        }
        .sheet(isPresented: $showMessageComposer) {
            SMSComposerView(
                recipients: [contactStore.contact.phone],
                body: "[SAFE:SEARCH 긴급 공유]\n\(locationService.shareText)\n현재 안전 확인이 필요해요.",
                onFinish: { showMessageComposer = false }
            )
        }
    }

    private var locationCard: some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack {
                Label("현재 위치", systemImage: "location.fill")
                    .font(.headline)
                Spacer()
                Button("새로고침") { locationService.requestCurrentLocation() }
                    .font(.caption)
            }

            if let coordinate = locationService.coordinateText {
                Text(coordinate).font(.subheadline.monospacedDigit())
                if let url = locationService.mapsURL {
                    Link("지도에서 열기", destination: url)
                        .font(.subheadline.bold())
                }
            } else {
                Text(locationService.locationError ?? "위치를 확인하고 있어.")
                    .font(.subheadline).foregroundStyle(.secondary)
            }
        }
        .padding(16)
        .background(.background, in: RoundedRectangle(cornerRadius: 18))
    }

    private var actionButtons: some View {
        VStack(spacing: 10) {
            Button {
                if let url = URL(string: "tel://112") { openURL(url) }
            } label: {
                Label("112 연결", systemImage: "phone.fill")
                    .font(.headline).frame(maxWidth: .infinity).padding()
            }
            .buttonStyle(.borderedProminent)
            .tint(.red)

            Button {
                if contactStore.contact.isConfigured, MFMessageComposeViewController.canSendText() {
                    showMessageComposer = true
                } else {
                    showContactSettings = true
                }
            } label: {
                Label(
                    contactStore.contact.isConfigured ? "\(contactStore.contact.name)에게 알림 준비" : "보호자 설정 후 알림",
                    systemImage: "person.crop.circle.badge.exclamationmark"
                )
                .frame(maxWidth: .infinity)
            }
            .buttonStyle(.bordered)

            ShareLink(item: locationService.shareText) {
                Label("현재 위치 공유", systemImage: "square.and.arrow.up")
                    .frame(maxWidth: .infinity)
            }
            .buttonStyle(.bordered)

            Button {
                var urlString = "https://maps.apple.com/?q=경찰서"
                if let location = locationService.lastLocation?.coordinate {
                    urlString += "&sll=\(location.latitude),\(location.longitude)"
                }
                if let url = URL(string: urlString) { openURL(url) }
            } label: {
                Label("주변 경찰서·안전 장소 찾기", systemImage: "map.fill")
                    .frame(maxWidth: .infinity)
            }
            .buttonStyle(.bordered)
        }
    }
}
