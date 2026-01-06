import subprocess
import re

# -----------------------------
# Load script
# -----------------------------
text = open("script.txt", "r", encoding="utf-8").read().strip()
words = re.findall(r"\b[\w’']+\b", text)

if not words:
    raise Exception("No words found in script")

# -----------------------------
# Get audio duration (seconds)
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

duration_sec = float(probe.stdout.strip())
duration_ms = duration_sec * 1000

# -----------------------------
# Karaoke timing
# -----------------------------
per_word_ms = duration_ms / len(words)
per_word_cs = max(1, int(per_word_ms / 10))  # centiseconds

karaoke = ""
for w in words:
    karaoke += f"{{\\k{per_word_cs}}}{w} "

start = "0:00:00.00"
end = f"0:00:{duration_sec:05.2f}"

# -----------------------------
# ASS file
# -----------------------------
ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial Black,96,&H00FFFFFF,&H0000FF00,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,5,2,2,60,60,260,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,{start},{end},Default,,0,0,0,,{karaoke}
"""

with open("captions.ass", "w", encoding="utf-8") as f:
    f.write(ass)

print("✅ Karaoke captions generated (audio-synced)")
