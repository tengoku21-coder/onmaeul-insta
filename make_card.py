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
    d.text((80, 90), TAG.get(post["target"], ""), font=ImageFont.truetype(FONT, 40), fill=ACCENT)
    f = ImageFont.truetype(FONT, 76)
    y = 220
    for line in textwrap.wrap(post["title"], 13):
        d.text((80, y), line, font=f, fill=FG); y += 100
    d.text((80, 940), "onmaeul.co.kr  |  1551-6188", font=ImageFont.truetype(FONT, 36), fill=ACCENT)
    im.save(out)

if __name__ == "__main__":
    (ROOT / "images").mkdir(exist_ok=True)
    rows = list(csv.DictReader(open(ROOT / "posts.csv", encoding="utf-8")))
    for p in rows:
        card(p, ROOT / "images" / f"{int(p['id']):03d}.png")
    assert (ROOT / "images" / "001.png").stat().st_size > 5000
    print(f"{len(rows)} cards")
