import os, json, requests, re

API_KEY = os.getenv("OPENROUTER_API_KEY")

MODELS = [
    "meta-llama/llama-3.1-8b-instruct",
    "mistralai/mistral-7b-instruct",
    "openchat/openchat-3.5",
    "gryphe/mythomax-l2-13b"
]

brain = json.load(open("brain.json"))

def top(bucket):
    return sorted(bucket.items(), key=lambda x:x[1], reverse=True)[:4]

hooks = top(brain.get("hooks", {}))
angles = top(brain.get("angles", {}))
topics = top(brain.get("topics", {}))
niches = top(brain.get("niches", {"cars":1.0}))

prompt = f"""
You are an autonomous YouTube Shorts script engine.

Generate 120 JSON objects.

Each object must be:

{{
 "script": "45-65 word YouTube Shorts script",
 "hook": "curiosity_gap | contrarian | identity | nostalgia",
 "angle": "manual_vs_auto | old_vs_new | electric | supercar | daily_driving",
 "engine": "story | contrast | reveal",
 "topic": "driving_feel | car_psychology | engineering_truth | nostalgia"
}}

Return ONLY JSON array.
"""

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def extract_json(text):
    match = re.search(r"\[[\s\S]*\]", text)
    if not match:
        return None
    block = match.group(0)

    # Remove trailing commas before ]
    block = re.sub(r",\s*\]", "]", block)

    # Remove trailing commas before }
    block = re.sub(r",\s*\}", "}", block)

    try:
        return json.loads(block)
    except:
        return None

def call_model(model):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.9
    }

    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=180
        )
    except:
        return None

    if r.status_code != 200:
        return None

    try:
        data = r.json()
        return data["choices"][0]["message"]["content"]
    except:
        return None

print("Generating monthly script library...")

scripts = None

for m in MODELS:
    print("Trying model:", m)
    text = call_model(m)
    if not text:
        continue
    scripts = extract_json(text)
    if scripts:
        break

if not scripts:
    print("Failed to obtain valid JSON scripts")
    exit(0)

json.dump(
    {"unused": scripts, "used": []},
    open("script_library.json","w"),
    indent=2
)

print("Saved", len(scripts), "scripts")
