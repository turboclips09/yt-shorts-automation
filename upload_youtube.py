import os
import json
import random
import datetime
import sys

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import ResumableUploadError, HttpError

# -------------------------------------------------
# ENV VARIABLES (FROM GITHUB SECRETS)
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
# RANDOM PUBLISH TIME (1–18 HOURS FROM NOW)
# -------------------------------------------------
publish_at = (
    datetime.datetime.utcnow()
    + datetime.timedelta(hours=random.randint(1, 18))
).replace(microsecond=0).isoformat() + "Z"

# -------------------------------------------------
# UPLOAD VIDEO (UNLISTED FIRST)
# -------------------------------------------------
upload = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": meta["title"],
            "description": meta["description"],
            "tags": meta["tags"],
            "categoryId": "24"  # Entertainment
        },
        "status": {
            "privacyStatus": "unlisted",
            "selfDeclaredMadeForKids": False
        }
    },
    media_body=MediaFileUpload("final.mp4", resumable=True)
)

try:
    video = upload.execute()

except ResumableUploadError as e:
    if "uploadLimitExceeded" in str(e):
        print("🚫 Daily upload limit reached. Skipping upload safely.")
        sys.exit(0)
    else:
        raise

video_id = video["id"]
print("✅ Uploaded (unlisted):", video_id)

# -------------------------------------------------
# AUTO COMMENT (NO PIN — API LIMITATION)
# -------------------------------------------------
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

except HttpError as e:
    print("⚠️ Comment failed (non-critical)")
    print(e)

# -------------------------------------------------
# SCHEDULE VIDEO
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
