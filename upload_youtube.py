import os
import json
import random
import datetime
import sys

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# --------------------------------
# ENV
# --------------------------------
CLIENT_ID = os.getenv("YT_CLIENT_ID")
CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("YT_REFRESH_TOKEN")

# --------------------------------
# AUTH
# --------------------------------
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

# --------------------------------
# LOAD METADATA
# --------------------------------
meta = json.load(open("metadata.json"))

# --------------------------------
# RANDOM SCHEDULE TIME (1–18 HRS)
# --------------------------------
publish_at = (
    datetime.datetime.utcnow()
    + datetime.timedelta(hours=random.randint(1,18))
).replace(microsecond=0).isoformat()+"Z"

# --------------------------------
# UPLOAD VIDEO (NON-RESUMABLE)
# --------------------------------
request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet":{
            "title": meta["title"],
            "description": meta["description"],
            "tags": meta["tags"],
            "categoryId":"24"
        },
        "status":{
            "privacyStatus":"private",
            "publishAt": publish_at,
            "selfDeclaredMadeForKids": False
        }
    },
    media_body=MediaFileUpload("final.mp4", resumable=False)
)

try:
    response = request.execute()
    print("✅ Uploaded & scheduled:", response["id"])
    print("⏰ Publish time:", publish_at)

except HttpError as e:
    if "uploadLimitExceeded" in str(e):
        print("🚫 Daily upload limit reached")
        sys.exit(0)
    else:
        raise
