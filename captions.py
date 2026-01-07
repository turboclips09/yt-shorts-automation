import json
import math

# -------------------------------------------------
# Load word-level timestamps
# -------------------------------------------------
with open("words.json", "r", encoding="utf-8") as f:
    words = json.load(f)

if not words:
    raise Exception("❌ words.json is empty")

# Convert ms → seconds
def t(ms):
    return ms / 1000.0

# -------------------------------------------------
# Caption grouping rules (Shorts-optimized)
# -------------------------------------------------
WORDS_PER_PHRASE = 2      # 🔥 best sync + readability
MAX_GAP = 0.45            # seconds, prevents rushing

phrases = []
current = []

for w in words:
    if not current:
        current.append(w)
        continue

    gap = t(w["offset"]) - t(current[-1]["offset"] + current[-1]["duration"])

    if len(current) >= WORDS_PER_PHRASE or gap > MAX_GAP:
        phrases.append(current)
        current = [w]
    else:
        current.append(w)

if current:
    phrases.append(current)

# -------------------------------------------------
# ASS Header (PREMIUM SHORTS STYLE)
# -------------------------------------------------
ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding

Style: Default,Poppins ExtraBold,120,&H00FFFFFF,&H0000E6FF,&H00000000,&H3A000000,1,0,0,0,100,100,4,0,1,7,4,3,60,60,320,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def ts(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h}:{m:02d}:{s:05.2f}"

# -------------------------------------------------
# Build captions (VOICE-LOCKED)
# -------------------------------------------------
events = []

for phrase in phrases:
    start = t(phrase[0]["offset"])
    end = t(phrase[-1]["offset"] + phrase[-1]["duration"])

    # Safety padding (prevents flash)
    end += 0.08

    words_text = [w["word"].upper() for w in phrase]
    hi = len(words_text) // 2

    rendered = []
    for i, w in enumerate(words_text):
        if i == hi:
            rendered.append(
                r"{\c&H0000E6FF&\fscx92\fscy92\t(0,160,\fscx100\fscy100)}"
                + w +
                r"{\c&H00FFFFFF&}"
            )
        else:
            rendered.append(w)

    text = " ".join(rendered)

    events.append(
        f"Dialogue: 0,{ts(start)},{ts(end)},Default,,0,0,0,,{text}"
    )

# -------------------------------------------------
# Write ASS
# -------------------------------------------------
with open("captions.ass", "w", encoding="utf-8") as f:
    f.write(ass + "\n".join(events))

print("✅ Captions perfectly synced to voice (word-level)")
