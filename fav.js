// お気に入り（このブラウザだけに残る。ほかの人やほかの端末には出ない）
const FAV_KEY = "shigyo-fav";
function favLoad() { try { return new Set(JSON.parse(localStorage.getItem(FAV_KEY) || "[]")); } catch (e) { return new Set(); } }
function favSave(s) { try { localStorage.setItem(FAV_KEY, JSON.stringify([...s])); } catch (e) {} }
function favHas(id) { return favLoad().has(id); }
function favToggle(id) { const s = favLoad(); s.has(id) ? s.delete(id) : s.add(id); favSave(s); return s.has(id); }
function favLabel(on) { return on ? "★ お気に入り" : "☆ お気に入りに入れる"; }
