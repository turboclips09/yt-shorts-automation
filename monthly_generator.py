import os, json, requests

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

BRAIN_FILE = "brain.json"
LIB_FILE = "script_library.json"

brain = json.load(open(BRAIN_FILE))

history = brain.get("history", [])[-100:]

good = []
bad = []

if history:
    avg = sum(v["views"] for v in history) / len(history)
    for v in history:
        if v["views"] >= avg:
            good.append(v["title"])
        else:
            bad.append(v["title"])

prompt = f"""
You are an autonomous YouTube Shorts script engine.

Generate 120 SHORT-FORM scripts.

Niche: Car psychology, driving emotions, hidden facts, real incidents, strange truths.

Rules:
- 45 to 65 words each
- Strong hook in first sentence
- Curiosity-driven ending
- No emojis
- No hashtags
- No titles
- No lists
- No explanations
- One paragraph per script

High performing themes:
{good[:20]}

Underperforming themes:
{bad[:20]}

Mix:
- real car facts
- emotional observations
- real world incidents
- hidden engineering truths
- human psychology

Return ONLY a JSON array of strings.
"""

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

payload = {
    "inputs": prompt,
    "parameters": {"max_new_tokens": 4000, "temperature": 0.9}
}

print("Requesting scripts...")

r = requests.post(
    f"https://api-inference.huggingface.co/models/{MODEL}",
    headers=headers,
    json=payload,
    timeout=120
)

data = r.json()
text = data[0]["generated_text"]
scripts = json.loads(text[text.find("["):])

lib = {"unused": scripts, "used": []}
json.dump(lib, open(LIB_FILE,"w"), indent=2)

print("Saved", len(scripts), "scripts")
