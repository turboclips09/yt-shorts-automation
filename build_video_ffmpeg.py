import glob
import math
import random
import subprocess as sp
import os

# -------------------------------------------------
# Paths
# -------------------------------------------------
BG_MUSIC = "assets/bg_music.mp3"
CAPTIONS = "captions.ass"

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

if not os.path.exists(BG_MUSIC):
    raise Exception("❌ Background music not found at assets/bg_music.mp3")

if not os.path.exists(CAPTIONS):
    raise Exception("❌ captions.ass not found")

print(f"Using background music: {BG_MUSIC}")

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
# Build filter graph
# -------------------------------------------------
filters = []

# Video scaling & cropping
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
    # 🔥 FIXED LINE — QUOTED FONTSDIR
    + "[base]ass=captions.ass:fontsdir='assets/fonts:/usr/share/fonts'[outv]"
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

print("▶️ Running FFmpeg with custom font + music…")
sp.run(cmd, check=True)
print("✅ Final video created successfully")
