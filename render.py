
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUTPUT = ROOT / "final.mp4"
TEMP = ROOT / "temp"

TEMP.mkdir(exist_ok=True)

images = sorted(
    p for p in ASSETS.glob("*")
    if p.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]
)

if not images:
    raise SystemExit("No images found in the assets folder.")

clips = []

for i, image in enumerate(images):
    clip = TEMP / f"clip_{i:03}.mp4"

    subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1", "-framerate", "30",
        "-i", str(image),
        "-t", "6",
        "-vf",
        "scale=1920:1080:force_original_aspect_ratio=increase,"
        "crop=1920:1080,setsar=1,format=yuv420p",
        "-an",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        str(clip)
    ], check=True)

    clips.append(clip)

concat_file = TEMP / "concat.txt"

with concat_file.open("w") as f:
    for clip in clips:
        f.write(f"file '{clip.as_posix()}'\n")

subprocess.run([
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0",
    "-i", str(concat_file),
    "-c", "copy",
    str(OUTPUT)
], check=True)

print(f"Video created: {OUTPUT}")
