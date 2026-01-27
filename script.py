import random, json, os

BRAIN_FILE = "brain.json"
USED_FILE = "used_topics.json"

# -----------------------
# LOAD MEMORY
# -----------------------
brain = json.load(open(BRAIN_FILE))

if os.path.exists(USED_FILE):
    used = set(json.load(open(USED_FILE)))
else:
    used = set()

# -----------------------
# TOPIC LIBRARY (EXPANDABLE)
# -----------------------
TOPICS = {

"manual_identity": [
"Most people think manuals are about speed.",
"They’re not.",
"They’re about responsibility.",
"When you mess up, you feel it.",
"And strangely… that feels good.",
"Because effort creates attachment.",
"That’s why manuals refuse to die."
],

"old_vs_new_feel": [
"Old cars felt alive.",
"Not comfortable.",
"Not perfect.",
"Alive.",
"They fought you sometimes.",
"Modern cars remove the fight.",
"And they removed the feeling too."
],

"sound_psychology": [
"Your brain uses sound to measure speed.",
"Loud feels fast.",
"Quiet feels slow.",
"That’s why slow loud cars feel exciting.",
"And fast silent cars feel empty.",
"Speed is math.",
"Sound is emotion."
],

"first_car_memory": [
"You remember your first car.",
"Not your fastest.",
"Not your best.",
"Your first.",
"Because that’s where emotion formed.",
"Emotion beats horsepower.",
"Every time."
],

"drivers_to_passengers": [
"Old drivers were operators.",
"Modern drivers are passengers.",
"Cars decide more than you do.",
"Less control.",
"Less involvement.",
"Less emotion.",
"That’s the trade."
]

}

# -----------------------
# WEIGHTED PICK
# -----------------------
def weighted_pick():
    keys=[]
    weights=[]
    for k in TOPICS:
        w = brain["topics"].get(k,1.0)
        keys.append(k)
        weights.append(w)
    return random.choices(keys,weights=weights,k=1)[0]

topic = weighted_pick()

if topic in used:
    topic = random.choice(list(TOPICS.keys()))

used.add(topic)
json.dump(list(used),open(USED_FILE,"w"))

lines = TOPICS[topic]
random.shuffle(lines)

# -----------------------
# BUILD 45–60s SCRIPT
# -----------------------
script = " ".join([
"Here’s something nobody tells you about cars.",
lines[0],
lines[1],
lines[2],
lines[3],
lines[4],
lines[5],
lines[6],
"Once you notice this, you can’t unsee it."
])

with open("script.txt","w",encoding="utf-8") as f:
    f.write(script)

print("Topic:",topic)
print(script)
