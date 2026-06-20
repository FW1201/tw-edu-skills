// grid.mjs — 版面網格契約（Part 4）
// 16:9 畫布的座標常數、12 欄網格、年級自適應字級（pt）、8pt 間距系統。
// 所有 layout renderer 一律從這裡取數值，禁止 hardcode 魔術數字。

/** 畫布尺寸（吋）。PptxGenJS LAYOUT_WIDE = 13.333 × 7.5 */
export const CANVAS = { w: 13.333, h: 7.5 };

/** 外邊距 → 安全內容區 */
export const MARGIN = { x: 0.7, top: 0.55, bottom: 0.55 };
export const SAFE = {
  x: MARGIN.x,
  y: MARGIN.top,
  w: CANVAS.w - MARGIN.x * 2,            // 11.933
  h: CANVAS.h - MARGIN.top - MARGIN.bottom, // 6.4
};

/** 12 欄網格：欄寬與跨欄錨點 */
export const GRID = (() => {
  const cols = 12;
  const gutter = 0.15;
  const colW = (SAFE.w - gutter * (cols - 1)) / cols;
  /** span(startCol 1-based, spanCount) → { x, w } */
  const span = (start, count) => ({
    x: +(SAFE.x + (start - 1) * (colW + gutter)).toFixed(3),
    w: +(count * colW + (count - 1) * gutter).toFixed(3),
  });
  return { cols, gutter, colW: +colW.toFixed(3), span };
})();

/** 三段帶狀 y 錨點（垂直節奏）— 避免每張漂移 */
export const BANDS = {
  titleY: SAFE.y,            // 標題帶起點
  titleH: 1.15,
  get contentY() { return +(this.titleY + this.titleH + 0.25).toFixed(3); }, // 內容帶
  get contentH() { return +(CANVAS.h - MARGIN.bottom - 0.35 - this.contentY).toFixed(3); },
  footerY: +(CANVAS.h - MARGIN.bottom - 0.3).toFixed(3), // 頁尾帶（走 master）
};

/** 8pt 間距系統（吋）：1 單位 = 8pt = 0.0833"。取倍數，杜絕魔術數字 */
const U = 8 / 96; // 0.0833"
export const SPACE = {
  unit: +U.toFixed(4),
  xs: +(U * 1).toFixed(3),   // 8pt
  sm: +(U * 2).toFixed(3),   // 16pt
  md: +(U * 3).toFixed(3),   // 24pt
  lg: +(U * 4).toFixed(3),   // 32pt
  xl: +(U * 6).toFixed(3),   // 48pt
};

/**
 * 年級自適應字級（pt = px ÷ 1.333）。
 * 對應 SKILL 的 1920×1080 px 字級表。
 */
export const TYPE = {
  '國小低':   { title: 54, h2: 40, body: 32, small: 24, maxBullets: 3 },
  '國小中高': { title: 48, h2: 34, body: 28, small: 22, maxBullets: 4 },
  '國中':     { title: 41, h2: 30, body: 23, small: 19, maxBullets: 5 },
  '高中':     { title: 36, h2: 27, body: 21, small: 17, maxBullets: 6 },
  '大學':     { title: 32, h2: 25, body: 19, small: 16, maxBullets: 6 },
};
/** 字級下限（pt）：低於此值 validate 報 P0 */
export const MIN_FONT_PT = 16;

/** 行高倍數（避免 PowerPoint 預設行高撐爆文字框） */
export const LINE = { title: 1.05, body: 1.25 };

/** 字型（中文 Noto Sans TC；標題字型由 master 指定） */
export const FONT = {
  body: 'Noto Sans TC',
  bodyFallback: 'PingFang TC',
};

/** 圖片槽鎖定比例（寬:高），renderer 依此配 w/h，sizing 用 cover 防變形 */
export const IMAGE_RATIO = {
  hero: 16 / 9,
  half: 4 / 3,
  thumb: 1,
};

/** 由年級取字級表 */
export function typeFor(grade) {
  return TYPE[grade] || TYPE['國中'];
}

/**
 * CJK 文字框高度估算（吋）— 主動防溢出用。
 * 全形字寬 ≈ 字級 pt；半形 ≈ 0.5。依框寬估每行字數→行數→高度。
 * @returns {number} 估算所需高度（吋）
 */
export function estimateTextHeight(text, fontPt, boxWidthInch, lineMul = LINE.body) {
  const ptToInch = 1 / 72;
  const charWidthInch = fontPt * ptToInch;          // 全形字寬 ≈ 字級
  const charsPerLine = Math.max(1, Math.floor(boxWidthInch / charWidthInch));
  // 以全形計（保守）：CJK 算 1，ASCII 算 0.55
  let units = 0;
  for (const ch of String(text)) units += /[\x00-\xff]/.test(ch) ? 0.55 : 1;
  const lines = Math.max(1, Math.ceil(units / charsPerLine));
  const lineHeightInch = fontPt * ptToInch * lineMul;
  return +(lines * lineHeightInch).toFixed(3);
}
