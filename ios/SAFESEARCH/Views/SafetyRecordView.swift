import SwiftUI

struct SafetyRecordView: View {
    @EnvironmentObject private var evidenceStore: EvidenceStore
    @EnvironmentObject private var journeyStore: SafeJourneyStore

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                if let session = journeyStore.session {
                    VStack(alignment: .leading, spacing: 6) {
                        Label("안심 귀가 진행 중", systemImage: "figure.walk.motion")
                            .font(.headline).foregroundStyle(.blue)
                        Text("목적지: \(session.destination)")
                        Text("도착 예정: \(session.expectedArrivalAt.formatted(date: .omitted, time: .shortened))")
                            .font(.subheadline).foregroundStyle(.secondary)
                    }
                    .padding(16)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(Color.blue.opacity(0.08), in: RoundedRectangle(cornerRadius: 18))
                }

                NavigationLink { EvidenceVaultView() } label: {
                    recordCard(
                        icon: "externaldrive.badge.checkmark",
                        title: "증거 보존함",
                        subtitle: "저장된 기록 \(evidenceStore.records.count)개",
                        accent: .purple
                    )
                }

                NavigationLink { SafeJourneyView() } label: {
                    recordCard(
                        icon: "figure.walk.motion",
                        title: "안심 귀가",
                        subtitle: journeyStore.session == nil ? "새 귀가 세션 시작" : "현재 귀가 상태 확인",
                        accent: .blue
                    )
                }

                if !evidenceStore.records.isEmpty {
                    VStack(alignment: .leading, spacing: 10) {
                        Text("최근 보존 기록").font(.title3.bold())
                        ForEach(evidenceStore.records.prefix(3)) { record in
                            VStack(alignment: .leading, spacing: 4) {
                                Text(record.title).font(.headline)
                                Text(record.createdAt.formatted(date: .abbreviated, time: .shortened))
                                    .font(.caption).foregroundStyle(.secondary)
                            }
                            .padding(14)
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .background(.background, in: RoundedRectangle(cornerRadius: 15))
                        }
                    }
                }
            }
            .padding()
        }
        .background(Color(red: 0.96, green: 0.98, blue: 1.0))
        .navigationTitle("안전 기록")
    }

    private func recordCard(icon: String, title: String, subtitle: String, accent: Color) -> some View {
        HStack(spacing: 14) {
            Image(systemName: icon)
                .font(.title2).foregroundStyle(accent)
                .frame(width: 48, height: 48)
                .background(accent.opacity(0.10), in: Circle())
            VStack(alignment: .leading, spacing: 4) {
                Text(title).font(.headline).foregroundStyle(.primary)
                Text(subtitle).font(.subheadline).foregroundStyle(.secondary)
            }
            Spacer()
            Image(systemName: "chevron.right").foregroundStyle(.tertiary)
        }
        .padding(16)
        .background(.background, in: RoundedRectangle(cornerRadius: 18))
    }
}
