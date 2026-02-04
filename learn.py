import json

brain = json.load(open("brain.json"))
hist = brain["history"]

if len(hist) < 40:
    exit()

recent = hist[-40:]
avg = sum(v["views"] for v in recent) / len(recent)

def update(bucket, sat_bucket, key, good):
    bucket.setdefault(key,1.0)
    sat_bucket.setdefault(key,0)

    if good:
        bucket[key] *= 1.07
        sat_bucket[key] = max(0, sat_bucket[key]-1)
    else:
        bucket[key] *= 0.93
        sat_bucket[key] += 1

for v in recent:
    good = v["views"] > avg

    update(brain["hooks"], brain["saturation"]["hooks"], v.get("hook"), good)
    update(brain["angles"], brain["saturation"]["angles"], v.get("angle"), good)
    update(brain["topics"], brain["saturation"]["topics"], v.get("topic"), good)

# Auto retire saturated patterns
for group in ["hooks","angles","topics"]:
    for k in list(brain[group].keys()):
        if brain["saturation"][group].get(k,0) >= 6:
            brain[group][k] *= 0.6

# Detect niche plateau
last20 = recent[-20:]
avg20 = sum(v["views"] for v in last20) / 20

prev20 = recent[:20]
avg_prev = sum(v["views"] for v in prev20) / 20

if avg20 <= avg_prev * 0.92:
    brain["niches"].setdefault("car_history",1.0)
    brain["niches"].setdefault("car_facts",1.0)
    brain["niches"].setdefault("car_technology",1.0)

json.dump(brain,open("brain.json","w"),indent=2)
