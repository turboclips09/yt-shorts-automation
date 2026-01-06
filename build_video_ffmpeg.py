import subprocess
import glob

# Collect assets
videos = sorted(glob.glob("assets/videos/*.mp4"))
images = sorted(glob.glob("assets/images/*.jpg"))
assets = videos + images

# Build FFmpeg input list
with open("inputs.txt", "w") as f:
    for a in assets:
        f.write(f"file '{a}'\n")
        f.write("duration 1.8\n")

cmd = [
    "ffmpeg",
    "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", "inputs.txt",
    "-i", "voice.mp3",
    "-filter_complex",
    (
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,"
        "zoompan=z='min(zoom+0.0015,1.1)':d=45,"
        "fps=30"
    ),
    "-shortest",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "short.mp4"
]

subprocess.run(cmd, check=True)
print("FFmpeg dynamic short created")
