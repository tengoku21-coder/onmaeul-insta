"""posts.csv 전체를 1080x1080 카드로 렌더 → images/NNN.png"""
import csv, pathlib, textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).parent
FONT = "C:/Windows/Fonts/malgunbd.ttf"   # ponytail: 윈도우 전용, 리눅스면 NanumGothicBold.ttf 경로로 교체
BG, FG, ACCENT = "#0B3D2E", "#FFFFFF", "#7CE0A6"
TAG = {"입주민": "입주민에게", "관리소장": "관리소장님께", "입대의": "입주자대표님께"}

def wrap(title, width=10):
    """2줄로 균형 있게 나누고, 안 되면 textwrap. 한 글자 조사('안','차')가 줄 끝에 남는 것 방지."""
    if len(title) <= width: return [title]
    w = title.split()
    best = None
    for i in range(1, len(w)):
        a, b = " ".join(w[:i]), " ".join(w[i:])
        if len(a) <= width and len(b) <= width and len(w[i-1]) > 1:
            if best is None or abs(len(a) - len(b)) < abs(len(best[0]) - len(best[1])): best = (a, b)
    return list(best) if best else textwrap.wrap(title, width)

def card(post, out):
    im = Image.new("RGB", (1080, 1080), BG)
    d = ImageDraw.Draw(im)
    # 프로필 그리드는 3:4로 좌우가 잘리므로 가운데 정렬 + 중앙 760px 안에 배치
    d.text((540, 300), TAG.get(post["target"], ""), font=ImageFont.truetype(FONT, 40), fill=ACCENT, anchor="mm")
    f = ImageFont.truetype(FONT, 72)
    lines = wrap(post["title"])
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
