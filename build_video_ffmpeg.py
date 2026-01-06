import subprocess
import glob
import math
import random
import subprocess as sp

# =========================
# LOAD VIDEO POOLS
# =========================
my_videos = glob.glob("assets/assets/my_videos/*.mp4")
pixabay_videos = glob.glob("assets/videos/*.mp4")

print(f"Found {len(my_videos)} personal videos")
print(f"Found {len(pixabay_videos)} pixabay videos")

if len(pixabay_videos) == 0:
    raise Exception("No Pixabay videos found in assets/videos")

# =========================
# GET AUDIO DURATION
# =========================
probe = sp.run(
    [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        "voice.mp3"
    ],
    capture_output=True,
    text=True
)

audio_duration = float(probe.stdout.strip())

# =========================
# CLIP CALCULATION
# =========================
clip_duration = 1.6  # seconds per visual
clips_needed = math.ceil(audio_duration / clip_duration)

# =========================
# CALCULATE 70 / 30 MIX
# =========================
if len(my_videos) >= 3:
    my_count = int(clips_needed * 0.7)
else:
    my_count = 0

pixabay_count = clips_needed - my_count

# =========================
# RANDOM SELECTION
# =========================
random.shuffle(my_videos)
random.shuffle(pixabay_videos)

selected = []

selected.extend(my_videos[:my_count])
selected.extend(pixabay_videos[:pixabay_count])

# Shuffle combined list
random.shuffle(selected)

# Prevent immediate repeats
final_sequence = []
last = None
for v in selected:
    if v != last:
        final_sequence.append(v)
        last = v

# =========================
# BUILD FFMPEG COMMAND
# =========================
cmd = ["ffmpeg", "-y"]

# Skip first frames to avoid black flashes
for v in final_sequence:
    cmd.extend(["-ss", "0.4", "-t", str(clip_duration), "-i", v])

filters = []
for i in range(len(final_sequence)):
    filters.append(
        f"[{i}:v]"
        f"scale=1080:1920:force_original_aspect_ratio=increase,"
        f"crop=1080:1920,"
        f"setsar=1,"
        f"fps=30,"
        f"format=yuv420p"
        f"[v{i}]"
    )

concat_inputs = "".join(f"[v{i}]" for i in range(len(final_sequence)))

filter_complex = (
    ";".join(filters)
    + f";{concat_inputs}concat=n={len(final_sequence)}:v=1:a=0[outv]"
)

cmd.extend([
    "-i", "voice.mp3",
    "-filter_complex", filter_complex,
    "-map", "[outv]",
    "-map", str(len(final_sequence)),
    "-shortest",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "base.mp4"
])

# =========================
# RUN
# =========================
subprocess.run(cmd, check=True)

print("✅ Final base video created successfully")
