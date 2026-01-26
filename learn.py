import json

brain=json.load(open("brain.json"))
perf=json.load(open("performance.json"))

if len(perf)<30:
    print("Not enough data yet")
    exit()

recent=perf[-30:]
avg=sum(v["views"] for v in recent)/len(recent)

for v in recent:
    title=v["title"].lower()
    for t in brain["topics"]:
        if t.replace("_"," ") in title:
            brain["topics"][t]=brain["topics"].get(t,1)
            if v["views"]>avg:
                brain["topics"][t]*=1.08
            else:
                brain["topics"][t]*=0.93

json.dump(brain,open("brain.json","w"),indent=2)
print("Brain updated")
