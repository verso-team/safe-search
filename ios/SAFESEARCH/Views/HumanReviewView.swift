import SwiftUI

struct HumanReviewView: View {
    let isRequired: Bool
    @State private var showInfo = false

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack(alignment: .top, spacing: 12) {
                Image(systemName: isRequired ? "person.2.badge.gearshape.fill" : "checkmark.shield.fill")
                    .font(.title3)
                    .foregroundStyle(isRequired ? .purple : .green)

                VStack(alignment: .leading, spacing: 5) {
                    Text(isRequired ? "사람의 추가 검토가 필요해" : "자동 분석이 완료됐어")
                        .font(.headline)
                    Text(isRequired
                         ? "가디의 분석만으로 확정하지 않고, 사람이 다시 확인할 수 있는 단계로 넘기는 구조야."
                         : "상황이 달라지거나 불안이 커지면 다시 분석하거나 공식기관에 확인해줘.")
                        .font(.subheadline).foregroundStyle(.secondary)
                }
            }

            if isRequired {
                Button("Human Review 동작 방식 보기") { showInfo = true }
                    .buttonStyle(.bordered)
                    .tint(.purple)
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(16)
        .background((isRequired ? Color.purple : Color.green).opacity(0.08), in: RoundedRectangle(cornerRadius: 18))
        .sheet(isPresented: $showInfo) {
            NavigationStack {
                VStack(alignment: .leading, spacing: 16) {
                    Text("Human Review")
                        .font(.title2.bold())
                    Text("현재 프로토타입은 '사람 검토가 필요한 사례'를 표시하는 단계까지 구현돼 있어. 실제 전문가 배정·상담 연결은 운영기관과의 연계 정책이 확정된 뒤 붙여야 해.")
                        .foregroundStyle(.secondary)
                    Text("따라서 앱은 AI 판단을 범죄 확정이나 법률 판단처럼 표현하지 않고, 공식기관 상담을 함께 안내해.")
                    Spacer()
                }
                .padding()
                .toolbar {
                    ToolbarItem(placement: .confirmationAction) {
                        Button("닫기") { showInfo = false }
                    }
                }
            }
            .presentationDetents([.medium])
        }
    }
}

#Preview { HumanReviewView(isRequired: true).padding() }
