import requests
import os
import random

API_KEY = os.getenv("PIXABAY_API_KEY")

# EXTREMELY STRICT — ONLY CARS
SEARCH_TERMS = [
    "supercar driving",
    "sports car racing",
    "race car track",
    "luxury car driving",
    "hypercar driving",
    "car acceleration",
    "car cockpit driving",
    "car interior driving",
    "night car racing",
    "supercar highway"
]

os.makedirs("assets/videos", exist_ok=True)

downloaded = 0
seen_ids = set()
attempts = 0

while downloaded < 40 and attempts < 200:
    attempts += 1
    query = random.choice(SEARCH_TERMS)

    r = requests.get(
        "https://pixabay.com/api/videos/",
        params={
            "key": API_KEY,
            "q": query,
            "per_page": 50,
            "safesearch": "true",
            "order": "latest"
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

        tags = video.get("tags", "").lower()
        name = video.get("user", "").lower()

        # 🚫 HARD FILTER — MUST CONTAIN "car"
        if "car" not in tags:
            continue

        seen_ids.add(vid)

        url = video["videos"]["medium"]["url"]
        path = f"assets/videos/v{downloaded}.mp4"

        with open(path, "wb") as f:
            f.write(requests.get(url).content)

        downloaded += 1

print(f"🔥 Downloaded {downloaded} CAR-ONLY cinematic videos")
