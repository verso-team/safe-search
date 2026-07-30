import SwiftUI

struct SafeQueryView: View {
    let queries: [String]
    @Environment(\.openURL) private var openURL

    var body: some View {
        VStack(spacing: 8) {
            ForEach(queries, id: \.self) { query in
                SafeQueryChip(query: query) {
                    let encoded = query.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? query
                    if let url = URL(string: "https://www.google.com/search?q=\(encoded)") { openURL(url) }
                }
            }
        }
    }
}

#Preview { SafeQueryView(queries: MockSafetyAnalysis.highRisk.safeSearchQueries).padding() }

