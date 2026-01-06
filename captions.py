import json

words = json.load(open("words.json", "r", encoding="utf-8"))

if not words:
    raise Exception("❌ words.json is empty — cannot generate captions")

ass_header = """[Script Info]
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
"""

def to_time(ms):
    s = ms / 1000
    return f"0:00:{s:05.2f}"

start = to_time(words[0]["offset"])
end = to_time(words[-1]["offset"] + words[-1]["duration"])

karaoke = ""
for w in words:
    dur = max(1, int(w["duration"] / 10))  # centiseconds
    karaoke += f"{{\\k{dur}}}{w['word']} "

dialogue = f"Dialogue: 0,{start},{end},Default,,0,0,0,,{karaoke}"

with open("captions.ass", "w", encoding="utf-8") as f:
    f.write(ass_header + dialogue)

print("✅ Karaoke captions generated successfully")
