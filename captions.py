import json
import re

# Load word timestamps from edge-tts
with open("words.json", "r", encoding="utf-8") as f:
    words = json.load(f)

# Caption styling (ASS format)
ass_header = """[Script Info]
Title: Karaoke Captions
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Montserrat,96,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,6,0,5,80,80,400,1

[Events]
Format: Layer, Start, End, Style, Text
"""

def ms_to_ass(ms):
    h = ms // 3600000
    m = (ms % 3600000) // 60000
    s = (ms % 60000) // 1000
    cs = (ms % 1000) // 10
    return f"{h}:{m:02}:{s:02}.{cs:02}"

events = []
full_text = ""

for i, w in enumerate(words):
    start = ms_to_ass(w["offset"])
    end = ms_to_ass(w["offset"] + w["duration"])

    full_text += w["word"] + " "

    # Highlight current word in red
    highlighted = re.sub(
        re.escape(w["word"]),
        r"{\\c&H0000FF&}" + w["word"] + r"{\\c&HFFFFFF&}",
        full_text.strip(),
        count=1
    )

    events.append(
        f"Dialogue: 0,{start},{end},Default,{highlighted}"
    )

with open("captions.ass", "w", encoding="utf-8") as f:
    f.write(ass_header + "\n".join(events))

print("✅ Karaoke-style captions generated (captions.ass)")
