import json
import re

with open("words.json", "r", encoding="utf-8") as f:
    words = json.load(f)

ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,88,&H00FFFFFF,&H0000FF00,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,5,2,2,80,80,260,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def to_ass_time(ms):
    s = ms / 1000
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    s = s % 60
    return f"{h}:{m:02d}:{s:05.2f}"

events = []
line = ""

for w in words:
    word = w["word"]
    line += word + " "

    highlighted = re.sub(
        re.escape(word),
        r"{\\c&H0000FF&}" + word + r"{\\c&H00FFFFFF&}",
        line.strip(),
        count=1
    )

    start = to_ass_time(w["offset"])
    end = to_ass_time(w["offset"] + w["duration"])

    events.append(
        f"Dialogue: 0,{start},{end},Default,,0,0,0,,{highlighted}"
    )

with open("captions.ass", "w", encoding="utf-8") as f:
    f.write(ass_header + "\n".join(events))

print("✅ VALID karaoke ASS captions generated")
