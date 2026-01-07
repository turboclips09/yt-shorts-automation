import subprocess
import math
import pathlib

WORDS_PER_CHUNK = 3
MIN_DURATION = 0.25  # seconds

# Load script text
script = pathlib.Path("script.txt").read_text(encoding="utf-8").strip()
words = script.split()

# Get audio duration
result = subprocess.run(
    [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        "voice.mp3"
    ],
    capture_output=True,
    text=True
)

duration = float(result.stdout.strip())

chunks = [
    " ".join(words[i:i + WORDS_PER_CHUNK])
    for i in range(0, len(words), WORDS_PER_CHUNK)
]

time_per_chunk = max(duration / len(chunks), MIN_DURATION)

def to_ass_time(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

ass_header = """[Script Info]
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Poppins ExtraBold,136,&H00FFFFFF,&H0000FFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,6,0,2,80,80,360,1

[Events]
Format: Layer, Start, End, Style, Text
"""

events = []
current_time = 0.0

for chunk in chunks:
    start = current_time
    end = current_time + time_per_chunk
    events.append(
        f"Dialogue: 0,{to_ass_time(start)},{to_ass_time(end)},Default,{chunk}"
    )
    current_time = end

with open("captions.ass", "w", encoding="utf-8") as f:
    f.write(ass_header + "\n".join(events))

print("✅ captions.ass generated (audio-synced, readable, stable)")
