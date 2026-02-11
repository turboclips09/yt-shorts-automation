import json
import os

LIB_FILE = "script_library.json"

if not os.path.exists(LIB_FILE):
    raise RuntimeError("❌ script_library.json not found")

lib = json.load(open(LIB_FILE))

unused = lib.get("unused", [])
used = lib.get("used", [])

if not unused:
    raise RuntimeError("❌ No unused scripts available")

# Take first script
entry = unused.pop(0)

script_text = entry["script"]

# Move to used
used.append(entry)

# Save updated library
lib["unused"] = unused
lib["used"] = used

json.dump(lib, open(LIB_FILE, "w"), indent=2)

# Write script.txt for pipeline
with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script_text)

print("✅ Script selected and saved to script.txt")
print("Remaining unused scripts:", len(unused))
