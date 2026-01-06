import subprocess
import re

# -----------------------------
# Load script words
# -----------------------------
text = open("script.txt", "r", encoding="utf-8").read().strip()
words = re.findall(r"\b[\w’']+\b", text)

if not words:
    raise Exception("No words found")

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
# Per-word timing (realistic)
# -----------------------------
total_words = len(words)
per_word = duration / total_words   # seconds per word

# -----------------------------
# ASS header (LOUD & SAFE)
# -----------------------------
ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Impact,102,&H00FFFFFF,&H0000FF00,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,5,3,2,80,80,300,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def ts(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

# -----------------------------
# Rolling teleprompter captions
# -----------------------------
events = []
current_time = 0.0

WINDOW = 3  # words visible (prev, current, next)

for i in range(total_words):
    start = ts(current_time)
    end = ts(current_time + per_word)

    prev_word = words[i - 1] if i - 1 >= 0 else ""
    curr_word = words[i]
    next_word = words[i + 1] if i + 1 < total_words else ""

    rendered = " ".join(
        w for w in [
            prev_word,
            r"{\c&H0000FF&}" + curr_word + r"{\c&H00FFFFFF&}",
            next_word
        ] if w
    )

    events.append(
        f"Dialogue: 0,{start},{end},Default,,0,0,0,,{rendered}"
    )

    current_time += per_word

with open("captions.ass", "w", encoding="utf-8") as f:
    f.write(ass + "\n".join(events))

print("✅ Word-synced teleprompter captions generated")
