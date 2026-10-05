"""土地家屋調査士の3D計測の絵（合格分）をカタログに足す（2026-10-05）。python3 _build/add_3d.py ファイル名 ..."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
G = "generated_shigyo_ishiyama_2026-10/"
C = ["土地家屋調査士"]
U = ["ホームページ", "説明の紙", "チラシ"]
META = {
 "T01_scanner": ("chousashi-3d-scanner", C, "3Dレーザースキャナー", "現場", "道具", "三脚にのせた、小さな3Dレーザースキャナー", "3Dで測る仕事の紹介に使えます。", ["3D", "レーザースキャナー", "測量"]),
 "T02_tengun_pc": ("chousashi-3d-tengun-pc", C, "点群が映ったパソコン", "書類", "道具", "家と塀の点群（点の集まりの3Dデータ）が映ったパソコン", "測ったデータの説明に使えます。", ["3D", "点群", "パソコン"]),
 "T03_tengun_kyoukai": ("chousashi-3d-kyoukai", C, "点群で見る境界", "調査", "図解の部品", "点群で描いた家と塀のあいだに、境界の線が黄色で浮かぶ図", "境界を3Dで見せる説明に使えます。", ["3D", "点群", "境界"]),
 "T04_kikaiten": ("chousashi-3d-kikaiten", C, "上から見た器械点", "現場", "図解の部品", "上から見た敷地のまわりに、器械を置く点を丸で並べて点線でつないだ図", "現地でどこから測るかの説明に使えます。", ["3D", "器械点", "測量"]),
 "T11_roji_scan": ("chousashi-3d-roji", C, "細い路地を3Dで測る", "現場", "場面", "高い塀にはさまれた細い路地に3Dスキャナーを置き、調査士が少し離れて待つ場面", "見通しの悪い現場でも測れることの説明に使えます。", ["3D", "路地", "現地調査"]),
 "T12_yuugata_scan": ("chousashi-3d-yuugata", C, "夕方に1人で測る", "現場", "場面", "夕方、取り壊す前の古い家の前で、調査士が1人で3Dスキャナーを置く場面", "1人で、夕方でも測れることの説明に使えます。", ["3D", "取り壊し", "現地調査"]),
 "T13_gousei": ("chousashi-3d-gousei", C, "点群を整える", "書類", "場面", "事務所で、調査士が画面の点群から余分な点を消して整える場面", "測ったあとの事務所の作業の説明に使えます。", ["3D", "点群", "事務所"]),
 "T14_tachiai_3d": ("chousashi-3d-tachiai", C, "立会いで3Dの画像を見せる", "現場", "場面", "境界の立会いで、調査士がタブレットの3Dの画像をお隣の方に見せて説明する場面", "立会いの説明に使えます。", ["3D", "立会い", "境界"]),
 "T15_danmen": ("chousashi-3d-danmen", C, "断面図を画面で作る", "書類", "場面", "調査士が、画面で土地の高さの断面図を作る場面", "高低差や断面図の追加のご依頼の説明に使えます。", ["3D", "断面図", "高低差"]),
 "T16_3d_uchiawase": ("chousashi-3d-uchiawase", C, "設計の方と3Dデータを見る", "相談", "場面", "調査士と住宅の設計の方が、パソコンの3Dデータを見ながら打合せする場面", "設計事務所や建築会社との連携の説明に使えます。", ["3D", "設計", "打合せ"]),
}
c = json.loads((ROOT / "_build/catalog.json").read_text())
ids = {a["id"] for a in c["assets"]}
for f in sys.argv[1:]:
    key = f.split("_", 1)[1].replace(".png", "")
    for suf in ("_v2", "_v3", "_v4"):
        if key.endswith(suf):
            key = key[: -len(suf)]
    iid, sh, t, dk, k, d, how, tags = META[key]
    a = {"id": iid, "src": G + f, "author": "riko", "title": t, "shikaku": sh, "dankai": dk, "kind": k, "uses": U,
         "description": d + "のイラストです。", "howto": how, "alt": d + "のイラスト。", "tags": tags}
    if iid in ids:
        c["assets"] = [a if x["id"] == iid else x for x in c["assets"]]
    else:
        c["assets"].append(a); ids.add(iid)
    print("足した", iid)
(ROOT / "_build/catalog.json").write_text(json.dumps(c, ensure_ascii=False, indent=1) + "\n")
