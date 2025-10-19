# ui/config/capabilities.py (있으면 수정, 없으면 생성)
from appium.options.android import UiAutomator2Options

def get_capabilities():
    """Appium Capabilities"""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "SM-S921N"
    options.app_package = "com.hyundai.shucle.gmaas"
    options.app_activity = ".MainActivity"
    options.no_reset = True
    options.full_reset = False
    options.new_command_timeout = 300
    
    return options