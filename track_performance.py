import os
import json
import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# -----------------------------------
# ENV
# -----------------------------------
CLIENT_ID = os.getenv("YT_CLIENT_ID")
CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("YT_REFRESH_TOKEN")

# -----------------------------------
# AUTH
# -----------------------------------
creds = Credentials(
    None,
    refresh_token=REFRESH_TOKEN,
    token_uri="https://oauth2.googleapis.com/token",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    scopes=[
        "https://www.googleapis.com/auth/youtube.force-ssl"
    ]
)

youtube = build("youtube", "v3", credentials=creds)

# -----------------------------------
# LOAD BRAIN
# -----------------------------------
BRAIN_FILE = "brain.json"

if os.path.exists(BRAIN_FILE):
    brain = json.load(open(BRAIN_FILE))
else:
    brain = {"topics": {}, "styles": {}, "history": []}

# -----------------------------------
# GET LAST 5 VIDEOS
# -----------------------------------
search = youtube.search().list(
    part="id",
    forMine=True,
    type="video",
    order="date",
    maxResults=5
).execute()

video_ids = [i["id"]["videoId"] for i in search["items"]]

if not video_ids:
    print("No videos found")
    exit()

stats = youtube.videos().list(
    part="snippet,statistics",
    id=",".join(video_ids)
).execute()

now = datetime.datetime.utcnow().isoformat()

for v in stats["items"]:
    brain["history"].append({
        "video_id": v["id"],
        "title": v["snippet"]["title"],
        "views": int(v["statistics"].get("viewCount", 0)),
        "time": now
    })

# Keep only last 500 records
brain["history"] = brain["history"][-500:]

json.dump(brain, open(BRAIN_FILE, "w"), indent=2)

print("✅ Performance tracked")
