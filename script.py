import random
import json
import os

USED_FILE = "used_topics.json"

if os.path.exists(USED_FILE):
    used = set(json.load(open(USED_FILE)))
else:
    used = set()

# -------------------------------------------------
# STORY ENGINE WITH EMOTIONAL WAVES
# -------------------------------------------------
TOPICS = {

"manual_driver_story": {
"hook":[
"I didn’t expect a manual car to change anything.",
"I thought manuals were outdated."
],
"human":[
"Then I drove one.",
"I borrowed an old manual for a day."
],
"contrast":[
"It wasn’t fast.",
"It wasn’t perfect."
],
"tension":[
"But I couldn’t stop smiling.",
"I felt connected."
],
"reveal":[
"Every shift is a choice.",
"Choices create involvement.",
"Involvement creates emotion."
],
"payoff":[
"That’s why manuals survive."
],
"loop":[
"And this explains something bigger about modern life."
]
},

"old_car_feels_alive": {
"hook":[
"Old cars feel alive.",
"Modern cars feel finished."
],
"human":[
"I noticed this on a quiet road one night."
],
"contrast":[
"The old car felt rough.",
"The new one felt smooth."
],
"tension":[
"But only one felt exciting."
],
"reveal":[
"Old cars punished mistakes.",
"Modern cars erase them.",
"No consequences means no thrill."
],
"payoff":[
"That’s what disappeared."
],
"loop":[
"And you feel it everywhere."
]
},

"sound_speed_psych": {
"hook":[
"A loud slow car can feel faster than a silent fast one."
],
"human":[
"I didn’t believe it until I felt it."
],
"contrast":[
"Same road.",
"Same speed."
],
"tension":[
"Completely different feeling."
],
"reveal":[
"Your brain measures speed using sound.",
"Sound creates drama."
],
"payoff":[
"Silence feels empty."
],
"loop":[
"EVs accidentally proved it."
]
},

"drivers_to_passengers": {
"hook":[
"Drivers didn’t change.",
"Cars did."
],
"human":[
"My dad drove differently than I do."
],
"contrast":[
"He controlled everything.",
"My car controls itself."
],
"tension":[
"That feels safer.",
"But also emptier."
],
"reveal":[
"Less control removes involvement.",
"Less involvement removes emotion."
],
"payoff":[
"That’s why driving feels different."
],
"loop":[
"And it wasn’t accidental."
]
},

"first_car_memory": {
"hook":[
"You remember your first car."
],
"human":[
"Not your fastest.",
"Not your best."
],
"contrast":[
"Your first."
],
"tension":[
"Why?"
],
"reveal":[
"Because emotion beats numbers."
],
"payoff":[
"Always has."
],
"loop":[
"And always will."
]
}

}

# -------------------------------------------------
# PICK UNUSED TOPIC
# -------------------------------------------------
available = [k for k in TOPICS if k not in used]
if not available:
    used.clear()
    available = list(TOPICS.keys())

topic = random.choice(available)
used.add(topic)
json.dump(list(used), open(USED_FILE,"w"))

t = TOPICS[topic]

# -------------------------------------------------
# BUILD STORY
# -------------------------------------------------
script = " ".join([
    random.choice(t["hook"]),
    random.choice(t["human"]),
    random.choice(t["contrast"]),
    random.choice(t["tension"]),
    random.choice(t["reveal"]),
    random.choice(t["payoff"]),
    random.choice(t["loop"])
])

# -------------------------------------------------
# SAVE
# -------------------------------------------------
with open("script.txt","w",encoding="utf-8") as f:
    f.write(script)

print("Topic:",topic)
print(script)
