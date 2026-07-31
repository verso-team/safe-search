import SwiftUI

struct RootTabView: View {
    @StateObject private var locationService = LocationSafetyService()
    @StateObject private var contactStore = SafetyContactStore()
    @StateObject private var journeyStore = SafeJourneyStore()
    @StateObject private var evidenceStore = EvidenceStore()

    var body: some View {
        TabView {
            NavigationStack { HomeView() }
                .tabItem { Label("홈", systemImage: "house.fill") }

            NavigationStack { SafeSearchHubView() }
                .tabItem { Label("안전검색", systemImage: "shield.lefthalf.filled") }

            NavigationStack { SupportHubView() }
                .tabItem { Label("지원기관", systemImage: "building.columns.fill") }

            NavigationStack { SafetyRecordView() }
                .tabItem { Label("기록", systemImage: "folder.fill") }
        }
        .tint(.indigo)
        .environmentObject(locationService)
        .environmentObject(contactStore)
        .environmentObject(journeyStore)
        .environmentObject(evidenceStore)
    }
}
