import SwiftUI

struct SafetyGuideInfoView: View {
    var body: some View {
        List {
            Section("SAFE:SEARCH가 하는 일") {
                Label("피해 상황 구조화 분석", systemImage: "brain.head.profile")
                Label("Safe Query 생성", systemImage: "shield.lefthalf.filled")
                Label("공식기관 우선 연결", systemImage: "checkmark.seal.fill")
                Label("사람 추가 검토 필요 여부 표시", systemImage: "person.2.fill")
            }
            Section("개인 안전 기능") {
                Label("SOS와 112 연결", systemImage: "sos.circle.fill")
                Label("현재 위치·보호자 공유", systemImage: "location.fill")
                Label("안심 귀가", systemImage: "figure.walk.motion")
                Label("증거 보존", systemImage: "externaldrive.badge.checkmark")
            }
            Section("중요") {
                Text("AI 분석은 범죄 확정, 법률 판단, 경찰 신고를 대신하지 않아. 즉각적인 생명·신체 위험이 있으면 안전한 장소로 이동하고 112에 연락해야 해.")
            }
        }
        .navigationTitle("SAFE 이용 가이드")
    }
}
