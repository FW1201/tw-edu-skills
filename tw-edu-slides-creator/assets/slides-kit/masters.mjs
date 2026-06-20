// masters.mjs — PptxGenJS slide master 定義（v3.1 視覺升級）
// 每個色系註冊 LIGHT（內文）與 DARK（封面/結語 premium）。
// 品牌母題：左側全高色鐵軌（rail），跨頁重複、強化 primary 視覺權重。
// 標題下「絕不」加 accent line。

import { CANVAS, MARGIN, SAFE } from './grid.mjs';

export const RAIL_W = 0.16; // 左側品牌軌寬（吋）

/**
 * 註冊 LIGHT / DARK 兩個 master。
 * @returns {{light:string, dark:string}}
 */
export function defineMasters(pptx, theme, courseName = '') {
  const footerY = CANVAS.h - MARGIN.bottom - 0.02;
  const mk = (name, bg, railColor, footColor, footTrans) => pptx.defineSlideMaster({
    title: name,
    background: { color: bg },
    objects: [
      // 左側全高品牌軌
      { rect: { x: 0, y: 0, w: RAIL_W, h: CANVAS.h, fill: { color: railColor } } },
      // 頁尾課程名
      { text: { text: courseName, options: {
        x: MARGIN.x, y: footerY - 0.18, w: SAFE.w - 1.0, h: 0.28,
        fontSize: 10, color: footColor, transparency: footTrans, fontFace: 'Noto Sans TC',
        align: 'left', valign: 'middle' } } },
    ],
    slideNumber: { x: CANVAS.w - MARGIN.x - 0.6, y: footerY - 0.18, w: 0.6, h: 0.28,
      fontSize: 10, color: footColor, transparency: footTrans, fontFace: 'Noto Sans TC', align: 'right' },
  });

  mk('LIGHT', theme.bg, theme.primary, theme.muted, 0);
  mk('DARK', theme.dark.bg, theme.dark.primary, theme.dark.text, 35);
  return { light: 'LIGHT', dark: 'DARK' };
}

/** 哪些版型預設用深底（dark/light sandwich） */
export const DARK_LAYOUTS = new Set(['cover', 'section', 'hero', 'quote', 'closing']);
