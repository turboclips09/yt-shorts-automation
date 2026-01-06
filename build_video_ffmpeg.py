import glob, math, random, subprocess as sp

my = glob.glob("assets/assets/my_videos/*.mp4")
px = glob.glob("assets/videos/*.mp4")

print(len(my), "personal")
print(len(px), "pixabay")

probe = sp.run(
    ["ffprobe","-v","error","-show_entries","format=duration",
     "-of","default=nokey=1:noprint_wrappers=1","voice.mp3"],
    capture_output=True, text=True
)

dur = float(probe.stdout.strip())
clips = math.ceil(dur / 1.6)

m = int(clips * 0.7)
p = clips - m

random.shuffle(my)
random.shuffle(px)

sel = my[:m] + px[:p]
random.shuffle(sel)

cmd = ["ffmpeg","-y"]

for v in sel:
    cmd += ["-ss","0.4","-t","1.6","-i",v]

cmd += ["-i","voice.mp3"]

filters = []
for i in range(len(sel)):
    filters.append(
        f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,"
        f"crop=1080:1920,setsar=1[v{i}]"
    )

fc = (
    ";".join(filters)
    + ";"
    + "".join(f"[v{i}]" for i in range(len(sel)))
    + f"concat=n={len(sel)}:v=1:a=0[base]"
    + ";[base]ass=captions.ass[outv]"
)

cmd += [
    "-filter_complex", fc,
    "-map","[outv]",
    "-map",str(len(sel)),
    "-shortest",
    "-movflags","+faststart",
    "final.mp4"
]

sp.run(cmd, check=True)
print("Video done")
