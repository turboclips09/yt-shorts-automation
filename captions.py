import textwrap
import subprocess as sp

# Read script
text = open("script.txt","r",encoding="utf-8").read()

# Get real voice duration
dur = float(sp.run([
    "ffprobe","-v","error",
    "-show_entries","format=duration",
    "-of","default=noprint_wrappers=1:nokey=1",
    "voice.mp3"
], capture_output=True, text=True).stdout.strip())

# Shorter lines for fast speech
lines = textwrap.wrap(text, 16)

total_chars = sum(len(l) for l in lines)

header = """[Script Info]
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Alignment, MarginV, Outline, Shadow

Style: Default,Poppins,78,&H00FFFFFF,&H00000000,&H00000000,1,5,150,4,1

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

    # minimum duration safeguard for readability
    if line_duration < 0.35:
        line_duration = 0.35

    end = start + line_duration

    events.append(
        f"Dialogue:0,{t(start)},{t(end)},Default,{line}"
    )

    start = end

# Force final caption to end exactly with audio
if events:
    parts = events[-1].split(",")
    parts[2] = t(dur)
    events[-1] = ",".join(parts)

open("captions.ass","w",encoding="utf-8").write(header+"\n".join(events))
