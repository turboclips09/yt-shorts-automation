import os
import json
import random
import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# -------------------------------------------------
# ENV
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
    client_secret=CLIENT_SECRET,
    scopes=[
        "https://www.googleapis.com/auth/youtube.upload",
        "https://www.googleapis.com/auth/youtube.force-ssl"
    ]
)

print("Scopes:", creds.scopes)

youtube = build("youtube", "v3", credentials=creds)

# -------------------------------------------------
# LOAD METADATA
# -------------------------------------------------
with open("metadata.json", "r", encoding="utf-8") as f:
    meta = json.load(f)

# -------------------------------------------------
# RANDOM SCHEDULE TIME (UTC, FUTURE)
# -------------------------------------------------
publish_at = (
    datetime.datetime.utcnow()
    + datetime.timedelta(hours=random.randint(1, 18))
).replace(microsecond=0).isoformat() + "Z"

# -------------------------------------------------
# STEP 1 — UPLOAD AS UNLISTED (NO publishAt)
# -------------------------------------------------
upload = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": meta["title"],
            "description": meta["description"],
            "tags": meta["tags"],
            "categoryId": "24"
        },
        "status": {
            "privacyStatus": "unlisted",
            "selfDeclaredMadeForKids": False
        }
    },
    media_body=MediaFileUpload("final.mp4", resumable=True)
)

video = upload.execute()
video_id = video["id"]

print("✅ Uploaded (unlisted):", video_id)

# -------------------------------------------------
# COMMENT + PIN
# -------------------------------------------------
try:
    comment = youtube.commentThreads().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": video_id,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": meta.get(
                            "comment",
                            "Do you agree with this, or am I wrong? 👇"
                        )
                    }
                }
            }
        }
    ).execute()

    thread_id = comment["id"]

    youtube.commentThreads().update(
        part="snippet",
        body={
            "id": thread_id,
            "snippet": {"isPinned": True}
        }
    ).execute()

    print("📌 Comment posted and pinned")

except Exception as e:
    print("⚠️ Comment failed (continuing)")
    print(e)

# -------------------------------------------------
# STEP 2 — SCHEDULE THE VIDEO (PRIVATE + publishAt)
# -------------------------------------------------
youtube.videos().update(
    part="status",
    body={
        "id": video_id,
        "status": {
            "privacyStatus": "private",
            "publishAt": publish_at,
            "selfDeclaredMadeForKids": False
        }
    }
).execute()

print("⏰ Video scheduled for:", publish_at)
