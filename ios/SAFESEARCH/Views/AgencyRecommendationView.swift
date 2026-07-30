import SwiftUI

struct AgencyRecommendationView: View {
    let agencies: [Agency]
    var body: some View {
        VStack(spacing: 10) {
            ForEach(agencies) { AgencyCard(agency: $0) }
        }
    }
}

#Preview { AgencyRecommendationView(agencies: MockSafetyAnalysis.highRisk.recommendedAgencies).padding() }

