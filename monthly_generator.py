import os, json, requests

API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL = "openrouter/cinematika-7b"  # free reliable model

brain = json.load(open("brain.json"))

def top(bucket):
    return sorted(bucket.items(), key=lambda x: x[1], reverse=True)[:4]

hooks = top(brain.get("hooks", {}))
angles = top(brain.get("angles", {}))
topics = top(brain.get("topics", {}))
niches = top(brain.get("niches", {"cars": 1.0}))

prompt = f"""
You are an autonomous YouTube Shorts script engine.

Generate 120 JSON objects.

Each object:

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

payload = {
    "model": MODEL,
    "messages": [
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.9
}

print("Generating monthly script library...")

r = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers=headers,
    json=payload,
    timeout=180
)

if r.status_code != 200:
    print("OpenRouter HTTP Error:", r.status_code)
    print(r.text[:300])
    exit(0)

data = r.json()

text = data["choices"][0]["message"]["content"]

start = text.find("[")
if start == -1:
    print("JSON not found in output")
    print(text[:300])
    exit(0)

scripts = json.loads(text[start:])

json.dump(
    {"unused": scripts, "used": []},
    open("script_library.json", "w"),
    indent=2
)

print("Saved", len(scripts), "scripts")
