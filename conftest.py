"""
pytest 설정 및 공통 fixture (Mock 데이터 + Allure 통합)
"""
import pytest
import allure
import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# ========================================
# Allure 환경 정보
# ========================================

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Allure 환경 정보 설정"""
    if not hasattr(config, 'workerinput'):
        allure_dir = config.getoption('--alluredir')
        if allure_dir:
            env_path = os.path.join(allure_dir, 'environment.properties')
            
            with open(env_path, 'w', encoding='utf-8') as f:
                f.write('Application=똑타(DDOKTA) 앱\n')
                f.write('Test.Environment=Android\n')
                f.write('Device=SM-S921N (Galaxy S24)\n')
                f.write('OS.Version=Android 16\n')
                f.write('Appium.Version=2.x\n')
                f.write('Python.Version=3.11.9\n')
                f.write('Framework=Pytest + Appium\n')


# ========================================
# Mock API Client
# ========================================

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
        """GetZoneOperationInfo API Mock - 실제 응답 구조 반영"""
        zone = next((z for z in self.zones_data["zones"] if z["id"] == zone_id), None)
        if not zone:
            return None
        
        return {
            "zone_id": zone_id,
            "zone_name": zone["name"],
            "city": zone["city"],
            "status": zone.get("status", "active"),
            "image_url": f"https://d1fxl86ei6civ0.cloudfront.net/zone_images/{zone_id}/sample.png",
            "operation_hours": "06:00~23:29",
            "operation_days": "매일/공휴일",
            "vehicle_count": 10,
            "drt_type": "실시간 호출에 따라 배차되며, 경로가 같은 승객과 합승할 수 있습니다.",
            "routes": [
                "신곡리↔고촌역",
                "김포공항역↔신곡리",
                "김포공항역↔향산리"
            ],
            "grpc_status": 0,
            "grpc_message": ""
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


# ========================================
# Appium Driver Fixture (Allure 통합)
# ========================================

@pytest.fixture(scope="function")
@allure.title("Appium 드라이버 초기화")
def appium_driver(request):
    """
    Appium WebDriver fixture with Allure integration
    
    Args:
        request: pytest request object
    
    Yields:
        WebDriver: Appium WebDriver instance
    """
    from appium import webdriver
    from appium.options.android import UiAutomator2Options
    
    with allure.step("Appium 드라이버 설정"):
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = "SM-S921N"
        options.app_package = "com.hyundai.shucle.gmaas"
        options.app_activity = "com.hyundai.airlab.shucle.presenter.MainActivity"
        options.automation_name = "UiAutomator2"
        options.no_reset = True
        options.full_reset = False
        options.new_command_timeout = 300
        options.uiautomator2_server_launch_timeout = 60000
        
        allure.attach(
            f"Package: {options.app_package}\n"
            f"Activity: {options.app_activity}\n"
            f"Device: {options.device_name}",
            name="Appium_설정",
            attachment_type=allure.attachment_type.TEXT
        )
    
    driver = None
    try:
        with allure.step("Appium 서버 연결"):
            driver = webdriver.Remote(
                "http://127.0.0.1:4724",
                options=options
            )
            driver.implicitly_wait(10)
        
        # 초기 스크린샷
        try:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="초기_화면",
                attachment_type=allure.attachment_type.PNG
            )
        except:
            pass
        
        # 앱을 홈 화면으로 초기화
        try:
            # 뒤로가기 버튼을 여러 번 눌러 홈으로 이동
            for _ in range(3):
                driver.back()
                time.sleep(0.5)
        except:
            pass
        
        # 앱 재시작으로 확실하게 홈 화면으로
        try:
            driver.terminate_app(options.app_package)
            time.sleep(1)
            driver.activate_app(options.app_package)
            time.sleep(2)
        except:
            pass
        
        yield driver
        
        # 테스트 실패 시 최종 스크린샷 캡처
        if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="실패_시_화면",
                    attachment_type=allure.attachment_type.PNG
                )
            except:
                pass
        
        # 테스트 종료 후 앱 초기화
        try:
            driver.terminate_app(options.app_package)
            time.sleep(1)
            driver.activate_app(options.app_package)
            time.sleep(1)
        except:
            pass
        
    except Exception as e:
        pytest.skip(f"Appium 연결 실패: {str(e)}")
    finally:
        if driver:
            with allure.step("Appium 드라이버 종료"):
                try:
                    driver.quit()
                except:
                    pass


@pytest.fixture(scope="function")
def ddokta_bus_page(appium_driver):
    """똑버스 Page Object fixture"""
    from mobile.pages.ddokta_bus_page import DdoktaBusPage
    return DdoktaBusPage(appium_driver)


# ========================================
# Pytest Hooks
# ========================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    테스트 실행 결과를 캡처하여 실패 시 스크린샷을 찍을 수 있도록 함
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def pytest_runtest_setup(item):
    """테스트 시작 전"""
    print(f"\n▶ {item.name}")


def pytest_runtest_teardown(item, nextitem):
    """테스트 종료 후"""
    pass


def pytest_collection_modifyitems(config, items):
    """테스트 아이템에 자동으로 마커 추가"""
    for item in items:
        # 파일 경로 기반 마커 추가
        if "api" in str(item.fspath):
            item.add_marker(pytest.mark.api)
        elif "mobile" in str(item.fspath) or "ui" in str(item.fspath):
            item.add_marker(pytest.mark.ui)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # E2E 테스트 마커
        if "e2e" in item.name.lower() or "end_to_end" in item.name.lower():
            item.add_marker(pytest.mark.e2e)