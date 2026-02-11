import json
import subprocess as sp
import os
import textwrap

def t(sec):
    return f"0:00:{sec:05.2f}"

# Check if word timings exist
if os.path.exists("word_timings.json"):
    with open("word_timings.json") as f:
        words = json.load(f)
else:
    words = []

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

events=[]

# ---------------------------------------------------
# CASE 1: True word timing available
# ---------------------------------------------------
if words:

    MAX_WORDS_PER_CHUNK = 4
    chunk = []
    start_time = None

    for i, w in enumerate(words):

        if start_time is None:
            start_time = w["start"]

        chunk.append(w["word"])

        if len(chunk) >= MAX_WORDS_PER_CHUNK:
            end_time = w["end"]

            style = "Normal"
            if len(events) < 2:
                style = "Hook"

            events.append(
                f"Dialogue:0,{t(start_time)},{t(end_time)},{style},{' '.join(chunk)}"
            )

            chunk = []
            start_time = None

    # Handle remainder
    if chunk:
        end_time = words[-1]["end"]
        events.append(
            f"Dialogue:0,{t(start_time)},{t(end_time)},Climax,{' '.join(chunk)}"
        )

# ---------------------------------------------------
# CASE 2: Fallback (proportional timing)
# ---------------------------------------------------
else:
    print("⚠ Using fallback caption timing")

    text = open("script.txt","r",encoding="utf-8").read()

    dur = float(sp.run([
        "ffprobe","-v","error",
        "-show_entries","format=duration",
        "-of","default=noprint_wrappers=1:nokey=1",
        "voice.mp3"
    ], capture_output=True, text=True).stdout.strip())

    lines = textwrap.wrap(text, 14)
    total_chars = sum(len(l) for l in lines)

    start = 0
    for i, line in enumerate(lines):
        proportion = len(line) / total_chars
        line_duration = dur * proportion

        end = start + line_duration

        style = "Normal"
        if i < 2:
            style = "Hook"
        elif i >= len(lines) - 2:
            style = "Climax"

        events.append(
            f"Dialogue:0,{t(start)},{t(end)},{style},{line}"
        )

        start = end

    if events:
        parts = events[-1].split(",")
        parts[2] = t(dur)
        events[-1] = ",".join(parts)

open("captions.ass","w",encoding="utf-8").write(header+"\n".join(events))
