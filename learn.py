import json

brain=json.load(open("brain.json"))
hist=brain["history"]

if len(hist)<30:
    exit()

recent=hist[-30:]
avg=sum(v["views"] for v in recent)/len(recent)

def learn(bucket,key,value,good):
    bucket.setdefault(key,{})
    bucket[key].setdefault(value,1.0)
    bucket[key][value]*=1.08 if good else 0.94

for v in recent:
    good = v["views"] > avg

    learn(brain,"hooks",v.get("hook"),good)
    learn(brain,"angles",v.get("angle"),good)
    learn(brain,"engines",v.get("engine"),good)
    learn(brain,"topics",v.get("topic"),good)

json.dump(brain,open("brain.json","w"),indent=2)
