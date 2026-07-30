import SwiftUI

struct HumanReviewView: View {
    let isRequired: Bool

    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Image(systemName: isRequired ? "person.crop.circle.badge.questionmark" : "checkmark.shield")
                .foregroundStyle(isRequired ? .orange : .green)
            VStack(alignment: .leading, spacing: 4) {
                Text(isRequired ? "추가 확인이 필요해요" : "자동 분석이 완료됐어요").font(.headline)
                Text(isRequired
                     ? "전문가 검토가 필요한 사례로 표시했습니다. 공식기관 상담을 함께 이용해주세요."
                     : "상황이 바뀌거나 불안이 커지면 다시 분석하거나 공식기관에 문의해주세요.")
                    .font(.subheadline).foregroundStyle(.secondary)
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(16)
        .background(Color.orange.opacity(isRequired ? 0.10 : 0.04), in: RoundedRectangle(cornerRadius: 16))
    }
}

#Preview { HumanReviewView(isRequired: true).padding() }

