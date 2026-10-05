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

STYLE_OF = {"riko": "フラット", "mitoma": "線画", "sumire": "水彩"}
items = []
for a in cat["assets"]:
    im = flat(Image.open(SOZAI / a["src"]))
    out = ROOT / "img"
    fit(im, FULL_W).save(out / f'{a["id"]}.jpg', quality=Q)
    fit(im, THUMB_W).save(out / f'{a["id"]}_thumb.jpg', quality=Q)
    ImageOps.grayscale(fit(im, FULL_W)).save(out / f'{a["id"]}_mono.jpg', quality=Q)
    it = {k: v for k, v in a.items() if k != "src"}
    it["credit"] = authors[a["author"]]["romaji"]
    it["style"] = STYLE_OF[a["author"]]
    it["w"], it["h"] = fit(im, FULL_W).size
    items.append(it)

(ROOT / "items.js").write_text("const ITEMS=" + json.dumps(items, ensure_ascii=False, indent=0) + ";\n")

PAGE = """<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="robots" content="noindex">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}｜士業ストック</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:site_name" content="士業ストック">
<meta property="og:title" content="{title}｜士業ストック"><meta property="og:description" content="{desc}">
<meta property="og:image" content="{img}"><meta name="twitter:card" content="summary_large_image">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap" rel="stylesheet"><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22%3E%3Crect width=%2232%22 height=%2232%22 rx=%225%22 fill=%22%231b3a6b%22/%3E%3Cpath d=%22M9 22h14M16 9v13M11 13h10%22 stroke=%22white%22 stroke-width=%222.6%22 stroke-linecap=%22round%22/%3E%3C/svg%3E"><link rel="stylesheet" href="../style.css?v=1005c">
<script type="application/ld+json">{ld}</script>
</head><body>
<header class="top"><div class="top-in"><a class="logo" href=".././"><b>士業ストック</b><small>石山通りグループの説明イラスト</small></a><nav aria-label="サイトの案内"><a href=".././">素材をさがす</a><a href="../templates.html">スライドのひな形</a><a href="../yobo.html">要望を送る</a><a href="../about.html">このサイトについて</a><a href="../terms.html">利用の決まり</a></nav></div></header>
<main class="detail">
<div class="figure"><img class="big" src="../img/{id}.jpg" alt="{alt}" width="{w}" height="{h}"></div>
<div class="info">
<p class="crumb"><a href="../">素材をさがす</a> ／ {shikaku} ／ {dankai}</p>
<h1>{title}</h1>
<div class="tagline">{chips}</div>
<div class="dl"><a class="btn" href="../img/{id}.jpg" download>カラーで保存</a><a class="btn sub" href="../img/{id}_mono.jpg" download>白黒で保存</a><button class="favbtn" id="fav" data-id="{id}" aria-pressed="false">☆ お気に入りに入れる</button></div>
<h2>この絵について</h2><p>{desc_h}</p>
<h2>使い方の例</h2><p>{howto}</p>
<p class="tags">{tags}</p>
<a class="ask" href="../yobo.html?from={id}">この絵について要望を送る</a>
<p class="credit">生成AIのイラストレーターが描き、AIの検品役が確かめた絵です。</p>
</div>
</main>
{related}
<footer><div class="foot-in"><span>© 石山通りグループ</span><nav aria-label="下の案内"><a href="../templates.html">スライドのひな形</a><a href="../yobo.html">要望を送る</a><a href="../about.html">このサイトについて</a><a href="../terms.html">利用の決まり</a></nav></div></footer>
<script src="../fav.js?v=1004"></script><script>const fb=document.getElementById("fav");function sh(on){{fb.setAttribute("aria-pressed",on);fb.textContent=favLabel(on)}}sh(favHas(fb.dataset.id));fb.onclick=()=>sh(favToggle(fb.dataset.id));</script>
</body></html>"""

urls = [BASE, BASE + "about.html", BASE + "terms.html", BASE + "templates.html", BASE + "yobo.html"]
for it in items:
    url = f'{BASE}i/{it["id"]}.html'
    img = f'{BASE}img/{it["id"]}.jpg'
    ld = {
        "@context": "https://schema.org", "@type": "ImageObject",
        "name": it["title"], "contentUrl": img, "description": it["description"],
        "license": BASE + "terms.html", "acquireLicensePage": BASE + "terms.html",
        "creditText": "石山通りグループ", "copyrightNotice": "© 石山通りグループ",
    }
    e = html.escape
    sh0 = it["shikaku"][0]
    rel = [x for x in items if x["id"] != it["id"] and sh0 in x["shikaku"] and x["dankai"] == it["dankai"]]
    rel += [x for x in items if x["id"] != it["id"] and sh0 in x["shikaku"] and x not in rel]
    rel = rel[:6]
    related = ('<section class="related" aria-labelledby="h-rel"><h2 id="h-rel">同じ分野の絵</h2><div class="grid">' + "".join(
        f'<article class="card"><a class="pic" href="{x["id"]}.html" tabindex="-1"><img loading="lazy" src="../img/{x["id"]}_thumb.jpg" alt="{e(x["alt"])}"></a>'
        f'<div class="b"><h3><a href="{x["id"]}.html">{e(x["title"])}</a></h3></div></article>' for x in rel) + '</div></section>') if rel else ""
    chips = "".join(f"<span>{e(x)}</span>" for x in it["shikaku"]) + f"<span>{e(it['dankai'])}</span><span>{e(it['kind'])}</span>"
    (ROOT / "i" / f'{it["id"]}.html').write_text(PAGE.format(related=related, chips=chips, 
        title=e(it["title"]), desc=e(it["description"]), desc_h=e(it["description"]),
        url=url, img=img, ld=json.dumps(ld, ensure_ascii=False), id=it["id"],
        alt=e(it["alt"]), w=it["w"], h=it["h"], howto=e(it["howto"]),
        shikaku=e("、".join(it["shikaku"])), dankai=e(it["dankai"]),
        style=it["style"], tags=" ".join(f"<span>{e(t)}</span>" for t in it["tags"]), credit=it["credit"]))
    urls.append(url)

sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
sm += [f"<url><loc>{u}</loc></url>" for u in urls]
sm.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n")
print(f"{len(items)}点を書き出しました")
