import textwrap
import subprocess as sp

# Read script
text = open("script.txt","r",encoding="utf-8").read()

# Get voice duration
dur = float(sp.run([
    "ffprobe","-v","error",
    "-show_entries","format=duration",
    "-of","default=noprint_wrappers=1:nokey=1",
    "voice.mp3"
], capture_output=True, text=True).stdout.strip())

# Break into punchy short lines
lines = textwrap.wrap(text, 20)

total_chars = sum(len(l) for l in lines)

header = """[Script Info]
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Alignment, MarginV
Style: Default,Poppins,60,&H00FFFFFF,&H00000000,&H00000000,1,5,120

[Events]
Format: Layer, Start, End, Style, Text
"""

def t(sec):
    return f"0:00:{sec:05.2f}"

events=[]
start=0

for line in lines:
    proportion = len(line) / total_chars
    line_duration = dur * proportion
    end = start + line_duration

    events.append(
        f"Dialogue:0,{t(start)},{t(end)},Default,{line}"
    )

    start = end

# Force last caption to end exactly at audio duration
if events:
    last = events[-1]
    parts = last.split(",")
    parts[2] = t(dur)
    events[-1] = ",".join(parts)

open("captions.ass","w",encoding="utf-8").write(header+"\n".join(events))
