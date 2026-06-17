from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from urllib.request import urlretrieve

from playwright.sync_api import sync_playwright

TIMEZONE = "Europe/Ljubljana"

WEB_URL = "https://emonika.rvo.si/"
IMAGE_URL = "https://emonika.rvo.si/lastsnapshot-emonika.jpeg"

ts = datetime.now(ZoneInfo(TIMEZONE)).strftime("%Y-%m-%d_%H-%M-%S")

# Mapi
slike_dir = Path("slike")
spletna_dir = Path("spletna")

slike_dir.mkdir(exist_ok=True)
spletna_dir.mkdir(exist_ok=True)

# 1) Shrani direktno JPEG sliko iz linka
image_file = slike_dir / f"emonika_slika_{ts}.jpg"
urlretrieve(IMAGE_URL, image_file)
print(f"Saved {image_file}")

# 2) Shrani screenshot glavne spletne strani
web_file = spletna_dir / f"emonika_spletna_{ts}.png"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(
        viewport={"width": 1920, "height": 1080},
        device_scale_factor=1,
    )

    page.goto(WEB_URL, wait_until="networkidle", timeout=60000)
    page.screenshot(path=str(web_file), full_page=True)

    browser.close()

print(f"Saved {web_file}")
