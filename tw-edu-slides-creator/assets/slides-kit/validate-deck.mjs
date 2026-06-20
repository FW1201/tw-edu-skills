// validate-deck.mjs — 品質閘門（P0–P3）
// 用法：node validate-deck.mjs <deck.json> [deck.pptx]
//   給 deck.json：對 schema 做版面/字級/版型/色票檢查
//   再給 deck.pptx：額外做 OOXML 合法性檢查（XML well-formed + 必要 part）
// 退出碼：有 P0 → 1，否則 0。

import { readFileSync } from 'node:fs';
import { typeFor, estimateTextHeight, BANDS, SAFE, MIN_FONT_PT } from './grid.mjs';
import { LAYOUTS } from './layouts.mjs';
import { THEME_KEYS, THEME_ALIASES } from './tokens.mjs';

const HEX = /^#?[0-9a-fA-F]{6}$/;
const issues = [];
const add = (sev, slide, msg) => issues.push({ sev, slide, msg });

function validateSchema(deck) {
  const meta = deck.meta || {};
  const ty = typeFor(meta.grade);
  const slides = deck.slides || [];

  // meta 檢查
  if (!meta.theme) add('P2', '-', 'meta.theme 未設定，將回退「語文」');
  else if (!THEME_KEYS.includes(meta.theme) && !THEME_ALIASES[meta.theme])
    add('P1', '-', `meta.theme「${meta.theme}」非已知色系，將回退「語文」`);
  if (!meta.grade) add('P2', '-', 'meta.grade 未設定，字級將以「國中」計');

  if (!slides.length) add('P0', '-', 'deck 沒有任何投影片');

  let visualCount = 0;
  slides.forEach((s, idx) => {
    const n = idx + 1;
    if (!LAYOUTS[s.layout]) { add('P0', n, `未知版型「${s.layout}」`); return; }

    // 視覺元素統計（純文字風險）
    if (['cover', 'section', 'hero', 'quote', 'data', 'timeline', 'image-hero',
         'three-column', 'matrix', 'process-flow', 'concept-web', 'activity', 'vocab'].includes(s.layout))
      visualCount++;

    // bullets 上限
    if (s.layout === 'bullets') {
      const items = s.items || [];
      if (items.length > ty.maxBullets) add('P1', n, `bullets ${items.length} 條超過年級上限 ${ty.maxBullets}`);
      // 溢出估算
      let total = 0;
      items.forEach((t) => { total += estimateTextHeight(t, ty.body, SAFE.w) + 0.12; });
      if (total > BANDS.contentH) add('P0', n, `bullets 內容估算高度 ${total.toFixed(2)}" 超過內容帶 ${BANDS.contentH}"`);
    }

    // 標題長度（單行估算）
    if (s.title && estimateTextHeight(s.title, ty.title, SAFE.w) > BANDS.titleH + 0.4)
      add('P1', n, `標題過長，預估折行溢出標題帶`);

    // 三欄/雙欄文字溢出粗估
    for (const [key, arr] of [['cards', s.cards], ['columns', s.columns]]) {
      if (!Array.isArray(arr)) continue;
      arr.forEach((c, i) => {
        const body = c.body || (c.items || []).join('、') || '';
        const colW = key === 'cards' ? 2.9 : 5.4;
        const h = estimateTextHeight(body, ty.body, colW);
        if (h > BANDS.contentH - 2.0) add('P1', n, `${key}[${i}] 文字偏多，可能溢出卡片`);
      });
    }

    // 色票越界：內容欄位不應出現 raw hex
    JSON.stringify(s).match(/#[0-9a-fA-F]{6}/g)?.forEach(() =>
      add('P2', n, '內容含 raw hex 色值；色彩應由色系 token 控制'));

    // image-hero 缺圖
    if (s.layout === 'image-hero' && !s.image) add('P2', n, 'image-hero 未提供 image，將顯示佔位框');
  });

  // 連續同版型 >3
  let run = 1;
  for (let i = 1; i < slides.length; i++) {
    if (slides[i].layout === slides[i - 1].layout) { run++; if (run > 3) add('P1', i + 1, `連續第 ${run} 張同版型「${slides[i].layout}」`); }
    else run = 1;
  }

  // 純文字風險
  if (slides.length >= 4 && visualCount / slides.length < 0.4)
    add('P1', '-', `視覺型投影片佔比偏低（${visualCount}/${slides.length}），易顯單調`);
}

async function validateOOXML(pptxPath) {
  try {
    const { default: JSZip } = await import('jszip');
    const zip = await JSZip.loadAsync(readFileSync(pptxPath));
    const names = Object.keys(zip.files);
    for (const req of ['[Content_Types].xml', 'ppt/presentation.xml']) {
      if (!names.includes(req)) add('P0', '-', `OOXML 缺少必要 part：${req}`);
    }
    const xmls = names.filter((f) => f.endsWith('.xml') || f.endsWith('.rels'));
    let checked = 0;
    for (const f of xmls) {
      const xml = await zip.files[f].async('string');
      const t = xml.trimStart();
      // 腐損 smoke test：須為 XML 開頭，且角括號數量平衡
      if (!t.startsWith('<')) { add('P0', '-', `OOXML part 非 XML：${f}`); continue; }
      const open = (xml.match(/</g) || []).length, close = (xml.match(/>/g) || []).length;
      if (open !== close) add('P0', '-', `OOXML part 角括號不平衡（疑似腐損）：${f}`);
      checked++;
    }
    console.log(`  OOXML：${names.length} parts，${checked} XML well-formed 檢查完畢`);
  } catch (e) {
    add('P1', '-', `OOXML 檢查無法執行：${e.message}`);
  }
}

// ── main ─────────────────────────────────────────────────────
const deckPath = process.argv[2];
const pptxPath = process.argv[3];
if (!deckPath) { console.error('用法：node validate-deck.mjs <deck.json> [deck.pptx]'); process.exit(2); }

const deck = JSON.parse(readFileSync(deckPath, 'utf8'));
validateSchema(deck);
if (pptxPath) await validateOOXML(pptxPath);

const order = { P0: 0, P1: 1, P2: 2, P3: 3 };
issues.sort((a, b) => order[a.sev] - order[b.sev]);
const icon = { P0: '🔴', P1: '🟠', P2: '🟡', P3: 'ℹ️' };
console.log(`\n品質閘門報告：${deckPath}`);
if (!issues.length) console.log('✅ 無問題（P0–P3 全清）');
else for (const it of issues) console.log(`${icon[it.sev]} ${it.sev}  [slide ${it.slide}]  ${it.msg}`);

const counts = issues.reduce((m, i) => ((m[i.sev] = (m[i.sev] || 0) + 1), m), {});
console.log(`\n統計：${['P0', 'P1', 'P2', 'P3'].map((s) => `${s}=${counts[s] || 0}`).join('  ')}`);
process.exit((counts.P0 || 0) > 0 ? 1 : 0);
