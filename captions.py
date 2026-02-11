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

# Aggressive short lines
lines = textwrap.wrap(text, 14)

total_chars = sum(len(l) for l in lines)

header = """[Script Info]
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Alignment, MarginV, Outline, Shadow

Style: Normal,Poppins,78,&H00FFFFFF,&H00000000,&H00000000,1,5,150,4,1
Style: Hook,Poppins,92,&H00FFFFFF,&H00000000,&H00000000,1,5,170,5,1
Style: Climax,Poppins,88,&H00FFFFFF,&H00000000,&H00000000,1,5,160,5,1

[Events]
Format: Layer, Start, End, Style, Text
"""

def t(sec):
    return f"0:00:{sec:05.2f}"

events=[]
start=0

for i, line in enumerate(lines):

    proportion = len(line) / total_chars
    line_duration = dur * proportion

    # Minimum readable duration
    if line_duration < 0.30:
        line_duration = 0.30

    # Hook style (first 2 lines)
    if i < 2:
        style = "Hook"
        line_duration *= 1.15
    # Climax (last 2 lines)
    elif i >= len(lines) - 2:
        style = "Climax"
        line_duration *= 1.20
    else:
        style = "Normal"

    end = start + line_duration

    events.append(
        f"Dialogue:0,{t(start)},{t(end)},{style},{line}"
    )

    start = end

# Force final caption to match audio exactly
if events:
    parts = events[-1].split(",")
    parts[2] = t(dur)
    events[-1] = ",".join(parts)

open("captions.ass","w",encoding="utf-8").write(header+"\n".join(events))
