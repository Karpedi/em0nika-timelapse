from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
import subprocess

TZ = ZoneInfo("Europe/Ljubljana")

IMAGES_DIR = Path("slike")
OUT_DIR = Path("timelapse")
OUT_DIR.mkdir(exist_ok=True)

# Včerajšnji datum
yesterday = datetime.now(TZ).date() - timedelta(days=1)

date_prefix = yesterday.strftime("%Y-%m-%d")
display_date = yesterday.strftime("%d.%m.%Y")

# Poišči vse slike od včeraj
images = sorted(IMAGES_DIR.glob(f"emonika_{date_prefix}_*.jpg"))

if len(images) < 2:
    raise SystemExit(
        f"Premalo slik za {date_prefix}: {len(images)}"
    )

# FFmpeg seznam
frames_file = OUT_DIR / "frames.txt"

with frames_file.open("w", encoding="utf-8") as f:
    for image in images:
        f.write(f"file '../{image.as_posix()}'\n")
        f.write("duration 0.25\n")

    # zadnja slika še enkrat
    f.write(f"file '../{images[-1].as_posix()}'\n")

latest_gif = OUT_DIR / "latest.gif"

# Ustvari GIF
subprocess.run(
    [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(frames_file),
        "-vf",
        "fps=8,scale=960:-1:flags=lanczos",
        str(latest_gif),
    ],
    check=True,
)

# Posodobi README
readme = Path("README.md")

if readme.exists():
    content = readme.read_text(encoding="utf-8")
else:
    content = "# Emonika Timelapse\n"

block = f"""## 🎬 Zadnji dnevni timelapse

📅 **{display_date}**

📸 Število slik: **{len(images)}**

![Timelapse za {display_date}](timelapse/latest.gif)
"""

start_marker = "<!-- TIMELAPSE_START -->"
end_marker = "<!-- TIMELAPSE_END -->"

replacement = (
    f"{start_marker}\n"
    f"{block}\n"
    f"{end_marker}"
)

if start_marker in content and end_marker in content:
    before = content.split(start_marker)[0]
    after = content.split(end_marker)[1]
    content = before + replacement + after
else:
    content += "\n\n" + replacement + "\n"

readme.write_text(content, encoding="utf-8")

# Počisti začasno datoteko
if frames_file.exists():
    frames_file.unlink()

print(
    f"Ustvarjen timelapse za {display_date} iz {len(images)} slik."
)
