import SwiftUI

struct HomeView: View {
    @State private var input = ""
    @FocusState private var isFocused: Bool

    private let columns = [
        GridItem(.flexible(), spacing: 10),
        GridItem(.flexible(), spacing: 10),
        GridItem(.flexible(), spacing: 10)
    ]

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 22) {
                hero
                inputCard
                quickActions
                safetyTools
                emergencyStrip
            }
            .padding()
        }
        .background(Color(red: 0.96, green: 0.98, blue: 1.0))
        .navigationTitle("SAFE:SEARCH")
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItemGroup(placement: .navigationBarTrailing) {
                Button(action: {}) { Image(systemName: "bell") }
                Menu {
                    NavigationLink("보호자 설정") { EmergencyContactSettingsView() }
                    NavigationLink("SAFE 이용 가이드") { SafetyGuideInfoView() }
                } label: {
                    Image(systemName: "line.3.horizontal")
                }
            }
        }
        .onTapGesture { isFocused = false }
    }

    private var hero: some View {
        HStack(spacing: 14) {
            VStack(alignment: .leading, spacing: 6) {
                Text("가디가")
                    .font(.title2.bold()).foregroundStyle(.indigo)
                Text("안전하게 확인해줄게")
                    .font(.title2.bold())
                Text("무엇이든 편하게 알려줘.")
                    .font(.subheadline).foregroundStyle(.secondary)
            }
            Spacer()
            Image("GuardianTiger")
                .resizable()
                .scaledToFit()
                .frame(width: 110, height: 92)
                .clipShape(RoundedRectangle(cornerRadius: 24))
        }
        .padding(20)
        .background(
            LinearGradient(
                colors: [Color.indigo.opacity(0.10), Color.blue.opacity(0.05)],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            ),
            in: RoundedRectangle(cornerRadius: 22)
        )
    }

    private var inputCard: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("어떤 상황인지 알려줘")
                .font(.headline)

            TextEditor(text: $input)
                .focused($isFocused)
                .frame(minHeight: 150)
                .padding(10)
                .scrollContentBackground(.hidden)
                .background(Color(.secondarySystemBackground), in: RoundedRectangle(cornerRadius: 16))
                .overlay(alignment: .topLeading) {
                    if input.isEmpty {
                        Text("예: 모르는 사람이 내 영상을 가지고 돈을 요구해.")
                            .foregroundStyle(.tertiary)
                            .padding(16)
                            .allowsHitTesting(false)
                    }
                }
                .accessibilityLabel("피해 상황 입력")

            NavigationLink {
                AnalysisView(input: input)
            } label: {
                Label("안전하게 분석하기", systemImage: "magnifyingglass")
                    .font(.headline)
                    .frame(maxWidth: .infinity)
                    .padding()
            }
            .buttonStyle(.borderedProminent)
            .tint(.indigo)
            .disabled(input.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
        }
        .padding(16)
        .background(.background, in: RoundedRectangle(cornerRadius: 20))
    }

    private var quickActions: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("빠르게 확인하기").font(.title3.bold())

            LazyVGrid(columns: columns, spacing: 10) {
                NavigationLink { SuspiciousCheckView(kind: .message) } label: {
                    QuickActionTile(title: "문자", subtitle: "스미싱", systemImage: "message.fill")
                }
                NavigationLink { SuspiciousCheckView(kind: .link) } label: {
                    QuickActionTile(title: "링크", subtitle: "URL", systemImage: "link")
                }
                NavigationLink { SuspiciousCheckView(kind: .phone) } label: {
                    QuickActionTile(title: "전화", subtitle: "모르는 번호", systemImage: "phone.fill")
                }
                NavigationLink {
                    SuspiciousCheckView(
                        kind: .message,
                        initialText: "계정 복구를 해준다며 돈이나 인증번호를 요구받았어요."
                    )
                } label: {
                    QuickActionTile(title: "계정", subtitle: "탈취", systemImage: "person.crop.circle.badge.exclamationmark")
                }
                NavigationLink { ThreatSafetyView() } label: {
                    QuickActionTile(title: "협박", subtitle: "피해", systemImage: "exclamationmark.triangle.fill", accent: .orange)
                }
                NavigationLink { SupportHubView() } label: {
                    QuickActionTile(title: "신고", subtitle: "기관 찾기", systemImage: "checkmark.shield.fill")
                }
            }
            .buttonStyle(.plain)
        }
    }

    private var safetyTools: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("안전 기능").font(.title3.bold())

            NavigationLink { SafeJourneyView() } label: {
                featureRow(
                    icon: "figure.walk.motion",
                    title: "안심 귀가 모드",
                    subtitle: "도착 예정시간과 보호자 공유를 준비해",
                    accent: .blue
                )
            }
            NavigationLink { EvidenceVaultView() } label: {
                featureRow(
                    icon: "externaldrive.badge.checkmark",
                    title: "증거 자동 보존 모드",
                    subtitle: "시간·위치·문자·링크·번호를 한곳에 기록해",
                    accent: .purple
                )
            }
        }
        .buttonStyle(.plain)
    }

    private var emergencyStrip: some View {
        NavigationLink {
            EmergencySOSView()
        } label: {
            HStack(spacing: 12) {
                Image(systemName: "sos.circle.fill")
                    .font(.title2).foregroundStyle(.red)
                VStack(alignment: .leading, spacing: 3) {
                    Text("지금 위험하거나 긴급한 상황이야?").font(.headline)
                    Text("SOS · 현재 위치 공유 · 보호자 알림 · 112 연결")
                        .font(.caption).foregroundStyle(.secondary)
                }
                Spacer()
                Image(systemName: "chevron.right").foregroundStyle(.secondary)
            }
            .padding(16)
            .background(Color.red.opacity(0.06), in: RoundedRectangle(cornerRadius: 18))
        }
        .buttonStyle(.plain)
    }

    private func featureRow(icon: String, title: String, subtitle: String, accent: Color) -> some View {
        HStack(spacing: 14) {
            Image(systemName: icon)
                .font(.title3.weight(.semibold))
                .foregroundStyle(accent)
                .frame(width: 42, height: 42)
                .background(accent.opacity(0.10), in: Circle())
            VStack(alignment: .leading, spacing: 4) {
                Text(title).font(.headline).foregroundStyle(.primary)
                Text(subtitle).font(.subheadline).foregroundStyle(.secondary)
            }
            Spacer()
            Image(systemName: "chevron.right").foregroundStyle(.tertiary)
        }
        .padding(15)
        .background(.background, in: RoundedRectangle(cornerRadius: 17))
    }
}

#Preview {
    NavigationStack { HomeView() }
}
