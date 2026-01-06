import subprocess
import re
import math

# -------------------------------------------------
# Load script
# -------------------------------------------------
text = open("script.txt", "r", encoding="utf-8").read().strip()
words = re.findall(r"\b[\w’']+\b", text)

if not words:
    raise Exception("No words found in script")

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
# Caption pacing (Shorts-optimized)
# -------------------------------------------------
WORDS_PER_PHRASE = 3          # ideal for reading speed
READABILITY_BOOST = 1.3      # captions stay longer than speech

total_phrases = math.ceil(len(words) / WORDS_PER_PHRASE)
spoken_time = duration / total_phrases
caption_time = spoken_time * READABILITY_BOOST

# -------------------------------------------------
# ASS header (VIRAL STYLE)
# -------------------------------------------------
ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding

; ===== VIRAL SHORTS STYLE =====
; Clean modern font, strong outline, soft shadow
Style: Default,DejaVu Sans Bold,104,&H00FFFFFF,&H0000FFFF,&H00000000,&H4A000000,1,0,0,0,100,100,3,0,1,6,3,3,70,70,300,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def ts(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

# -------------------------------------------------
# Build captions (ONE at a time, no overlap)
# -------------------------------------------------
events = []
current_time = 0.0
MAX_LINE_CHARS = 18  # prevents overflow on mobile

for i in range(0, len(words), WORDS_PER_PHRASE):
    phrase = words[i:i + WORDS_PER_PHRASE]

    # Choose highlight word (middle feels natural)
    hi = len(phrase) // 2

    # Build lines safely (no tag splitting)
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

    lines = lines[:2]  # max 2 lines

    # Apply highlight AFTER layout
    flat_index = 0
    for li in range(len(lines)):
        parts = lines[li].split()
        for pi in range(len(parts)):
            if flat_index == hi:
                parts[pi] = (
                    r"{\c&H0000FFFF&}"
                    + parts[pi] +
                    r"{\c&H00FFFFFF&}"
                )
            flat_index += 1
        lines[li] = " ".join(parts)

    rendered = r"\N".join(lines)

    start = ts(current_time)
    end = ts(current_time + caption_time)

    events.append(
        f"Dialogue: 0,{start},{end},Default,,0,0,0,,{rendered}"
    )

    # Next caption starts AFTER this one (no stacking)
    current_time += spoken_time

# -------------------------------------------------
# Write captions
# -------------------------------------------------
with open("captions.ass", "w", encoding="utf-8") as f:
    f.write(ass + "\n".join(events))

print("🔥 Viral YouTube Shorts captions generated")
