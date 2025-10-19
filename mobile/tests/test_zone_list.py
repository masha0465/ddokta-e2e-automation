"""
Allure 리포트가 적용된 E2E 테스트
파일: mobile/tests/test_zone_list.py
목적지: 김포공항역 9호선
"""
import pytest
import time
import allure
from mobile.pages.ddokta_bus_page import DdoktaBusPage
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature('똑타 앱')
@allure.story('Zone 목록')
class TestZoneListUI:
    """Zone 목록 UI 테스트"""
    
    @pytest.fixture
    def page(self, appium_driver):
        """Page Object fixture"""
        return DdoktaBusPage(appium_driver)
    
    @allure.title("Zone 목록이 정상적으로 로드되는지 확인")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_zone_list_loaded(self, page):
        """Zone 목록이 정상적으로 로드되는지 확인"""
        page.click_ddokta_bus_menu()
        page.click_explore_button()
        
        assert page.wait_for_zone_list(timeout=10), "Zone 목록이 로드되지 않았습니다"
        
        zone_count = page.get_zone_count()
        assert zone_count > 0, f"Zone이 없습니다. 발견된 Zone: {zone_count}개"
        
        print(f"✅ Zone 목록 로드 성공: {zone_count}개")
    
    @allure.title("Zone 목록에 충분한 항목이 있는지 확인")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    def test_zone_list_has_multiple_items(self, page):
        """Zone 목록에 여러 개의 항목이 있는지 확인"""
        page.click_ddokta_bus_menu()
        page.click_explore_button()
        page.wait_for_zone_list()
        
        zone_count = page.get_zone_count()
        assert zone_count >= 5, f"Zone이 충분하지 않습니다. 발견된 Zone: {zone_count}개"
        
        print(f"✅ Zone 개수 확인 성공: {zone_count}개")
    
    @pytest.mark.skip(reason="김포 Zone 검색 테스트 - 스크롤 로직 개선 필요")
    @allure.title("특정 Zone을 검색할 수 있는지 확인")
    @allure.severity(allure.severity_level.NORMAL)
    def test_specific_zone_search(self, page):
        """특정 Zone을 검색할 수 있는지 확인"""
        page.click_ddokta_bus_menu()
        page.click_explore_button()
        page.wait_for_zone_list()
        
        gimpo_element = page.scroll_to_element("김포")
        
        assert gimpo_element is not None, "김포 Zone을 찾을 수 없습니다"
        print("✅ 김포 Zone 발견")
    
    @allure.title("Zone 상세 화면으로 이동")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    def test_zone_detail_navigation(self, page):
        """Zone 상세 화면으로 이동할 수 있는지 확인"""
        page.click_ddokta_bus_menu()
        page.click_explore_button()
        page.wait_for_zone_list()
        
        from mobile.locators.ddokta_bus_locators import DdoktaBusLocators
        zones = page.driver.find_elements(*DdoktaBusLocators.ZONE_ITEM)
        assert len(zones) > 0, "Zone이 없습니다"
        
        zones[0].click()
        time.sleep(2)
        
        page.take_screenshot("zone_detail.png")
        print("✅ Zone 상세 화면 진입 성공")
    
    @allure.title("UI 요소들이 화면에 표시되는지 확인")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    def test_ui_elements_visible(self, page):
        """주요 UI 요소들이 화면에 표시되는지 확인"""
        page.click_ddokta_bus_menu()
        page.click_explore_button()
        page.wait_for_zone_list()
        
        from mobile.locators.ddokta_bus_locators import DdoktaBusLocators
        zone_list = page.driver.find_element(*DdoktaBusLocators.ZONE_LIST)
        
        assert zone_list.is_displayed(), "Zone 목록이 화면에 표시되지 않습니다"
        print("✅ UI 요소 표시 확인 성공")


@allure.feature('똑타 앱')
@allure.story('버스 예약')
@allure.suite('E2E 테스트')
class TestDestinationAndBusList:
    """목적지 선택 및 버스 리스트 E2E 테스트"""
    
    @pytest.fixture
    def page(self, appium_driver):
        """Page Object fixture"""
        return DdoktaBusPage(appium_driver)
    
    @allure.title("똑버스에서 김포공항역 선택 후 버스 리스트 확인")
    @allure.description("""
    E2E 시나리오:
    1. 홈 화면에서 똑버스 클릭
    2. 김포공항역 9호선 선택
    3. 버스 리스트 표시 확인
    4. 버스 정보 검증
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.e2e
    @pytest.mark.smoke
    def test_select_destination_and_check_bus_list(self, page):
        """E2E 시나리오: 목적지 선택 후 버스 리스트 확인"""
        
        print("\n🚀 E2E 테스트 시작: 똑버스 → 김포공항역 → 버스 리스트")
        
        # Step 1: 똑버스 메뉴 클릭
        print("  [1/3] 똑버스 메뉴 클릭...")
        menu_clicked = page.click_ddokta_bus_menu()
        assert menu_clicked, "똑버스 메뉴 클릭 실패"
        
        page.take_screenshot("step1_after_ddokbus.png")
        print("  ✅ 똑버스 클릭 완료")
        
        # Step 2: 김포공항역 9호선 선택
        print("  [2/3] 김포공항역 9호선 선택...")
        time.sleep(2)
        
        gimpo_airport_found = False
        
        # 방법 1: 화면에 이미 보이는 김포공항역 9호선 직접 클릭
        print("    → 방법 1: 화면의 김포공항역 9호선 직접 클릭 시도...")
        try:
            gimpo_elements = page.driver.find_elements(
                AppiumBy.XPATH,
                "//*[contains(@text, '김포공항역 9호선')]"
            )
            
            if gimpo_elements:
                gimpo_elements[0].click()
                gimpo_airport_found = True
                print(f"    ✅ 김포공항역 9호선 직접 클릭 성공 (총 {len(gimpo_elements)}개 발견)")
        except Exception as e:
            print(f"    ❌ 방법 1 실패: {e}")
        
        # 방법 2: "도착지 검색" 클릭 후 선택
        if not gimpo_airport_found:
            print("    → 방법 2: '도착지 검색' 클릭 시도...")
            try:
                search_button = page.driver.find_element(
                    AppiumBy.XPATH,
                    "//*[contains(@text, '도착지 검색')]"
                )
                search_button.click()
                print("    ✅ '도착지 검색' 클릭 성공")
                time.sleep(2)
                
                gimpo_in_search = page.driver.find_element(
                    AppiumBy.XPATH,
                    "//*[contains(@text, '김포공항역 9호선')]"
                )
                gimpo_in_search.click()
                gimpo_airport_found = True
                print("    ✅ 김포공항역 9호선 선택 성공")
                
            except Exception as e:
                print(f"    ❌ 방법 2 실패: {e}")
        
        if not gimpo_airport_found:
            print("\n  ❌ 모든 방법 실패: 김포공항역을 찾을 수 없습니다")
            all_texts = page.driver.find_elements(AppiumBy.XPATH, "//*[@text!='']")
            print("\n  📱 현재 화면:")
            for elem in all_texts[:30]:
                try:
                    print(f"     • {elem.text}")
                except:
                    pass
            page.take_screenshot("gimpo_airport_not_found.png")
        
        assert gimpo_airport_found, "김포공항역 9호선 선택 실패"
        
        page.take_screenshot("step2_after_gimpo_airport.png")
        print("  ✅ 김포공항역 선택 완료")
        
        # Step 3: 버스 리스트 확인
        print("  [3/3] 버스 리스트 확인...")
        time.sleep(3)
        
        bus_list_found = page.wait_for_bus_list(timeout=20)
        
        if bus_list_found:
            print("  ✅ 버스 리스트 발견!")
            
            bus_count = page.get_bus_count()
            print(f"  📊 발견된 버스: {bus_count}개")
            
            bus_info = page.get_bus_info()
            if bus_info:
                print(f"  🚌 버스 정보:")
                print(f"     - {bus_info['boarding_time']}")
                print(f"     - {bus_info['arrival_info']}")
            
            page.take_screenshot("step3_bus_list_final.png")
            print("  ✅ 스크린샷 저장: step3_bus_list_final.png")
            
        else:
            print("  ❌ 버스 리스트를 찾을 수 없습니다")
            page.take_screenshot("bus_list_not_found.png")
            
            all_texts = page.driver.find_elements(AppiumBy.XPATH, "//*[@text!='']")
            print("\n  📱 현재 화면의 텍스트 요소:")
            for element in all_texts[:20]:
                try:
                    text = element.text
                    if text:
                        print(f"     • {text}")
                except:
                    pass
        
        assert bus_list_found, "버스 리스트가 표시되지 않았습니다"
        print("\n✅ E2E 테스트 완료!")
    
    @allure.title("운행 시간 외 메시지 확인")
    @allure.description("""
    운행 시간 외(6시 이전, 23시 이후) 테스트:
    1. 똑버스 클릭
    2. 김포공항역 9호선 선택
    3. "지금은 운행종료 시간이에요" 메시지 확인
    
    Note: 운행 시간(6:00~23:00) 외에만 실행
    """)
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.e2e
    def test_off_hours_message(self, page):
        """운행 시간 외 메시지 표시 확인"""
        
        from datetime import datetime
        
        # 현재 시간 확인
        current_hour = datetime.now().hour
        
        # 운행 시간 중이면 테스트 스킵
        if 6 <= current_hour < 23:
            pytest.skip(f"현재 운행 시간입니다 ({current_hour}시). 운행 시간 외에만 실행 가능합니다.")
        
        print("\n🌙 운행 시간 외 테스트 시작")
        
        # 똑버스 클릭
        print("  [1/2] 똑버스 메뉴 클릭...")
        menu_clicked = page.click_ddokta_bus_menu()
        assert menu_clicked, "똑버스 메뉴 클릭 실패"
        
        # 김포공항역 선택
        print("  [2/2] 김포공항역 9호선 선택...")
        time.sleep(2)
        
        gimpo_airport_found = False
        try:
            gimpo_elements = page.driver.find_elements(
                AppiumBy.XPATH,
                "//*[contains(@text, '김포공항역 9호선')]"
            )
            if gimpo_elements:
                gimpo_elements[0].click()
                gimpo_airport_found = True
        except:
            pass
        
        assert gimpo_airport_found, "김포공항역 9호선 선택 실패"
        
        time.sleep(3)
        
        # 운행 종료 메시지 확인
        print("  [3/3] 운행 종료 메시지 확인...")
        
        off_hours_messages = [
            "지금은 운행종료 시간이에요",
            "운행종료",
            "운행 시간",
        ]
        
        message_found = False
        for message in off_hours_messages:
            try:
                element = page.driver.find_element(
                    AppiumBy.XPATH,
                    f"//*[contains(@text, '{message}')]"
                )
                message_found = True
                print(f"  ✅ 운행 종료 메시지 발견: '{element.text}'")
                break
            except:
                continue
        
        page.take_screenshot("off_hours_message.png")
        
        assert message_found, "운행 종료 메시지를 찾을 수 없습니다"
        print("\n✅ 운행 시간 외 메시지 확인 완료!")
    
    @allure.title("운행 시간 내 버스 리스트 표시 확인")
    @allure.description("""
    운행 시간 내(6:00~23:00) 테스트:
    1. 똑버스 클릭
    2. 김포공항역 9호선 선택
    3. 버스 리스트가 정상 표시되는지 확인
    
    Note: 운행 시간(6:00~23:00) 내에만 실행
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.e2e
    def test_operating_hours_bus_list(self, page):
        """운행 시간 내 버스 리스트 확인"""
        
        from datetime import datetime
        
        # 현재 시간 확인
        current_hour = datetime.now().hour
        
        # 운행 시간 외면 테스트 스킵
        if current_hour < 6 or current_hour >= 23:
            pytest.skip(f"현재 운행 시간이 아닙니다 ({current_hour}시). 06:00~23:00에만 실행 가능합니다.")
        
        print("\n🚌 운행 시간 내 테스트 시작")
        
        # 똑버스 → 김포공항역 선택
        menu_clicked = page.click_ddokta_bus_menu()
        assert menu_clicked, "똑버스 메뉴 클릭 실패"
        
        time.sleep(2)
        
        gimpo_airport_found = False
        try:
            gimpo_elements = page.driver.find_elements(
                AppiumBy.XPATH,
                "//*[contains(@text, '김포공항역 9호선')]"
            )
            if gimpo_elements:
                gimpo_elements[0].click()
                gimpo_airport_found = True
        except:
            pass
        
        assert gimpo_airport_found, "김포공항역 9호선 선택 실패"
        
        # 버스 리스트 확인
        time.sleep(3)
        
        bus_list_found = page.wait_for_bus_list(timeout=20)
        
        page.take_screenshot("operating_hours_bus_list.png")
        
        if bus_list_found:
            bus_count = page.get_bus_count()
            assert bus_count > 0, "운행 시간 내인데 버스가 없습니다"
            print(f"  ✅ 버스 {bus_count}개 발견")
        else:
            pytest.fail("운행 시간 내인데 버스 리스트가 표시되지 않습니다")
        
        print("\n✅ 운행 시간 내 버스 리스트 확인 완료!")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--alluredir=allure-results"])