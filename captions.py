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
# Caption pacing (KEY FIX)
# -----------------------------
WORDS_PER_PHRASE = 3          # readable chunk
HOLD_MULTIPLIER = 1.3         # captions stay longer than speech
OVERLAP = 0.12                # smooth transitions

total_phrases = math.ceil(len(words) / WORDS_PER_PHRASE)
base_phrase_time = duration / total_phrases
phrase_time = base_phrase_time * HOLD_MULTIPLIER

# -----------------------------
# ASS header (LOUD BUT CLEAN)
# -----------------------------
ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Impact,100,&H00FFFFFF,&H0000FF00,&H00000000,&H64000000,1,0,0,0,100,100,1,0,1,5,3,2,80,80,300,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def ts(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

# -----------------------------
# Build captions
# -----------------------------
events = []
current_time = 0.0

for i in range(0, len(words), WORDS_PER_PHRASE):
    phrase = words[i:i + WORDS_PER_PHRASE]

    # highlight middle word (feels most natural)
    mid = len(phrase) // 2
    rendered = " ".join(
        phrase[:mid]
        + [r"{\c&H0000FF&}" + phrase[mid] + r"{\c&H00FFFFFF&}"]
        + phrase[mid + 1:]
    )

    start = ts(max(0, current_time - OVERLAP))
    end = ts(current_time + phrase_time)

    events.append(
        f"Dialogue: 0,{start},{end},Default,,0,0,0,,{rendered}"
    )

    current_time += base_phrase_time

with open("captions.ass", "w", encoding="utf-8") as f:
    f.write(ass + "\n".join(events))

print("✅ Smooth, speech-matched captions generated")
