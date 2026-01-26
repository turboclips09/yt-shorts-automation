import os
import json
import datetime

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# -------------------------------------------------
# ENV VARIABLES
# -------------------------------------------------
CLIENT_ID = os.getenv("YT_CLIENT_ID")
CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("YT_REFRESH_TOKEN")

# -------------------------------------------------
# AUTH (READ-ONLY)
# -------------------------------------------------
creds = Credentials(
    None,
    refresh_token=REFRESH_TOKEN,
    token_uri="https://oauth2.googleapis.com/token",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    scopes=["https://www.googleapis.com/auth/youtube.readonly"]
)

youtube = build("youtube", "v3", credentials=creds)

# -------------------------------------------------
# LOAD EXISTING HISTORY
# -------------------------------------------------
HISTORY_FILE = "performance.json"

if os.path.exists(HISTORY_FILE):
    history = json.load(open(HISTORY_FILE, "r", encoding="utf-8"))
else:
    history = []

# -------------------------------------------------
# GET LAST 20 VIDEOS FROM YOUR CHANNEL
# -------------------------------------------------
search = youtube.search().list(
    part="id",
    forMine=True,
    type="video",
    order="date",
    maxResults=20
).execute()

video_ids = [item["id"]["videoId"] for item in search["items"]]

if not video_ids:
    print("No videos found.")
    exit()

# -------------------------------------------------
# GET VIDEO STATS
# -------------------------------------------------
stats = youtube.videos().list(
    part="snippet,statistics",
    id=",".join(video_ids)
).execute()

today = datetime.date.today().isoformat()

for v in stats["items"]:
    history.append({
        "date": today,
        "id": v["id"],
        "title": v["snippet"]["title"],
        "views": int(v["statistics"].get("viewCount", 0)),
        "likes": int(v["statistics"].get("likeCount", 0)),
        "comments": int(v["statistics"].get("commentCount", 0))
    })

# Keep file from growing forever
history = history[-2000:]

with open(HISTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2)

print("📊 Performance updated successfully")
