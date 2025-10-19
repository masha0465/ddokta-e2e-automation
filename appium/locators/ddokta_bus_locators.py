# ui/locators/ddokta_bus_locators.py (새로 생성)
from appium.webdriver.common.mobileby import MobileBy

class DdoktaBusLocators:
    """똑버스 페이지 Locators"""
    
    # TODO: Appium Inspector로 찾은 실제 locator로 교체
    ZONE_CARDS = (MobileBy.XPATH, '//android.widget.TextView[@resource-id="zone_card"]')
    ZONE_IMAGES = (MobileBy.XPATH, '//android.widget.ImageView[@resource-id="zone_image"]')
    ZONE_TITLE = (MobileBy.ID, 'zone_title')