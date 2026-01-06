import subprocess
import glob

video_files = sorted(glob.glob("assets/videos/*.mp4"))
image_files = sorted(glob.glob("assets/images/*.jpg"))

assets = video_files + image_files

# Ensure enough assets
while len(assets) < 12:
    assets = assets + assets

assets = assets[:12]
duration = 1.4  # seconds per asset

cmd = ["ffmpeg", "-y"]

# Add inputs correctly
for a in assets:
    if a.endswith(".jpg"):
        cmd.extend(["-loop", "1", "-t", str(duration), "-i", a])
    else:
        cmd.extend(["-t", str(duration), "-i", a])

# Build filter_complex
filters = []
for i in range(len(assets)):
    filters.append(
        f"[{i}:v]"
        f"scale=1080:1920:force_original_aspect_ratio=increase,"
        f"crop=1080:1920,"
        f"fps=30,"
        f"format=yuv420p"
        f"[v{i}]"
    )

concat = "".join(f"[v{i}]" for i in range(len(assets)))

filter_complex = (
    ";".join(filters)
    + f";{concat}concat=n={len(assets)}:v=1:a=0[outv]"
)

cmd.extend([
    "-i", "voice.mp3",
    "-filter_complex", filter_complex,
    "-map", "[outv]",
    "-map", str(len(assets)),
    "-shortest",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "base.mp4"
])

subprocess.run(cmd, check=True)
print("Base video created successfully: base.mp4")
