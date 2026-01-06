import requests
import os
import random
import time

API_KEY = os.getenv("PIXABAY_API_KEY")

# VERY PRECISE, CAR-ONLY SEARCH TERMS
SEARCH_TERMS = [
    "supercar driving",
    "sports car racing",
    "race car track",
    "supercar highway",
    "car drifting",
    "drift car smoke",
    "racing car POV",
    "car cockpit POV",
    "luxury sports car",
    "hypercar driving",
    "night car racing",
    "supercar acceleration",
    "fast car road",
    "track racing cars",
    "drift racing cars"
]

# HARD FILTER WORDS (must appear in tags)
REQUIRED_KEYWORDS = [
    "car",
    "cars",
    "supercar",
    "racing",
    "race",
    "drift",
    "drifting",
    "automobile"
]

os.makedirs("assets/videos", exist_ok=True)

TARGET_COUNT = 50
downloaded = 0
seen_ids = set()
attempts = 0

while downloaded < TARGET_COUNT and attempts < 300:
    attempts += 1
    query = random.choice(SEARCH_TERMS)

    response = requests.get(
        "https://pixabay.com/api/videos/",
        params={
            "key": API_KEY,
            "q": query,
            "per_page": 50,
            "safesearch": "true",
            "order": "latest"
        },
        timeout=10
    )

    if response.status_code != 200:
        continue

    data = response.json()
    hits = data.get("hits", [])
    if not hits:
        continue

    random.shuffle(hits)

    for video in hits:
        if downloaded >= TARGET_COUNT:
            break

        vid = video.get("id")
        if vid in seen_ids:
            continue

        tags = video.get("tags", "").lower()

        # 🚫 HARD REJECT IF NOT CAR-RELATED
        if not any(word in tags for word in REQUIRED_KEYWORDS):
            continue

        # Prefer higher resolution if available
        video_files = video.get("videos", {})
        chosen = (
            video_files.get("large") or
            video_files.get("medium") or
            video_files.get("small")
        )

        if not chosen:
            continue

        url = chosen.get("url")
        if not url:
            continue

        path = f"assets/videos/v{downloaded}.mp4"

        try:
            with requests.get(url, stream=True, timeout=15) as r:
                with open(path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
        except:
            continue

        seen_ids.add(vid)
        downloaded += 1
        print(f"Downloaded {downloaded}/{TARGET_COUNT}")

        # Small delay to avoid API throttling
        time.sleep(0.2)

print(f"🔥 DONE: {downloaded} high-quality car videos downloaded")
