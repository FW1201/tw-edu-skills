// layouts.mjs — 版型渲染器（schema → PptxGenJS 原生元素）v3.1 視覺升級
// 每個 renderer: (slide, pptx, data, ctx) => void
// ctx = { theme, pal, ty, isDark, meta }
// 全部座標取自 grid.mjs 常數，顏色取自 ctx.pal（已依 light/dark 解析），不得 hardcode。
// 設計語言：左側品牌軌（master）＋ kicker 前導色塊 ＋ 卡片頂部 accent bar ＋ 陰影 ＋ 數字徽章。

import { SAFE, BANDS, GRID, SPACE, LINE, FONT } from './grid.mjs';

const HEAD = FONT.body;

// ── 共用視覺工具 ─────────────────────────────────────────────
const sh = (ctx) => ctx.isDark
  ? { type: 'outer', color: '000000', blur: 9, offset: 3, angle: 90, opacity: 0.5 }
  : { type: 'outer', color: '404040', blur: 7, offset: 3, angle: 90, opacity: 0.22 };

/** 標題帶：kicker 前導色塊 + 大標題（標題下絕不加線） */
function header(slide, ctx, kickerText, titleText, titleColor) {
  if (kickerText) {
    slide.addShape('rect', { x: SAFE.x, y: BANDS.titleY + 0.1, w: 0.09, h: 0.32,
      fill: { color: ctx.pal.primary }, line: { type: 'none' } });
    slide.addText(String(kickerText).toUpperCase(), { x: SAFE.x + 0.22, y: BANDS.titleY + 0.02, w: SAFE.w - 0.3, h: 0.45,
      fontSize: ctx.ty.small, bold: true, color: ctx.pal.primary, charSpacing: 2, fontFace: HEAD, align: 'left', valign: 'middle' });
  }
  if (titleText !== undefined) slide.addText(titleText || '', { x: SAFE.x, y: BANDS.titleY + 0.5, w: SAFE.w, h: BANDS.titleH - 0.42,
    fontSize: ctx.ty.title, bold: true, color: titleColor || ctx.pal.text, fontFace: HEAD, align: 'left', valign: 'bottom', lineSpacingMultiple: LINE.title });
}

/** 卡片：圓角面 + 頂部 accent bar + 陰影 */
function accentCard(slide, ctx, x, y, w, h, bar) {
  slide.addShape('roundRect', { x, y, w, h, rectRadius: 0.08, fill: { color: ctx.pal.surface }, line: { type: 'none' }, shadow: sh(ctx) });
  slide.addShape('rect', { x: x + 0.001, y, w, h: 0.085, fill: { color: bar || ctx.pal.primary }, line: { type: 'none' } });
}
/** 純面卡片（無 accent bar） */
function plainCard(slide, ctx, x, y, w, h, fill) {
  slide.addShape('roundRect', { x, y, w, h, rectRadius: 0.08, fill: { color: fill || ctx.pal.surface }, line: { type: 'none' }, shadow: sh(ctx) });
}
/** 數字圓徽章 */
function numBadge(slide, ctx, x, y, d, n, fill, txt) {
  slide.addShape('ellipse', { x, y, w: d, h: d, fill: { color: fill || ctx.pal.primary }, line: { type: 'none' } });
  slide.addText(String(n), { x, y, w: d, h: d, fontSize: ctx.ty.body, bold: true, color: txt || ctx.pal.onPrimary, fontFace: HEAD, align: 'center', valign: 'middle' });
}
/** 膠囊標籤 */
function pill(slide, ctx, x, y, w, h, text, fill, txt) {
  slide.addShape('roundRect', { x, y, w, h, rectRadius: h / 2, fill: { color: fill }, line: { type: 'none' } });
  slide.addText(text, { x, y, w, h, fontSize: ctx.ty.small - 2, bold: true, color: txt, fontFace: HEAD, align: 'center', valign: 'middle' });
}

// ── 版型 ─────────────────────────────────────────────────────

export function cover(slide, pptx, d, ctx) {
  // 右下大色塊 + 點綴方塊（primary 視覺主導）
  slide.addShape('roundRect', { x: 9.7, y: 3.4, w: 3.1, h: 3.3, rectRadius: 0.18, fill: { color: ctx.pal.primary }, line: { type: 'none' } });
  slide.addShape('roundRect', { x: 8.5, y: 1.0, w: 1.15, h: 1.15, rectRadius: 0.14, fill: { color: ctx.pal.accent }, line: { type: 'none' } });
  // 文字
  slide.addShape('rect', { x: SAFE.x, y: 1.62, w: 0.55, h: 0.1, fill: { color: ctx.pal.primary }, line: { type: 'none' } });
  slide.addText(String(d.subject || ctx.meta.course || '').toUpperCase(), { x: SAFE.x, y: 1.8, w: 8.2, h: 0.5,
    fontSize: ctx.ty.small + 1, bold: true, color: ctx.pal.primary, charSpacing: 3, fontFace: HEAD, align: 'left' });
  slide.addText(d.title || ctx.meta.course || '', { x: SAFE.x, y: 2.45, w: 8.6, h: 2.7,
    fontSize: ctx.ty.title + 14, bold: true, color: ctx.pal.text, fontFace: HEAD, align: 'left', valign: 'top', lineSpacingMultiple: LINE.title });
  const meta = [d.instructor || ctx.meta.instructor, d.date || ctx.meta.date].filter(Boolean).join('　｜　');
  slide.addText(meta, { x: SAFE.x, y: 5.7, w: 8.2, h: 0.6, fontSize: ctx.ty.body, color: ctx.pal.muted, fontFace: HEAD, align: 'left' });
}

export function section(slide, pptx, d, ctx) {
  slide.addText(String(d.number || '').padStart(2, '0'), { x: 6.0, y: 0.4, w: 7.0, h: 7.0, fontSize: 360, bold: true,
    color: ctx.pal.primary, transparency: 82, fontFace: HEAD, align: 'right', valign: 'middle' });
  slide.addShape('rect', { x: SAFE.x, y: 3.05, w: 0.6, h: 0.12, fill: { color: ctx.pal.primary }, line: { type: 'none' } });
  slide.addText(String(d.kicker || '章節').toUpperCase(), { x: SAFE.x, y: 3.25, w: 8, h: 0.5,
    fontSize: ctx.ty.small + 1, bold: true, color: ctx.pal.primary, charSpacing: 3, fontFace: HEAD });
  slide.addText(d.title || '', { x: SAFE.x, y: 3.8, w: 8.5, h: 1.6, fontSize: ctx.ty.title + 6, bold: true,
    color: ctx.pal.text, fontFace: HEAD, align: 'left', valign: 'top', lineSpacingMultiple: LINE.title });
}

export function objectives(slide, pptx, d, ctx) {
  header(slide, ctx, d.kicker || 'OBJECTIVES', d.title || '學習目標');
  const items = (d.items || []).slice(0, 3);
  const bars = [ctx.pal.primary, ctx.pal.secondary, ctx.pal.accent];
  const n = Math.max(items.length, 1);
  for (let i = 0; i < n; i++) {
    const { x, w } = GRID.span(1 + i * 4, 4);
    const it = items[i] || {};
    accentCard(slide, ctx, x, BANDS.contentY, w, BANDS.contentH, bars[i]);
    numBadge(slide, ctx, x + 0.3, BANDS.contentY + 0.35, 0.7, i + 1, bars[i]);
    slide.addText(it.kind || '', { x: x + 0.3, y: BANDS.contentY + 1.25, w: w - 0.6, h: 0.6,
      fontSize: ctx.ty.h2, bold: true, color: bars[i], fontFace: HEAD, align: 'left' });
    slide.addText(it.text || '', { x: x + 0.3, y: BANDS.contentY + 1.95, w: w - 0.6, h: BANDS.contentH - 2.2,
      fontSize: ctx.ty.body, color: ctx.pal.text, fontFace: HEAD, align: 'left', valign: 'top', lineSpacingMultiple: LINE.body });
  }
}

export function bullets(slide, pptx, d, ctx) {
  header(slide, ctx, d.kicker, d.title || '');
  const items = (d.items || []).slice(0, ctx.ty.maxBullets);
  const rh = Math.min(0.95, BANDS.contentH / Math.max(items.length, 1));
  const d0 = Math.min(0.6, rh - 0.2);
  items.forEach((t, i) => {
    const y = BANDS.contentY + i * rh;
    numBadge(slide, ctx, SAFE.x, y + (rh - d0) / 2, d0, String(i + 1).padStart(2, '0'));
    slide.addText(String(t), { x: SAFE.x + d0 + 0.35, y, w: SAFE.w - d0 - 0.35, h: rh,
      fontSize: ctx.ty.body, color: ctx.pal.text, fontFace: HEAD, valign: 'middle', lineSpacingMultiple: LINE.body });
  });
}

export function twoColumn(slide, pptx, d, ctx) {
  header(slide, ctx, d.kicker, d.title || '');
  const cols = (d.columns || []).slice(0, 2);
  const bars = [ctx.pal.primary, ctx.pal.secondary];
  for (let i = 0; i < 2; i++) {
    const { x, w } = GRID.span(1 + i * 6, 6);
    const c = cols[i] || {};
    plainCard(slide, ctx, x, BANDS.contentY, w, BANDS.contentH);
    slide.addShape('roundRect', { x, y: BANDS.contentY, w, h: 0.85, rectRadius: 0.08, fill: { color: bars[i] }, line: { type: 'none' } });
    slide.addShape('rect', { x, y: BANDS.contentY + 0.42, w, h: 0.43, fill: { color: bars[i] }, line: { type: 'none' } });
    slide.addText(c.heading || '', { x: x + 0.3, y: BANDS.contentY, w: w - 0.6, h: 0.85,
      fontSize: ctx.ty.h2, bold: true, color: ctx.pal.onPrimary, fontFace: HEAD, valign: 'middle' });
    slide.addText((c.items || []).map((t) => ({ text: String(t), options: { bullet: { code: '2022', indent: 16 }, paraSpaceAfter: 10 } })), {
      x: x + 0.3, y: BANDS.contentY + 1.1, w: w - 0.6, h: BANDS.contentH - 1.35,
      fontSize: ctx.ty.body, color: ctx.pal.text, fontFace: HEAD, valign: 'top', lineSpacingMultiple: LINE.body });
  }
}

export function vocab(slide, pptx, d, ctx) {
  header(slide, ctx, d.kicker || 'VOCABULARY', d.title || '詞彙');
  const items = (d.items || []).slice(0, 6);
  const cw = GRID.span(1, 4).w, gap = SPACE.md;
  const ch = (BANDS.contentH - gap) / 2;
  const bars = [ctx.pal.primary, ctx.pal.secondary, ctx.pal.accent];
  items.forEach((it, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const { x } = GRID.span(1 + col * 4, 4);
    const y = BANDS.contentY + row * (ch + gap);
    accentCard(slide, ctx, x, y, cw, ch, bars[col]);
    slide.addText(it.word || '', { x: x + 0.28, y: y + 0.3, w: cw - 0.56, h: 0.7,
      fontSize: ctx.ty.h2, bold: true, color: ctx.pal.text, fontFace: HEAD });
    if (it.zhuyin) pill(slide, ctx, x + 0.28, y + 1.05, Math.min(cw - 0.56, 2.4), 0.42, it.zhuyin, bars[col], ctx.pal.onPrimary);
    slide.addText(it.def || '', { x: x + 0.28, y: y + (it.zhuyin ? 1.6 : 1.05), w: cw - 0.56, h: ch - (it.zhuyin ? 1.75 : 1.2),
      fontSize: ctx.ty.small, color: ctx.pal.muted, fontFace: HEAD, valign: 'top', lineSpacingMultiple: LINE.body });
  });
}

export function activity(slide, pptx, d, ctx) {
  header(slide, ctx, d.kicker || 'ACTIVITY', d.title || '課堂活動');
  let px = SAFE.x + SAFE.w;
  if (d.group) { px -= 1.7; pill(slide, ctx, px, BANDS.titleY + 0.1, 1.6, 0.42, `👥 ${d.group}`, ctx.pal.secondary, ctx.pal.onPrimary); }
  if (d.time) { px -= 1.7; pill(slide, ctx, px, BANDS.titleY + 0.1, 1.6, 0.42, `⏱ ${d.time}`, ctx.pal.primary, ctx.pal.onPrimary); }
  const steps = (d.steps || []).slice(0, 5);
  const rh = BANDS.contentH / Math.max(steps.length, 1);
  steps.forEach((s, i) => {
    const y = BANDS.contentY + i * rh;
    plainCard(slide, ctx, SAFE.x, y + 0.04, SAFE.w, rh - 0.16);
    numBadge(slide, ctx, SAFE.x + 0.25, y + rh / 2 - 0.32, 0.6, i + 1);
    slide.addText(String(s), { x: SAFE.x + 1.1, y: y + 0.04, w: SAFE.w - 1.3, h: rh - 0.16,
      fontSize: ctx.ty.body, color: ctx.pal.text, fontFace: HEAD, valign: 'middle', lineSpacingMultiple: LINE.body });
  });
}

export function discussion(slide, pptx, d, ctx) {
  slide.addText('?', { x: 9.5, y: 0.3, w: 4.0, h: 5.0, fontSize: 380, bold: true, color: ctx.pal.primary, transparency: 86, fontFace: HEAD, align: 'right', valign: 'top' });
  slide.addShape('rect', { x: SAFE.x, y: 1.7, w: 0.6, h: 0.12, fill: { color: ctx.pal.primary }, line: { type: 'none' } });
  slide.addText(String(d.kicker || '討論').toUpperCase(), { x: SAFE.x, y: 1.9, w: 8, h: 0.5, fontSize: ctx.ty.small + 1, bold: true, color: ctx.pal.primary, charSpacing: 3, fontFace: HEAD });
  slide.addText(d.question || d.title || '', { x: SAFE.x, y: 2.5, w: 10.5, h: 2.6,
    fontSize: ctx.ty.title, bold: true, color: ctx.pal.text, fontFace: HEAD, align: 'left', valign: 'top', lineSpacingMultiple: LINE.title });
  if (d.thinkTime) pill(slide, ctx, SAFE.x, 5.55, 3.0, 0.5, `💭 思考時間 ${d.thinkTime}`, ctx.pal.secondary, ctx.pal.onPrimary);
}

export function hero(slide, pptx, d, ctx) {
  slide.background = { color: ctx.pal.primary };
  const onP = ctx.pal.onPrimary;
  slide.addShape('rect', { x: SAFE.x + SAFE.w / 2 - 0.4, y: 2.0, w: 0.8, h: 0.1, fill: { color: onP }, line: { type: 'none' } });
  if (d.kicker) slide.addText(String(d.kicker).toUpperCase(), { x: SAFE.x, y: 2.25, w: SAFE.w, h: 0.5,
    fontSize: ctx.ty.small, color: onP, transparency: 10, charSpacing: 4, bold: true, fontFace: HEAD, align: 'center' });
  slide.addText(d.text || d.title || '', { x: SAFE.x, y: 2.85, w: SAFE.w, h: 2.2,
    fontSize: ctx.ty.title + 12, bold: true, color: onP, fontFace: HEAD, align: 'center', valign: 'middle', lineSpacingMultiple: LINE.title });
}

export function data(slide, pptx, d, ctx) {
  header(slide, ctx, d.kicker || 'DATA', d.title || '');
  const stats = (d.stats || []).slice(0, 4);
  const bars = [ctx.pal.primary, ctx.pal.secondary, ctx.pal.accent, ctx.pal.primary];
  const n = Math.max(stats.length, 1);
  const span = Math.floor(12 / n);
  stats.forEach((s, i) => {
    const { x, w } = GRID.span(1 + i * span, span);
    accentCard(slide, ctx, x, BANDS.contentY, w, BANDS.contentH, bars[i]);
    slide.addText(String(s.value || ''), { x: x + 0.15, y: BANDS.contentY + 0.5, w: w - 0.3, h: 1.7,
      fontSize: ctx.ty.title + 10, bold: true, color: bars[i], fontFace: HEAD, align: 'center', valign: 'middle' });
    slide.addText(s.label || '', { x: x + 0.15, y: BANDS.contentY + 2.3, w: w - 0.3, h: 0.6,
      fontSize: ctx.ty.h2 - 4, bold: true, color: ctx.pal.text, fontFace: HEAD, align: 'center' });
    if (s.desc) slide.addText(s.desc, { x: x + 0.25, y: BANDS.contentY + 2.95, w: w - 0.5, h: BANDS.contentH - 3.1,
      fontSize: ctx.ty.small, color: ctx.pal.muted, fontFace: HEAD, align: 'center', valign: 'top', lineSpacingMultiple: LINE.body });
  });
}

export function summary(slide, pptx, d, ctx) {
  header(slide, ctx, d.kicker || 'SUMMARY', d.title || '重點回顧');
  const items = (d.items || []).slice(0, 5);
  const rh = BANDS.contentH / Math.max(items.length, 1);
  items.forEach((it, i) => {
    const y = BANDS.contentY + i * rh;
    plainCard(slide, ctx, SAFE.x, y + 0.03, SAFE.w, rh - 0.14);
    pill(slide, ctx, SAFE.x + 0.2, y + rh / 2 - 0.24, 2.8, 0.48, it.key || '', ctx.pal.primary, ctx.pal.onPrimary);
    slide.addText(it.value || '', { x: SAFE.x + 3.3, y, w: SAFE.w - 3.55, h: rh,
      fontSize: ctx.ty.body, color: ctx.pal.text, fontFace: HEAD, valign: 'middle', lineSpacingMultiple: LINE.body });
  });
}

export function timeline(slide, pptx, d, ctx) {
  header(slide, ctx, d.kicker || 'TIMELINE', d.title || '時間軸');
  const pts = (d.points || []).slice(0, 4);
  const n = Math.max(pts.length, 1);
  const lineY = BANDS.contentY + 0.7;
  slide.addShape('line', { x: SAFE.x + 0.2, y: lineY, w: SAFE.w - 0.4, h: 0, line: { color: ctx.pal.muted, width: 1.5, transparency: 40 } });
  const step = SAFE.w / n;
  pts.forEach((p, i) => {
    const cx = SAFE.x + step * i + step / 2;
    slide.addShape('ellipse', { x: cx - 0.16, y: lineY - 0.16, w: 0.32, h: 0.32, fill: { color: ctx.pal.primary }, line: { color: ctx.pal.bg, width: 2.5 } });
    pill(slide, ctx, cx - 0.9, lineY - 1.05, 1.8, 0.5, String(p.year || ''), ctx.pal.primary, ctx.pal.onPrimary);
    plainCard(slide, ctx, cx - step / 2 + 0.18, lineY + 0.45, step - 0.36, BANDS.contentH - 1.7);
    slide.addText(p.event || '', { x: cx - step / 2 + 0.34, y: lineY + 0.6, w: step - 0.68, h: BANDS.contentH - 2.0,
      fontSize: ctx.ty.small, color: ctx.pal.text, fontFace: HEAD, align: 'center', valign: 'top', lineSpacingMultiple: LINE.body });
  });
}

export function quote(slide, pptx, d, ctx) {
  slide.addText('“', { x: SAFE.x - 0.1, y: 0.5, w: 3, h: 3, fontSize: 320, bold: true, color: ctx.pal.primary, transparency: 72, fontFace: HEAD });
  slide.addShape('rect', { x: SAFE.x + 0.2, y: 2.35, w: 0.12, h: 2.4, fill: { color: ctx.pal.primary }, line: { type: 'none' } });
  slide.addText(d.text || '', { x: SAFE.x + 0.7, y: 2.3, w: SAFE.w - 1.0, h: 2.6,
    fontSize: ctx.ty.h2 + 6, italic: true, color: ctx.pal.text, fontFace: HEAD, align: 'left', valign: 'middle', lineSpacingMultiple: LINE.title });
  if (d.cite) slide.addText(`— ${d.cite}`, { x: SAFE.x + 0.7, y: 5.1, w: SAFE.w - 1.0, h: 0.6,
    fontSize: ctx.ty.body, bold: true, color: ctx.pal.primary, fontFace: HEAD, align: 'left' });
}

export function threeColumn(slide, pptx, d, ctx) {
  header(slide, ctx, d.kicker, d.title || '');
  const cards = (d.cards || []).slice(0, 3);
  const bars = [ctx.pal.primary, ctx.pal.secondary, ctx.pal.accent];
  for (let i = 0; i < 3; i++) {
    const { x, w } = GRID.span(1 + i * 4, 4);
    const c = cards[i] || {};
    accentCard(slide, ctx, x, BANDS.contentY, w, BANDS.contentH, bars[i]);
    slide.addShape('ellipse', { x: x + 0.3, y: BANDS.contentY + 0.35, w: 0.85, h: 0.85, fill: { color: bars[i] }, line: { type: 'none' } });
    slide.addText(c.icon || '●', { x: x + 0.3, y: BANDS.contentY + 0.35, w: 0.85, h: 0.85, fontSize: 26, color: ctx.pal.onPrimary, align: 'center', valign: 'middle' });
    slide.addText(c.title || '', { x: x + 0.3, y: BANDS.contentY + 1.45, w: w - 0.6, h: 0.6,
      fontSize: ctx.ty.h2 - 2, bold: true, color: ctx.pal.text, fontFace: HEAD });
    slide.addText(c.body || '', { x: x + 0.3, y: BANDS.contentY + 2.15, w: w - 0.6, h: BANDS.contentH - 2.4,
      fontSize: ctx.ty.body, color: ctx.pal.muted, fontFace: HEAD, valign: 'top', lineSpacingMultiple: LINE.body });
  }
}

export function imageHero(slide, pptx, d, ctx) {
  const imgW = SAFE.w * 0.6, txtX = SAFE.x + imgW + SPACE.lg, txtW = SAFE.w - imgW - SPACE.lg;
  if (d.image) slide.addImage({ path: d.image, x: SAFE.x, y: SAFE.y, w: imgW, h: SAFE.h, rounding: true, sizing: { type: 'cover', w: imgW, h: SAFE.h } });
  else {
    plainCard(slide, ctx, SAFE.x, SAFE.y, imgW, SAFE.h);
    slide.addText('🖼\n圖片槽 16:9', { x: SAFE.x, y: SAFE.y, w: imgW, h: SAFE.h, fontSize: ctx.ty.body, color: ctx.pal.muted, align: 'center', valign: 'middle', fontFace: HEAD });
  }
  slide.addShape('rect', { x: txtX, y: SAFE.y + 0.35, w: 0.5, h: 0.1, fill: { color: ctx.pal.primary }, line: { type: 'none' } });
  if (d.kicker) slide.addText(String(d.kicker).toUpperCase(), { x: txtX, y: SAFE.y + 0.5, w: txtW, h: 0.4,
    fontSize: ctx.ty.small, color: ctx.pal.primary, bold: true, charSpacing: 2, fontFace: HEAD });
  slide.addText(d.title || '', { x: txtX, y: SAFE.y + 1.0, w: txtW, h: 1.6,
    fontSize: ctx.ty.h2, bold: true, color: ctx.pal.text, fontFace: HEAD, valign: 'top', lineSpacingMultiple: LINE.title });
  slide.addText(d.body || '', { x: txtX, y: SAFE.y + 2.6, w: txtW, h: SAFE.h - 2.8,
    fontSize: ctx.ty.body, color: ctx.pal.text, fontFace: HEAD, valign: 'top', lineSpacingMultiple: LINE.body });
}

export function prosCons(slide, pptx, d, ctx) {
  header(slide, ctx, d.kicker, d.title || '優缺點分析');
  const sides = [
    { heading: d.prosLabel || '優點', items: d.pros || [], color: '15803D', mark: '＋' },
    { heading: d.consLabel || '缺點', items: d.cons || [], color: 'B91C1C', mark: '－' },
  ];
  sides.forEach((s, i) => {
    const { x, w } = GRID.span(1 + i * 6, 6);
    plainCard(slide, ctx, x, BANDS.contentY, w, BANDS.contentH);
    slide.addShape('roundRect', { x, y: BANDS.contentY, w, h: 0.85, rectRadius: 0.08, fill: { color: s.color }, line: { type: 'none' } });
    slide.addShape('rect', { x, y: BANDS.contentY + 0.42, w, h: 0.43, fill: { color: s.color }, line: { type: 'none' } });
    slide.addText(`${s.mark}  ${s.heading}`, { x: x + 0.3, y: BANDS.contentY, w: w - 0.6, h: 0.85,
      fontSize: ctx.ty.h2, bold: true, color: 'FFFFFF', fontFace: HEAD, valign: 'middle' });
    slide.addText((s.items || []).map((t) => ({ text: String(t), options: { bullet: { code: '2022' }, paraSpaceAfter: 10 } })), {
      x: x + 0.3, y: BANDS.contentY + 1.1, w: w - 0.6, h: BANDS.contentH - 1.35,
      fontSize: ctx.ty.body, color: ctx.pal.text, fontFace: HEAD, valign: 'top', lineSpacingMultiple: LINE.body });
  });
}

export function checklist(slide, pptx, d, ctx) {
  header(slide, ctx, d.kicker || 'CHECKLIST', d.title || '學習自評');
  const items = (d.items || []).slice(0, 6);
  const rh = Math.min(0.8, (BANDS.contentH - (d.reflect ? 0.9 : 0)) / Math.max(items.length, 1));
  items.forEach((t, i) => {
    const y = BANDS.contentY + i * rh;
    if (i % 2 === 0) plainCard(slide, ctx, SAFE.x, y + 0.02, SAFE.w, rh - 0.1);
    slide.addShape('roundRect', { x: SAFE.x + 0.25, y: y + rh / 2 - 0.19, w: 0.38, h: 0.38, rectRadius: 0.06,
      fill: { color: ctx.pal.primary }, line: { type: 'none' } });
    slide.addText('✓', { x: SAFE.x + 0.25, y: y + rh / 2 - 0.19, w: 0.38, h: 0.38, fontSize: ctx.ty.small, bold: true, color: ctx.pal.onPrimary, align: 'center', valign: 'middle', fontFace: HEAD });
    slide.addText(String(t), { x: SAFE.x + 0.9, y, w: SAFE.w - 1.1, h: rh,
      fontSize: ctx.ty.body, color: ctx.pal.text, fontFace: HEAD, valign: 'middle', lineSpacingMultiple: LINE.body });
  });
  if (d.reflect) {
    const y = BANDS.contentY + items.length * rh + 0.1;
    slide.addText(`✍  ${d.reflect}`, { x: SAFE.x, y, w: SAFE.w, h: 0.7, fontSize: ctx.ty.small, italic: true, color: ctx.pal.primary, fontFace: HEAD, valign: 'middle' });
  }
}

// ── 補缺口版型 ───────────────────────────────────────────────
export function matrix(slide, pptx, d, ctx) {
  header(slide, ctx, d.kicker, d.title || '');
  const q = (d.quadrants || []).slice(0, 4);
  const gap = SPACE.sm;
  const cw = (SAFE.w - gap) / 2, ch = (BANDS.contentH - gap) / 2;
  const colors = [ctx.pal.primary, ctx.pal.secondary, ctx.pal.accent, ctx.pal.muted];
  q.forEach((quad, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = SAFE.x + col * (cw + gap), y = BANDS.contentY + row * (ch + gap);
    accentCard(slide, ctx, x, y, cw, ch, colors[i]);
    pill(slide, ctx, x + 0.3, y + 0.32, Math.min(cw - 0.6, 3.4), 0.5, quad.heading || '', colors[i], ctx.pal.onPrimary);
    slide.addText(quad.text || '', { x: x + 0.32, y: y + 1.0, w: cw - 0.64, h: ch - 1.2,
      fontSize: ctx.ty.body, color: ctx.pal.text, fontFace: HEAD, valign: 'top', lineSpacingMultiple: LINE.body });
  });
}

export function processFlow(slide, pptx, d, ctx) {
  header(slide, ctx, d.kicker, d.title || '流程');
  const steps = (d.steps || []).slice(0, 4);
  const n = Math.max(steps.length, 1);
  const gap = 0.55;
  const bw = (SAFE.w - gap * (n - 1)) / n;
  const by = BANDS.contentY + BANDS.contentH / 2 - 1.15;
  const bh = 2.3;
  steps.forEach((s, i) => {
    const x = SAFE.x + i * (bw + gap);
    accentCard(slide, ctx, x, by, bw, bh);
    numBadge(slide, ctx, x + bw / 2 - 0.35, by + 0.35, 0.7, i + 1);
    slide.addText(s.label || s || '', { x: x + 0.2, y: by + 1.2, w: bw - 0.4, h: 1.0,
      fontSize: ctx.ty.body, bold: true, color: ctx.pal.text, fontFace: HEAD, align: 'center', valign: 'top', lineSpacingMultiple: LINE.body });
    if (i < n - 1) slide.addShape('chevron', { x: x + bw + 0.08, y: by + bh / 2 - 0.22, w: gap - 0.16, h: 0.44, fill: { color: ctx.pal.primary }, line: { type: 'none' } });
  });
}

export function conceptWeb(slide, pptx, d, ctx) {
  header(slide, ctx, d.kicker, d.title || '概念網');
  const cx = SAFE.x + SAFE.w / 2, cy = BANDS.contentY + BANDS.contentH / 2 + 0.1;
  const nodes = (d.nodes || []).slice(0, 6);
  const R = 3.4, ry = 1.7;
  nodes.forEach((_, i) => {
    const a = (Math.PI * 2 * i) / Math.max(nodes.length, 1) - Math.PI / 2;
    slide.addShape('line', { x: cx, y: cy, w: Math.cos(a) * R, h: Math.sin(a) * ry, line: { color: ctx.pal.muted, width: 1.25, transparency: 40 } });
  });
  nodes.forEach((node, i) => {
    const a = (Math.PI * 2 * i) / Math.max(nodes.length, 1) - Math.PI / 2;
    const nx = cx + Math.cos(a) * R - 1.0, ny = cy + Math.sin(a) * ry - 0.32;
    slide.addShape('roundRect', { x: nx, y: ny, w: 2.0, h: 0.64, rectRadius: 0.1, fill: { color: ctx.pal.surface }, line: { color: ctx.pal.primary, width: 1.25 }, shadow: sh(ctx) });
    slide.addText(String(node), { x: nx, y: ny, w: 2.0, h: 0.64, fontSize: ctx.ty.small, bold: true, color: ctx.pal.text, fontFace: HEAD, align: 'center', valign: 'middle' });
  });
  slide.addShape('ellipse', { x: cx - 1.15, y: cy - 0.62, w: 2.3, h: 1.24, fill: { color: ctx.pal.primary }, line: { type: 'none' }, shadow: sh(ctx) });
  slide.addText(d.center || '核心', { x: cx - 1.15, y: cy - 0.62, w: 2.3, h: 1.24, fontSize: ctx.ty.body, bold: true, color: ctx.pal.onPrimary, fontFace: HEAD, align: 'center', valign: 'middle' });
}

export function closing(slide, pptx, d, ctx) {
  slide.addShape('roundRect', { x: 9.9, y: 0.7, w: 2.9, h: 2.9, rectRadius: 0.18, fill: { color: ctx.pal.primary }, line: { type: 'none' } });
  slide.addShape('rect', { x: SAFE.x, y: 2.7, w: 0.6, h: 0.12, fill: { color: ctx.pal.primary }, line: { type: 'none' } });
  if (d.kicker) slide.addText(String(d.kicker).toUpperCase(), { x: SAFE.x, y: 2.9, w: 8, h: 0.5,
    fontSize: ctx.ty.small + 1, bold: true, color: ctx.pal.primary, charSpacing: 3, fontFace: HEAD });
  slide.addText(d.title || '謝謝聆聽', { x: SAFE.x, y: 3.45, w: 8.5, h: 1.4,
    fontSize: ctx.ty.title + 8, bold: true, color: ctx.pal.text, fontFace: HEAD, align: 'left', valign: 'top' });
  if (d.subtitle) slide.addText(d.subtitle, { x: SAFE.x, y: 4.95, w: 8.5, h: 0.6,
    fontSize: ctx.ty.body, color: ctx.pal.muted, fontFace: HEAD, align: 'left' });
}

/** 版型登記表：layout key → renderer */
export const LAYOUTS = {
  cover, section, objectives, bullets,
  'two-column': twoColumn, vocab, activity, discussion, hero, data,
  summary, timeline, quote, 'three-column': threeColumn,
  'image-hero': imageHero, 'pros-cons': prosCons, checklist,
  matrix, 'process-flow': processFlow, 'concept-web': conceptWeb, closing,
};
