import random
import json
import os

USED_FILE = "used_topics.json"

# -------------------------------------------------
# LOAD MEMORY
# -------------------------------------------------
if os.path.exists(USED_FILE):
    with open(USED_FILE, "r", encoding="utf-8") as f:
        used = set(json.load(f))
else:
    used = set()

# -------------------------------------------------
# MASSIVE TOPIC POOL (IDEA-LEVEL UNIQUE)
# -------------------------------------------------
topics = {

    "old_vs_modern_danger": {
        "hook": [
            "Modern cars are insanely fast. But they don’t feel exciting anymore.",
            "Speed has never been higher. Excitement has never been lower."
        ],
        "points": [
            "Number one. Old cars were dangerous, and your brain loved it.",
            "Number two. Fear sharpened your focus and amplified every sensation.",
            "Number three. Modern cars remove danger, and excitement disappears."
        ],
        "payoff": [
            "That’s why slower cars used to feel faster.",
            "The thrill didn’t vanish. It was engineered out."
        ]
    },

    "manual_transmissions": {
        "hook": [
            "There’s a reason manual cars feel more fun, even when they’re slower.",
            "Manual cars aren’t faster. They’re more engaging."
        ],
        "points": [
            "Number one. Manuals force you to think ahead constantly.",
            "Number two. Every gear change is a decision, not automation.",
            "Number three. Responsibility creates connection."
        ],
        "payoff": [
            "That’s why manuals feel alive.",
            "Automation removes involvement."
        ]
    },

    "steering_feel": {
        "hook": [
            "Steering feel didn’t disappear by accident.",
            "Modern steering feels numb for a reason."
        ],
        "points": [
            "Number one. Hydraulic steering transmitted real road forces.",
            "Number two. Electric steering filters feedback for comfort.",
            "Number three. Comfort increases, communication dies."
        ],
        "payoff": [
            "That’s why old cars talked to you.",
            "Modern cars stay silent."
        ]
    },

    "sound_vs_speed": {
        "hook": [
            "Sound matters more than speed, and here’s proof.",
            "A loud slow car can feel faster than a silent fast one."
        ],
        "points": [
            "Number one. Sound tells your brain how fast you’re moving.",
            "Number two. Silence removes your sense of speed.",
            "Number three. That’s why EVs feel fast but forgettable."
        ],
        "payoff": [
            "Speed is numbers. Sound is emotion.",
            "Emotion is what sticks."
        ]
    },

    "supercars_problem": {
        "hook": [
            "Supercars are incredible, yet somehow underwhelming.",
            "Today’s supercars are faster than ever, but less thrilling."
        ],
        "points": [
            "Number one. Electronics prevent you from exploring the limits.",
            "Number two. You experience perfection, not struggle.",
            "Number three. Struggle creates excitement."
        ],
        "payoff": [
            "That’s why normal cars can feel more fun.",
            "Perfection impresses, not excites."
        ]
    },

    "weight_problem": {
        "hook": [
            "Cars keep getting heavier, and it’s killing the fun.",
            "Weight is the silent performance killer."
        ],
        "points": [
            "Number one. Heavier cars feel slower to respond.",
            "Number two. Weight dulls steering, braking, and acceleration.",
            "Number three. Lightness creates agility."
        ],
        "payoff": [
            "That’s why lightweight cars feel alive.",
            "Mass kills feedback."
        ]
    },

    "turbo_vs_na": {
        "hook": [
            "Turbo engines are faster, but something feels missing.",
            "Naturally aspirated engines feel different for a reason."
        ],
        "points": [
            "Number one. Turbos compress power into bursts.",
            "Number two. NA engines deliver power linearly.",
            "Number three. Linear power feels predictable and engaging."
        ],
        "payoff": [
            "That’s why NA engines feel special.",
            "Smoothness builds connection."
        ]
    },

    "driver_skills_decline": {
        "hook": [
            "Drivers didn’t get worse by accident.",
            "Modern cars quietly made drivers lazy."
        ],
        "points": [
            "Number one. Cars correct mistakes instantly.",
            "Number two. Drivers stop learning vehicle limits.",
            "Number three. Skill fades when consequences disappear."
        ],
        "payoff": [
            "That’s why old drivers felt sharper.",
            "Technology changes behavior."
        ]
    },

    "ev_weight_problem": {
        "hook": [
            "Electric cars feel quick, but something feels off.",
            "EVs hide a massive problem."
        ],
        "points": [
            "Number one. Batteries add huge amounts of weight.",
            "Number two. Weight reduces feedback and agility.",
            "Number three. Speed increases, feel decreases."
        ],
        "payoff": [
            "That’s why EVs feel impressive, not emotional.",
            "Physics always wins."
        ]
    },

    "brake_feel": {
        "hook": [
            "Brake feel matters more than stopping power.",
            "Strong brakes don’t always feel good."
        ],
        "points": [
            "Number one. Pedal feel builds confidence.",
            "Number two. Confidence allows precision.",
            "Number three. Electronic systems dull feedback."
        ],
        "payoff": [
            "That’s why older brakes felt better.",
            "Feel matters more than force."
        ]
    },

    "traction_control": {
        "hook": [
            "Traction control is a double-edged sword.",
            "Traction control saves lives, but costs excitement."
        ],
        "points": [
            "Number one. It prevents loss of control.",
            "Number two. It blocks learning vehicle limits.",
            "Number three. Limits create excitement."
        ],
        "payoff": [
            "That’s why raw cars feel intense.",
            "Control removes drama."
        ]
    },

    "gearbox_speed": {
        "hook": [
            "Fast gearboxes don’t guarantee fun.",
            "Instant shifts changed driving forever."
        ],
        "points": [
            "Number one. Quick shifts remove anticipation.",
            "Number two. Anticipation creates engagement.",
            "Number three. Engagement makes memories."
        ],
        "payoff": [
            "That’s why slower gearboxes feel better.",
            "Waiting builds excitement."
        ]
    },

    "analog_vs_digital": {
        "hook": [
            "Analog cars feel alive for a reason.",
            "Digital cars feel impressive, not emotional."
        ],
        "points": [
            "Number one. Analog systems respond directly.",
            "Number two. Digital systems filter reactions.",
            "Number three. Filtering removes connection."
        ],
        "payoff": [
            "That’s why analog feels real.",
            "Reality creates emotion."
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
# BUILD SCRIPT
# -------------------------------------------------
script = " ".join([
    random.choice(topic["hook"]),
    topic["points"][0],
    topic["points"][1],
    topic["points"][2],
    random.choice(topic["payoff"]),
    "Once you notice this, you’ll never drive the same way again."
])

with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script)

print(f"✅ script.txt generated | topic = {topic_key}")
print(script)
