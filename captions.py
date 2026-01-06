import subprocess
import re
import math
import textwrap

# -----------------------------
# Load script
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
# Caption pacing (balanced)
# -----------------------------
WORDS_PER_PHRASE = 3
READABILITY_MULTIPLIER = 1.25   # captions stay longer than spoken
total_phrases = math.ceil(len(words) / WORDS_PER_PHRASE)

spoken_phrase_time = duration / total_phrases
caption_time = spoken_phrase_time * READABILITY_MULTIPLIER

# -----------------------------
# ASS header (STYLISH + SAFE)
# -----------------------------
ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial Black,96,&H00FFFFFF,&H0000FF00,&H00000000,&H64000000,1,0,0,0,100,100,2,0,1,4,2,2,80,80,260,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def ts(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

# -----------------------------
# Build captions (NO OVERLAP)
# -----------------------------
events = []
current_time = 0.0

for i in range(0, len(words), WORDS_PER_PHRASE):
    phrase = words[i:i + WORDS_PER_PHRASE]

    # Highlight middle word
    mid = len(phrase) // 2
    phrase[mid] = r"{\c&H0000FF&}" + phrase[mid] + r"{\c&H00FFFFFF&}"

    text_line = " ".join(phrase)

    # Hard wrap to max 2 lines
    wrapped = textwrap.fill(text_line, width=18)
    lines = wrapped.split("\n")[:2]
    rendered = r"\N".join(lines)

    start = ts(current_time)
    end = ts(current_time + caption_time)

    events.append(
        f"Dialogue: 0,{start},{end},Default,,0,0,0,,{rendered}"
    )

    # IMPORTANT: next caption starts AFTER this ends
    current_time += spoken_phrase_time

with open("captions.ass", "w", encoding="utf-8") as f:
    f.write(ass + "\n".join(events))

print("✅ Clean, non-stacking captions generated")
