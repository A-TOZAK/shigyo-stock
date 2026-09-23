#!/usr/bin/env python3
"""士業ストック　書き出し（2026-09-23）

_build/catalog.json を読み、次を作る。
  img/<id>.jpg        幅1600（ダウンロード用）
  img/<id>_thumb.jpg  幅640（一覧用）
  img/<id>_mono.jpg   白黒（ダウンロード用）
  items.js            const ITEMS=[...]
  i/<id>.html         1点ずつのページ（検索にかかる）
  sitemap.xml
使い方: python3 _build/build.py
push はしない。School Stock のカタログとは混ぜない。
"""
import html, json, sys
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SOZAI = Path.home() / "Desktop" / "LiFE with" / "17 素材集"
BASE = "https://a-tozak.github.io/shigyo-stock/"
FULL_W, THUMB_W, Q = 1600, 640, 84

cat = json.loads((ROOT / "_build" / "catalog.json").read_text())
authors = cat["authors"]


def fit(im, w):
    if im.width <= w:
        return im.copy()
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)


def flat(im):
    if im.mode in ("RGBA", "LA", "P"):
        rgba = im.convert("RGBA")
        bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        bg.alpha_composite(rgba)
        return bg.convert("RGB")
    return im.convert("RGB")


missing = [a["src"] for a in cat["assets"] if not (SOZAI / a["src"]).exists()]
if missing:
    print("元の画像が見つかりません:", *missing, sep="\n  ")
    sys.exit(1)

items = []
for a in cat["assets"]:
    im = flat(Image.open(SOZAI / a["src"]))
    out = ROOT / "img"
    fit(im, FULL_W).save(out / f'{a["id"]}.jpg', quality=Q)
    fit(im, THUMB_W).save(out / f'{a["id"]}_thumb.jpg', quality=Q)
    ImageOps.grayscale(fit(im, FULL_W)).save(out / f'{a["id"]}_mono.jpg', quality=Q)
    it = {k: v for k, v in a.items() if k != "src"}
    it["credit"] = authors[a["author"]]["romaji"]
    it["w"], it["h"] = fit(im, FULL_W).size
    items.append(it)

(ROOT / "items.js").write_text("const ITEMS=" + json.dumps(items, ensure_ascii=False, indent=0) + ";\n")

PAGE = """<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}｜士業の説明に使えるイラスト素材（無料）｜士業ストック</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:site_name" content="士業ストック">
<meta property="og:title" content="{title}｜士業ストック"><meta property="og:description" content="{desc}">
<meta property="og:image" content="{img}"><meta name="twitter:card" content="summary_large_image">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="../style.css">
<script type="application/ld+json">{ld}</script>
</head><body>
<header class="top"><a class="logo" href="../">士業ストック</a><nav><a href="../">素材をさがす</a><a href="../about.html">このサイトについて</a><a href="../terms.html">利用規約</a></nav></header>
<main class="one">
<p class="crumb"><a href="../">トップ</a> ／ {shikaku} ／ {dankai}</p>
<h1>{title}</h1>
<img class="big" src="../img/{id}.jpg" alt="{alt}" width="{w}" height="{h}">
<div class="dl"><a class="btn" href="../img/{id}.jpg" download>カラーで保存</a><a class="btn sub" href="../img/{id}_mono.jpg" download>白黒で保存</a></div>
<p>{desc_h}</p>
<h2>使い方の例</h2><p>{howto}</p>
<p class="tags">{tags}</p>
<p class="credit">絵　{credit}　／　AIで下絵を作り、人が1枚ずつ確かめています。</p>
</main>
<footer>© 士業ストック（外﨑顯博）　<a href="../terms.html">利用規約</a></footer>
</body></html>"""

urls = [BASE, BASE + "about.html", BASE + "terms.html"]
for it in items:
    url = f'{BASE}i/{it["id"]}.html'
    img = f'{BASE}img/{it["id"]}.jpg'
    ld = {
        "@context": "https://schema.org", "@type": "ImageObject",
        "name": it["title"], "contentUrl": img, "description": it["description"],
        "license": BASE + "terms.html", "acquireLicensePage": BASE + "terms.html",
        "creditText": "士業ストック", "copyrightNotice": "© 士業ストック",
    }
    e = html.escape
    (ROOT / "i" / f'{it["id"]}.html').write_text(PAGE.format(
        title=e(it["title"]), desc=e(it["description"]), desc_h=e(it["description"]),
        url=url, img=img, ld=json.dumps(ld, ensure_ascii=False), id=it["id"],
        alt=e(it["alt"]), w=it["w"], h=it["h"], howto=e(it["howto"]),
        shikaku=e("、".join(it["shikaku"])), dankai=e(it["dankai"]),
        tags=" ".join(f"<span>{e(t)}</span>" for t in it["tags"]), credit=it["credit"]))
    urls.append(url)

sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
sm += [f"<url><loc>{u}</loc></url>" for u in urls]
sm.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n")
print(f"{len(items)}点を書き出しました")
