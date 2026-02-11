import textwrap
import subprocess as sp

# Get script
text = open("script.txt","r",encoding="utf-8").read()

# Get voice duration
dur = float(sp.run([
    "ffprobe","-v","error",
    "-show_entries","format=duration",
    "-of","default=noprint_wrappers=1:nokey=1",
    "voice.mp3"
], capture_output=True, text=True).stdout.strip())

# Split into short punch lines
lines = textwrap.wrap(text, 24)

# Distribute evenly across full audio duration
line_duration = dur / len(lines)

header = """[Script Info]
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Alignment, MarginV
Style: Default,Poppins,58,&H00FFFFFF,&H00000000,&H00000000,1,5,120

[Events]
Format: Layer, Start, End, Style, Text
"""

def t(sec):
    return f"0:00:{sec:05.2f}"

events=[]
start=0

for line in lines:
    end = start + line_duration
    events.append(
        f"Dialogue:0,{t(start)},{t(end)},Default,{line}"
    )
    start = end

open("captions.ass","w",encoding="utf-8").write(header+"\n".join(events))
