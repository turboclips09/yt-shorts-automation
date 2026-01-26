import random
import json
import os

# --------------------------------
# FILES
# --------------------------------
BRAIN_FILE = "brain.json"
USED_FILE = "used_topics.json"

brain = json.load(open(BRAIN_FILE))

if os.path.exists(USED_FILE):
    used = set(json.load(open(USED_FILE)))
else:
    used = set()

# --------------------------------
# SCRIPT STYLES
# --------------------------------
STYLES = {
    "aggressive": "Fast. Bold. Punchy.",
    "mysterious": "Slow. Curious. Hidden truth.",
    "story": "Mini story with twist.",
    "educational": "Facts + explanations.",
    "controversial": "Challenges belief."
}

# --------------------------------
# MASSIVE TOPIC POOL (EXPANDED)
# --------------------------------
TOPICS = {

"old_vs_new": [
"Old cars felt alive.",
"Modern cars feel perfect.",
"Perfect removes struggle.",
"Struggle creates emotion.",
"That’s what disappeared."
],

"manual_magic": [
"Manual cars force thinking.",
"Thinking creates involvement.",
"Involvement creates emotion.",
"Emotion creates addiction.",
"That’s why manuals survive."
],

"danger_equals_fun": [
"Your brain likes danger.",
"Not chaos. Controlled danger.",
"Old cars had consequences.",
"Consequences create focus.",
"Focus creates thrill."
],

"sound_psychology": [
"Your brain measures speed using sound.",
"Loud equals fast.",
"Quiet equals slow.",
"That’s why EVs feel empty.",
"Speed needs drama."
],

"weight_problem": [
"Cars got heavier.",
"Heavier means slower reactions.",
"Slower reactions feel boring.",
"Light cars feel playful.",
"Physics never lies."
],

"supercars_problem": [
"Supercars are too good.",
"They hide their limits.",
"No limits means no adrenaline.",
"No adrenaline means no memory.",
"That’s the paradox."
],

"steering_numb": [
"Modern steering is filtered.",
"Old steering was raw.",
"Raw equals communication.",
"Communication builds trust.",
"Trust builds connection."
],

"tech_ruined_drivers": [
"Cars fix mistakes.",
"Drivers stop learning.",
"Skill fades.",
"Confidence becomes fake.",
"That’s dangerous."
],

"ev_emotion_gap": [
"EVs are fast.",
"But not exciting.",
"Excitement needs buildup.",
"Instant removes buildup.",
"That’s the problem."
],

"drivers_vs_passengers": [
"Old drivers were operators.",
"Modern drivers are passengers.",
"Passengers don’t feel control.",
"Control creates emotion.",
"Emotion creates love."
],

"braking_feel": [
"Old brakes talked.",
"New brakes isolate.",
"Isolation removes fear.",
"No fear means no thrill.",
"Simple."
],

"clutch_magic": [
"The clutch is a conversation.",
"You listen.",
"You respond.",
"That’s bonding.",
"Machines rarely bond."
],

"first_car_memory": [
"Everyone remembers their first car.",
"Not their fastest.",
"Not their best.",
"Their first.",
"Emotion beats numbers."
],

"cheap_fast_vs_expensive_slow": [
"A cheap fun car beats a perfect one.",
"Fun isn’t expensive.",
"Fun is involvement.",
"Involvement is cheap.",
"Manufacturers forgot."
],

"why_people_modify": [
"People modify for feel.",
"Not for speed.",
"Feel beats numbers.",
"Always has.",
"Always will."
],

"why_car_meets_exist": [
"People want connection.",
"Not transportation.",
"Cars became culture.",
"Not appliances.",
"That matters."
]

}

# --------------------------------
# WEIGHTED PICK
# --------------------------------
def weighted_pick(pool, memory):
    keys=[]
    weights=[]
    for k in pool:
        w = memory.get(k,1.0)
        keys.append(k)
        weights.append(w)
    return random.choices(keys,weights=weights,k=1)[0]

topic = weighted_pick(TOPICS, brain["topics"])
style = weighted_pick(STYLES, brain["styles"])

if topic in used:
    topic = random.choice(list(TOPICS.keys()))

used.add(topic)
json.dump(list(used),open(USED_FILE,"w"))

lines = TOPICS[topic]
random.shuffle(lines)

# --------------------------------
# SCRIPT BUILDER
# --------------------------------
if style=="aggressive":
    script = f"{lines[0]} {lines[1]} {lines[2]} {lines[3]} {lines[4]} Once you notice this, you can’t unfeel it."

elif style=="mysterious":
    script = f"Nobody explains this. {lines[0]} {lines[2]} {lines[4]} Think about that."

elif style=="story":
    script = f"I once drove an old car. {lines[0]} {lines[1]} {lines[3]} {lines[4]} It changed how I see cars."

elif style=="educational":
    script = f"Here’s something most people miss. {lines[0]} {lines[1]} {lines[2]} {lines[3]} {lines[4]}"

else: # controversial
    script = f"People won’t like this. {lines[0]} {lines[1]} {lines[2]} {lines[3]} {lines[4]}"

with open("script.txt","w",encoding="utf-8") as f:
    f.write(script)

print("Topic:",topic)
print("Style:",style)
print(script)
