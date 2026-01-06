import subprocess
import glob

videos = sorted(glob.glob("assets/videos/*.mp4"))

# Ensure enough clips
while len(videos) < 12:
    videos += videos

videos = videos[:12]
duration = 1.6  # seconds per clip

cmd = ["ffmpeg", "-y"]

for v in videos:
    cmd.extend(["-t", str(duration), "-i", v])

filters = []
for i in range(len(videos)):
    filters.append(
        f"[{i}:v]"
        f"scale=1080:1920:force_original_aspect_ratio=increase,"
        f"crop=1080:1920,"
        f"setsar=1,"
        f"fps=30,"
        f"format=yuv420p"
        f"[v{i}]"
    )

concat_inputs = "".join(f"[v{i}]" for i in range(len(videos)))

filter_complex = (
    ";".join(filters)
    + f";{concat_inputs}concat=n={len(videos)}:v=1:a=0[outv]"
)

cmd.extend([
    "-i", "voice.mp3",
    "-filter_complex", filter_complex,
    "-map", "[outv]",
    "-map", str(len(videos)),
    "-shortest",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "base.mp4"
])

subprocess.run(cmd, check=True)
print("✅ Base video created with high-quality driving footage")
