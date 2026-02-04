import os, json, requests, re

API_KEY = os.getenv("OPENROUTER_API_KEY")
LIB_FILE = "script_library.json"

MIN_SCRIPTS = 20
TARGET_SCRIPTS = 120

# -----------------------------
# Skip refill if library healthy
# -----------------------------
if os.path.exists(LIB_FILE):
    lib = json.load(open(LIB_FILE))
    if len(lib.get("unused", [])) >= MIN_SCRIPTS:
        print("Library has enough scripts. Skipping monthly refill.")
        exit(0)
else:
    lib = {"unused": [], "used": []}

# -----------------------------
# Free Models (fallback order)
# -----------------------------
MODELS = [
    "meta-llama/llama-3.1-8b-instruct",
    "mistralai/mistral-7b-instruct",
    "openchat/openchat-3.5",
    "gryphe/mythomax-l2-13b"
]

brain = json.load(open("brain.json"))

def top(bucket):
    return sorted(bucket.items(), key=lambda x: x[1], reverse=True)[:4]

hooks = top(brain.get("hooks", {}))
angles = top(brain.get("angles", {}))
topics = top(brain.get("topics", {}))
niches = top(brain.get("niches", {"cars":1.0}))

# -----------------------------
# PROMPT
# -----------------------------
PROMPT = f"""
Generate YouTube Shorts SCRIPTS using these proportions:

- 30% psychology_story
- 25% fact_episode
- 20% incident_story
- 15% brand_story
- 10% engineering_story

Each script must:

- 110 to 150 words
- 6 to 9 sentences
- Include a small real-life story OR scenario
- Include at least one real car fact or engineering truth
- Include psychology or emotional insight
- Strong hook in first sentence
- Clear buildup and climax
- Curiosity-driven ending
- No emojis
- No hashtags
- One paragraph only

Return JSON array of objects:

{{
 "script": "...",
 "format": "fact_episode | incident_story | brand_story | psychology_story | engineering_story",
 "hook": "curiosity_gap | contrarian | identity | nostalgia",
 "angle": "manual_vs_auto | old_vs_new | electric | supercar | daily_driving",
 "engine": "story | contrast | reveal",
 "topic": "driving_feel | car_psychology | engineering_truth | nostalgia"
}}

High Performing Hooks:
{hooks}

High Performing Angles:
{angles}

High Performing Topics:
{topics}

When appropriate, include:
- Real people
- Real brands
- Real companies
- Real incidents
- Real models

Return ONLY JSON.
"""

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# -----------------------------
# Helpers
# -----------------------------
def extract_json(text):
    match = re.search(r"\[[\s\S]*\]", text)
    if not match:
        return None
    block = match.group(0)
    block = re.sub(r",\s*\]", "]", block)
    block = re.sub(r",\s*\}", "}", block)
    try:
        return json.loads(block)
    except:
        return None

def valid_script(s):
    words = len(s.split())
    sentences = len(re.findall(r"[.!?]", s))

    if words < 110 or words > 160:
        return False

    if sentences < 5:
        return False

    if "you won't believe" in s.lower() and words < 120:
        return False

    return True

def call_model(model):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": PROMPT}],
        "temperature": 0.9
    }

    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=HEADERS,
            json=payload,
            timeout=180
        )
    except:
        return None

    if r.status_code != 200:
        return None

    try:
        return r.json()["choices"][0]["message"]["content"]
    except:
        return None

# -----------------------------
# Generate Scripts
# -----------------------------

print("Refilling script library...")

collected = []

ROUNDS_PER_MODEL = 4   # how many times we ask each model

for model in MODELS:
    print("Using model:", model)

    for r in range(ROUNDS_PER_MODEL):
        print(" Round", r+1)

        text = call_model(model)
        if not text:
            continue

        items = extract_json(text)
        if not items:
            continue

        for obj in items:
            if "script" in obj and valid_script(obj["script"]):
                collected.append(obj)

            if len(collected) >= TARGET_SCRIPTS:
                break

        if len(collected) >= TARGET_SCRIPTS:
            break

    if len(collected) >= TARGET_SCRIPTS:
        break


if not collected:
    print("Failed to collect valid scripts.")
    exit(0)

lib["unused"].extend(collected)

json.dump(lib, open(LIB_FILE,"w"), indent=2)

print("Added", len(collected), "high-quality scripts")
