"""
Appium 연결 테스트
ui/tests/ 폴더에 임시로 생성
"""
import pytest


@pytest.mark.ui
def test_appium_connection(appium_driver):
    """Appium 드라이버 연결 테스트"""
    print(f"\n현재 Activity: {appium_driver.current_activity}")
    print(f"현재 Package: {appium_driver.current_package}")
    
    assert appium_driver is not None
    assert appium_driver.current_package == "com.hyundai.shucle.gmaas"