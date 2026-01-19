import random
import json
import os

USED_TOPICS_FILE = "used_topics.json"
STYLE_STATE_FILE = "style_state.json"

# -------------------------------------------------
# LOAD MEMORY
# -------------------------------------------------
used_topics = set()
if os.path.exists(USED_TOPICS_FILE):
    used_topics = set(json.load(open(USED_TOPICS_FILE, "r", encoding="utf-8")))

style_state = {"index": 0}
if os.path.exists(STYLE_STATE_FILE):
    style_state = json.load(open(STYLE_STATE_FILE, "r", encoding="utf-8"))

STYLES = ["story", "insight", "myth"]

current_style = STYLES[style_state["index"] % len(STYLES)]
style_state["index"] += 1

# -------------------------------------------------
# TOPIC BRAIN (HIGH-QUALITY ONLY)
# -------------------------------------------------
TOPICS = {

    # ================= STORY =================
    "porsche_saved_911": {
        "style": "story",
        "lines": [
            "In the 1990s, Porsche almost killed the 911.",
            "Executives believed it was outdated and too dangerous.",
            "Engineers were told to make it safer and easier.",
            "But hardcore fans panicked.",
            "The 911 wasn’t supposed to be safe.",
            "It was supposed to be demanding.",
            "Porsche made a risky decision.",
            "They kept the difficulty.",
            "And the 911 became a legend."
        ]
    },

    "first_manual_memory": {
        "style": "story",
        "lines": [
            "Most people remember their first manual car forever.",
            "Not because it was fast.",
            "But because it made them feel responsible.",
            "Stalling felt embarrassing.",
            "A perfect shift felt incredible.",
            "The car reacted to your decisions.",
            "That relationship created emotion.",
            "Automation removes effort.",
            "And effort creates attachment."
        ]
    },

    "ferrari_driver_problem": {
        "style": "story",
        "lines": [
            "Ferrari once faced a strange problem.",
            "Their cars were becoming too fast for drivers.",
            "Reflexes couldn’t keep up anymore.",
            "So computers were added to help.",
            "Lap times improved instantly.",
            "But drivers felt disconnected.",
            "Ferrari learned something important.",
            "Speed alone isn’t excitement.",
            "Involvement is."
        ]
    },

    # ================= INSIGHT =================
    "why_old_cars_feel_alive": {
        "style": "insight",
        "lines": [
            "Old cars didn’t feel exciting because they were faster.",
            "They felt exciting because they talked to you.",
            "The steering pulled in your hands.",
            "The pedals vibrated.",
            "The engine sound rose naturally.",
            "Your brain stitched these signals together.",
            "Modern cars filter them out.",
            "Speed remains.",
            "Feeling disappears."
        ]
    },

    "sound_controls_speed": {
        "style": "insight",
        "lines": [
            "Your brain doesn’t measure speed with numbers.",
            "It measures it with sound.",
            "Loud engines signal danger and urgency.",
            "Silence signals control.",
            "That’s why loud slow cars feel fast.",
            "And quiet fast cars feel calm.",
            "Speed is physics.",
            "Sound is emotion."
        ]
    },

    "weight_kills_fun": {
        "style": "insight",
        "lines": [
            "Cars didn’t get boring.",
            "They got heavy.",
            "Your brain feels mass before speed.",
            "Heavy cars react slower.",
            "Feedback dulls.",
            "Confidence drops.",
            "Light cars communicate instantly.",
            "Physics doesn’t lie."
        ]
    },

    # ================= MYTH =================
    "horsepower_myth": {
        "style": "myth",
        "lines": [
            "More horsepower does not mean more fun.",
            "That sounds wrong.",
            "But here’s the truth.",
            "Power is only exciting near its limit.",
            "Most modern cars never reach it.",
            "Electronics intervene first.",
            "You feel safe.",
            "But not thrilled."
        ]
    },

    "supercars_are_boring": {
        "style": "myth",
        "lines": [
            "People think supercars are the most exciting cars.",
            "In reality, they can feel intimidating.",
            "They are too capable.",
            "Mistakes are corrected instantly.",
            "Limits are unreachable on public roads.",
            "Normal cars allow exploration.",
            "Exploration creates adrenaline."
        ]
    },

    "ev_fun_problem": {
        "style": "myth",
        "lines": [
            "Electric cars feel fast.",
            "But many people say they feel empty.",
            "Instant torque removes buildup.",
            "Sound disappears.",
            "Weight increases.",
            "Drama is lost.",
            "Speed remains.",
            "Emotion fades."
        ]
    }
}

# -------------------------------------------------
# PICK UNUSED TOPIC MATCHING STYLE
# -------------------------------------------------
available = [
    k for k, v in TOPICS.items()
    if v["style"] == current_style and k not in used_topics
]

if not available:
    used_topics.clear()
    available = [k for k, v in TOPICS.items() if v["style"] == current_style]

topic_key = random.choice(available)
used_topics.add(topic_key)

# -------------------------------------------------
# SAVE MEMORY
# -------------------------------------------------
json.dump(list(used_topics), open(USED_TOPICS_FILE, "w", encoding="utf-8"), indent=2)
json.dump(style_state, open(STYLE_STATE_FILE, "w", encoding="utf-8"), indent=2)

# -------------------------------------------------
# BUILD FINAL SCRIPT
# -------------------------------------------------
lines = TOPICS[topic_key]["lines"]

ending = random.choice([
    "Once you notice this, driving feels different forever.",
    "That’s why some cars stay in your memory forever.",
    "And now you understand why driving used to feel alive."
])

script = " ".join(lines) + " " + ending

with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script)

print(f"🔥 Script generated | style={current_style} | topic={topic_key}")
print(script)
