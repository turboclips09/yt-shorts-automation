import json
import re
import math
import subprocess

# -------------------------------------------------
# Load inputs
# -------------------------------------------------
text = open("script.txt", "r", encoding="utf-8").read().strip()
words = re.findall(r"\b[\w’']+\b", text.upper())

if not words:
    raise Exception("❌ No words found")

with open("voice_meta.json", "r", encoding="utf-8") as f:
    meta = json.load(f)

voice_duration = meta["duration"]

# -------------------------------------------------
# Caption pacing (speech-locked)
# -------------------------------------------------
WORDS_PER_PHRASE = 2
TOTAL_PHRASES = math.ceil(len(words) / WORDS_PER_PHRASE)

# Exact pacing
phrase_time = voice_duration / TOTAL_PHRASES

# Human clamp
phrase_time = max(0.55, min(0.85, phrase_time))

# Anticipation (feels synced)
ANTICIPATION = 0.05  # 50ms lead

# -------------------------------------------------
# ASS header (Shorts premium)
# -------------------------------------------------
ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Poppins ExtraBold,132,&H00FFFFFF,&H0000E6FF,&H00000000,&H3A000000,1,0,0,0,100,100,4,0,1,7,4,3,60,60,320,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def ts(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

# -------------------------------------------------
# Build captions
# -------------------------------------------------
events = []
current_time = 0.0

for i in range(0, len(words), WORDS_PER_PHRASE):
    phrase = words[i:i + WORDS_PER_PHRASE]
    hi = len(phrase) // 2

    rendered = []
    for idx, w in enumerate(phrase):
        if idx == hi:
            rendered.append(
                r"{\c&H0000E6FF&\fscx92\fscy92\t(0,160,\fscx100\fscy100)}"
                + w +
                r"{\c&H00FFFFFF&}"
            )
        else:
            rendered.append(w)

    text = " ".join(rendered)

    start = max(0, current_time - ANTICIPATION)
    end = min(current_time + phrase_time, voice_duration)

    events.append(
        f"Dialogue: 0,{ts(start)},{ts(end)},Default,,0,0,0,,{text}"
    )

    current_time += phrase_time

# Force last caption to end with voice
if events:
    last = events[-1].split(",")
    last[2] = ts(voice_duration)
    events[-1] = ",".join(last)

# -------------------------------------------------
# Write ASS
# -------------------------------------------------
with open("captions.ass", "w", encoding="utf-8") as f:
    f.write(ass + "\n".join(events))

print("✅ Captions perceptually synced to voice")
