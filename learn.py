import json

brain=json.load(open("brain.json"))
hist=brain["history"]

if len(hist)<30:
    exit()

recent=hist[-30:]
avg=sum(v["views"] for v in recent)/len(recent)

brain["topics"]={}

for v in recent:
    for w in v["title"].lower().split():
        brain["topics"].setdefault(w,1.0)
        if v["views"]>avg:
            brain["topics"][w]*=1.05
        else:
            brain["topics"][w]*=0.97

json.dump(brain,open("brain.json","w"),indent=2)
