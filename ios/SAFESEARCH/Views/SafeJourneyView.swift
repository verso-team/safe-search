import MessageUI
import SwiftUI

struct SafeJourneyView: View {
    @EnvironmentObject private var journeyStore: SafeJourneyStore
    @EnvironmentObject private var locationService: LocationSafetyService
    @EnvironmentObject private var contactStore: SafetyContactStore

    @State private var destination = ""
    @State private var durationMinutes = 30
    @State private var showMessageComposer = false
    @State private var showContactSettings = false

    private let durationOptions = [15, 30, 60, 90]

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                GuardianTigerGuideView(message: "안심 귀가는 자동 위험 판정이 아니라, 네가 정한 도착시간과 현재 위치를 기준으로 안전 확인을 돕는 모드야.")

                if let session = journeyStore.session {
                    activeSession(session)
                } else {
                    setupForm
                }

                Text("현재 프로토타입은 앱이 열려 있는 동안 위치를 갱신하고 도착 예정 알림을 제공해. 보호자에게 위치를 자동으로 계속 전송하는 기능은 서버·백그라운드 권한·동의 정책이 확정된 뒤 구현해야 해.")
                    .font(.footnote).foregroundStyle(.secondary)
            }
            .padding()
        }
        .background(Color(red: 0.96, green: 0.98, blue: 1.0))
        .navigationTitle("안심 귀가")
        .onDisappear {
            if journeyStore.session == nil {
                locationService.stopContinuousUpdates()
            }
        }
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
            if let session = journeyStore.session {
                SMSComposerView(
                    recipients: [contactStore.contact.phone],
                    body: journeyShareText(session),
                    onFinish: { showMessageComposer = false }
                )
            }
        }
    }

    private var setupForm: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("귀가 계획").font(.title3.bold())

            TextField("목적지 예: 집", text: $destination)
                .textFieldStyle(.roundedBorder)

            VStack(alignment: .leading, spacing: 8) {
                Text("예상 이동시간").font(.subheadline.bold())
                Picker("예상 이동시간", selection: $durationMinutes) {
                    ForEach(durationOptions, id: \.self) { minute in
                        Text("\(minute)분").tag(minute)
                    }
                }
                .pickerStyle(.segmented)
            }

            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text("보호자").font(.subheadline.bold())
                    Text(contactStore.contact.isConfigured ? contactStore.contact.name : "아직 설정 안 됨")
                        .font(.caption).foregroundStyle(.secondary)
                }
                Spacer()
                Button("설정") { showContactSettings = true }
            }

            Button {
                locationService.requestCurrentLocation()
                locationService.startContinuousUpdates()
                journeyStore.start(
                    destination: destination,
                    durationMinutes: durationMinutes,
                    startCoordinate: locationService.coordinateText
                )
            } label: {
                Label("안심 귀가 시작", systemImage: "figure.walk.motion")
                    .font(.headline).frame(maxWidth: .infinity).padding()
            }
            .buttonStyle(.borderedProminent)
            .tint(.blue)
            .disabled(destination.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
        }
        .padding(18)
        .background(.background, in: RoundedRectangle(cornerRadius: 20))
    }

    private func activeSession(_ session: SafeJourneySession) -> some View {
        VStack(alignment: .leading, spacing: 16) {
            Label("안심 귀가 진행 중", systemImage: "location.circle.fill")
                .font(.title3.bold()).foregroundStyle(.blue)

            Text(session.destination).font(.title2.bold())
            Text("도착 예정 \(session.expectedArrivalAt.formatted(date: .omitted, time: .shortened))")
                .foregroundStyle(.secondary)

            TimelineView(.periodic(from: .now, by: 1)) { context in
                let remaining = max(0, session.expectedArrivalAt.timeIntervalSince(context.date))
                Text(formatRemaining(remaining))
                    .font(.system(size: 36, weight: .bold, design: .rounded))
                    .monospacedDigit()
            }

            if let coordinate = locationService.coordinateText {
                Label(coordinate, systemImage: "location.fill")
                    .font(.caption.monospacedDigit()).foregroundStyle(.secondary)
            }

            Button {
                if contactStore.contact.isConfigured, MFMessageComposeViewController.canSendText() {
                    showMessageComposer = true
                } else {
                    showContactSettings = true
                }
            } label: {
                Label("보호자에게 현재 상태 공유", systemImage: "message.fill")
                    .frame(maxWidth: .infinity)
            }
            .buttonStyle(.bordered)

            ShareLink(item: journeyShareText(session)) {
                Label("다른 방법으로 위치 공유", systemImage: "square.and.arrow.up")
                    .frame(maxWidth: .infinity)
            }
            .buttonStyle(.bordered)

            NavigationLink { EmergencySOSView() } label: {
                Label("긴급 SOS", systemImage: "sos.circle.fill")
                    .font(.headline).frame(maxWidth: .infinity).padding()
            }
            .buttonStyle(.borderedProminent)
            .tint(.red)

            Button("안전하게 도착했어 · 종료") {
                journeyStore.finish()
                locationService.stopContinuousUpdates()
            }
            .frame(maxWidth: .infinity)
            .buttonStyle(.bordered)
            .tint(.green)
        }
        .padding(18)
        .background(.background, in: RoundedRectangle(cornerRadius: 20))
    }

    private func journeyShareText(_ session: SafeJourneySession) -> String {
        "[SAFE:SEARCH 안심 귀가]\n목적지: \(session.destination)\n도착 예정: \(session.expectedArrivalAt.formatted(date: .numeric, time: .shortened))\n\(locationService.shareText)"
    }

    private func formatRemaining(_ interval: TimeInterval) -> String {
        let total = Int(interval)
        let minutes = total / 60
        let seconds = total % 60
        return String(format: "%02d:%02d", minutes, seconds)
    }
}
