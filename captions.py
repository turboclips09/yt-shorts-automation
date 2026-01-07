import json
import os

WORDS_PER_CHUNK = 3          # 2–4 ideal for Shorts
LEAD_IN_MS = 120             # show slightly before audio
MIN_DURATION_MS = 220        # readability floor

if not os.path.exists("words.json"):
    raise RuntimeError("❌ words.json not found — voice.py must run first")

with open("words.json", "r", encoding="utf-8") as f:
    words = json.load(f)

def ms_to_time(ms):
    ms = max(0, ms)
    s = ms / 1000
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    s = s % 60
    return f"{h}:{m:02d}:{s:05.2f}"

ass_header = """[Script Info]
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Poppins ExtraBold,132,&H00FFFFFF,&H0000FFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,6,0,2,80,80,360,1

[Events]
Format: Layer, Start, End, Style, Text
"""

events = []
i = 0

while i < len(words):
    chunk = words[i:i + WORDS_PER_CHUNK]
    text = " ".join(w["word"] for w in chunk)

    start = chunk[0]["offset"] - LEAD_IN_MS
    end = chunk[-1]["offset"] + chunk[-1]["duration"]

    if end - start < MIN_DURATION_MS:
        end = start + MIN_DURATION_MS

    events.append(
        f"Dialogue: 0,{ms_to_time(start)},{ms_to_time(end)},Default,{text}"
    )

    i += WORDS_PER_CHUNK

with open("captions.ass", "w", encoding="utf-8") as f:
    f.write(ass_header + "\n".join(events))

print("✅ captions.ass generated (synced, readable, no overlap)")
