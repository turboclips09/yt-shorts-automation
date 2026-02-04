import os, json, requests

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

brain = json.load(open("brain.json"))
history = brain.get("history", [])[-100:]

prompt = f"""
You are an autonomous YouTube Shorts script engine.

Generate 120 objects in JSON array.

Each object format:

{{
 "script": "...45-65 word script...",
 "hook": "curiosity_gap | contrarian | identity | nostalgia",
 "angle": "manual_vs_auto | old_vs_new | electric | supercar | daily_driving",
 "engine": "story | contrast | reveal",
 "topic": "driving_feel | car_psychology | engineering_truth | nostalgia"
}}

Rules:
- Strong hook first sentence
- Curiosity ending
- No emojis, no hashtags
- One paragraph only

Return ONLY JSON.
"""

headers={"Authorization":f"Bearer {HF_TOKEN}"}
payload={"inputs":prompt,"parameters":{"max_new_tokens":4000}}

r=requests.post(
    f"https://api-inference.huggingface.co/models/{MODEL}",
    headers=headers,
    json=payload,
    timeout=120
)

text=r.json()[0]["generated_text"]
scripts=json.loads(text[text.find("["):])

lib={"unused":scripts,"used":[]}
json.dump(lib,open("script_library.json","w"),indent=2)

print("Saved",len(scripts),"scripts")
