// 石山通りグループ　PowerPointのひな形3本（2026-10-04）
// node _build/templates/make_templates.js → templates/*.pptx
// スライドの文字には句読点を打たない（本人の決まり）。差しかえる所は［ ］で示す。
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const sharp = require("sharp");
const { applyTheme } = require(process.env.PPTX_SKILL + "/scripts/apply_theme.js");

const ROOT = path.resolve(__dirname, "../..");
const IMG = (id) => path.join(ROOT, "img", id + ".jpg");
const OUT = path.join(ROOT, "templates");
const FONT = "BIZ UDPGothic";
const THEME = {
  name: "Ishiyama", headFontFace: FONT, bodyFontFace: FONT,
  colors: { dk1: "1C1C1E", lt1: "FFFFFF", dk2: "1B3A6B", lt2: "EEF0F3",
    accent1: "1B3A6B", accent2: "D9A43A", accent3: "5A5F66", accent4: "C5C9CF",
    accent5: "3F5F8F", accent6: "F4E3B5", hlink: "1B3A6B", folHlink: "5A5F66" },
};
const W = 13.333, H = 7.5, M = 0.6;
const COPY = "© 石山通りグループ";

async function sizeOf(id) { const m = await sharp(IMG(id)).metadata(); return m.width / m.height; }
// 箱の中に絵を収める（縦横比を保って中央に置く）
async function pic(s, id, x, y, w, h) {
  const r = await sizeOf(id); let iw = w, ih = w / r;
  if (ih > h) { ih = h; iw = h * r; }
  s.addImage({ path: IMG(id), x: x + (w - iw) / 2, y: y + (h - ih) / 2, w: iw, h: ih, altText: id, objectName: "絵_" + id });
}

function setup(title) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; pres.author = "石山通りグループ"; pres.company = "石山通りグループ"; pres.title = title;
  pres.theme = { headFontFace: FONT, bodyFontFace: FONT };
  const C = pres.SchemeColor;
  pres.defineSlideMaster({
    title: "表紙", background: { color: "FFFFFF" },
    objects: [
      { rect: { x: 0, y: 0, w: 7.2, h: H, fill: { color: C.accent1 } } },
      { text: { text: COPY, options: { x: M, y: H - 0.7, w: 6, h: 0.35, fontSize: 11, color: C.background1, fontFace: FONT, margin: 0 } } },
    ],
  });
  pres.defineSlideMaster({
    title: "本文", background: { color: "FFFFFF" },
    objects: [
      { text: { text: COPY, options: { x: M, y: H - 0.5, w: 5, h: 0.3, fontSize: 10, color: C.accent3, fontFace: FONT, margin: 0 } } },
    ],
    slideNumber: { x: W - M - 0.6, y: H - 0.5, w: 0.6, h: 0.3, fontSize: 10, color: C.accent3, fontFace: FONT, align: "right" },
  });
  pres.defineSlideMaster({
    title: "終わり", background: { color: "1B3A6B" },
    objects: [
      { text: { text: COPY, options: { x: M, y: H - 0.7, w: 6, h: 0.35, fontSize: 11, color: C.background1, fontFace: FONT, margin: 0 } } },
    ],
  });
  return { pres, C };
}

const T = (s, text, o) => s.addText(text, Object.assign({ isTextBox: true, fontFace: FONT, margin: 0, valign: "top" }, o));

async function cover(pres, title, sub, imgId, note) {
  const s = pres.addSlide({ masterName: "表紙" }); const C = pres.SchemeColor;
  T(s, title, { x: M, y: 1.8, w: 6.2, h: 2.4, fontSize: 40, bold: true, color: C.background1, valign: "bottom", objectName: "題名" });
  T(s, sub, { x: M, y: 4.45, w: 6.2, h: 1.2, fontSize: 18, color: C.background1, objectName: "日付と場所" });
  await pic(s, imgId, 7.6, 1.2, 5.2, 5.0);
  s.addNotes(note); return s;
}
function ending(pres, title, sub, note) {
  const s = pres.addSlide({ masterName: "終わり" }); const C = pres.SchemeColor;
  T(s, title, { x: M, y: 2.4, w: W - 2 * M, h: 1.4, fontSize: 40, bold: true, color: C.background1, align: "center", valign: "middle", objectName: "しめの言葉" });
  T(s, sub, { x: M, y: 3.9, w: W - 2 * M, h: 1.0, fontSize: 18, color: C.background1, align: "center", objectName: "連絡先" });
  s.addNotes(note); return s;
}
function page(pres, title, note) {
  const s = pres.addSlide({ masterName: "本文" }); const C = pres.SchemeColor;
  T(s, title, { x: M, y: 0.45, w: W - 2 * M, h: 0.85, fontSize: 32, bold: true, color: C.text2, valign: "middle", objectName: "見出し" });
  s.addNotes(note); return s;
}

// 丸数字の番号
function num(s, C, n, x, y, d = 0.55) {
  s.addShape("ellipse", { x, y, w: d, h: d, fill: { color: C.accent1 }, line: { color: C.accent1 }, objectName: "番号" + n });
  T(s, String(n), { x, y, w: d, h: d, fontSize: 18, bold: true, color: C.background1, align: "center", valign: "middle" });
}
// 横に並ぶ段（絵＋段の名前＋ひとこと）
async function steps(s, C, items, top = 1.7) {
  const n = items.length, gap = 0.35, cw = (W - 2 * M - gap * (n - 1)) / n;
  for (let i = 0; i < n; i++) {
    const [name, desc, img] = items[i], x = M + i * (cw + gap);
    s.addShape("roundRect", { x, y: top, w: cw, h: 4.6, rectRadius: 0.12, fill: { color: C.background2 }, line: { color: C.background2 }, objectName: "段の台" + (i + 1) });
    num(s, C, i + 1, x + 0.2, top + 0.2, 0.5);
    await pic(s, img, x + 0.15, top + 0.8, cw - 0.3, 1.9);
    T(s, name, { x: x + 0.2, y: top + 2.85, w: cw - 0.4, h: 0.5, fontSize: 18, bold: true, color: C.text2 });
    T(s, desc, { x: x + 0.2, y: top + 3.4, w: cw - 0.4, h: 1.1, fontSize: 14, color: C.text1 });
    if (i < n - 1) s.addShape("chevron", { x: x + cw + 0.08, y: top + 2.1, w: 0.2, h: 0.4, fill: { color: C.accent2 }, line: { color: C.accent2 }, objectName: "矢印" + (i + 1) });
  }
}
function table(s, C, head, rows, top = 1.7, colW) {
  const hdr = head.map((t) => ({ text: t, options: { bold: true, color: C.background1, fill: { color: C.accent1 } } }));
  const body = rows.map((r, i) => r.map((t, j) => ({ text: t, options: { fill: { color: i % 2 ? C.background1 : C.background2 }, bold: j === 0, color: j === 0 ? C.text2 : C.text1 } })));
  s.addTable([hdr, ...body], { x: M, y: top, w: W - 2 * M, colW, fontFace: FONT, fontSize: 15, rowH: 0.62, valign: "middle", margin: [0.08, 0.15, 0.08, 0.15], border: { type: "solid", pt: 0.75, color: "C5C9CF" } });
}
function cards(s, C, items, top = 1.7, h = 4.6) {
  const n = items.length, gap = 0.4, cw = (W - 2 * M - gap * (n - 1)) / n;
  items.forEach(([head, body], i) => {
    const x = M + i * (cw + gap);
    s.addShape("roundRect", { x, y: top, w: cw, h, rectRadius: 0.12, fill: { color: C.background2 }, line: { color: C.background2 }, objectName: "カード" + (i + 1) });
    T(s, head, { x: x + 0.3, y: top + 0.3, w: cw - 0.6, h: 0.9, fontSize: 20, bold: true, color: C.text2 });
    T(s, body, { x: x + 0.3, y: top + 1.25, w: cw - 0.6, h: h - 1.5, fontSize: 15, color: C.text1, paraSpaceAfter: 6 });
  });
}
const list = (arr) => arr.map((t, i) => ({ text: t, options: { breakLine: i < arr.length - 1 } }));

// ───────── 1 説明会 ─────────
async function setsumeikai() {
  const { pres, C } = setup("説明会のひな形");
  await cover(pres, "［説明会の名前］\n相続と登記の説明会", "［2026年◯月◯日（◯）◯時から］\n［会場の名前］", "kyoutsu-seminar-koushi",
    "表紙です。題名と日付と会場を差しかえます。右の絵は士業ストックの好きな絵に入れかえてかまいません。");

  let s = page(pres, "本日の流れ", "当日の時間割です。行が足りないときは、表の行を増やします。");
  table(s, C, ["時間", "内容", "話す人"], [
    ["［13:00］", "はじめのあいさつ", "［代表の名前］"],
    ["［13:10］", "［テーマ1］相続の手続きの全体", "［担当の名前］"],
    ["［13:40］", "［テーマ2］よくあるご相談の例", "［担当の名前］"],
    ["［14:10］", "質問の時間", "全員"],
    ["［14:30］", "個別のご相談（ご希望の方）", "全員"],
  ], 1.7, [2.2, 6.9, 3.03]);

  s = page(pres, "私たちについて", "グループの紹介です。事務所の数や資格に合わせて、カードを足したり減らしたりします。");
  T(s, "［グループの紹介を2行から3行で書きます］\n例）司法書士と土地家屋調査士と行政書士が\nひとつの窓口でご相談をお受けしています", { x: M, y: 1.6, w: W - 2 * M, h: 1.2, fontSize: 18, color: C.text1 });
  const pros = [["司法書士", "登記と相続の手続き", "shiho-shoshi-f"], ["土地家屋調査士", "土地と建物の調査と測量", "chousashi-shihoshoshi"], ["事務所のスタッフ", "受付と書類の準備", "shiho-hojosha"]];
  for (let i = 0; i < 3; i++) {
    const cw = (W - 2 * M - 0.8) / 3, x = M + i * (cw + 0.4);
    s.addShape("roundRect", { x, y: 3.0, w: cw, h: 3.6, rectRadius: 0.12, fill: { color: C.background2 }, line: { color: C.background2 }, objectName: "紹介" + (i + 1) });
    await pic(s, pros[i][2], x + 0.15, 3.2, 1.3, 2.4);
    T(s, pros[i][0], { x: x + 1.55, y: 3.6, w: cw - 1.7, h: 0.6, fontSize: 18, bold: true, color: C.text2, valign: "middle" });
    T(s, pros[i][1], { x: x + 1.55, y: 4.25, w: cw - 1.7, h: 1.2, fontSize: 15, color: C.text1 });
  }

  s = page(pres, "こんなときにご相談ください", "よくある相談を6つ並べるページです。絵と言葉を入れかえて使います。");
  const nayami = [["家族が\n亡くなって\n手続きが\n分からない", "kyoutsu-jikka-kazoku"], ["実家の土地や\n建物を\n整理したい", "chousashi-akiya"], ["遺言を\n残して\nおきたい", "shiho-souzoku-soudan"],
    ["会社を\n立ち上げたい", "shiho-kaisha-setsuritsu"], ["引っ越して\n住所が\n変わった", "shiho-juusho-henkou"], ["届いた手紙の\n意味が\n分からない", "kyoutsu-tegami-yomu"]];
  for (let i = 0; i < 6; i++) {
    const cw = (W - 2 * M - 0.8) / 3, ch = 2.45, x = M + (i % 3) * (cw + 0.4), y = 1.6 + Math.floor(i / 3) * (ch + 0.3);
    s.addShape("roundRect", { x, y, w: cw, h: ch, rectRadius: 0.12, fill: { color: C.background2 }, line: { color: C.background2 }, objectName: "相談" + (i + 1) });
    await pic(s, nayami[i][1], x + 0.15, y + 0.15, 1.6, ch - 0.3);
    T(s, nayami[i][0], { x: x + 1.9, y: y + 0.2, w: cw - 2.0, h: ch - 0.4, fontSize: 16, bold: true, color: C.text2, valign: "middle" });
  }

  s = page(pres, "ご依頼の流れ", "ご相談から完了までの5つの段です。段の数が違うときは、段の台と絵をまとめて消すか写して増やします。");
  await steps(s, C, [["ご相談", "お電話か窓口で\nお話をうかがいます", "shiho-uketsuke"], ["お見積もり", "必要な手続きと\n費用をご説明します", "chousashi-mitsumori-setsumei"],
    ["書類の準備", "戸籍などの書類を\nこちらで集めます", "shiho-koseki-atsume"], ["申請", "法務局へ\n申請します", "shiho-houmukyoku-shinsei"], ["完了", "完了の書類を\nお渡しします", "shiho-kanryou-watasu"]]);

  s = page(pres, "よくあるご質問", "質問と答えを3つ載せるページです。答えは短く2行までにします。");
  [["相談にお金はかかりますか", "［答えを書きます］"], ["どんな書類を持っていけばよいですか", "［答えを書きます］"], ["家族の代わりに相談できますか", "［答えを書きます］"]].forEach(([q, a], i) => {
    const y = 1.65 + i * 1.62;
    s.addShape("roundRect", { x: M, y, w: W - 2 * M, h: 1.4, rectRadius: 0.12, fill: { color: C.background2 }, line: { color: C.background2 }, objectName: "質問" + (i + 1) });
    T(s, "Q", { x: M + 0.3, y: y + 0.2, w: 0.6, h: 0.6, fontSize: 28, bold: true, color: C.accent2, valign: "middle" });
    T(s, q, { x: M + 1.0, y: y + 0.22, w: W - 2 * M - 1.4, h: 0.5, fontSize: 19, bold: true, color: C.text2, valign: "middle" });
    T(s, a, { x: M + 1.0, y: y + 0.78, w: W - 2 * M - 1.4, h: 0.5, fontSize: 15, color: C.text1, valign: "middle" });
  });

  s = page(pres, "ご相談の窓口", "連絡先のページです。電話番号と受付時間を差しかえます。");
  s.addShape("roundRect", { x: M, y: 1.7, w: 7.2, h: 4.6, rectRadius: 0.12, fill: { color: C.background2 }, line: { color: C.background2 }, objectName: "窓口" });
  T(s, list(["電話　［000-000-0000］", "受付　［平日 9時から17時まで］", "場所　［住所］", "担当　［名前］"]), { x: M + 0.4, y: 2.1, w: 6.4, h: 3.8, fontSize: 22, color: C.text1, paraSpaceAfter: 18 });
  await pic(s, "shiho-denwa", 8.2, 1.7, 4.5, 4.6);

  ending(pres, "ありがとうございました", "［事務所の名前］　［電話番号］", "しめのページです。");
  return save(pres, "01_説明会のひな形.pptx");
}

// ───────── 2 仕事の流れ ─────────
async function shigotoNoNagare() {
  const { pres, C } = setup("仕事の流れのひな形");
  await cover(pres, "［仕事の名前］の\n仕事の流れ", "［チームの名前］　［作った日］", "kyoutsu-renkei-kaigi", "表紙です。どの仕事の流れかを題名に入れます。");

  let s = page(pres, "［仕事の名前］の全体の流れ", "仕事の全体を5つの段で見せるページです。新人の方に最初に見せます。");
  await steps(s, C, [["受付", "電話と窓口で\n依頼を受ける", "shiho-uketsuke"], ["調査", "書類と現地を\n調べる", "shiho-koseki-atsume"], ["書類づくり", "申請の書類を\nつくる", "chousashi-shorui-taba"],
    ["申請", "役所へ\n申請する", "shiho-houmukyoku-shinsei"], ["完了の連絡", "お客さまに\nお渡しする", "shiho-kanryou-watasu"]]);

  s = page(pres, "段1　受付", "一つの段をくわしく書くページです。段の数だけ、このスライドを写して使います。");
  await pic(s, "shiho-uketsuke", M, 1.6, 5.4, 4.9);
  const rows = [["やること", "［例）依頼の内容を聞いて案件の台帳に入れる］"], ["受け持つ人", "［例）受付の担当］"], ["使う道具", "［例）案件の台帳と電話］"], ["目安の日数", "［例）当日］"], ["次の段へ渡すもの", "［例）聞き取りのメモ］"]];
  rows.forEach(([k, v], i) => {
    const y = 1.6 + i * 1.0;
    s.addShape("roundRect", { x: 6.4, y, w: W - M - 6.4, h: 0.85, rectRadius: 0.1, fill: { color: i % 2 ? C.background1 : C.background2 }, line: { color: C.background2 }, objectName: "項目" + (i + 1) });
    T(s, k, { x: 6.6, y, w: 2.2, h: 0.85, fontSize: 15, bold: true, color: C.text2, valign: "middle" });
    T(s, v, { x: 8.8, y, w: W - M - 9.0, h: 0.85, fontSize: 15, color: C.text1, valign: "middle" });
  });

  s = page(pres, "段ごとの受け持ち", "全部の段を一覧にした表です。誰がどの段を受け持つかを確かめるときに使います。");
  table(s, C, ["段", "受け持つ人", "使う道具", "目安の日数"], [
    ["受付", "［受付の担当］", "［案件の台帳］", "［当日］"], ["調査", "［担当］", "［ ］", "［ ］"], ["書類づくり", "［担当］", "［ ］", "［ ］"],
    ["申請", "［担当］", "［ ］", "［ ］"], ["完了の連絡", "［担当］", "［ ］", "［ ］"],
  ], 1.7, [2.6, 3.2, 3.6, 2.73]);

  s = page(pres, "つまずきやすいところ", "よく止まる所と、その手当てを3つ書きます。");
  cards(s, C, [["［例）書類が足りない］", "起きること\n［申請が止まる］\n\n手当て\n［受付で一覧表を渡す］"], ["［例）連絡が行き違う］", "起きること\n［同じことを二度聞く］\n\n手当て\n［連絡は案件ごとにまとめる］"], ["［例）担当が休み］", "起きること\n［進み具合が分からない］\n\n手当て\n［台帳に今の段を書く］"]]);

  s = page(pres, "段を終えるときの確かめ", "段を終えるときに見るチェック表です。項目を差しかえて使います。");
  const chk = ["［台帳に今の段を書いた］", "［お客さまに次の連絡日を伝えた］", "［書類を決まった棚に戻した］", "［次の担当にひとこと伝えた］", "［期限をカレンダーに入れた］"];
  chk.forEach((t, i) => {
    const y = 1.7 + i * 0.85;
    s.addShape("rect", { x: M + 0.1, y: y + 0.12, w: 0.4, h: 0.4, fill: { color: C.background1 }, line: { color: C.accent1, width: 1.5 }, objectName: "チェック欄" + (i + 1) });
    T(s, t, { x: M + 0.8, y, w: 6.6, h: 0.64, fontSize: 18, color: C.text1, valign: "middle" });
  });
  await pic(s, "chousashi-clipboard", 8.4, 1.7, 4.3, 4.6);

  ending(pres, "わからないときは聞いてください", "［相談する人の名前］　［連絡の方法］", "しめのページです。");
  return save(pres, "02_仕事の流れのひな形.pptx");
}

// ───────── 3 社内の連絡の流れ ─────────
async function renraku() {
  const { pres, C } = setup("社内の連絡の流れのひな形");
  await cover(pres, "社内の連絡の流れ", "［グループの名前］　［作った日］", "chousashi-asa-uchiawase", "表紙です。");

  let s = page(pres, "いまは連絡の道具が5つに分かれています", "いまの姿を見せるページです。道具の名前は実際に使っているものに差しかえます。");
  const tools = [["案件の管理", "［例）権システム］"], ["表計算", "［例）別のスプレッドシート］"], ["チャット", "［例）チャットワーク］"], ["電話", "［代表電話と携帯］"], ["メール", "［お客さまと役所］"]];
  const pos = [[1.0, 1.8], [5.0, 1.6], [9.1, 1.9], [2.6, 4.3], [7.4, 4.4]];
  tools.forEach(([h, b], i) => {
    const [x, y] = pos[i];
    s.addShape("roundRect", { x, y, w: 3.4, h: 1.7, rectRadius: 0.15, fill: { color: C.background2 }, line: { color: C.accent4 }, objectName: "道具" + (i + 1) });
    T(s, h, { x: x + 0.25, y: y + 0.25, w: 2.9, h: 0.5, fontSize: 20, bold: true, color: C.text2 });
    T(s, b, { x: x + 0.25, y: y + 0.85, w: 2.9, h: 0.6, fontSize: 15, color: C.text1 });
  });

  s = page(pres, "道具の使い分け", "どの話をどの道具でするかを決める表です。グループで決めた形に書きかえます。");
  table(s, C, ["道具", "使うとき", "返事の目安"], [
    ["案件の管理", "案件の進み具合と期限を書く", "［その日のうちに更新］"], ["チャット", "社内の相談と連絡", "［2時間以内］"], ["電話", "急ぎのときとお客さまから", "［その場で］"],
    ["メール", "お客さまや役所への書面", "［翌日まで］"], ["朝の打合せ", "今日の予定と困りごと", "［毎朝◯時］"],
  ], 1.7, [2.8, 6.0, 3.33]);

  s = page(pres, "報告の流れ", "誰から誰へ報告するかを見せる図です。役職と名前を差しかえます。");
  const lv = [["担当者", "案件を進める"], ["チームのリーダー", "まとめて確かめる"], ["代表", "大きな判断をする"]];
  lv.forEach(([h, b], i) => {
    const y = 1.6 + i * 1.7;
    s.addShape("roundRect", { x: M, y, w: 5.6, h: 1.25, rectRadius: 0.12, fill: { color: i === 2 ? C.accent1 : C.background2 }, line: { color: C.accent1 }, objectName: "報告" + (i + 1) });
    T(s, h, { x: M + 0.3, y, w: 2.6, h: 1.25, fontSize: 20, bold: true, color: i === 2 ? C.background1 : C.text2, valign: "middle" });
    T(s, b, { x: M + 3.0, y, w: 2.5, h: 1.25, fontSize: 15, color: i === 2 ? C.background1 : C.text1, valign: "middle" });
    if (i < 2) s.addShape("downArrow", { x: M + 2.55, y: y + 1.3, w: 0.5, h: 0.4, fill: { color: C.accent2 }, line: { color: C.accent2 }, objectName: "下向き矢印" + (i + 1) });
  });
  T(s, "迷ったら\nまずリーダーに\nひとこと", { x: 7.0, y: 1.8, w: 5.7, h: 1.6, fontSize: 24, bold: true, color: C.text2 });
  await pic(s, "kyoutsu-renkei-kaigi", 7.0, 3.5, 5.7, 3.1);

  s = page(pres, "1日の連絡のリズム", "1日のうち、いつ何を伝えるかを決めるページです。時刻と中身を書きかえます。");
  const day = [["［9:00］", "朝の打合せ", "今日の予定と\n困りごとを出す"], ["［12:00］", "昼の確かめ", "急ぎの案件だけ\nチャットで伝える"], ["［17:30］", "夕方の報告", "今日進んだことを\n案件の管理に書く"]];
  s.addShape("line", { x: M + 0.4, y: 2.45, w: W - 2 * M - 0.8, h: 0, line: { color: C.accent4, width: 2 }, objectName: "時の線" });
  day.forEach(([t, h, b], i) => {
    const cw = (W - 2 * M - 0.8) / 3, x = M + i * (cw + 0.4);
    s.addShape("ellipse", { x: x + cw / 2 - 0.2, y: 2.25, w: 0.4, h: 0.4, fill: { color: C.accent2 }, line: { color: C.accent2 }, objectName: "時刻の点" + (i + 1) });
    T(s, t, { x, y: 1.6, w: cw, h: 0.5, fontSize: 20, bold: true, color: C.text2, align: "center" });
    s.addShape("roundRect", { x, y: 3.0, w: cw, h: 3.4, rectRadius: 0.12, fill: { color: C.background2 }, line: { color: C.background2 }, objectName: "時刻の台" + (i + 1) });
    T(s, h, { x: x + 0.3, y: 3.3, w: cw - 0.6, h: 0.6, fontSize: 20, bold: true, color: C.text2 });
    T(s, b, { x: x + 0.3, y: 4.0, w: cw - 0.6, h: 1.6, fontSize: 16, color: C.text1 });
  });

  s = page(pres, "案件の情報を一本につなぐ", "受付から入金の確認までを一本の流れにした図です。前岡さんとの話で出た形です。");
  const flow = [["案件の管理", "受付で\n一度だけ入れる"], ["チャット", "案件ごとに\n話をまとめる"], ["お客さまへの連絡", "決まった文面で\n知らせる"], ["請求", "案件から\n請求書をつくる"], ["入金の確認", "確かめて\n案件を閉じる"]];
  const fw = (W - 2 * M - 4 * 0.35) / 5;
  flow.forEach(([h, b], i) => {
    const x = M + i * (fw + 0.35);
    s.addShape("roundRect", { x, y: 2.2, w: fw, h: 3.0, rectRadius: 0.12, fill: { color: i === 0 ? C.accent1 : C.background2 }, line: { color: C.accent1 }, objectName: "つなぎ" + (i + 1) });
    num(s, C, i + 1, x + fw / 2 - 0.27, 1.55);
    T(s, h, { x: x + 0.1, y: 2.5, w: fw - 0.2, h: 0.9, fontSize: 16, bold: true, color: i === 0 ? C.background1 : C.text2, align: "center", valign: "middle" });
    T(s, b, { x: x + 0.2, y: 3.5, w: fw - 0.4, h: 1.4, fontSize: 15, color: i === 0 ? C.background1 : C.text1, align: "center" });
    if (i < 4) s.addShape("chevron", { x: x + fw + 0.08, y: 3.5, w: 0.2, h: 0.4, fill: { color: C.accent2 }, line: { color: C.accent2 }, objectName: "矢印" + (i + 1) });
  });
  T(s, "入力は一度だけにして　あとは同じ情報を使い回します", { x: M, y: 5.6, w: W - 2 * M, h: 0.6, fontSize: 18, bold: true, color: C.text2, align: "center" });

  s = page(pres, "連絡の決まり", "グループで決めた連絡の決まりを5つまで書きます。");
  const rules = ["［案件の話はその案件の場所に書く］", "［お客さまの名前は略さない］", "［急ぎは電話　そうでなければチャット］", "［休む日は前の日までに伝える］", "［分からないことは30分で聞く］"];
  rules.forEach((t, i) => { const y = 1.7 + i * 0.95; num(s, C, i + 1, M, y); T(s, t, { x: M + 0.85, y, w: 7.0, h: 0.55, fontSize: 19, color: C.text1, valign: "middle" }); });
  await pic(s, "chousashi-denwa", 8.6, 1.9, 4.1, 4.2);

  ending(pres, "困ったら声をかけてください", "［相談する人の名前］", "しめのページです。");
  return save(pres, "03_社内の連絡の流れのひな形.pptx");
}

async function save(pres, name) {
  const f = path.join(OUT, name);
  await pres.writeFile({ fileName: f }); await applyTheme(f, THEME); console.log("書き出し", name); return f;
}
(async () => { fs.mkdirSync(OUT, { recursive: true }); await setsumeikai(); await shigotoNoNagare(); await renraku(); })();
