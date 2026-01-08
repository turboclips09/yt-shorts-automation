import os
import json
import random
import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

CLIENT_ID = os.getenv("YT_CLIENT_ID")
CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("YT_REFRESH_TOKEN")

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

youtube = build("youtube", "v3", credentials=creds)

with open("metadata.json", "r", encoding="utf-8") as f:
    meta = json.load(f)

publish_at = (
    datetime.datetime.utcnow()
    + datetime.timedelta(hours=random.randint(1, 18))
).replace(microsecond=0).isoformat() + "Z"

# Upload as UNLISTED
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

# Post comment (no pin)
try:
    youtube.commentThreads().insert(
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

    print("💬 Comment posted")

except Exception as e:
    print("⚠️ Comment failed (non-critical)")
    print(e)

# Schedule video
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
