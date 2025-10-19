"""
현재 앱 화면 확인 스크립트
파일: check_current_screen.py
실행: python check_current_screen.py
"""
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import time

options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "SM-S921N"
options.app_package = "com.hyundai.shucle.gmaas"
options.app_activity = "com.hyundai.airlab.shucle.presenter.MainActivity"
options.no_reset = True

driver = webdriver.Remote("http://127.0.0.1:4724", options=options)

try:
    print("\n" + "="*80)
    print("🔍 똑타 앱 - 현재 화면 분석")
    print("="*80)
    
    time.sleep(2)
    
    # 스크린샷 저장
    driver.save_screenshot("debug_current_screen.png")
    print("\n✅ 스크린샷 저장: debug_current_screen.png")
    
    # 현재 Activity 확인
    current_activity = driver.current_activity
    print(f"\n📱 현재 Activity: {current_activity}")
    
    # 모든 텍스트 요소 찾기
    all_texts = driver.find_elements(AppiumBy.XPATH, "//*[@text!='']")
    
    print(f"\n📋 화면의 모든 텍스트 요소 ({len(all_texts)}개):")
    print("-" * 80)
    
    for i, element in enumerate(all_texts, 1):
        try:
            text = element.text
            if text and len(text.strip()) > 0:
                print(f"{i:3d}. {text}")
        except:
            pass
    
    # 모든 버튼 찾기
    print("\n" + "="*80)
    print("🔘 화면의 모든 버튼:")
    print("-" * 80)
    
    buttons = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button")
    for i, button in enumerate(buttons, 1):
        try:
            text = button.text
            resource_id = button.get_attribute("resource-id")
            print(f"{i}. Text: '{text}' | ID: {resource_id}")
        except:
            pass
    
    # ImageButton도 확인
    image_buttons = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.ImageButton")
    for i, button in enumerate(image_buttons, 1):
        try:
            content_desc = button.get_attribute("content-desc")
            resource_id = button.get_attribute("resource-id")
            print(f"ImageButton {i}. Desc: '{content_desc}' | ID: {resource_id}")
        except:
            pass
    
    # RecyclerView 확인 (Zone 목록이 있는지)
    print("\n" + "="*80)
    print("📦 RecyclerView 확인:")
    print("-" * 80)
    
    recyclers = driver.find_elements(AppiumBy.CLASS_NAME, "androidx.recyclerview.widget.RecyclerView")
    if recyclers:
        print(f"✅ RecyclerView 발견: {len(recyclers)}개")
        print("   → Zone 목록이 이미 표시되어 있을 가능성")
    else:
        print("❌ RecyclerView 없음")
    
    # 특정 키워드로 검색
    print("\n" + "="*80)
    print("🔎 주요 키워드 검색:")
    print("-" * 80)
    
    keywords = ['개화', '김포', '목적지', '출발', '도착', '선택', '확인', '탐색', '예약', '버스']
    
    for keyword in keywords:
        try:
            elements = driver.find_elements(AppiumBy.XPATH, f"//*[contains(@text, '{keyword}')]")
            if elements:
                print(f"✅ '{keyword}' 포함 요소: {len(elements)}개")
                for elem in elements[:3]:  # 처음 3개만
                    try:
                        print(f"   - {elem.text}")
                    except:
                        pass
        except:
            pass
    
    # XML 저장
    print("\n" + "="*80)
    page_source = driver.page_source
    with open("debug_page_source.xml", "w", encoding="utf-8") as f:
        f.write(page_source)
    print("✅ 화면 XML 저장: debug_page_source.xml")
    
    print("\n" + "="*80)
    print("💡 다음 단계:")
    print("-" * 80)
    print("1. debug_current_screen.png 확인 - 현재 어떤 화면인지 확인")
    print("2. 위의 텍스트/버튼 목록에서 클릭할 요소 찾기")
    print("3. 필요시 debug_page_source.xml에서 정확한 locator 확인")
    print("="*80 + "\n")
    
finally:
    driver.quit()