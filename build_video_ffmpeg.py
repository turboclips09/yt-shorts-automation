import subprocess
import glob
import math
import random
import subprocess as sp

# Load videos
pixabay_videos = glob.glob("assets/videos/*.mp4")
my_videos = glob.glob("assets/my_videos/*.mp4")

if len(pixabay_videos) < 10:
    raise Exception("Not enough Pixabay videos")

if len(my_videos) == 0:
    print("⚠️ No personal videos found, using Pixabay only")

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

# Calculate mix
my_count = max(1, int(clips_needed * 0.3)) if my_videos else 0
pixabay_count = clips_needed - my_count

# Select clips
random.shuffle(my_videos)
random.shuffle(pixabay_videos)

selected = []

selected.extend(my_videos[:my_count])
selected.extend(pixabay_videos[:pixabay_count])

# Shuffle final sequence
random.shuffle(selected)

# Prevent back-to-back duplicates
final_sequence = []
last = None
for v in selected:
    if v != last:
        final_sequence.append(v)
        last = v

cmd = ["ffmpeg", "-y"]

# Skip first 0.4s to avoid black frames
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

subprocess.run(cmd, check=True)

print("✅ Mixed personal + Pixabay visuals created")
