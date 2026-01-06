import requests, os, random, time

API_KEY = os.getenv("PIXABAY_API_KEY")

if not API_KEY:
    raise Exception("❌ PIXABAY_API_KEY not found in environment")

print("✅ Pixabay API key detected")

SEARCH_TERMS = [
    "supercar driving",
    "sports car racing",
    "car drifting",
    "race car track",
    "hypercar",
    "supercar acceleration"
]

REQUIRED = ["car", "race", "drift", "supercar"]
BANNED = ["mountain", "nature", "cloth", "forest", "abstract"]

os.makedirs("assets/videos", exist_ok=True)

downloaded = 0
attempts = 0
MAX_VIDEOS = 30   # enough for 30% mix
MAX_ATTEMPTS = 10

while downloaded < MAX_VIDEOS and attempts < MAX_ATTEMPTS:
    attempts += 1
    q = random.choice(SEARCH_TERMS)

    print(f"🔍 Searching Pixabay for: {q}")

    r = requests.get(
        "https://pixabay.com/api/videos/",
        params={
            "key": API_KEY,
            "q": q,
            "per_page": 50
        },
        timeout=15
    ).json()

    hits = r.get("hits", [])
    print(f"📦 Results received: {len(hits)}")

    for v in hits:
        tags = v.get("tags", "").lower()

        if not any(k in tags for k in REQUIRED):
            continue
        if any(b in tags for b in BANNED):
            continue

        url = v["videos"]["medium"]["url"]
        out = f"assets/videos/v{downloaded}.mp4"

        print(f"⬇️ Downloading video {downloaded + 1}")

        with open(out, "wb") as f:
            f.write(requests.get(url, timeout=20).content)

        downloaded += 1
        time.sleep(0.3)

        if downloaded >= MAX_VIDEOS:
            break

print(f"✅ Total Pixabay videos downloaded: {downloaded}")

if downloaded < 10:
    raise Exception("❌ Too few Pixabay videos downloaded — check filters or API limits")
