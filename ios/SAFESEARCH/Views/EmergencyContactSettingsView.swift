import SwiftUI

struct EmergencyContactSettingsView: View {
    @EnvironmentObject private var contactStore: SafetyContactStore

    private var nameBinding: Binding<String> {
        Binding(
            get: { contactStore.contact.name },
            set: { contactStore.contact.name = $0 }
        )
    }

    private var phoneBinding: Binding<String> {
        Binding(
            get: { contactStore.contact.phone },
            set: { contactStore.contact.phone = $0 }
        )
    }

    var body: some View {
        Form {
            Section("주 보호자") {
                TextField("이름", text: nameBinding)
                TextField("전화번호", text: phoneBinding)
                    .keyboardType(.phonePad)
            }

            Section {
                Text("SAFE:SEARCH는 사용자의 확인 없이 자동으로 문자를 보내지 않아. SOS 화면에서 메시지를 준비하고, 실제 전송은 사용자가 최종 확인해.")
                    .font(.footnote).foregroundStyle(.secondary)
            }
        }
        .navigationTitle("보호자 설정")
    }
}
