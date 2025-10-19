"""
pytest 설정 및 공통 fixture (Mock 데이터 사용)
"""
import pytest
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class MockAPIClient:
    """Charles에서 캡처한 데이터 기반 Mock API 클라이언트"""
    
    def __init__(self):
        self.zones_data = self._load_zones_data()
    
    def _load_zones_data(self):
        """zones.json 로드"""
        zones_file = os.path.join('data', 'zones.json')
        if os.path.exists(zones_file):
            with open(zones_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"zones": [], "total_count": 0}
    
    def list_zones(self, timeout=10):
        """ListSimpleZones API Mock"""
        return {
            "zones": self.zones_data.get("zones", []),
            "total_count": self.zones_data.get("total_count", 52),
            "status": "success"
        }
    
    def list_simple_zones(self):
        """Alias for list_zones"""
        return self.list_zones()
    
    def get_zone_operation_info(self, zone_id):
        """GetZoneOperationInfo API Mock"""
        zone = next((z for z in self.zones_data["zones"] if z["id"] == zone_id), None)
        if not zone:
            return None
        
        return {
            "zone_id": zone_id,
            "zone_name": zone["name"],
            "city": zone["city"],
            "status": zone.get("status", "active"),
            "operation_status": "operating",
            "operating_hours": {
                "weekday": "06:00-23:00",
                "weekend": "07:00-22:00"
            }
        }
    
    def close(self):
        """세션 종료"""
        pass


@pytest.fixture(scope="session")
def api_client():
    """API 클라이언트 fixture - Mock 사용"""
    client = MockAPIClient()
    yield client
    client.close()


@pytest.fixture(scope="function")
def appium_driver():
    """Appium 드라이버 fixture"""
    pytest.skip("Appium 설정 필요")


@pytest.fixture(scope="function")
def ddokta_bus_page(appium_driver):
    """똑버스 Page Object fixture"""
    pytest.skip("UI 테스트 준비 중")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """테스트 실패 시 스크린샷 캡처"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        pass


def pytest_runtest_setup(item):
    """테스트 시작 전"""
    print(f"\n▶ {item.name}")


def pytest_runtest_teardown(item, nextitem):
    """테스트 종료 후"""
    pass