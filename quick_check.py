"""
빠른 똑버스 클릭 후 화면 확인
실행: python quick_check.py
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
    print("🔍 빠른 화면 확인")
    print("="*80)
    
    time.sleep(2)
    
    # 똑버스 클릭
    print("\n[1] 똑버스 클릭...")
    try:
        ddokbus = driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='똑버스']")
        ddokbus.click()
        print("✅ 똑버스 클릭 성공")
        time.sleep(3)
    except Exception as e:
        print(f"❌ 똑버스 클릭 실패: {e}")
        driver.quit()
        exit()
    
    # 화면 캡처
    driver.save_screenshot("quick_after_ddokbus.png")
    print("\n✅ 스크린샷 저장: quick_after_ddokbus.png")
    
    # 모든 텍스트 출력
    print("\n" + "="*80)
    print("📱 화면의 모든 텍스트:")
    print("-"*80)
    
    all_texts = driver.find_elements(AppiumBy.XPATH, "//*[@text!='']")
    for i, elem in enumerate(all_texts, 1):
        try:
            text = elem.text
            if text:
                print(f"{i:3d}. {text}")
        except:
            pass
    
    # EditText 찾기
    print("\n" + "="*80)
    print("🔍 EditText (입력창) 찾기:")
    print("-"*80)
    
    edits = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
    if edits:
        print(f"✅ EditText 발견: {len(edits)}개")
        for i, edit in enumerate(edits, 1):
            hint = edit.get_attribute("hint")
            text = edit.get_attribute("text")
            resource_id = edit.get_attribute("resource-id")
            print(f"\n{i}. Hint: '{hint}'")
            print(f"   Text: '{text}'")
            print(f"   ID: {resource_id}")
    else:
        print("❌ EditText 없음")
    
    # Button 찾기
    print("\n" + "="*80)
    print("🔘 Button 찾기:")
    print("-"*80)
    
    buttons = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.Button")
    if buttons:
        print(f"✅ Button 발견: {len(buttons)}개")
        for i, btn in enumerate(buttons, 1):
            text = btn.text
            resource_id = btn.get_attribute("resource-id")
            if text or resource_id:
                print(f"{i}. Text: '{text}' | ID: {resource_id}")
    else:
        print("❌ Button 없음")
    
    print("\n" + "="*80)
    print("💡 quick_after_ddokbus.png 파일을 확인하세요!")
    print("="*80 + "\n")
    
finally:
    driver.quit()