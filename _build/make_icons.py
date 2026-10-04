"""分野のアイコンを書き出す（2026-10-04）。python3 _build/make_icons.py
元＝17 素材集/generated_shigyo_ishiyama_2026-10/riko_I0*.png → icons/<key>.png（256px、余白をそろえる）"""
from pathlib import Path
from PIL import Image, ImageChops
ROOT = Path(__file__).resolve().parent.parent
SRC = Path.home() / "Desktop/LiFE with/17 素材集/generated_shigyo_ishiyama_2026-10"
KEYS = {"I01_kyoutsu": "kyoutsu", "I02_shihoshoshi": "shihoshoshi", "I03_chousashi": "chousashi", "I04_gyoseishoshi": "gyoseishoshi",
        "I05_sharoushi": "sharoushi", "I06_zeirishi": "zeirishi", "I07_bengoshi": "bengoshi", "I08_shanai_event": "shanai-event", "I09_gyomu_minaoshi": "gyomu-minaoshi"}
(ROOT / "icons").mkdir(exist_ok=True)
for k, out in KEYS.items():
    cands = sorted(SRC.glob(f"riko_{k}*.png"))
    if not cands:
        print("まだない", k); continue
    im = Image.open(cands[-1]).convert("RGB")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    box = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 18 else 0).getbbox()
    im = im.crop(box)
    side = int(max(im.size) * 1.12)
    sq = Image.new("RGB", (side, side), (255, 255, 255))
    sq.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
    sq.resize((256, 256), Image.LANCZOS).save(ROOT / "icons" / f"{out}.png", optimize=True)
    print("書き出し", out, cands[-1].name)
