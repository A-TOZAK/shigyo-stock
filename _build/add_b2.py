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
META.update({
 "R01_denwa": ("電話で相談を受ける女性の調査士", "女性の調査士が、机で電話を受けながらメモを取る場面", ["電話", "相談", "女性"]),
 "R02_denwa": ("電話で相談を受ける男性の調査士", "男性の調査士が、机で電話を受けながらメモを取る場面", ["電話", "相談", "男性"]),
 "R03_watasu": ("書類を渡す女性の調査士", "女性の調査士が、書類の入ったファイルを両手で差し出す場面", ["書類", "お渡し", "女性"]),
 "R04_watasu": ("書類を渡す男性の調査士", "男性の調査士が、書類の入ったファイルを両手で差し出す場面", ["書類", "お渡し", "男性"]),
 "R05_setsumei": ("図面で説明する女性の調査士", "女性の調査士が、机の図面を相手の側に向けてペンで指し、説明する場面", ["図面", "説明", "女性"]),
 "R06_setsumei": ("図面で説明する男性の調査士", "男性の調査士が、机の図面を相手の側に向けてペンで指し、説明する場面", ["図面", "説明", "男性"]),
 "R07_pc": ("パソコンで仕事をする女性の調査士", "女性の調査士が、机のノートパソコンで仕事をする場面", ["パソコン", "事務所", "女性"]),
 "R08_pc": ("パソコンで仕事をする男性の調査士", "男性の調査士が、机のノートパソコンで仕事をする場面", ["パソコン", "事務所", "男性"]),
 "S01_douro_ts": ("道路わきで観測する女性の調査士", "ヘルメットと安全ベストを着けた女性の調査士が、道路わきでトータルステーションをのぞく場面", ["道路", "観測", "ヘルメット", "女性"]),
 "S02_douro_ts": ("道路わきで観測する男性の調査士", "ヘルメットと安全ベストを着けた男性の調査士が、道路わきでトータルステーションをのぞく場面", ["道路", "観測", "ヘルメット", "男性"]),
 "S03_kyoukai_yubisasu": ("境界標を指して近所の方に説明する（女性）", "住宅地で、女性の調査士が境界標を指さし、近所の高齢の男性が見ている場面", ["境界標", "近所", "住宅地", "女性"]),
 "S04_kyoukai_yubisasu": ("境界標を指して近所の方に説明する（男性）", "住宅地で、男性の調査士が境界標を指さし、近所の高齢の女性が見ている場面", ["境界標", "近所", "住宅地", "男性"]),
 "S05_tachiai_zumen": ("立会いで図面を見せる（女性）", "住宅地の道で、女性の調査士が図面を高齢の夫婦に見せて説明する場面", ["立会い", "図面", "夫婦", "女性"]),
 "S06_tachiai_zumen": ("立会いで図面を見せる（男性）", "住宅地の道で、男性の調査士が図面を中年の夫婦に見せて説明する場面", ["立会い", "図面", "夫婦", "男性"]),
 "S07_douro_tatsu": ("道路わきに立つ女性の調査士", "ヘルメットと安全ベストを着けて、道路わきに立つ女性の調査士", ["道路", "ヘルメット", "女性"]),
 "S08_douro_tatsu": ("道路わきに立つ男性の調査士", "ヘルメットと安全ベストを着けて、道路わきに立つ男性の調査士", ["道路", "ヘルメット", "男性"]),
 "K01_shokai_soudan_v3": ("初めての相談", "40代の女性が、ソファに座って専門家に初めて相談する場面", ["相談", "女性", "初めて"]),
 "K02_aisatsu_meishi_v3": ("名刺を持ってあいさつする", "専門家が名刺入れを持ち、軽くおじぎをしてあいさつする場面", ["あいさつ", "名刺"]),
 "K06_kazoku_online_v3": ("離れた家族が画面で同席する相談", "高齢の夫婦の相談に、離れて住む息子がノートパソコンの画面で同席する場面", ["オンライン", "家族", "高齢の方"]),
 "K10_seminar_koushi_v3": ("勉強会で話す講師", "小さな集会所で、講師がスクリーンの横に立って話す場面", ["勉強会", "セミナー", "講師"]),
 "K15_houmon_v3": ("お宅を訪ねる", "専門家が高齢の方のお宅を訪ね、玄関であいさつする場面", ["訪問", "高齢の方", "玄関"]),
 "K18_tablet_v3": ("タブレットを並んで見る", "専門家と高齢の方が並んで座り、机のタブレットを一緒に見る場面", ["タブレット", "説明", "高齢の方"]),
})
PLACE = {"R": ("事務所", "相談"), "S": ("現場", "現場"), "K": ("相談", "相談")}
OLD = json.loads((ROOT / "_build/b2_old_meta.json").read_text())
REDO = {"F03": "chousashi-mitsumori-setsumei", "F04": "chousashi-shiryo-houmukyoku", "F15": "chousashi-zumen-check",
        "F05": "chousashi-kui-sagasu", "F06": "chousashi-ts-kansoku", "F07": "chousashi-pole-tateru",
        "F08": "chousashi-gnss-kansoku", "F09": "chousashi-shashin", "F13": "chousashi-kui-secchi",
        "F21": "chousashi-tatemono-chousa", "F22": "chousashi-housemaker-genba", "F31": "chousashi-shinchiku-kazoku",
        "B03": "chousashi-prism", "F18": "chousashi-online-shinsei"}
c = json.loads((ROOT / "_build/catalog.json").read_text())
ids = {a["id"] for a in c["assets"]}
for f in sys.argv[1:]:
    key = f.replace("riko_", "").replace("mitoma_", "").replace(".png", "")
    au = "mitoma" if f.startswith("mitoma") else "riko"
    if key[0] in "QRS" and key.endswith("_v2"):
        key = key[:-3]
    if key.startswith("P"):
        _, w, p = key.split("_")
        t = f"{W[w][0]}（{P[p][0]}）"; d = f"{W[w][0]}が、{P[p][1]}"
        iid, sh, dk, k, tags = f"chousashi-honnin-{w}-{p}", ["土地家屋調査士"], "相談", "人", ["調査士"] + W[w][1]
        how = "事務所の紹介、採用ページ、担当者の紹介に使えます。"
    elif key[:3] in REDO:
        iid = REDO[key[:3]]
        hit = [a for a in c["assets"] if a["id"] == iid]
        if hit:
            hit[0]["src"] = G + f; print("差し替え:", iid)
        else:
            a = dict(OLD[iid]); a["src"] = G + f; c["assets"].append(a); ids.add(iid); print("戻す:", iid)
        continue
    elif key in META and key[0] == "Q":
        t, d, tags = META[key]
        iid, sh, dk, k = "kyoutsu-" + key.split("_", 1)[1].replace("_", "-"), ["共通"], "相談", "人"
        how = "「こんな方がご相談に来られます」という案内や、相談の流れの説明に使えます。"
    elif key in META:
        t, d, tags = META[key]
        base = key.replace("_v3", "").split("_", 1)[1].replace("_", "-")
        if key[0] == "K":
            iid, sh, dk, k = f"kyoutsu-{base}-sen", ["共通"], "相談", "場面"
            how = "相談の流れや、事務所の案内に使えます。"
        else:
            sfx = {"R01": "f", "R03": "f", "R05": "f", "R07": "f", "S01": "f", "S03": "f", "S05": "f", "S07": "f"}.get(key[:3], "m")
            iid = f"chousashi-{base}-{sfx}"; sh = ["土地家屋調査士"]; k = "場面"
            dk = "現場" if key[0] == "S" else ("完了" if "watasu" in key else "相談")
            how = "ご依頼の流れの説明や、採用ページに使えます。"
        d = d
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
