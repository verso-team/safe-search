import SwiftUI

struct HomeView: View {
    @State private var input = ""
    @FocusState private var isFocused: Bool

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 24) {
                    NasumiGuideView(message: "당황하지 않아도 괜찮아요.\n필요한 것부터 확인해볼게요.")

                    VStack(alignment: .leading, spacing: 10) {
                        Text("어떤 상황인지 알려주세요").font(.title2.bold())
                        Text("이름, 연락처, 계좌번호 등 개인정보는 적지 않아도 됩니다.")
                            .font(.subheadline).foregroundStyle(.secondary)

                        TextEditor(text: $input)
                            .focused($isFocused)
                            .frame(minHeight: 180)
                            .padding(10)
                            .scrollContentBackground(.hidden)
                            .background(Color(.secondarySystemBackground), in: RoundedRectangle(cornerRadius: 16))
                            .overlay(alignment: .topLeading) {
                                if input.isEmpty {
                                    Text("예: 영상이 퍼지고 있는데 어디로 신고해야 할지 모르겠어요.")
                                        .foregroundStyle(.tertiary).padding(16).allowsHitTesting(false)
                                }
                            }
                            .accessibilityLabel("피해 상황 입력")
                    }

                    NavigationLink {
                        AnalysisView(input: input)
                    } label: {
                        Label("안전하게 분석하기", systemImage: "shield.lefthalf.filled")
                            .font(.headline).frame(maxWidth: .infinity).padding()
                    }
                    .buttonStyle(.borderedProminent).tint(.indigo)
                    .disabled(input.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)

                    Label("즉각적인 생명·신체 위험이 있다면 112에 먼저 연락하세요.", systemImage: "phone.fill")
                        .font(.footnote.weight(.medium)).foregroundStyle(.red)
                }
                .padding()
            }
            .navigationTitle("SAFE:SEARCH")
            .onTapGesture { isFocused = false }
        }
    }
}

#Preview { HomeView() }

