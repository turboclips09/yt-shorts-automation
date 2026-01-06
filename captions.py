import subprocess
import re
import math

# -------------------------------------------------
# Load script
# -------------------------------------------------
text = open("script.txt", "r", encoding="utf-8").read().strip()
words = re.findall(r"\b[\w’']+\b", text.upper())

if not words:
    raise Exception("No words found")

# -------------------------------------------------
# Get audio duration
# -------------------------------------------------
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

# -------------------------------------------------
# PERCEPTUAL TIMING (THIS IS THE KEY)
# -------------------------------------------------
WORDS_PER_PHRASE = 3

# Human-readable timing (Shorts standard)
MIN_CAPTION_TIME = 0.45
MAX_CAPTION_TIME = 0.75

total_phrases = math.ceil(len(words) / WORDS_PER_PHRASE)
avg_time = duration / total_phrases

caption_time = max(
    MIN_CAPTION_TIME,
    min(MAX_CAPTION_TIME, avg_time)
)

# -------------------------------------------------
# ASS header (CUSTOM FONT, PREMIUM LOOK)
# -------------------------------------------------
ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding

; === PREMIUM SHORTS STYLE ===
Style: Default,Poppins ExtraBold,110,&H00FFFFFF,&H0000E6FF,&H00000000,&H3C000000,1,0,0,0,100,100,4,0,1,7,4,3,60,60,320,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def ts(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

# -------------------------------------------------
# Build captions (CALM, CLEAN, COOL)
# -------------------------------------------------
events = []
current_time = 0.0
MAX_LINE_CHARS = 14

for i in range(0, len(words), WORDS_PER_PHRASE):
    phrase = words[i:i + WORDS_PER_PHRASE]

    hi = len(phrase) // 2

    # Line building
    lines = []
    line = ""

    for w in phrase:
        if len(line) + len(w) + 1 > MAX_LINE_CHARS:
            lines.append(line.strip())
            line = w + " "
        else:
            line += w + " "

    if line.strip():
        lines.append(line.strip())

    lines = lines[:2]

    # Highlight + soft pop
    flat = 0
    for li in range(len(lines)):
        parts = lines[li].split()
        for pi in range(len(parts)):
            if flat == hi:
                parts[pi] = (
                    r"{\c&H0000E6FF&\fscx94\fscy94\t(0,160,\fscx100\fscy100)}"
                    + parts[pi] +
                    r"{\c&H00FFFFFF&}"
                )
            flat += 1
        lines[li] = " ".join(parts)

    rendered = r"\N".join(lines)

    start = ts(current_time)
    end = ts(current_time + caption_time)

    events.append(
        f"Dialogue: 0,{start},{end},Default,,0,0,0,,{rendered}"
    )

    current_time += caption_time

with open("captions.ass", "w", encoding="utf-8") as f:
    f.write(ass + "\n".join(events))

print("🔥 PREMIUM YouTube Shorts captions generated")
