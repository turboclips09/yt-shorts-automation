import subprocess
import glob
import math
import subprocess as sp

videos = sorted(glob.glob("assets/videos/*.mp4"))

if not videos:
    raise Exception("No videos found")

# Get audio duration
probe = sp.run(
    ["ffprobe", "-v", "error", "-show_entries",
     "format=duration", "-of",
     "default=noprint_wrappers=1:nokey=1", "voice.mp3"],
    capture_output=True, text=True
)

audio_duration = float(probe.stdout.strip())

clip_duration = 1.6
clips_needed = math.ceil(audio_duration / clip_duration)

while len(videos) < clips_needed:
    videos += videos

videos = videos[:clips_needed]

cmd = ["ffmpeg", "-y"]

# ⬇️ SKIP FIRST 0.3s TO AVOID BLACK FRAMES
for v in videos:
    cmd.extend(["-ss", "0.3", "-t", str(clip_duration), "-i", v])

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

print("✅ Black-frame-free base video created")
