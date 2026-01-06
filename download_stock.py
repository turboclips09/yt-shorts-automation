import requests
import os
import random

API_KEY = os.getenv("PIXABAY_API_KEY")

SEARCH_TERMS = [
    "car driving",
    "sports car road",
    "car interior driving",
    "highway driving car",
    "engine revving car"
]

os.makedirs("clips", exist_ok=True)

for i in range(3):  # download 3 clips
    query = random.choice(SEARCH_TERMS)
    url = "https://pixabay.com/api/videos/"
    params = {
        "key": API_KEY,
        "q": query,
        "per_page": 10
    }

    r = requests.get(url, params=params).json()
    video = random.choice(r["hits"])
    video_url = video["videos"]["medium"]["url"]

    clip_data = requests.get(video_url).content
    with open(f"clips/clip_{i}.mp4", "wb") as f:
        f.write(clip_data)

print("Downloaded stock clips")
