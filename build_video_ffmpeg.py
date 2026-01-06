import glob
import math
import random
import subprocess as sp

# -------------------------------------------------
# Collect video sources
# -------------------------------------------------
my_videos = glob.glob("assets/assets/my_videos/*.mp4")
pixabay_videos = glob.glob("assets/videos/*.mp4")

print(f"Found {len(my_videos)} personal videos")
print(f"Found {len(pixabay_videos)} pixabay videos")

if len(my_videos) < 5:
    raise Exception("❌ Not enough personal videos")

if len(pixabay_videos) < 5:
    raise Exception("❌ Not enough pixabay videos")

# -------------------------------------------------
# Get voice duration
# -------------------------------------------------
probe = sp.run(
    [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        "voice.mp3"
    ],
    capture_output=True,
    text=True
)

duration = float(probe.stdout.strip())

# -------------------------------------------------
# Clip planning
# -------------------------------------------------
CLIP_LEN = 1.6
total_clips = math.ceil(duration / CLIP_LEN)

my_count = int(total_clips * 0.7)
pix_count = total_clips - my_count

random.shuffle(my_videos)
random.shuffle(pixabay_videos)

selected = my_videos[:my_count] + pixabay_videos[:pix_count]
random.shuffle(selected)

print(f"Using {my_count} personal + {pix_count} pixabay clips")

# -------------------------------------------------
# Build FFmpeg command
# -------------------------------------------------
cmd = ["ffmpeg", "-y"]

# Video inputs
for v in selected:
    cmd += ["-ss", "0.4", "-t", str(CLIP_LEN), "-i", v]

# Audio input
cmd += ["-i", "voice.mp3"]

# -------------------------------------------------
# Filter graph
# -------------------------------------------------
filters = []

for i in range(len(selected)):
    filters.append(
        f"[{i}:v]"
        f"scale=1080:1920:force_original_aspect_ratio=increase,"
        f"crop=1080:1920,"
        f"setsar=1[v{i}]"
    )

video_chain = "".join(f"[v{i}]" for i in range(len(selected)))

filter_complex = (
    ";".join(filters)
    + ";"
    + f"{video_chain}concat=n={len(selected)}:v=1:a=0[base]"
    + ";"
    + "[base]ass=captions.ass:fontsdir=/usr/share/fonts[outv]"
)

# -------------------------------------------------
# Output
# -------------------------------------------------
cmd += [
    "-filter_complex", filter_complex,
    "-map", "[outv]",
    "-map", str(len(selected)),   # voice.mp3
    "-shortest",
    "-movflags", "+faststart",
    "final.mp4"
]

print("▶️ Running FFmpeg…")
sp.run(cmd, check=True)
print("✅ Final video created: final.mp4")
