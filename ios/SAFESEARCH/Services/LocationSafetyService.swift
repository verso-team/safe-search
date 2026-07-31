import CoreLocation
import Foundation

@MainActor
final class LocationSafetyService: NSObject, ObservableObject, CLLocationManagerDelegate {
    @Published private(set) var lastLocation: CLLocation?
    @Published private(set) var authorizationStatus: CLAuthorizationStatus
    @Published private(set) var locationError: String?

    private let manager = CLLocationManager()

    override init() {
        authorizationStatus = manager.authorizationStatus
        super.init()
        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyBest
    }

    func requestCurrentLocation() {
        locationError = nil

        switch manager.authorizationStatus {
        case .notDetermined:
            manager.requestWhenInUseAuthorization()
        case .authorizedAlways, .authorizedWhenInUse:
            manager.requestLocation()
        case .denied, .restricted:
            locationError = "위치 권한이 꺼져 있어요. 설정에서 위치 접근을 허용해주세요."
        @unknown default:
            locationError = "위치 권한 상태를 확인할 수 없어요."
        }
    }

    /// 안심 귀가 화면이 열려 있는 동안 위치를 갱신한다.
    /// 백그라운드 실시간 공유는 별도 서버·권한·정책 설계가 필요한 후속 기능이다.
    func startContinuousUpdates() {
        switch manager.authorizationStatus {
        case .notDetermined:
            manager.requestWhenInUseAuthorization()
        case .authorizedAlways, .authorizedWhenInUse:
            manager.startUpdatingLocation()
        default:
            locationError = "위치 권한을 확인해주세요."
        }
    }

    func stopContinuousUpdates() {
        manager.stopUpdatingLocation()
    }

    var coordinateText: String? {
        guard let coordinate = lastLocation?.coordinate else { return nil }
        return String(format: "%.6f, %.6f", coordinate.latitude, coordinate.longitude)
    }

    var mapsURL: URL? {
        guard let coordinate = lastLocation?.coordinate else { return nil }
        return URL(string: "https://maps.apple.com/?ll=\(coordinate.latitude),\(coordinate.longitude)")
    }

    var shareText: String {
        var text = "SAFE:SEARCH에서 현재 위치를 공유합니다."
        if let coordinateText { text += "\n위치: \(coordinateText)" }
        if let mapsURL { text += "\n지도: \(mapsURL.absoluteString)" }
        text += "\n전송 시각: \(Date.now.formatted(date: .numeric, time: .shortened))"
        return text
    }

    func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        authorizationStatus = manager.authorizationStatus
        if manager.authorizationStatus == .authorizedWhenInUse || manager.authorizationStatus == .authorizedAlways {
            manager.requestLocation()
        }
    }

    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        lastLocation = locations.last
        locationError = nil
    }

    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        locationError = error.localizedDescription
    }
}
