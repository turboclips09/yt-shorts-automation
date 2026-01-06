import json, re

words = json.load(open("words.json", "r", encoding="utf-8"))

ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,88,&H00FFFFFF,&H0000FF00,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,4,2,2,80,80,260,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def t(ms):
    s = ms / 1000
    return f"0:00:{s:05.2f}"

line = ""
events = []

for w in words:
    line += w["word"] + " "
    txt = re.sub(
        re.escape(w["word"]),
        r"{\\c&H0000FF&}" + w["word"] + r"{\\c&H00FFFFFF&}",
        line.strip(),
        count=1
    )
    events.append(
        f"Dialogue: 0,{t(w['offset'])},{t(w['offset']+w['duration'])},Default,,0,0,0,,{txt}"
    )

open("captions.ass", "w", encoding="utf-8").write(ass + "\n".join(events))
print("Captions ready")
