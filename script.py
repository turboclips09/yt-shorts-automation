import random
import json
import os
import hashlib

# =====================================================
# FILES
# =====================================================

BRAIN_FILE = "brain.json"
USED_FILE = "used_scripts.json"

if os.path.exists(BRAIN_FILE):
    brain = json.load(open(BRAIN_FILE))
else:
    brain = {"topics": {}, "styles": {}, "history": []}

if os.path.exists(USED_FILE):
    used = set(json.load(open(USED_FILE)))
else:
    used = set()

# =====================================================
# CORE IDEA BANK (LARGE & EXPANDABLE)
# =====================================================

HOOKS = [
    "Nobody talks about this part of cars.",
    "This is why your first car felt different.",
    "Modern cars are fast… but something is missing.",
    "Here’s the uncomfortable truth about driving.",
    "This changes how you see cars forever.",
    "Most people misunderstand what makes cars fun.",
    "Car companies don’t want you to notice this."
]

OBSERVATIONS = [
    "Old cars demanded attention.",
    "Modern cars remove effort.",
    "Drivers used to work with machines.",
    "Now machines work around drivers.",
    "Cars used to feel alive.",
    "Cars now feel perfect.",
    "Perfect feels empty."
]

PSYCHOLOGY = [
    "Humans bond with things that fight back.",
    "Emotion comes from effort.",
    "Involvement creates attachment.",
    "Control creates confidence.",
    "Silence removes drama.",
    "Friction creates memory.",
    "Struggle creates meaning."
]

FACTS = [
    "Older cars had mechanical steering.",
    "Manual transmissions require constant decisions.",
    "Modern cars filter feedback digitally.",
    "Cars today weigh hundreds of kilos more.",
    "Electronics stop mistakes instantly.",
    "EVs remove engine sound completely.",
    "Stability systems intervene before drivers feel danger."
]

MICRO_STORIES = [
    "I once drove an old beater that felt alive.",
    "Someone handed me the keys to an old manual.",
    "I expected a supercar to blow my mind.",
    "I drove a modern car right after an old one.",
    "I didn’t understand this until I felt it."
]

REVEALS = [
    "Fun was never about speed.",
    "The thrill wasn’t lost. It was engineered out.",
    "Cars didn’t get boring. They got safe.",
    "Comfort replaced connection.",
    "We didn’t change. The machines did."
]

LOOPS = [
    "Once you notice this, driving feels different.",
    "You can’t unsee this now.",
    "Think about this next time you drive.",
    "Watch this again and it hits harder.",
    "Most people never realize this."
]

CTA_SOFT = [
    "Follow for daily car psychology.",
    "Follow if cars live in your head.",
    "More hidden car truths coming."
]

# =====================================================
# STORY ENGINES (STRUCTURES)
# =====================================================

def engine_story_arc():
    return [
        random.choice(HOOKS),
        random.choice(MICRO_STORIES),
        random.choice(OBSERVATIONS),
        random.choice(FACTS),
        random.choice(PSYCHOLOGY),
        random.choice(REVEALS),
        random.choice(LOOPS)
    ]

def engine_contrast():
    return [
        random.choice(HOOKS),
        "Old cars demanded involvement.",
        "Modern cars remove involvement.",
        random.choice(FACTS),
        random.choice(PSYCHOLOGY),
        random.choice(REVEALS),
        random.choice(LOOPS)
    ]

def engine_confession():
    return [
        "I didn’t believe this at first.",
        random.choice(MICRO_STORIES),
        random.choice(FACTS),
        random.choice(PSYCHOLOGY),
        random.choice(REVEALS),
        random.choice(LOOPS)
    ]

def engine_fact_chain():
    return [
        random.choice(HOOKS),
        random.choice(FACTS),
        random.choice(FACTS),
        random.choice(PSYCHOLOGY),
        random.choice(REVEALS),
        random.choice(LOOPS)
    ]

def engine_philosophical():
    return [
        random.choice(HOOKS),
        random.choice(OBSERVATIONS),
        random.choice(PSYCHOLOGY),
        random.choice(FACTS),
        random.choice(REVEALS),
        random.choice(LOOPS)
    ]

ENGINES = [
    engine_story_arc,
    engine_contrast,
    engine_confession,
    engine_fact_chain,
    engine_philosophical
]

# =====================================================
# UTILS
# =====================================================

def clean(text):
    return text.replace("  ", " ").strip()

def script_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

# =====================================================
# BUILD SCRIPT WITH RETRIES
# =====================================================

def build_script():
    engine = random.choice(ENGINES)
    lines = engine()

    if random.random() < 0.35:
        lines.insert(0, random.choice(CTA_SOFT))

    script = " ".join(lines)
    return clean(script)

attempts = 0
final_script = build_script()
h = script_hash(final_script)

while h in used and attempts < 25:
    final_script = build_script()
    h = script_hash(final_script)
    attempts += 1

used.add(h)

json.dump(list(used), open(USED_FILE, "w"), indent=2)

# =====================================================
# SAVE
# =====================================================

with open("script.txt", "w", encoding="utf-8") as f:
    f.write(final_script)

print("✅ Procedural AI Script Generated")
print(final_script)
