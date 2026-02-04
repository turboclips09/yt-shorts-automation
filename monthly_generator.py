import os, json, requests

HF_TOKEN = os.getenv("HF_TOKEN")

MODELS = [
    "mistralai/Mistral-7B-Instruct-v0.3",
    "HuggingFaceH4/zephyr-7b-beta",
    "openchat/openchat-3.5-0106"
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

def try_model(model):
    print("Trying model:", model)
    try:
        r = requests.post(
            f"https://router.huggingface.co/hf-inference/models/{model}",
            headers=headers,
            json=payload,
            timeout=180
        )
    except Exception as e:
        print("Request error:", e)
        return None

    if r.status_code != 200:
        print("HTTP", r.status_code)
        return None

    if not r.text.strip():
        print("Empty response")
        return None

    try:
        data = json.loads(r.text)
    except:
        print("Non JSON response")
        return None

    if isinstance(data, dict) and "error" in data:
        print("HF Error:", data["error"])
        return None

    if not isinstance(data, list):
        print("Unexpected format")
        return None

    if "generated_text" not in data[0]:
        print("Missing generated_text")
        return None

    return data[0]["generated_text"]

text = None

for m in MODELS:
    text = try_model(m)
    if text:
        break

if not text:
    print("All models failed. Skipping monthly generation.")
    exit(0)

start = text.find("[")
if start == -1:
    print("JSON not found in output")
    exit(0)

scripts = json.loads(text[start:])

json.dump(
    {"unused": scripts, "used": []},
    open("script_library.json","w"),
    indent=2
)

print("Saved", len(scripts), "scripts")
