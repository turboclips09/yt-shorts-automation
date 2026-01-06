import subprocess
import glob
import math

videos = sorted(glob.glob("assets/videos/*.mp4"))
images = sorted(glob.glob("assets/images/*.jpg"))
assets = videos + images

# Repeat assets if not enough
while len(assets) < 12:
    assets += assets

duration_per_asset = 1.4  # seconds
inputs = []

for a in assets[:15]:
    inputs.extend(["-loop", "1", "-t", str(duration_per_asset), "-i", a])

filter_parts = []
for i in range(len(assets[:15])):
    filter_parts.append(
        f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,"
        f"crop=1080:1920,"
        f"fps=30,"
        f"format=yuv420p[v{i}]"
    )

concat_inputs = "".join([f"[v{i}]" for i in range(len(assets[:15]))])

filter_complex = (
    ";".join(filter_parts)
    + f";{concat_inputs}concat=n={len(assets[:15])}:v=1:a=0[outv]"
)

cmd = [
    "ffmpeg", "-y",
    *inputs,
    "-i", "voice.mp3",
    "-filter_complex", filter_complex,
    "-map", "[outv]",
    "-map", str(len(assets[:15])),
    "-shortest",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "base.mp4"
]

subprocess.run(cmd, check=True)
print("Base visual video created (base.mp4)")
