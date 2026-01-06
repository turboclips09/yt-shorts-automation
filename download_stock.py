import os, requests, random, time

API_KEY = os.getenv("PIXABAY_API_KEY")
if not API_KEY:
    raise Exception("PIXABAY_API_KEY missing")

SEARCH = [
    "supercar driving", "car drifting",
    "race car track", "hypercar acceleration"
]

os.makedirs("assets/videos", exist_ok=True)
count = 0

while count < 30:
    q = random.choice(SEARCH)
    r = requests.get(
        "https://pixabay.com/api/videos/",
        params={"key": API_KEY, "q": q, "per_page": 50}
    ).json()

    for v in r.get("hits", []):
        url = v["videos"]["medium"]["url"]
        out = f"assets/videos/v{count}.mp4"
        with open(out, "wb") as f:
            f.write(requests.get(url).content)
        count += 1
        time.sleep(0.3)
        if count >= 30:
            break

print(f"Downloaded {count} Pixabay videos")
