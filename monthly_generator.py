import os, json, requests, random

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

brain = json.load(open("brain.json"))
history = brain.get("history", [])[-120:]

def top_weights(bucket):
    if bucket not in brain:
        return []
    return sorted(
        brain[bucket].items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]

top_hooks = top_weights("hooks")
top_angles = top_weights("angles")
top_engines = top_weights("engines")
top_topics = top_weights("topics")

prompt = f"""
You are an autonomous YouTube Shorts script engine.

Generate 120 JSON objects.

Each object format:

{{
 "script": "45-65 word YouTube Shorts script",
 "hook": "curiosity_gap | contrarian | identity | nostalgia",
 "angle": "manual_vs_auto | old_vs_new | electric | supercar | daily_driving",
 "engine": "story | contrast | reveal",
 "topic": "driving_feel | car_psychology | engineering_truth | nostalgia"
}}

Rules:
- Strong hook in first sentence
- Curiosity-driven ending
- No emojis
- No hashtags
- No titles
- One paragraph only

Learning Insights:

High Performing Hooks:
{top_hooks}

High Performing Angles:
{top_angles}

High Performing Engines:
{top_engines}

High Performing Topics:
{top_topics}

Instructions:
- Bias generation toward high-performing patterns
- Still generate 20% experimental combinations
- Avoid repeating identical ideas
- Create emotionally engaging and curiosity-heavy scripts

Return ONLY JSON array.
"""

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

payload = {
    "inputs": prompt,
    "parameters": {
        "max_new_tokens": 4000,
        "temperature": 0.9
    }
}

print("Generating monthly script library...")

r = requests.post(
    f"https://api-inference.huggingface.co/models/{MODEL}",
    headers=headers,
    json=payload,
    timeout=120
)

data = r.json()
text = data[0]["generated_text"]
scripts = json.loads(text[text.find("["):])

library = {
    "unused": scripts,
    "used": []
}

json.dump(library, open("script_library.json","w"), indent=2)

print("Saved", len(scripts), "scripts")
