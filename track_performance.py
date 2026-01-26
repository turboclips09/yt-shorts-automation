import os
import json
import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# -----------------------------
# ENV
# -----------------------------
CLIENT_ID = os.getenv("YT_CLIENT_ID")
CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("YT_REFRESH_TOKEN")

# -----------------------------
# AUTH
# -----------------------------
creds = Credentials(
    None,
    refresh_token=REFRESH_TOKEN,
    token_uri="https://oauth2.googleapis.com/token",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    scopes=["https://www.googleapis.com/auth/youtube.readonly"]
)

youtube = build("youtube", "v3", credentials=creds)

# -----------------------------
# LOAD HISTORY
# -----------------------------
FILE = "performance.json"

if os.path.exists(FILE):
    history = json.load(open(FILE))
else:
    history = []

# -----------------------------
# GET LAST 5 VIDEOS
# -----------------------------
resp = youtube.search().list(
    part="id",
    forMine=True,
    type="video",
    maxResults=5,
    order="date"
).execute()

video_ids = [i["id"]["videoId"] for i in resp["items"]]

stats = youtube.videos().list(
    part="statistics,snippet",
    id=",".join(video_ids)
).execute()

now = datetime.datetime.utcnow().isoformat()

for v in stats["items"]:
    history.append({
        "video_id": v["id"],
        "title": v["snippet"]["title"],
        "views": int(v["statistics"].get("viewCount",0)),
        "likes": int(v["statistics"].get("likeCount",0)),
        "time": now
    })

json.dump(history[-500:], open(FILE,"w"), indent=2)

print("✅ Performance updated")
