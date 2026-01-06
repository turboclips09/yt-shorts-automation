import subprocess
import glob
import math
import random
import subprocess as sp

videos = glob.glob("assets/videos/*.mp4")
if len(videos) < 20:
    raise Exception("Not enough videos — need at least 20")

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

# 🔀 RANDOM SUBSET EACH RUN
random.shuffle(videos)
sequence = videos[:clips_needed]

cmd = ["ffmpeg", "-y"]

for v in sequence:
    cmd.extend(["-ss", "0.4", "-t", str(clip_duration), "-i", v])

filters = []
for i in range(len(sequence)):
    filters.append(
        f"[{i}:v]"
        f"scale=1080:1920:force_original_aspect_ratio=increase,"
        f"crop=1080:1920,"
        f"setsar=1,"
        f"fps=30,"
        f"format=yuv420p"
        f"[v{i}]"
    )

concat_inputs = "".join(f"[v{i}]" for i in range(len(sequence)))

filter_complex = (
    ";".join(filters)
    + f";{concat_inputs}concat=n={len(sequence)}:v=1:a=0[outv]"
)

cmd.extend([
    "-i", "voice.mp3",
    "-filter_complex", filter_complex,
    "-map", "[outv]",
    "-map", str(len(sequence)),
    "-shortest",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "base.mp4"
])

subprocess.run(cmd, check=True)
print("✅ Fresh, non-repeating visual set created")
