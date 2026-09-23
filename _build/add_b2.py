"""第2陣の合格分をカタログに足す（2026-09-23）。python3 _build/add_b2.py ファイル名 ..."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
G = "generated_shigyo_b2_2026-09/"
W = {"ym": ("若手の男性の調査士", ["男性", "若手"]), "yf": ("若手の女性の調査士", ["女性", "若手"]),
     "vm": ("ベテランの男性の調査士", ["男性", "ベテラン"]), "vf": ("ベテランの女性の調査士", ["女性", "ベテラン"])}
P = {"a": ("クリップボードを持つ", "落ち着いた表情で、クリップボードを胸に持って立つ"),
     "b": ("図面を持って笑顔", "丸めた図面を持ち、笑顔で立つ"),
     "c": ("書類を見せて説明する", "クリップボードをこちらに向けて、指さしながら説明する")}
META = {
 "Q01_wakai_dansei": ("相談に来た20代の男性", "封筒を持って、ひとりで相談に来た20代の男性", ["男性", "20代", "ひとり"]),
 "Q02_wakai_josei": ("相談に来た20代の女性", "書類のファイルを持って、ひとりで相談に来た20代の女性", ["女性", "20代", "ひとり"]),
 "Q03_chunen_dansei": ("相談に来た40代の男性", "大きな封筒を持って、ひとりで相談に来た40代の男性", ["男性", "40代", "ひとり"]),
 "Q04_chunen_josei": ("相談に来た40代の女性", "封筒を持って、ひとりで相談に来た40代の女性", ["女性", "40代", "ひとり"]),
 "Q05_koureisha_dansei": ("相談に来た70代の男性", "封筒を持って、ひとりで相談に来た70代の男性", ["男性", "高齢の方", "ひとり"]),
 "Q06_koureisha_josei": ("相談に来た70代の女性", "手さげを持って、ひとりで相談に来た70代の女性", ["女性", "高齢の方", "ひとり"]),
 "Q07_wakai_fufu": ("相談に来た30代の夫婦", "並んで立つ30代の夫婦", ["夫婦", "30代"]),
 "Q08_chunen_fufu": ("相談に来た50代の夫婦", "並んで立つ50代の夫婦", ["夫婦", "50代"]),
 "Q09_koureisha_fufu_suwaru": ("待合で座る高齢の夫婦", "待合のいすに並んで座る70代の夫婦", ["夫婦", "高齢の方", "待合"]),
 "Q10_haha_musume": ("高齢の母と娘", "並んで立つ70代の母と40代の娘", ["親子", "高齢の方", "相続"]),
 "Q11_chichi_musuko": ("高齢の父と息子", "並んで立つ70代の父と40代の息子", ["親子", "高齢の方", "相続"]),
 "Q12_kyoudai": ("相談に来たきょうだい", "並んで立つ50代の兄と妹", ["きょうだい", "相続"]),
}
c = json.loads((ROOT / "_build/catalog.json").read_text())
ids = {a["id"] for a in c["assets"]}
for f in sys.argv[1:]:
    key = f.replace("riko_", "").replace("mitoma_", "").replace(".png", "")
    au = "mitoma" if f.startswith("mitoma") else "riko"
    if key.startswith("P"):
        _, w, p = key.split("_")
        t = f"{W[w][0]}（{P[p][0]}）"; d = f"{W[w][0]}が、{P[p][1]}"
        iid, sh, dk, k, tags = f"chousashi-honnin-{w}-{p}", ["土地家屋調査士"], "相談", "人", ["調査士"] + W[w][1]
        how = "事務所の紹介、採用ページ、担当者の紹介に使えます。"
    elif key in META:
        t, d, tags = META[key]
        iid, sh, dk, k = "kyoutsu-" + key.split("_", 1)[1].replace("_", "-"), ["共通"], "相談", "人"
        how = "「こんな方がご相談に来られます」という案内や、相談の流れの説明に使えます。"
    else:
        print("META待ち:", f); continue
    if iid in ids:
        print("重複:", iid); continue
    desc = d + "のイラストです。"
    c["assets"].append({"id": iid, "src": G + f, "author": au, "title": t, "shikaku": sh, "dankai": dk, "kind": k,
                        "uses": ["ホームページ", "説明の紙", "チラシ"], "description": desc, "howto": how,
                        "alt": desc.replace("です。", "。"), "tags": tags})
    ids.add(iid)
(ROOT / "_build/catalog.json").write_text(json.dumps(c, ensure_ascii=False, indent=1))
print(len(c["assets"]), "点")
