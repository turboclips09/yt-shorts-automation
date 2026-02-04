import os, json, requests

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

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
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "inputs": prompt,
    "parameters": {
        "max_new_tokens": 3500,
        "temperature": 0.9
    }
}

print("Generating monthly script library...")

try:
    r = requests.post(
        f"https://router.huggingface.co/hf-inference/models/{MODEL}",
        headers=headers,
        json=payload,
        timeout=180
    )
except Exception as e:
    print("Request failed:", e)
    exit(0)

if r.status_code != 200:
    print("HF HTTP Error:", r.status_code)
    print(r.text[:500])
    exit(0)

raw = r.text.strip()

if not raw:
    print("Empty response from HF")
    exit(0)

try:
    data = json.loads(raw)
except Exception:
    print("Non JSON response:")
    print(raw[:500])
    exit(0)

# ----------------------------

if isinstance(data, dict) and "error" in data:
    print("HF Error:", data["error"])
    exit(0)

if not isinstance(data, list):
    print("Unexpected response format:", data)
    exit(0)

if "generated_text" not in data[0]:
    print("Missing generated_text:", data)
    exit(0)

text = data[0]["generated_text"]

start = text.find("[")
if start == -1:
    print("JSON not found in model output")
    exit(0)

scripts = json.loads(text[start:])

json.dump(
    {"unused": scripts, "used": []},
    open("script_library.json", "w"),
    indent=2
)

print("Saved", len(scripts), "scripts")
