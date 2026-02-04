import os, json, requests

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

brain = json.load(open("brain.json"))

def top(bucket):
    return sorted(bucket.items(), key=lambda x:x[1], reverse=True)[:4]

hooks = top(brain["hooks"])
angles = top(brain["angles"])
topics = top(brain["topics"])
niches = top(brain["niches"])

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

Primary Niches To Generate:
{niches}

High Performing Hooks:
{hooks}

High Performing Angles:
{angles}

High Performing Topics:
{topics}

Instructions:
- Avoid saturated patterns
- Favor high performing ones
- 20% experimental scripts
- Strong curiosity endings
- No emojis
- No hashtags
- No titles
- One paragraph

Return ONLY JSON array.
"""

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

payload = {
    "inputs": prompt,
    "parameters": {"max_new_tokens":4000,"temperature":0.9}
}

r = requests.post(
    f"https://api-inference.huggingface.co/models/{MODEL}",
    headers=headers,
    json=payload,
    timeout=120
)

text = r.json()[0]["generated_text"]
scripts = json.loads(text[text.find("["):])

json.dump(
    {"unused":scripts,"used":[]},
    open("script_library.json","w"),
    indent=2
)

print("Saved",len(scripts),"scripts")
