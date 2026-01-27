import json
import os

BRAIN_FILE = "brain.json"

# ---------------------------------
# LOAD BRAIN
# ---------------------------------
if not os.path.exists(BRAIN_FILE):
    print("No brain.json found")
    exit()

brain = json.load(open(BRAIN_FILE))

history = brain.get("history", [])

# ---------------------------------
# REQUIRE MIN DATA
# ---------------------------------
if len(history) < 30:
    print("Not enough data yet")
    exit()

recent = history[-30:]

avg_views = sum(v["views"] for v in recent) / len(recent)

# ---------------------------------
# LEARN TOPICS FROM TITLES
# ---------------------------------
for v in recent:
    title = v["title"].lower()
    views = v["views"]

    for topic in brain["topics"]:
        key = topic.replace("_", " ")

        if key in title:
            brain["topics"][topic] = brain["topics"].get(topic, 1.0)

            if views > avg_views:
                brain["topics"][topic] *= 1.08   # promote
            else:
                brain["topics"][topic] *= 0.94   # demote gently

# ---------------------------------
# SAVE
# ---------------------------------
json.dump(brain, open(BRAIN_FILE, "w"), indent=2)

print("🧠 Brain updated successfully")
