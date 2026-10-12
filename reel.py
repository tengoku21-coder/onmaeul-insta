"""릴스 1건 게시: py reel.py <videos/파일.mp4> "<캡션>"  (env IG_USER_ID, IG_TOKEN)"""
import os, sys, time, requests

IG_ID, TOKEN = os.environ["IG_USER_ID"], os.environ["IG_TOKEN"]
BASE = f"https://raw.githubusercontent.com/{os.getenv('GITHUB_REPOSITORY', 'tengoku21-coder/onmaeul-insta')}/main"
API = "https://graph.instagram.com/v21.0"
path, caption = sys.argv[1], sys.argv[2]

r = requests.post(f"{API}/{IG_ID}/media", data={"media_type": "REELS", "video_url": f"{BASE}/{path}",
                  "caption": caption, "share_to_feed": "true", "access_token": TOKEN}, timeout=60)
assert r.ok, r.text
cid = r.json()["id"]
for _ in range(36):  # 영상 처리 대기 (최대 3분)
    s = requests.get(f"{API}/{cid}", params={"fields": "status_code,status", "access_token": TOKEN}, timeout=60).json()
    if s.get("status_code") == "FINISHED": break
    assert s.get("status_code") != "ERROR", s
    time.sleep(5)
r = requests.post(f"{API}/{IG_ID}/media_publish", data={"creation_id": cid, "access_token": TOKEN}, timeout=60)
assert r.ok, r.text
print("published", r.json())
