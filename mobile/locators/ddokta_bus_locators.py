"""
똑타 앱의 UI 요소 Locators - 완전한 버전
파일 경로: mobile/locators/ddokta_bus_locators.py
"""
from appium.webdriver.common.appiumby import AppiumBy as MobileBy


class DdoktaBusLocators:
    """따복버스 앱의 UI 요소 locators"""
    
    # ========================================
    # 홈 화면
    # ========================================
    DDOKTA_BUS_MENU = (MobileBy.XPATH, "//android.widget.TextView[@text='똑타']")
    EXPLORE_BUTTON = (MobileBy.ID, "com.hyundai.shucle.gmaas:id/btn_explore")
    
    # ========================================
    # Zone 목록 화면
    # ========================================
    ZONE_LIST = (MobileBy.ID, "com.hyundai.shucle.gmaas:id/recyclerView")
    ZONE_ITEM = (MobileBy.ID, "com.hyundai.shucle.gmaas:id/zone_item")
    
    # 특정 Zone 검색
    GIMPO_ZONE = (MobileBy.XPATH, "//android.widget.TextView[contains(@text, '김포')]")
    
    # ========================================
    # 목적지 선택 화면
    # ========================================
    # 개화역 9호선 목적지
    GAEHWA_DESTINATION = (MobileBy.XPATH, "//android.widget.TextView[contains(@text, '개화역')]")
    
    # 확인 버튼
    CONFIRM_BUTTON = (MobileBy.ID, "com.hyundai.shucle.gmaas:id/btn_confirm")
    
    # ========================================
    # 버스 리스트 화면 (수정됨)
    # ========================================
    
    # 방법 1: 버스 탑승 시간 텍스트로 확인 (가장 확실)
    BUS_TIME_TEXT = (MobileBy.XPATH, "//*[contains(@text, '분 후 탑승')]")
    
    # 방법 2: 목적지 도착 예정 텍스트로 확인
    BUS_ARRIVAL_TEXT = (MobileBy.XPATH, "//*[contains(@text, '목적지 도착 예정')]")
    
    # 방법 3: RecyclerView 또는 리스트 컨테이너
    BUS_LIST_CONTAINER = (MobileBy.XPATH, 
        "//androidx.recyclerview.widget.RecyclerView | "
        "//android.view.ViewGroup[contains(@resource-id, 'bus')] | "
        "//android.widget.LinearLayout[.//android.widget.TextView[contains(@text, '분 후 탑승')]]"
    )
    
    # 방법 4: 버스 카드뷰 (가장 포괄적)
    BUS_CARD = (MobileBy.XPATH, 
        "//*[contains(@text, '분 후 탑승')]/ancestor::android.view.ViewGroup[1]"
    )
    
    # 방법 5: 버스 아이콘 이미지
    BUS_ICON = (MobileBy.XPATH, "//android.widget.ImageView[contains(@content-desc, '버스')]")
    
    # ========================================
    # Zone 상세 화면
    # ========================================
    ZONE_DETAIL_TITLE = (MobileBy.ID, "com.hyundai.shucle.gmaas:id/zone_title")
    OPERATION_INFO_BUTTON = (MobileBy.ID, "com.hyundai.shucle.gmaas:id/btn_operation_info")