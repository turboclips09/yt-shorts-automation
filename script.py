import random
import json
import os

USED_FILE = "used_topics.json"

# -------------------------------------------------
# LOAD MEMORY (PREVENT REPEATS)
# -------------------------------------------------
if os.path.exists(USED_FILE):
    with open(USED_FILE, "r", encoding="utf-8") as f:
        used = set(json.load(f))
else:
    used = set()

# -------------------------------------------------
# TOPIC ENGINE (IDEA-LEVEL UNIQUE + EMOTIONAL)
# -------------------------------------------------
topics = {

    "danger_equals_fun": {
        "hook": [
            "Here’s something modern cars will never admit.",
            "This is why old cars felt more exciting than today’s supercars."
        ],
        "shock": [
            "Danger didn’t scare your brain. It woke it up.",
            "Your brain actually enjoys controlled risk."
        ],
        "points": [
            "Number one. Old cars punished mistakes instantly.",
            "Number two. That fear sharpened your senses.",
            "Number three. Modern cars remove fear, and excitement dies."
        ],
        "payoff": [
            "That’s why slower cars used to feel faster.",
            "The thrill wasn’t lost. It was removed on purpose."
        ]
    },

    "manuals_create_emotion": {
        "hook": [
            "Manual cars aren’t faster. But they feel more alive.",
            "There’s a reason manuals still have cult followings."
        ],
        "shock": [
            "Fun doesn’t come from speed. It comes from responsibility.",
            "Your brain loves being in charge."
        ],
        "points": [
            "Number one. Manuals force constant decision-making.",
            "Number two. Every shift has consequences.",
            "Number three. Consequences create emotional attachment."
        ],
        "payoff": [
            "That’s why manuals feel unforgettable.",
            "Automation kills involvement."
        ]
    },

    "steering_was_neutered": {
        "hook": [
            "Modern steering feels numb for a reason.",
            "Steering feel didn’t disappear by accident."
        ],
        "shock": [
            "Car companies removed feedback on purpose.",
            "Comfort was chosen over communication."
        ],
        "points": [
            "Number one. Hydraulic steering transmitted real forces.",
            "Number two. Electric steering filters sensations.",
            "Number three. Filtering removes trust and connection."
        ],
        "payoff": [
            "That’s why old cars talked to you.",
            "Silence feels safe, not exciting."
        ]
    },

    "sound_controls_speed": {
        "hook": [
            "Sound matters more than speed. Here’s proof.",
            "A loud slow car can feel faster than a silent fast one."
        ],
        "shock": [
            "Your brain measures speed using sound.",
            "Silence tricks your perception."
        ],
        "points": [
            "Number one. Engine noise signals acceleration.",
            "Number two. Quiet removes urgency.",
            "Number three. That’s why EVs feel fast but empty."
        ],
        "payoff": [
            "Speed is math. Sound is emotion.",
            "Emotion is what you remember."
        ]
    },

    "supercars_are_too_good": {
        "hook": [
            "Supercars are incredible. And that’s the problem.",
            "Here’s why supercars don’t feel as fun as you expect."
        ],
        "shock": [
            "Perfection removes struggle.",
            "And struggle creates excitement."
        ],
        "points": [
            "Number one. Electronics stop mistakes instantly.",
            "Number two. You never explore the limit.",
            "Number three. No limits means no adrenaline."
        ],
        "payoff": [
            "That’s why normal cars can feel more fun.",
            "Perfection impresses. Imperfection excites."
        ]
    },

    "weight_kills_fun": {
        "hook": [
            "Cars didn’t get boring. They got heavy.",
            "Weight is the silent fun killer."
        ],
        "shock": [
            "Your brain feels mass before speed.",
            "Heaviness dulls excitement."
        ],
        "points": [
            "Number one. Heavy cars react slower.",
            "Number two. Feedback disappears.",
            "Number three. Lightness creates joy."
        ],
        "payoff": [
            "That’s why lightweight cars feel alive.",
            "Physics never lies."
        ]
    },

    "tech_made_drivers_worse": {
        "hook": [
            "Drivers didn’t get worse by accident.",
            "Modern cars quietly trained bad drivers."
        ],
        "shock": [
            "Technology removed consequences.",
            "And consequences create skill."
        ],
        "points": [
            "Number one. Cars fix mistakes instantly.",
            "Number two. Drivers stop learning limits.",
            "Number three. Skill fades without feedback."
        ],
        "payoff": [
            "That’s why old drivers felt sharper.",
            "Comfort changes behavior."
        ]
    },

    "ev_emotion_gap": {
        "hook": [
            "Electric cars feel fast. But not exciting.",
            "EVs hide a serious emotional problem."
        ],
        "shock": [
            "Instant torque isn’t enough.",
            "Emotion needs build-up."
        ],
        "points": [
            "Number one. EVs add massive weight.",
            "Number two. Sound disappears.",
            "Number three. Speed loses drama."
        ],
        "payoff": [
            "That’s why EVs feel impressive, not thrilling.",
            "Emotion needs friction."
        ]
    }
}

# -------------------------------------------------
# PICK UNUSED TOPIC
# -------------------------------------------------
available = [k for k in topics if k not in used]

if not available:
    used.clear()
    available = list(topics.keys())

topic_key = random.choice(available)
used.add(topic_key)

with open(USED_FILE, "w", encoding="utf-8") as f:
    json.dump(list(used), f, indent=2)

topic = topics[topic_key]

# -------------------------------------------------
# BUILD VIRAL SCRIPT (FIXED STRUCTURE)
# -------------------------------------------------
script = " ".join([
    random.choice(topic["hook"]),
    random.choice(topic["shock"]),
    topic["points"][0],
    topic["points"][1],
    topic["points"][2],
    random.choice(topic["payoff"]),
    "Once you notice this, you can’t unfeel it."
])

# -------------------------------------------------
# WRITE OUTPUT
# -------------------------------------------------
with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script)

print(f"✅ VIRAL script generated | topic = {topic_key}")
print(script)
