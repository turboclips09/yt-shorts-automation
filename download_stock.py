import requests
import os
import random

API_KEY = os.getenv("PIXABAY_API_KEY")

SEARCH_TERMS = [
    "car pov driving",
    "sports car interior driving",
    "night car driving city",
    "car tunnel driving",
    "fast car road",
    "luxury car cockpit",
    "steering wheel driving",
    "high speed car road",
    "rain night car driving",
    "car acceleration pov"
]

os.makedirs("assets/videos", exist_ok=True)

downloaded = 0
seen_ids = set()

while downloaded < 40:
    query = random.choice(SEARCH_TERMS)

    r = requests.get(
        "https://pixabay.com/api/videos/",
        params={
            "key": API_KEY,
            "q": query,
            "per_page": 50,
            "safesearch": "true",
            "order": "latest"   # VERY IMPORTANT
        }
    ).json()

    if not r.get("hits"):
        continue

    random.shuffle(r["hits"])

    for video in r["hits"]:
        if downloaded >= 40:
            break

        vid = video["id"]
        if vid in seen_ids:
            continue

        seen_ids.add(vid)

        url = video["videos"]["medium"]["url"]
        path = f"assets/videos/v{downloaded}.mp4"

        with open(path, "wb") as f:
            f.write(requests.get(url).content)

        downloaded += 1

print(f"🔥 Downloaded {downloaded} high-energy driving videos")
