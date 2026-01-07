import os
import json
import random
import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# -------------------------------------------------
# LOAD SECRETS
# -------------------------------------------------
CLIENT_ID = os.getenv("YT_CLIENT_ID")
CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("YT_REFRESH_TOKEN")

# -------------------------------------------------
# AUTH
# -------------------------------------------------
creds = Credentials(
    None,
    refresh_token=REFRESH_TOKEN,
    token_uri="https://oauth2.googleapis.com/token",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

youtube = build("youtube", "v3", credentials=creds)

# -------------------------------------------------
# LOAD METADATA
# -------------------------------------------------
with open("metadata.json", "r", encoding="utf-8") as f:
    meta = json.load(f)

# -------------------------------------------------
# RANDOM PUBLISH TIME (1–18 HOURS FROM NOW)
# -------------------------------------------------
publish_at = (
    datetime.datetime.utcnow()
    + datetime.timedelta(hours=random.randint(1, 18))
).isoformat() + "Z"

# -------------------------------------------------
# UPLOAD VIDEO
# -------------------------------------------------
request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": meta["title"],
            "description": meta["description"],
            "tags": meta["tags"],
            "categoryId": "24"  # Entertainment
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": publish_at,
            "selfDeclaredMadeForKids": False
        }
    },
    media_body=MediaFileUpload("final.mp4", resumable=True)
)

response = request.execute()
video_id = response["id"]

print("✅ Uploaded & scheduled:", video_id)

# -------------------------------------------------
# AUTO-PINNED COMMENT (ENGAGEMENT BOOST)
# -------------------------------------------------
comment_templates = [
    "Do you agree, or am I wrong? 👇",
    "Most people miss this. What do you think?",
    "Once you notice this, you can’t unsee it. Thoughts?",
    "Is this true, or just nostalgia? 👇",
    "Car people know this. Others don’t. Agree?"
]

comment_text = random.choice(comment_templates)

comment_response = youtube.commentThreads().insert(
    part="snippet",
    body={
        "snippet": {
            "videoId": video_id,
            "topLevelComment": {
                "snippet": {
                    "textOriginal": comment_text
                }
            }
        }
    }
).execute()

comment_id = comment_response["id"]

# Pin the comment
youtube.commentThreads().update(
    part="snippet",
    body={
        "id": comment_id,
        "snippet": {
            "videoId": video_id,
            "topLevelComment": comment_response["snippet"]["topLevelComment"],
            "isPublic": True,
            "isPinned": True
        }
    }
).execute()

print("📌 Comment posted and pinned")
