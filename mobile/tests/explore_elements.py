"""
똑버스 화면 Element 탐색 스크립트
appium/tests/ 폴더에 임시 생성
"""
import pytest
from appium.webdriver.common.appiumby import AppiumBy


@pytest.mark.ui
def test_explore_ddokta_bus_elements(appium_driver):
    """똑버스 화면 Element 탐색"""
    import time
    
    print("\n=== 화면 탐색 시작 ===")
    
    # 앱 로드 대기
    time.sleep(3)
    
    # 1. 페이지 소스 출력
    print("\n[Page Source]")
    page_source = appium_driver.page_source
    print(page_source[:2000])  # 처음 2000자만
    
    # 2. 모든 TextView 찾기 (Zone 이름이 TextView일 가능성)
    try:
        textviews = appium_driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
        print(f"\n[TextView 개수]: {len(textviews)}")
        for i, tv in enumerate(textviews[:10]):  # 처음 10개만
            try:
                print(f"  {i}: {tv.text} (resource-id: {tv.get_attribute('resource-id')})")
            except:
                pass
    except Exception as e:
        print(f"TextView 찾기 실패: {e}")
    
    # 3. 클릭 가능한 요소 찾기 (Zone 카드)
    try:
        clickables = appium_driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
        print(f"\n[클릭 가능한 요소]: {len(clickables)}개")
        for i, elem in enumerate(clickables[:5]):  # 처음 5개만
            try:
                resource_id = elem.get_attribute('resource-id')
                class_name = elem.get_attribute('class')
                print(f"  {i}: {class_name} - {resource_id}")
            except:
                pass
    except Exception as e:
        print(f"클릭 가능한 요소 찾기 실패: {e}")
    
    # 4. RecyclerView/ListView 찾기 (Zone 목록)
    try:
        recyclerview = appium_driver.find_elements(AppiumBy.CLASS_NAME, "androidx.recyclerview.widget.RecyclerView")
        print(f"\n[RecyclerView]: {len(recyclerview)}개 발견")
    except:
        print("\n[RecyclerView]: 없음")
    
    # 5. 특정 텍스트 찾기 (예: "동탄신도시")
    try:
        dongtan = appium_driver.find_elements(AppiumBy.XPATH, "//*[contains(@text, '동탄')]")
        print(f"\n['동탄' 포함 요소]: {len(dongtan)}개")
    except:
        print("\n['동탄' 포함 요소]: 없음")
    
    print("\n=== 탐색 완료 ===")
    
    # 스크린샷 저장
    appium_driver.save_screenshot("screenshots/explore_ddokbus.png")
    print("\n스크린샷 저장: screenshots/explore_ddokbus.png")