"""posts.csv 전체를 1080x1080 카드로 렌더 → images/NNN.png"""
import csv, pathlib, textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).parent
FONT = "C:/Windows/Fonts/malgunbd.ttf"   # ponytail: 윈도우 전용, 리눅스면 NanumGothicBold.ttf 경로로 교체
BG, FG, ACCENT = "#0B3D2E", "#FFFFFF", "#7CE0A6"
TAG = {"입주민": "입주민에게", "관리소장": "관리소장님께", "입대의": "입주자대표님께"}

def card(post, out):
    im = Image.new("RGB", (1080, 1080), BG)
    d = ImageDraw.Draw(im)
    # 프로필 그리드는 3:4로 좌우가 잘리므로 가운데 정렬 + 중앙 760px 안에 배치
    d.text((540, 300), TAG.get(post["target"], ""), font=ImageFont.truetype(FONT, 40), fill=ACCENT, anchor="mm")
    f = ImageFont.truetype(FONT, 72)
    lines = textwrap.wrap(post["title"], 10)
    y = 540 - (len(lines) - 1) * 48
    for line in lines:
        d.text((540, y), line, font=f, fill=FG, anchor="mm"); y += 96
    d.text((540, 800), "onmaeul.co.kr  |  1551-6188", font=ImageFont.truetype(FONT, 34), fill=ACCENT, anchor="mm")
    im.save(out)

if __name__ == "__main__":
    (ROOT / "images").mkdir(exist_ok=True)
    rows = list(csv.DictReader(open(ROOT / "posts.csv", encoding="utf-8")))
    for p in rows:
        card(p, ROOT / "images" / f"{int(p['id']):03d}.png")
    assert (ROOT / "images" / "001.png").stat().st_size > 5000
    print(f"{len(rows)} cards")
