import os
import time
from datetime import datetime
from PIL import ImageGrab, Image
import mss

SCREENSHOT_FOLDER = "screenshots"
os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)


def capture_full_screen():
    """Capture entire screen and return PIL Image."""
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        shot = sct.grab(monitor)
        return Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")


def capture_region(bbox):
    """Capture specific region (left, top, right, bottom)."""
    return ImageGrab.grab(bbox=bbox)


def save_screenshot(img, prefix="screen"):
    """Save image with timestamp. Returns filepath."""
    filename = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = os.path.join(SCREENSHOT_FOLDER, filename)
    img.save(path)
    print(f"📸 Screenshot saved: {path}")
    return path
