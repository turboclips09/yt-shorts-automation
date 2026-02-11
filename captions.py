import json

# Load word timing
with open("word_timings.json") as f:
    words = json.load(f)

if not words:
    raise RuntimeError("No word timings found")

# Group words into short punchy caption chunks
chunks = []
current_chunk = []
current_start = None

MAX_WORDS_PER_CHUNK = 4  # small chunks for TikTok energy

for w in words:
    if current_start is None:
        current_start = w["start"]

    current_chunk.append(w["word"])

    if len(current_chunk) >= MAX_WORDS_PER_CHUNK:
        end_time = w["start"] + w["duration"]
        chunks.append({
            "text": " ".join(current_chunk),
            "start": current_start,
            "end": end_time
        })
        current_chunk = []
        current_start = None

# Add leftover words
if current_chunk:
    end_time = words[-1]["start"] + words[-1]["duration"]
    chunks.append({
        "text": " ".join(current_chunk),
        "start": current_start,
        "end": end_time
    })

# ASS header
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

for i, chunk in enumerate(chunks):

    if i < 2:
        style = "Hook"
    elif i >= len(chunks) - 2:
        style = "Climax"
    else:
        style = "Normal"

    events.append(
        f"Dialogue:0,{t(chunk['start'])},{t(chunk['end'])},{style},{chunk['text']}"
    )

open("captions.ass","w",encoding="utf-8").write(header+"\n".join(events))
