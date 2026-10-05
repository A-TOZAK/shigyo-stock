# 士業ストック

石山通りグループの仕事を説明するイラストとスライドのひな形のサイト。2026-10-04 に正式な案件になり、石山通りグループ向けに作り替えました（公開資料ではない扱い。URLは本人の判断で公開のまま、検索には出さない設定）。

- 元データ：`_build/catalog.json`（人が書く）
- 書き出し：`python3 _build/build.py`（img/・items.js・i/*.html・sitemap.xml を作る。push はしない）
- 企画書：LiFE with の案件フォルダ `40 学校と案件/28 …/12-士業イラスト素材サイト/00_企画書.md`
- 絵の元画像：`~/Desktop/LiFE with/17 素材集/generated_chousashi_2026-09/` ほか
- 公開の状態：2026-09-23 に公開しました。公開先は https://a-tozak.github.io/shigyo-stock/ です。リポジトリ A-TOZAK/shigyo-stock は public で、GitHub Pages は main の直下から配信しています。
- 点数：2026-09-26 の時点で342点です。絵柄はリコ（フラット）だけです。2026-10-04 にパソコンの裏にロゴのような印が見える1点（kyoutsu-desk-pc）を外しました。
- 2026-10-04 の追加：社内イベント24点と業務の見直し24点（`_build/add_ishiyama.py`）。分野の絞りこみに「社内イベント」「業務の見直し」を足しました。
- お気に入り：`fav.js`。カードの右上の☆と、詳しいページのボタンで入れる。localStorage（キー shigyo-fav）なので、使っている端末のブラウザだけに残る。
- 2026-10-05 の追加：土地家屋調査士の3D計測の絵10点（`_build/add_3d.py`）、分野のアイコン9点（`_build/make_icons.py` → `icons/`）、要望フォーム（`yobo.html`、作り方は `_build/form/`）。この日の時点で399点です。
- スライドのひな形：`templates/`（説明会・仕事の流れ・社内の連絡の流れ）。元は `_build/templates/make_templates.js` です。pptxgenjs と sharp はリポジトリに入れず、別の場所に入れて NODE_PATH で渡します。
- 足し方：検品に合格した絵だけを catalog.json に足し、build.py で書き出してから push します。著作権ゲートは1回の push で画像30枚を超えると止まります。1点で3枚なので、1回の push は10点までにします。

© 石山通りグループ
