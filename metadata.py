import random
import json
import hashlib
import os

MEMORY_FILE = "used_metadata.json"

if os.path.exists(MEMORY_FILE):
    memory = json.load(open(MEMORY_FILE))
else:
    memory = {"titles": [], "descriptions": []}

# ---------------- TITLES ----------------
title_templates = [
    "Why Modern Cars Feel Fast But Boring",
    "The Hidden Reason Driving Feels Less Fun",
    "Why Old Cars Felt More Alive Than New Ones",
    "This Is Why Cars Lost Their Soul",
    "Why Speed Doesn’t Feel Exciting Anymore",
    "The Uncomfortable Truth About Modern Cars",
    "Why Slower Cars Used To Feel Faster",
    "What Car Companies Don’t Tell Drivers"
]

while True:
    title = random.choice(title_templates)
    h = hashlib.md5(title.encode()).hexdigest()
    if h not in memory["titles"]:
        memory["titles"].append(h)
        break

# ---------------- DESCRIPTION ----------------
desc_blocks = [
    "Modern cars are faster than ever, yet driving feels less exciting.",
    "This video explains what really changed in how cars are designed.",
    "It’s not nostalgia — it’s psychology, physics, and engineering.",
    "Once you notice this, driving won’t feel the same again."
]

description = "\n\n".join(random.sample(desc_blocks, 3))
memory["descriptions"].append(hashlib.md5(description.encode()).hexdigest())

# ---------------- TAGS ----------------
tags = [
    "cars", "car facts", "automotive", "driving",
    "why cars feel boring", "old cars vs new cars",
    "car enthusiasts", "car psychology", "driving fun"
]

random.shuffle(tags)
tags = tags[:12]

# Save memory
json.dump(memory, open(MEMORY_FILE, "w"), indent=2)

# Write output
json.dump({
    "title": title,
    "description": description,
    "tags": tags
}, open("metadata.json", "w"), indent=2)

print("✅ metadata.json generated")
