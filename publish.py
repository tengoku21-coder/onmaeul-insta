"""미게시 1건을 Instagram에 게시하고 posts.csv에 날짜 기록. 토큰 없으면 dry-run(파일 미수정)."""
import csv, os, pathlib, datetime, time, requests

ROOT = pathlib.Path(__file__).parent
CSV = ROOT / "posts.csv"
IG_ID, TOKEN = os.getenv("IG_USER_ID"), os.getenv("IG_TOKEN")
BASE = os.getenv("IMAGE_BASE_URL") or f"https://raw.githubusercontent.com/{os.getenv('GITHUB_REPOSITORY', 'USER/REPO')}/main"
API = "https://graph.instagram.com/v21.0"

def caption(p):
    return f"{p['title']}\n\n{p['body']}\n\n상담 신청은 프로필 링크 ▶ onmaeul.co.kr\n\n{p['hashtags']}"

def publish(p):
    url = f"{BASE}/images/{int(p['id']):03d}.png"
    r = requests.post(f"{API}/{IG_ID}/media", data={"image_url": url, "caption": caption(p), "access_token": TOKEN}, timeout=60)
    assert r.ok, r.text
    cid = r.json()["id"]
    for _ in range(12):  # 이미지 처리 대기 (최대 60초)
        s = requests.get(f"{API}/{cid}", params={"fields": "status_code", "access_token": TOKEN}, timeout=60).json()
        if s.get("status_code") == "FINISHED": break
        assert s.get("status_code") != "ERROR", s
        time.sleep(5)
    r = requests.post(f"{API}/{IG_ID}/media_publish", data={"creation_id": cid, "access_token": TOKEN}, timeout=60)
    assert r.ok, r.text
    print("published", r.json())

if __name__ == "__main__":
    rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
    todo = next((p for p in rows if not p["posted"]), None)
    assert todo, "posts.csv 소진 — 새 글 추가 필요"
    if not TOKEN:
        print("[dry-run]\n" + caption(todo)); raise SystemExit
    publish(todo)
    todo["posted"] = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).date().isoformat()  # KST
    with open(CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
