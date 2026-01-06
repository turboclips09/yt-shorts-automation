import requests
import os
import random

API_KEY = os.getenv("PIXABAY_API_KEY")

VIDEO_TERMS = [
    "sports car driving",
    "luxury car",
    "car highway",
    "car interior driving",
    "engine revving"
]

IMAGE_TERMS = [
    "supercar",
    "luxury car exterior",
    "sports car front",
    "car dashboard",
    "car steering wheel"
]

os.makedirs("assets/videos", exist_ok=True)
os.makedirs("assets/images", exist_ok=True)

# Download videos
for i in range(6):
    query = random.choice(VIDEO_TERMS)
    r = requests.get(
        "https://pixabay.com/api/videos/",
        params={"key": API_KEY, "q": query, "per_page": 20}
    ).json()

    video = random.choice(r["hits"])
    url = video["videos"]["medium"]["url"]

    with open(f"assets/videos/v{i}.mp4", "wb") as f:
        f.write(requests.get(url).content)

# Download images
for i in range(6):
    query = random.choice(IMAGE_TERMS)
    r = requests.get(
        "https://pixabay.com/api/",
        params={"key": API_KEY, "q": query, "per_page": 20}
    ).json()

    img = random.choice(r["hits"])
    url = img["largeImageURL"]

    with open(f"assets/images/i{i}.jpg", "wb") as f:
        f.write(requests.get(url).content)

print("Downloaded stock videos and images")
