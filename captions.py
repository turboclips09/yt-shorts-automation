import subprocess
import re
import math

# -----------------------------
# Load script
# -----------------------------
text = open("script.txt", "r", encoding="utf-8").read().strip()
words = re.findall(r"\b[\w’']+\b", text)

if not words:
    raise Exception("No words found in script")

# -----------------------------
# Get audio duration
# -----------------------------
probe = subprocess.run(
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

# -----------------------------
# Caption pacing
# -----------------------------
WORDS_PER_CHUNK = 3        # teleprompter size (2–4 is ideal)
total_chunks = math.ceil(len(words) / WORDS_PER_CHUNK)
chunk_duration = duration / total_chunks

# -----------------------------
# ASS header
# -----------------------------
ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial Black,92,&H00FFFFFF,&H0000FF00,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,4,2,2,80,80,260,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def ts(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

# -----------------------------
# Build teleprompter captions
# -----------------------------
events = []
current_time = 0.0

for i in range(0, len(words), WORDS_PER_CHUNK):
    chunk = words[i:i + WORDS_PER_CHUNK]

    # highlight last word in chunk
    rendered = " ".join(
        chunk[:-1]
        + [r"{\c&H0000FF&}" + chunk[-1] + r"{\c&H00FFFFFF&}"]
    )

    start = ts(current_time)
    end = ts(current_time + chunk_duration)

    events.append(
        f"Dialogue: 0,{start},{end},Default,,0,0,0,,{rendered}"
    )

    current_time += chunk_duration

with open("captions.ass", "w", encoding="utf-8") as f:
    f.write(ass + "\n".join(events))

print("✅ Teleprompter-style captions generated")
