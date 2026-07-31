import SwiftUI

struct EvidenceVaultView: View {
    @EnvironmentObject private var evidenceStore: EvidenceStore
    @EnvironmentObject private var locationService: LocationSafetyService

    @State private var kind: EvidenceKind = .note
    @State private var title = ""
    @State private var content = ""
    @State private var includeLocation = true

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                GuardianTigerGuideView(message: "증거는 원문을 임의로 수정하기보다, 시간과 출처를 함께 남겨두는 게 좋아.")

                editor
                screenshotGuide
                savedRecords
            }
            .padding()
        }
        .background(Color(red: 0.96, green: 0.98, blue: 1.0))
        .navigationTitle("증거 보존함")
    }

    private var editor: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("새 기록 보존").font(.title3.bold())

            Picker("종류", selection: $kind) {
                ForEach(EvidenceKind.allCases) { kind in
                    Text(kind.displayName).tag(kind)
                }
            }
            .pickerStyle(.menu)

            TextField("제목", text: $title)
                .textFieldStyle(.roundedBorder)

            TextField("문자 내용, URL, 전화번호, 계정명, 메모", text: $content, axis: .vertical)
                .lineLimit(4...8)
                .textFieldStyle(.roundedBorder)

            Toggle("현재 위치 함께 저장", isOn: $includeLocation)
                .onChange(of: includeLocation) { enabled in
                    if enabled { locationService.requestCurrentLocation() }
                }

            if includeLocation {
                HStack {
                    Text(locationService.coordinateText ?? "위치 미확인")
                        .font(.caption).foregroundStyle(.secondary)
                    Spacer()
                    Button("위치 갱신") { locationService.requestCurrentLocation() }
                        .font(.caption)
                }
            }

            Button {
                evidenceStore.add(
                    kind: kind,
                    title: title,
                    content: content,
                    coordinate: includeLocation ? locationService.coordinateText : nil
                )
                title = ""
                content = ""
            } label: {
                Label("시간과 함께 보존", systemImage: "externaldrive.badge.checkmark")
                    .font(.headline).frame(maxWidth: .infinity).padding()
            }
            .buttonStyle(.borderedProminent)
            .tint(.purple)
            .disabled(content.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
        }
        .padding(18)
        .background(.background, in: RoundedRectangle(cornerRadius: 20))
    }

    private var screenshotGuide: some View {
        VStack(alignment: .leading, spacing: 8) {
            Label("스크린샷 가이드", systemImage: "camera.viewfinder")
                .font(.headline)
            Text("• 발신자/계정명과 시간 정보가 같이 보이게 저장\n• URL은 주소 전체가 보이도록 기록\n• 송금·대화 기록은 원본을 지우지 말고 별도로 보관\n• 캡처 이미지를 편집해 원본과 섞지 않기")
                .font(.subheadline).foregroundStyle(.secondary)
        }
        .padding(16)
        .background(Color.purple.opacity(0.07), in: RoundedRectangle(cornerRadius: 18))
    }

    private var savedRecords: some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack {
                Text("보존된 기록").font(.title3.bold())
                Spacer()
                if !evidenceStore.records.isEmpty {
                    ShareLink(item: evidenceStore.exportText()) {
                        Label("내보내기", systemImage: "square.and.arrow.up")
                            .font(.caption)
                    }
                }
            }

            if evidenceStore.records.isEmpty {
                Text("아직 저장된 기록이 없어.")
                    .font(.subheadline).foregroundStyle(.secondary)
                    .padding(.vertical, 20)
            } else {
                ForEach(evidenceStore.records) { record in
                    VStack(alignment: .leading, spacing: 7) {
                        HStack {
                            Text(record.title).font(.headline)
                            Spacer()
                            Text(record.kind.displayName)
                                .font(.caption).foregroundStyle(.purple)
                        }
                        Text(record.content)
                            .font(.subheadline)
                            .lineLimit(3)
                        Text(record.createdAt.formatted(date: .abbreviated, time: .shortened))
                            .font(.caption).foregroundStyle(.secondary)
                        if let coordinate = record.coordinate {
                            Label(coordinate, systemImage: "location")
                                .font(.caption2).foregroundStyle(.secondary)
                        }
                    }
                    .padding(14)
                    .background(.background, in: RoundedRectangle(cornerRadius: 16))
                    .contextMenu {
                        Button(role: .destructive) {
                            evidenceStore.delete(record)
                        } label: {
                            Label("삭제", systemImage: "trash")
                        }
                    }
                }
            }
        }
    }
}
