import os, json, requests, re

API_KEY = os.getenv("OPENROUTER_API_KEY")
LIB_FILE = "script_library.json"

MIN_SCRIPTS = 80
TARGET_SCRIPTS = 120

# -----------------------------
# Skip if enough scripts
# -----------------------------
if os.path.exists(LIB_FILE):
    lib = json.load(open(LIB_FILE))
    if len(lib.get("unused", [])) >= MIN_SCRIPTS:
        print("Library healthy. Skipping refill.")
        exit(0)
else:
    lib = {"unused": [], "used": []}

MODELS = [
    "meta-llama/llama-3.1-8b-instruct",
    "mistralai/mistral-7b-instruct",
    "openchat/openchat-3.5",
    "gryphe/mythomax-l2-13b"
]

PROMPT = """
Generate YouTube Shorts scripts (40–50 seconds).

Each script must:
- 100–150 words
- 5–8 sentences
- Clear structure:
    Hook
    Story setup
    Real fact
    Conflict
    Climax
    Insight ending
- Include real brands, companies, models, executives or real incidents when relevant
- Avoid focusing only on fatal crashes
- One paragraph only
- No emojis
- No hashtags

Content distribution:
- 25% brand rivalries
- 25% corporate controversies
- 25% engineering or history stories
- 15% psychology of driving
- 10% real-life incidents

Return ONLY a JSON array of objects:

{
 "script": "...",
 "format": "brand_story | controversy_story | engineering_story | psychology_story | incident_story"
}
"""

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

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
    return 100 <= words <= 150 and sentences >= 5

def call_model(model):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": PROMPT}],
        "temperature": 0.85
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

print("Refilling script library...")

collected = []
ROUNDS = 4

for model in MODELS:
    print("Using model:", model)
    for _ in range(ROUNDS):
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
    print("No valid scripts collected.")
    exit(0)

lib["unused"].extend(collected)

json.dump(lib, open(LIB_FILE,"w"), indent=2)

print("Added", len(collected), "high-quality scripts")
