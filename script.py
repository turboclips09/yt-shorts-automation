import json, os

LIB_FILE = "script_library.json"

if not os.path.exists(LIB_FILE):
    print("Library missing")
    exit()

lib = json.load(open(LIB_FILE))

if not lib["unused"]:
    print("Script library empty")
    exit()

script = lib["unused"].pop(0)
lib["used"].append(script)

json.dump(lib, open(LIB_FILE,"w"), indent=2)

open("script.txt","w",encoding="utf-8").write(script)
print(script)
