import requests
import os
import random
import time

API_KEY = os.getenv("PIXABAY_API_KEY")

# EXTREMELY STRICT CAR-ONLY SEARCH TERMS
SEARCH_TERMS = [
    "supercar driving",
    "sports car racing",
    "race car track",
    "drift car racing",
    "car drifting smoke",
    "racing car POV",
    "car cockpit POV",
    "supercar acceleration",
    "hypercar driving",
    "night car racing",
    "luxury sports car driving",
    "track racing cars",
    "supercar highway",
    "race car onboard",
    "drift racing cars"
]

# REQUIRED WORDS — MUST APPEAR IN TAGS
REQUIRED_KEYWORDS = [
    "car",
    "cars",
    "supercar",
    "race",
    "racing",
    "drift",
    "drifting",
    "automobile",
    "vehicle"
]

# BANNED WORDS — IF PRESENT, REJECT
BANNED_KEYWORDS = [
    "mountain",
    "nature",
    "forest",
    "landscape",
    "scenery",
    "road",
    "highway",
    "city",
    "traffic",
    "sky",
    "cloud",
    "cloth",
    "fabric",
    "abstract",
    "background",
    "timelapse"
]

TARGET_COUNT = 50
os.makedirs("assets/videos", exist_ok=True)

downloaded = 0
seen_ids = set()
attempts = 0

while downloaded < TARGET_COUNT and attempts < 400:
    attempts += 1
    query = random.choice(SEARCH_TERMS)

    try:
        response = requests.get(
            "https://pixabay.com/api/videos/",
            params={
                "key": API_KEY,
                "q": query,
                "per_page": 50,
                "safesearch": "true",
                "order": "latest"
            },
            timeout=12
        )
    except:
        continue

    if response.status_code != 200:
        continue

    hits = response.json().get("hits", [])
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

        # MUST contain car-related keywords
        if not any(word in tags for word in REQUIRED_KEYWORDS):
            continue

        # MUST NOT contain banned keywords
        if any(word in tags for word in BANNED_KEYWORDS):
            continue

        videos = video.get("videos", {})
        chosen = (
            videos.get("large") or
            videos.get("medium") or
            videos.get("small")
        )

        if not chosen or not chosen.get("url"):
            continue

        path = f"assets/videos/v{downloaded}.mp4"

        try:
            with requests.get(chosen["url"], stream=True, timeout=20) as r:
                with open(path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
        except:
            continue

        seen_ids.add(vid)
        downloaded += 1
        print(f"Downloaded {downloaded}/{TARGET_COUNT}")

        time.sleep(0.15)  # avoid API throttling

print(f"🔥 DONE: {downloaded} refined, car-only cinematic videos downloaded")
