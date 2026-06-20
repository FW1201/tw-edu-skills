// build.mjs — 投影片結構 schema → 原生 .pptx
// 用法：node build.mjs <deck.json> [out.pptx]
// deck.json 結構見 references/pptx-layout-templates.md 與 examples/。

import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import PptxGenJS from 'pptxgenjs';
import { getTheme } from './tokens.mjs';
import { defineMasters, DARK_LAYOUTS } from './masters.mjs';
import { LAYOUTS } from './layouts.mjs';
import { typeFor } from './grid.mjs';

/** hex 線性混合 a→b，t∈[0,1] */
function mix(a, b, t) {
  const pa = [0, 2, 4].map((i) => parseInt(a.slice(i, i + 2), 16));
  const pb = [0, 2, 4].map((i) => parseInt(b.slice(i, i + 2), 16));
  return pa.map((v, i) => Math.round(v + (pb[i] - v) * t).toString(16).padStart(2, '0')).join('').toUpperCase();
}

/** 依 tone 解析出 renderer 用的色票 */
function resolvePalette(theme, tone) {
  if (tone === 'dark') {
    const d = theme.dark;
    return {
      bg: d.bg, text: d.text, primary: d.primary, secondary: theme.secondary,
      accent: d.accent, onPrimary: d.onPrimary,
      surface: mix(d.bg, d.text, 0.09), muted: mix(d.bg, d.text, 0.55),
    };
  }
  return {
    bg: theme.bg, text: theme.text, primary: theme.primary, secondary: theme.secondary,
    accent: theme.accent, onPrimary: theme.onPrimary, surface: theme.surface, muted: theme.muted,
  };
}

export async function build(deck, outPath = 'deck.pptx') {
  const meta = deck.meta || {};
  const theme = getTheme(meta.theme);
  const ty = typeFor(meta.grade);

  const pptx = new PptxGenJS();
  pptx.defineLayout({ name: 'WIDE', width: 13.333, height: 7.5 });
  pptx.layout = 'WIDE';
  pptx.author = meta.instructor || '';
  pptx.title = meta.course || '';
  // 標題字型透過 theme.headingFont（PptxGenJS 無全域 headingFont，renderer 已指定 fontFace）

  defineMasters(pptx, theme, meta.course || '');

  for (const s of (deck.slides || [])) {
    const renderer = LAYOUTS[s.layout];
    if (!renderer) { console.warn(`⚠ 未知版型：${s.layout}，跳過`); continue; }
    const tone = s.tone || (DARK_LAYOUTS.has(s.layout) ? 'dark' : 'light');
    const masterName = tone === 'dark' ? 'DARK' : 'LIGHT';
    const slide = pptx.addSlide({ masterName });
    const pal = resolvePalette(theme, tone);
    const ctx = { theme, pal, ty, isDark: tone === 'dark', meta };
    renderer(slide, pptx, s, ctx);
    if (s.notes) slide.addNotes(String(s.notes));
  }

  await pptx.writeFile({ fileName: outPath });
  return outPath;
}

// CLI
if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const deckPath = process.argv[2];
  const out = process.argv[3] || 'deck.pptx';
  if (!deckPath) { console.error('用法：node build.mjs <deck.json> [out.pptx]'); process.exit(1); }
  const deck = JSON.parse(readFileSync(deckPath, 'utf8'));
  build(deck, out).then((p) => console.log(`✅ 已輸出 ${p}（${(deck.slides || []).length} 張）`))
    .catch((e) => { console.error('❌ build 失敗：', e.message); process.exit(1); });
}
