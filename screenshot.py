from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from urllib.request import urlretrieve

URL = "https://emonika.rvo.si/lastsnapshot-emonika.jpeg"

OUT = Path("shots")
OUT.mkdir(exist_ok=True)

timestamp = datetime.now(
    ZoneInfo("Europe/Ljubljana")
).strftime("%Y-%m-%d_%H-%M-%S")

filename = OUT / f"emonika_{timestamp}.jpg"

urlretrieve(URL, filename)

print(f"Saved {filename}")
