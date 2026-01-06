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
# Caption pacing (locked to speech)
# -------------------------------------------------
WORDS_PER_PHRASE = 3
total_phrases = math.ceil(len(words) / WORDS_PER_PHRASE)
phrase_time = duration / total_phrases

# -------------------------------------------------
# ASS header (SHORTS-COOL STYLE)
# -------------------------------------------------
ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding

; ===== YOUTUBE SHORTS STYLE =====
Style: Default,DejaVu Sans Condensed Bold,108,&H00FFFFFF,&H0000E6FF,&H00000000,&H40000000,1,0,0,0,100,100,4,0,1,7,3,2,70,70,320,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def ts(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

# -------------------------------------------------
# Build captions (NO overlap, smooth pop)
# -------------------------------------------------
events = []
current_time = 0.0
MAX_LINE_CHARS = 16

for i in range(0, len(words), WORDS_PER_PHRASE):
    phrase = words[i:i + WORDS_PER_PHRASE]

    # Highlight middle word
    hi = len(phrase) // 2

    # Build lines safely
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

    # Apply highlight + subtle pop
    flat = 0
    for li in range(len(lines)):
        parts = lines[li].split()
        for pi in range(len(parts)):
            if flat == hi:
                parts[pi] = (
                    r"{\c&H0000E6FF&\fscx92\fscy92\t(0,140,\fscx100\fscy100)}"
                    + parts[pi] +
                    r"{\c&H00FFFFFF&}"
                )
            flat += 1
        lines[li] = " ".join(parts)

    rendered = r"\N".join(lines)

    start = ts(current_time)
    end = ts(current_time + phrase_time)

    events.append(
        f"Dialogue: 0,{start},{end},Default,,0,0,0,,{rendered}"
    )

    current_time += phrase_time

# -------------------------------------------------
# Write captions
# -------------------------------------------------
with open("captions.ass", "w", encoding="utf-8") as f:
    f.write(ass + "\n".join(events))

print("🔥 COOL YouTube Shorts captions generated")
