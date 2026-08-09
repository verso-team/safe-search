import SwiftUI

struct SafeSearchHubView: View {
    @State private var input: String
    @Environment(\.openURL) private var openURL
    private let rewriter = SafeQueryRewriter()

    init(initialText: String = "") {
        _input = State(initialValue: initialText)
    }

    private var queries: [String] {
        rewriter.rewrite(input)
    }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 22) {
                GuardianTigerGuideView(message: "검색어가 불안하거나 광고·2차 사기가 걱정되면 공식 정보 중심으로 다시 바꿔줄게.")

                VStack(alignment: .leading, spacing: 10) {
                    Text("원래 검색하려던 말").font(.headline)
                    TextField("예: 몸캠피싱 영상 삭제 업체", text: $input, axis: .vertical)
                        .textFieldStyle(.roundedBorder)
                }
                .padding(16)
                .background(.background, in: RoundedRectangle(cornerRadius: 18))

                VStack(alignment: .leading, spacing: 12) {
                    Label("Safe Query", systemImage: "shield.lefthalf.filled")
                        .font(.title3.bold()).foregroundStyle(.indigo)
                    Text("공식기관·증거보존·신고 절차를 먼저 찾도록 검색 의도를 바꿔.")
                        .font(.subheadline).foregroundStyle(.secondary)

                    ForEach(queries, id: \.self) { query in
                        SafeQueryChip(query: query) {
                            let encoded = query.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? query
                            if let url = URL(string: "https://www.google.com/search?q=\(encoded)") {
                                openURL(url)
                            }
                        }
                    }
                }

                NavigationLink {
                    SearchRiskCheckView()
                } label: {
                    Label("검색결과 위험 신호 확인", systemImage: "exclamationmark.shield.fill")
                        .font(.headline)
                        .frame(maxWidth: .infinity)
                        .padding()
                }
                .buttonStyle(.borderedProminent)
                .tint(.orange)

                NavigationLink { SupportHubView() } label: {
                    Label("검증된 공식기관 먼저 보기", systemImage: "checkmark.shield.fill")
                        .font(.headline).frame(maxWidth: .infinity).padding()
                }
                .buttonStyle(.borderedProminent)
                .tint(.indigo)
            }
            .padding()
        }
        .background(Color(red: 0.96, green: 0.98, blue: 1.0))
        .navigationTitle("안전하게 검색하기")
    }
}
