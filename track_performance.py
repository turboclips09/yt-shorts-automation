import os,json,datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

brain=json.load(open("brain.json"))

creds=Credentials(
None,
refresh_token=os.getenv("YT_REFRESH_TOKEN"),
token_uri="https://oauth2.googleapis.com/token",
client_id=os.getenv("YT_CLIENT_ID"),
client_secret=os.getenv("YT_CLIENT_SECRET"),
scopes=["https://www.googleapis.com/auth/youtube.force-ssl"]
)

yt=build("youtube","v3",credentials=creds)

search=yt.search().list(
part="id",
forMine=True,
type="video",
order="date",
maxResults=5
).execute()

ids=[i["id"]["videoId"] for i in search["items"]]

stats=yt.videos().list(
part="statistics",
id=",".join(ids)
).execute()

for v in stats["items"]:
    brain["history"].append({
        "video_id": v["id"],
        "views": int(v["statistics"].get("viewCount",0)),
        "time": datetime.datetime.utcnow().isoformat(),
        **brain.get("last_meta",{})
    })

brain["history"]=brain["history"][-500:]
json.dump(brain,open("brain.json","w"),indent=2)
