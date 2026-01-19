import glob
import math
import random
import subprocess as sp
import os
import json

# -------------------------------------------------
# Paths
# -------------------------------------------------
BG_MUSIC = "assets/bg_music.mp3"
CAPTIONS = "captions.ass"
FONT_DIR = "assets/fonts"
USED_VIDEOS_FILE = "used_videos.json"

# -------------------------------------------------
# Visual memory settings (BALANCED)
# -------------------------------------------------
RECENT_BLOCK = 40      # do not reuse last 40 clips
MAX_HISTORY = 300      # keep history bounded

# -------------------------------------------------
# Load visual memory
# -------------------------------------------------
used_videos = []
if os.path.exists(USED_VIDEOS_FILE):
    used_videos = json.load(open(USED_VIDEOS_FILE, "r", encoding="utf-8"))

recently_used = set(used_videos[-RECENT_BLOCK:])

# -------------------------------------------------
# Collect video sources
# -------------------------------------------------
my_videos_all = glob.glob("assets/assets/my_videos/*.mp4")
pixabay_videos_all = glob.glob("assets/videos/*.mp4")

print(f"Found {len(my_videos_all)} personal videos")
print(f"Found {len(pixabay_videos_all)} pixabay videos")

if len(my_videos_all) < 5:
    raise Exception("❌ Not enough personal videos")

if len(pixabay_videos_all) < 5:
    raise Exception("❌ Not enough pixabay videos")

if not os.path.exists(BG_MUSIC):
    raise Exception("❌ Background music not found")

if not os.path.exists(CAPTIONS):
    raise Exception("❌ captions.ass not found")

if not os.path.isdir(FONT_DIR):
    raise Exception("❌ assets/fonts directory not found")

# -------------------------------------------------
# Filter out recently used videos (soft filter)
# -------------------------------------------------
def filter_recent(videos):
    fresh = [v for v in videos if v not in recently_used]
    return fresh if len(fresh) >= 5 else videos  # fallback if too strict

my_videos = filter_recent(my_videos_all)
pixabay_videos = filter_recent(pixabay_videos_all)

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

voice_duration = float(probe.stdout.strip())

# -------------------------------------------------
# Clip planning
# -------------------------------------------------
CLIP_LEN = 1.6
total_clips = math.ceil(voice_duration / CLIP_LEN)

my_count = int(total_clips * 0.7)
pix_count = total_clips - my_count

random.shuffle(my_videos)
random.shuffle(pixabay_videos)

selected = my_videos[:my_count] + pixabay_videos[:pix_count]
random.shuffle(selected)

print(f"Using {my_count} personal + {pix_count} pixabay clips")

# -------------------------------------------------
# Save visual memory
# -------------------------------------------------
used_videos.extend(selected)
used_videos = used_videos[-MAX_HISTORY:]
json.dump(used_videos, open(USED_VIDEOS_FILE, "w", encoding="utf-8"), indent=2)

# -------------------------------------------------
# Build FFmpeg command
# -------------------------------------------------
cmd = ["ffmpeg", "-y"]

# Video inputs
for v in selected:
    cmd += ["-ss", "0.4", "-t", str(CLIP_LEN), "-i", v]

# Audio inputs
cmd += [
    "-i", "voice.mp3",
    "-stream_loop", "-1", "-i", BG_MUSIC
]

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

voice_index = len(selected)
music_index = len(selected) + 1

filter_complex = (
    ";".join(filters)
    + ";"
    + f"{video_chain}concat=n={len(selected)}:v=1:a=0[base]"
    + ";"
    + f"[base]ass={CAPTIONS}:fontsdir={FONT_DIR}[outv]"
    + ";"
    + f"[{voice_index}:a]volume=1.0[a_voice]"
    + ";"
    + f"[{music_index}:a]volume=0.16[a_music]"
    + ";"
    + "[a_voice][a_music]amix=inputs=2:dropout_transition=0[aout]"
)

# -------------------------------------------------
# Output
# -------------------------------------------------
cmd += [
    "-filter_complex", filter_complex,
    "-map", "[outv]",
    "-map", "[aout]",
    "-t", str(voice_duration),
    "-movflags", "+faststart",
    "final.mp4"
]

print("▶️ Running FFmpeg with visual memory + captions + music…")
sp.run(cmd, check=True)
print("✅ Final video created successfully")
