import textwrap

text = open("script.txt","r",encoding="utf-8").read()

# Short lines for punch
lines = textwrap.wrap(text, 22)

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

for i,line in enumerate(lines):

    # Faster hook, slower ending
    if i < 3:
        dur = 0.55
    elif i > len(lines)-4:
        dur = 0.9
    else:
        dur = 0.7

    end=start+dur
    events.append(
        f"Dialogue:0,{t(start)},{t(end)},Default,{line}"
    )
    start=end

open("captions.ass","w",encoding="utf-8").write(header+"\n".join(events))
