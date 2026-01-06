import requests
import os
import random

API_KEY = os.getenv("PIXABAY_API_KEY")

SEARCH_TERMS = [
    "car pov driving",
    "sports car interior driving",
    "night car driving city",
    "car tunnel driving",
    "luxury car cockpit",
    "steering wheel driving",
    "rain night car driving",
    "fast car road cinematic"
]

os.makedirs("assets/videos", exist_ok=True)

downloaded = 0
attempts = 0

while downloaded < 15 and attempts < 50:
    attempts += 1
    query = random.choice(SEARCH_TERMS)

    r = requests.get(
        "https://pixabay.com/api/videos/",
        params={
            "key": API_KEY,
            "q": query,
            "per_page": 50,
            "safesearch": "true"
        }
    ).json()

    if not r.get("hits"):
        continue

    video = random.choice(r["hits"])
    url = video["videos"]["medium"]["url"]

    with open(f"assets/videos/v{downloaded}.mp4", "wb") as f:
        f.write(requests.get(url).content)

    downloaded += 1

print(f"✅ Downloaded {downloaded} cinematic driving videos")
