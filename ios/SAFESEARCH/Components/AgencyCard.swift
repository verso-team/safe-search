import SwiftUI

struct AgencyCard: View {
    let agency: Agency

    var body: some View {
        Link(destination: agency.website) {
            HStack(spacing: 12) {
                Image(systemName: "building.columns.fill")
                    .foregroundStyle(.indigo).frame(width: 32)
                VStack(alignment: .leading, spacing: 4) {
                    Text(agency.name).font(.headline).foregroundStyle(.primary)
                    Text(agency.role).font(.subheadline).foregroundStyle(.secondary)
                    if let phone = agency.phone {
                        Text(phone).font(.subheadline.bold()).foregroundStyle(.indigo)
                    }
                }
                Spacer()
                Image(systemName: "arrow.up.right").foregroundStyle(.secondary)
            }
            .padding(14)
            .background(.background, in: RoundedRectangle(cornerRadius: 16))
            .overlay(RoundedRectangle(cornerRadius: 16).stroke(Color.secondary.opacity(0.16)))
        }
        .accessibilityHint("공식 웹사이트 열기")
    }
}

#Preview { AgencyCard(agency: InstitutionService.shared.police).padding() }

