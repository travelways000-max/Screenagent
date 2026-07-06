import time
import pyautogui
from config import FORM_FIELDS_MAP, FORM_FILL_ENABLED


def fill_form(extracted_data):
    """Auto-type extracted data into a web/desktop form.
    User must position cursor in first field. Then it TABs through.
    """
    if not FORM_FILL_ENABLED:
        print("ℹ️ Form filling disabled in config.py")
        return

    print("🖱️ Place cursor in first form field. Starting in 5 seconds...")
    for i in range(5, 0, -1):
        print(f"   {i}...")
        time.sleep(1)

    for form_label, data_key in FORM_FIELDS_MAP.items():
        value = str(extracted_data.get(data_key, ''))
        pyautogui.typewrite(value, interval=0.05)
        pyautogui.press('tab')
        time.sleep(0.3)

    print("✅ Form filling complete!")
