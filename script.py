import random
import json
import os

# --------------------------------
# FILES
# --------------------------------
BRAIN_FILE = "brain.json"
USED_FILE = "used_topics.json"

if os.path.exists(BRAIN_FILE):
    brain = json.load(open(BRAIN_FILE))
else:
    brain = {"topics": {}, "styles": {}}

if os.path.exists(USED_FILE):
    used = set(json.load(open(USED_FILE)))
else:
    used = set()

# --------------------------------
# STYLES
# --------------------------------
STYLES = [
    "aggressive",
    "mysterious",
    "story",
    "educational",
    "controversial"
]

# --------------------------------
# MASSIVE TOPIC DATABASE
# --------------------------------
TOPICS = {

"manual_magic": {
"hooks":[
"Manual cars aren’t faster. But they feel better.",
"Manual cars refuse to die. Here’s why."
],
"ideas":[
"Manuals force you to think.",
"Every shift is a decision.",
"Decisions create involvement.",
"Involvement creates emotion.",
"Emotion creates attachment."
],
"payoff":[
"That’s why manuals feel alive.",
"Automation killed the magic."
]
},

"old_vs_new": {
"hooks":[
"Old cars felt slower. But more exciting.",
"Modern cars are faster. Yet boring."
],
"ideas":[
"Old cars punished mistakes.",
"You had to pay attention.",
"Modern cars fix everything.",
"No consequences means no thrill."
],
"payoff":[
"That’s what disappeared.",
"And you feel it every drive."
]
},

"sound_psychology": {
"hooks":[
"Sound matters more than speed.",
"A loud slow car can feel faster than a silent fast one."
],
"ideas":[
"Your brain measures speed using sound.",
"Sound creates drama.",
"Drama creates excitement."
],
"payoff":[
"Silence feels empty.",
"Speed without sound feels dead."
]
},

"weight_problem": {
"hooks":[
"Cars didn’t get boring. They got heavy.",
"Weight is the real fun killer."
],
"ideas":[
"Heavy cars react slower.",
"Slower reactions feel dull.",
"Light cars feel playful."
],
"payoff":[
"Physics never lies.",
"Playful feels fun."
]
},

"ev_emotion_gap": {
"hooks":[
"EVs feel fast. But not exciting.",
"Electric cars hide a big problem."
],
"ideas":[
"They’re silent.",
"They have no build-up.",
"Your brain needs build-up.",
"Build-up creates anticipation."
],
"payoff":[
"That’s why EVs feel impressive, not thrilling."
]
},

"steering_feel": {
"hooks":[
"Modern steering feels numb.",
"It wasn’t always this way."
],
"ideas":[
"Old steering transmitted forces.",
"You felt grip through your hands.",
"Feeling creates trust.",
"Trust creates confidence."
],
"payoff":[
"That’s what modern cars lost."
]
},

"cheap_fun_cars": {
"hooks":[
"Fun isn’t expensive.",
"Some cheap cars are more fun than supercars."
],
"ideas":[
"Low weight.",
"Simple engines.",
"Nothing filtered.",
"Everything mechanical."
],
"payoff":[
"Fun was never about money."
]
},

"first_car_memory": {
"hooks":[
"You remember your first car.",
"Not your fastest. Not your best."
],
"ideas":[
"You remember how it made you feel.",
"Emotion beats numbers.",
"Always has."
],
"payoff":[
"That’s why nostalgia never dies."
]
},

"modding_culture": {
"hooks":[
"People don’t modify for speed.",
"They modify for feel."
],
"ideas":[
"Exhaust for sound.",
"Suspension for response.",
"Wheels for stance.",
"Steering for feedback."
],
"payoff":[
"Feel matters more than numbers."
]
},

"drivers_vs_passengers": {
"hooks":[
"Old drivers were operators.",
"Modern drivers are passengers."
],
"ideas":[
"Cars make decisions now.",
"Less control.",
"Less involvement.",
"Less emotion."
],
"payoff":[
"That’s why driving feels different."
]
}

}

# --------------------------------
# WEIGHTED PICK
# --------------------------------
def weighted_pick(pool, memory):
    keys=[]
    weights=[]
    for k in pool:
        keys.append(k)
        weights.append(memory.get(k,1.0))
    return random.choices(keys,weights=weights,k=1)[0]

topic = weighted_pick(TOPICS, brain.get("topics",{}))
style = weighted_pick(STYLES, brain.get("styles",{}))

if topic in used:
    topic = random.choice(list(TOPICS.keys()))

used.add(topic)
json.dump(list(used),open(USED_FILE,"w"))

data = TOPICS[topic]

# --------------------------------
# SCRIPT BUILDERS
# --------------------------------
def aggressive(d):
    return (
        f"{random.choice(d['hooks'])} "
        f"{d['ideas'][0]} {d['ideas'][1]} {d['ideas'][2]} "
        f"{random.choice(d['payoff'])} "
        "Once you notice this, you can’t unfeel it."
    )

def mysterious(d):
    return (
        f"Nobody talks about this. "
        f"{random.choice(d['hooks'])} "
        f"{d['ideas'][0]} {d['ideas'][2]} "
        f"{random.choice(d['payoff'])}"
    )

def story(d):
    return (
        f"I noticed something while driving. "
        f"{random.choice(d['hooks'])} "
        f"{d['ideas'][0]} {d['ideas'][1]} "
        f"{random.choice(d['payoff'])}"
    )

def educational(d):
    return (
        f"Here’s something most people miss. "
        f"{random.choice(d['hooks'])} "
        f"{d['ideas'][0]} {d['ideas'][1]} {d['ideas'][2]} "
        f"{random.choice(d['payoff'])}"
    )

def controversial(d):
    return (
        f"People won’t like this. "
        f"{random.choice(d['hooks'])} "
        f"{d['ideas'][1]} {d['ideas'][2]} "
        f"{random.choice(d['payoff'])}"
    )

STYLE_FUNCS = {
"aggressive": aggressive,
"mysterious": mysterious,
"story": story,
"educational": educational,
"controversial": controversial
}

script = STYLE_FUNCS[style](data)

# --------------------------------
# SAVE
# --------------------------------
with open("script.txt","w",encoding="utf-8") as f:
    f.write(script)

print("Topic:",topic)
print("Style:",style)
print(script)
