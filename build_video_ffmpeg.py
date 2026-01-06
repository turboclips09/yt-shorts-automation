import glob, math, random, subprocess as sp

my_videos = glob.glob("assets/assets/my_videos/*.mp4")
pixabay_videos = glob.glob("assets/videos/*.mp4")

print(f"Found {len(my_videos)} personal videos")
print(f"Found {len(pixabay_videos)} pixabay videos")

if len(my_videos) < 5:
    raise Exception("❌ Not enough personal videos")

if len(pixabay_videos) < 5:
    raise Exception("❌ Not enough Pixabay videos")

# get voice duration
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

duration = float(probe.stdout.strip())

clip_len = 1.6
clips = math.ceil(duration / clip_len)

my_count = int(clips * 0.7)
pix_count = clips - my_count

random.shuffle(my_videos)
random.shuffle(pixabay_videos)

selected = my_videos[:my_count] + pixabay_videos[:pix_count]
random.shuffle(selected)

cmd = ["ffmpeg", "-y"]

# inputs
for v in selected:
    cmd += ["-ss", "0.4", "-t", str(clip_len), "-i", v]

cmd += ["-i", "voice.mp3"]

# build filter graph
filters = []
for i in range(len(selected)):
    filters.append(
        f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,"
        f"crop=1080:1920,setsar=1[v{i}]"
    )

video_chain = "".join(f"[v{i}]" for i in range(len(selected)))
filter_complex = (
    ";".join(filters)
    + ";"
    + f"{video_chain}concat=n={len(selected)}:v=1:a=0[base]"
    + ";"
    + "[base]ass=captions.ass[outv]"
)

cmd += [
    "-filter_complex", filter_complex,
    "-map", "[outv]",
    "-map", str(len(selected)),
    "-shortest",
    "-movflags", "+faststart",
    "final.mp4"
]

print("Running FFmpeg…")
sp.run(cmd, check=True)
print("✅ Video built successfully")
