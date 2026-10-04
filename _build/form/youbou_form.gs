/**
 * 士業ストックの要望フォーム（2026-10-04）
 * 新しいスプレッドシートの「拡張機能」→「Apps Script」に、この中身を全部はり付けて使います。
 *
 * 使う順番
 *   1  setup を1回だけ動かす（フォームを作り、回答をこの表に集め、届いたらメールで知らせる）
 *   2  実行ログに出た「送る場所」のURLを、Claudeに伝える（サイトの「要望を送る」ページに入れます）
 */
const FORM_TITLE = '士業ストックへの要望';
const TZ = 'Asia/Tokyo';
const KINDS = ['ほしい絵', '絵の直し', 'スライドのひな形', 'サイトの使い方', 'そのほか'];
const SCENES = ['説明会', 'ホームページ', 'チラシ', '依頼した方への説明の紙', '社内の資料', '採用', '社内のイベント', 'そのほか'];

function setup() {
  const ss = SpreadsheetApp.getActive();
  ss.setSpreadsheetTimeZone(TZ);
  ss.setSpreadsheetLocale('ja_JP');

  const form = FormApp.create(FORM_TITLE);
  form.setDescription('ほしい絵、直してほしい絵、ほしいスライドのひな形などを書いてください。一言でもかまいません。\n© 石山通りグループ');
  form.setCollectEmail(false);
  form.setLimitOneResponsePerUser(false);
  form.setConfirmationMessage('受け取りました。順に対応します。');

  form.addMultipleChoiceItem().setTitle('要望の種類').setChoiceValues(KINDS).setRequired(true);
  form.addParagraphTextItem().setTitle('要望の中身')
    .setHelpText('例）相続の説明会で使う、家族が集まって話し合う絵がほしい／この絵の手の形を直してほしい')
    .setRequired(true);
  form.addCheckboxItem().setTitle('使う場面').setChoiceValues(SCENES).setRequired(false);
  form.addTextItem().setTitle('直してほしい絵のページのURL（絵の直しのときだけ）').setRequired(false);
  form.addDateItem().setTitle('いつまでにほしいか（決まっていれば）').setRequired(false);
  form.addTextItem().setTitle('お名前（任意）').setRequired(false);
  form.addTextItem().setTitle('事務所やチームの名前（任意）').setRequired(false);

  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());
  ScriptApp.newTrigger('notify').forForm(form).onFormSubmit().create();

  Logger.log('フォームを直す場所：' + form.getEditUrl());
  Logger.log('送る場所（サイトに入れるURL）：' + form.getPublishedUrl());
}

/** 要望が届いたら、このスクリプトを動かした人にメールで知らせます。 */
function notify(e) {
  const lines = e.response.getItemResponses().map(r => {
    const v = r.getResponse();
    return '■ ' + r.getItem().getTitle() + '\n' + (Array.isArray(v) ? v.join('、') : v);
  });
  MailApp.sendEmail(Session.getEffectiveUser().getEmail(), '【士業ストック】要望が届きました', lines.join('\n\n'));
}
