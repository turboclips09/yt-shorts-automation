import re
import subprocess
import math

# -------------------------------
# READ SCRIPT
# -------------------------------
text = open("script.txt", "r", encoding="utf-8").read().strip()

# Split into phrases by punctuation
phrases = re.split(r"[,.!?]", text)
phrases = [p.strip() for p in phrases if len(p.strip().split()) >= 2]

# -------------------------------
# GET AUDIO DURATION
# -------------------------------
probe = subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
     "-of", "default=noprint_wrappers=1:nokey=1", "voice.mp3"],
    capture_output=True, text=True
)

duration = float(probe.stdout.strip())

# -------------------------------
# TIMING LOGIC
# -------------------------------
time_per_phrase = duration / len(phrases)

def ts(t):
    m = int(t // 60)
    s = t % 60
    return f"0:{m:02d}:{s:05.2f}"

# -------------------------------
# ASS FILE
# -------------------------------
ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Alignment, MarginV
Style: Default,Poppins,96,&H00FFFFFF,&H00000000,&H64000000,1,2,220

[Events]
Format: Layer, Start, End, Style, Text
"""

t = 0.0
for p in phrases:
    start = ts(t)
    end = ts(t + time_per_phrase)
    ass += f"Dialogue: 0,{start},{end},Default,{p.upper()}\n"
    t += time_per_phrase

open("captions.ass", "w", encoding="utf-8").write(ass)
print("✅ Captions generated (phrase-synced)")
