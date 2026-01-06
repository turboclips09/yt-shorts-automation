import requests
import os
import random

API_KEY = os.getenv("PIXABAY_API_KEY")

SEARCH_TERMS = [
    "sports car driving",
    "luxury car driving",
    "supercar highway",
    "car interior driving",
    "night car driving",
    "car tunnel driving",
    "engine revving car",
    "fast car road"
]

os.makedirs("assets/videos", exist_ok=True)

downloaded = 0
attempts = 0

while downloaded < 12 and attempts < 40:
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

    if "hits" not in r or len(r["hits"]) == 0:
        continue

    video = random.choice(r["hits"])
    url = video["videos"]["medium"]["url"]

    path = f"assets/videos/v{downloaded}.mp4"
    with open(path, "wb") as f:
        f.write(requests.get(url).content)

    downloaded += 1

print(f"Downloaded {downloaded} high-quality driving videos")
