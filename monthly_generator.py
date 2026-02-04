import os, json, requests

API_KEY = os.getenv("OPENROUTER_API_KEY")

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

Primary Niches:
{niches}

High Performing Hooks:
{hooks}

High Performing Angles:
{angles}

High Performing Topics:
{topics}

Rules:
- Strong hook first sentence
- Curiosity ending
- No emojis
- No hashtags
- No titles
- One paragraph only
- 20% experimental ideas

Return ONLY JSON array.
"""

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

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
    except Exception as e:
        print("Request failed:", e)
        return None

    if r.status_code != 200:
        print("Model", model, "HTTP", r.status_code)
        return None

    try:
        data = r.json()
        return data["choices"][0]["message"]["content"]
    except:
        return None


print("Generating monthly script library...")

text = None
for m in MODELS:
    print("Trying model:", m)
    text = call_model(m)
    if text:
        break

if not text:
    print("All models failed. Skipping monthly generation.")
    exit(0)

start = text.find("[")
if start == -1:
    print("JSON not found in model output")
    print(text[:300])
    exit(0)

scripts = json.loads(text[start:])

json.dump(
    {"unused": scripts, "used": []},
    open("script_library.json","w"),
    indent=2
)

print("Saved", len(scripts), "scripts")
