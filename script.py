import json, os, random

LIB_FILE = "script_library.json"
BRAIN_FILE = "brain.json"

lib = json.load(open(LIB_FILE))
brain = json.load(open(BRAIN_FILE))

if not lib["unused"]:
    print("Library empty")
    exit()

entry = lib["unused"].pop(0)

script = entry["script"]

meta = {
    "hook": entry["hook"],
    "angle": entry["angle"],
    "engine": entry["engine"],
    "topic": entry["topic"]
}

brain["last_meta"] = meta

json.dump(lib, open(LIB_FILE,"w"), indent=2)
json.dump(brain, open(BRAIN_FILE,"w"), indent=2)

open("script.txt","w",encoding="utf-8").write(script)
print(script)
