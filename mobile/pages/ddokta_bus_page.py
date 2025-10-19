"""
똑타 앱 Page Object - 완전한 버전
파일 경로: mobile/pages/ddokta_bus_page.py
"""
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from mobile.locators.ddokta_bus_locators import DdoktaBusLocators


class DdoktaBusPage:
    """똑타 앱 Page Object"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)  # 기본 대기 시간 15초
    
    # ========================================
    # 홈 화면 메서드
    # ========================================
    
    def click_ddokta_bus_menu(self):
        """똑버스 메뉴 클릭 (홈 화면에서)"""
        from appium.webdriver.common.appiumby import AppiumBy
        
        # 홈 화면에서 찾을 수 있는 메뉴들 (우선순위 순서)
        menu_options = [
            (AppiumBy.XPATH, "//android.widget.TextView[@text='똑버스']"),
            (AppiumBy.XPATH, "//*[contains(@text, '똑버스') and not(contains(@text, '노선'))]"),
            (AppiumBy.XPATH, "//*[@text='똑버스']"),
        ]
        
        for i, locator in enumerate(menu_options, 1):
            try:
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(locator)
                )
                # 클릭 가능한지 확인
                if element.is_displayed() and element.is_enabled():
                    element.click()
                    print(f"✅ '똑버스' 메뉴 클릭 성공 (방법 {i})")
                    time.sleep(2)
                    return True
            except Exception as e:
                if i == len(menu_options):
                    print(f"❌ 똑버스 메뉴를 찾을 수 없습니다: {e}")
                continue
        
        return False
    
    def click_explore_button(self):
        """탐색하기 버튼 클릭 (또는 Zone 목록으로 이동)"""
        from appium.webdriver.common.appiumby import AppiumBy
        
        # 여러 가능성 시도
        button_options = [
            (AppiumBy.ID, "com.hyundai.shucle.gmaas:id/btn_explore"),
            (AppiumBy.XPATH, "//android.widget.Button[contains(@text, '탐색')]"),
            (AppiumBy.XPATH, "//*[contains(@text, '탐색')]"),
        ]
        
        for locator in button_options:
            try:
                element = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(locator)
                )
                element.click()
                print(f"✅ 탐색 버튼 클릭 성공")
                time.sleep(2)
                return True
            except:
                continue
        
        # 버튼이 없다면 이미 Zone 목록 화면일 수 있음
        print("⚠️ 탐색하기 버튼 없음 - 이미 Zone 목록 화면일 가능성")
        return True  # 계속 진행
    
    # ========================================
    # Zone 목록 메서드
    # ========================================
    
    def wait_for_zone_list(self, timeout=10):
        """Zone 목록이 로드될 때까지 대기"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(DdoktaBusLocators.ZONE_LIST)
            )
            return True
        except TimeoutException:
            return False
    
    def get_zone_count(self):
        """Zone 개수 반환"""
        zones = self.driver.find_elements(*DdoktaBusLocators.ZONE_ITEM)
        return len(zones)
    
    def find_zone_by_text(self, zone_name):
        """특정 Zone 텍스트로 찾기"""
        from appium.webdriver.common.appiumby import AppiumBy
        locator = (AppiumBy.XPATH, f"//android.widget.TextView[contains(@text, '{zone_name}')]")
        try:
            element = self.driver.find_element(*locator)
            return element
        except:
            return None
    
    # ========================================
    # 목적지 선택 메서드
    # ========================================
    
    def select_destination(self, destination_name="개화역"):
        """목적지 선택"""
        from appium.webdriver.common.appiumby import AppiumBy
        
        # 여러 방법으로 시도
        locators = [
            (AppiumBy.XPATH, f"//android.widget.TextView[contains(@text, '{destination_name}')]"),
            (AppiumBy.XPATH, f"//*[contains(@text, '{destination_name}')]"),
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{destination_name}")'),
        ]
        
        for locator in locators:
            try:
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(locator)
                )
                element.click()
                time.sleep(1)
                return True
            except:
                continue
        
        return False
    
    def click_confirm(self):
        """확인 버튼 클릭"""
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(DdoktaBusLocators.CONFIRM_BUTTON)
            )
            element.click()
            time.sleep(2)  # 버스 리스트 로딩 대기
            return True
        except:
            return False
    
    # ========================================
    # 버스 리스트 메서드 (수정됨)
    # ========================================
    
    def wait_for_bus_list(self, timeout=20):
        """
        버스 리스트가 표시될 때까지 대기 (다중 방법)
        
        Args:
            timeout: 최대 대기 시간 (기본 20초)
        
        Returns:
            bool: 버스 리스트 발견 여부
        """
        wait = WebDriverWait(self.driver, timeout)
        
        # 방법 1: 버스 탑승 시간 텍스트로 확인 (가장 확실)
        try:
            wait.until(
                EC.presence_of_element_located(DdoktaBusLocators.BUS_TIME_TEXT)
            )
            print("✅ 버스 탑승 시간 텍스트 발견")
            return True
        except TimeoutException:
            print("⚠️ 방법 1 실패: 버스 탑승 시간 텍스트 못 찾음")
        
        # 방법 2: 목적지 도착 예정 텍스트로 확인
        try:
            wait.until(
                EC.presence_of_element_located(DdoktaBusLocators.BUS_ARRIVAL_TEXT)
            )
            print("✅ 목적지 도착 예정 텍스트 발견")
            return True
        except TimeoutException:
            print("⚠️ 방법 2 실패: 목적지 도착 예정 텍스트 못 찾음")
        
        # 방법 3: 버스 카드뷰 확인
        try:
            wait.until(
                EC.presence_of_element_located(DdoktaBusLocators.BUS_CARD)
            )
            print("✅ 버스 카드뷰 발견")
            return True
        except TimeoutException:
            print("⚠️ 방법 3 실패: 버스 카드뷰 못 찾음")
        
        # 방법 4: 버스 리스트 컨테이너 확인
        try:
            wait.until(
                EC.presence_of_element_located(DdoktaBusLocators.BUS_LIST_CONTAINER)
            )
            print("✅ 버스 리스트 컨테이너 발견")
            return True
        except TimeoutException:
            print("⚠️ 방법 4 실패: 버스 리스트 컨테이너 못 찾음")
        
        print("❌ 모든 방법 실패: 버스 리스트를 찾을 수 없음")
        return False
    
    def get_bus_count(self):
        """버스 개수 반환"""
        try:
            buses = self.driver.find_elements(*DdoktaBusLocators.BUS_TIME_TEXT)
            return len(buses)
        except:
            return 0
    
    def get_bus_info(self):
        """첫 번째 버스 정보 반환"""
        try:
            time_element = self.driver.find_element(*DdoktaBusLocators.BUS_TIME_TEXT)
            arrival_element = self.driver.find_element(*DdoktaBusLocators.BUS_ARRIVAL_TEXT)
            
            return {
                "boarding_time": time_element.text,
                "arrival_info": arrival_element.text
            }
        except:
            return None
    
    def is_bus_list_displayed(self):
        """버스 리스트가 화면에 표시되어 있는지 확인"""
        try:
            element = self.driver.find_element(*DdoktaBusLocators.BUS_TIME_TEXT)
            return element.is_displayed()
        except:
            return False
    
    # ========================================
    # Zone 상세 메서드
    # ========================================
    
    def click_operation_info(self):
        """운행 정보 버튼 클릭"""
        element = self.wait.until(
            EC.element_to_be_clickable(DdoktaBusLocators.OPERATION_INFO_BUTTON)
        )
        element.click()
        time.sleep(1)
    
    # ========================================
    # 유틸리티 메서드
    # ========================================
    
    def take_screenshot(self, filename):
        """스크린샷 저장"""
        self.driver.save_screenshot(f"screenshots/{filename}")
    
    def scroll_down(self, duration=1000):
        """화면 아래로 스크롤"""
        window_size = self.driver.get_window_size()
        start_x = window_size['width'] // 2
        start_y = window_size['height'] * 0.8
        end_y = window_size['height'] * 0.2
        
        self.driver.swipe(start_x, start_y, start_x, end_y, duration)
        time.sleep(0.5)
    
    def scroll_to_element(self, element_text):
        """특정 텍스트가 있는 요소까지 스크롤"""
        from appium.webdriver.common.appiumby import AppiumBy
        
        max_scrolls = 10
        for _ in range(max_scrolls):
            try:
                locator = (AppiumBy.XPATH, f"//*[contains(@text, '{element_text}')]")
                element = self.driver.find_element(*locator)
                if element.is_displayed():
                    return element
            except:
                pass
            self.scroll_down()
        
        return None