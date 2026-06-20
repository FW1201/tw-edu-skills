// tokens.mjs — 鎖定設計 token（色系庫）
// 12+ 學科色系，每組 6+ 色 token。renderer 只引用 key，禁止散落 hex。
// 每組附 dark{} premium 變體（封面/結語用），支援 dark/light sandwich。
// 全部色值在載入時跑 WCAG AA 檢查（見 validate-deck.mjs）。

/**
 * @typedef {Object} Theme
 * @property {string} bg        頁面背景
 * @property {string} surface   卡片/區塊表面（略異於 bg）
 * @property {string} text      主文字（對 bg ≥ 4.5:1）
 * @property {string} muted     次要文字
 * @property {string} primary   主色（佔 60–70% 視覺權重）
 * @property {string} secondary 輔色
 * @property {string} accent    銳利點綴色
 * @property {string} onPrimary 疊在 primary 上的文字色
 * @property {string} headingFont 標題字型
 * @property {{bg:string,text:string,primary:string,accent:string,onPrimary:string}} dark premium 深底變體
 * @property {boolean} [isDark] 此色系本身即深底
 */

/** @type {Record<string, Theme>} */
export const THEMES = {
  // 1. 語文・國語文 — 暖橙／墨韻
  '語文': {
    bg: 'FFFBF5', surface: 'F5EDE0', text: '2D1A0E', muted: '6E5A45',
    primary: 'C2410C', secondary: '3F6FA3', accent: 'B45309', onPrimary: 'FFFFFF',
    headingFont: 'Noto Sans TC',
    dark: { bg: '2A1A12', text: 'F5EDE0', primary: 'E9885F', accent: 'F0B25A', onPrimary: '2A1A12' },
  },
  // 2. 數學 — 靛藍／幾何
  '數學': {
    bg: 'F7F8FC', surface: 'EAEDF7', text: '1B1F3B', muted: '545B7A',
    primary: '4338CA', secondary: '0E7490', accent: 'D97706', onPrimary: 'FFFFFF',
    headingFont: 'Noto Sans TC',
    dark: { bg: '14152B', text: 'E7E9F6', primary: '8B83F0', accent: 'F0A93A', onPrimary: '14152B' },
  },
  // 3. 自然科學 — 森綠／海藍
  '自然': {
    bg: 'F4FBF6', surface: 'E1F1E6', text: '13261A', muted: '466052',
    primary: '15803D', secondary: '0E7490', accent: 'CA8A04', onPrimary: 'FFFFFF',
    headingFont: 'Noto Sans TC',
    dark: { bg: '0F2419', text: 'E2F3E8', primary: '4FB477', accent: 'EAB308', onPrimary: '0F2419' },
  },
  // 4. 社會 — 赭土／史冊
  '社會': {
    bg: 'FBF7F0', surface: 'EFE5D4', text: '2B2114', muted: '6B5B43',
    primary: 'B45309', secondary: '1D5FA0', accent: '7C5E3C', onPrimary: 'FFFFFF',
    headingFont: 'Noto Sans TC',
    dark: { bg: '241B10', text: 'F0E6D6', primary: 'D9913F', accent: '4F94CE', onPrimary: '241B10' },
  },
  // 5. 英語 — 莓紅／奶油
  '英語': {
    bg: 'FFF7FA', surface: 'F6E2EB', text: '2B0F1C', muted: '7A4F60',
    primary: 'BE185D', secondary: '6D28D9', accent: 'D97706', onPrimary: 'FFFFFF',
    headingFont: 'Noto Sans TC',
    dark: { bg: '2A0F1B', text: 'F7E4EC', primary: 'E96CA0', accent: 'F0A93A', onPrimary: '2A0F1B' },
  },
  // 6. 藝術 — 桃紫／粉彩
  '藝術': {
    bg: 'FBF7FF', surface: 'EDE4F8', text: '241433', muted: '63537A',
    primary: '7C3AED', secondary: 'DB2777', accent: '0D9488', onPrimary: 'FFFFFF',
    headingFont: 'Noto Sans TC',
    dark: { bg: '1E1330', text: 'EEE6F8', primary: 'A985F0', accent: '2DD4BF', onPrimary: '1E1330' },
  },
  // 7. 科技資訊 — 霓虹深色（本身即深底）
  '科技': {
    bg: '0D1117', surface: '161B22', text: 'E6EDF3', muted: '8B98A5',
    primary: '00D4FF', secondary: '7B2FFF', accent: 'FF6B35', onPrimary: '0D1117',
    headingFont: 'Noto Sans TC', isDark: true,
    dark: { bg: '0D1117', text: 'E6EDF3', primary: '00D4FF', accent: 'FF6B35', onPrimary: '0D1117' },
  },
  // 8. SEL 情意 — 鼠尾草／療癒綠
  'SEL': {
    bg: 'F4FAF7', surface: 'E1F0EA', text: '16271F', muted: '4C6B60',
    primary: '2F6F5E', secondary: '6F9C8B', accent: 'D98A3D', onPrimary: 'FFFFFF',
    headingFont: 'Noto Sans TC',
    dark: { bg: '12241D', text: 'E2F0EA', primary: '5FAE96', accent: 'EAA35A', onPrimary: '12241D' },
  },
  // 9. 體育健康 — 活力珊瑚
  '體育': {
    bg: 'FFF6F4', surface: 'F8E1DB', text: '2B1416', muted: '7A5552',
    primary: 'E11D48', secondary: '0E8F8E', accent: 'D97706', onPrimary: 'FFFFFF',
    headingFont: 'Noto Sans TC',
    dark: { bg: '2A1113', text: 'F8E3DE', primary: 'F2607E', accent: 'F0A93A', onPrimary: '2A1113' },
  },
  // 10. 生活綜合 — 大地米
  '生活': {
    bg: 'FAF6F0', surface: 'EEE4D6', text: '271E14', muted: '6E5C44',
    primary: '9A6A3A', secondary: '4F8060', accent: 'C2410C', onPrimary: 'FFFFFF',
    headingFont: 'Noto Sans TC',
    dark: { bg: '21190F', text: 'EFE6D8', primary: 'C49364', accent: 'E9885F', onPrimary: '21190F' },
  },
  // 11. 學術正式 — Academic Clean
  '學術': {
    bg: 'FAF9F5', surface: 'EBE9E1', text: '1A1814', muted: '5C5A52',
    primary: '34539C', secondary: '5C84B8', accent: 'B45309', onPrimary: 'FFFFFF',
    headingFont: 'Noto Sans TC',
    dark: { bg: '15171C', text: 'ECEAE2', primary: '7AA0D8', accent: 'D9913F', onPrimary: '15171C' },
  },
  // 12. 節慶通用 — 節慶紅金
  '節慶': {
    bg: 'FFF8F2', surface: 'F6E4D6', text: '2B1412', muted: '7A5548',
    primary: 'B91C1C', secondary: 'B7892B', accent: '0E7490', onPrimary: 'FFFFFF',
    headingFont: 'Noto Sans TC',
    dark: { bg: '2A100F', text: 'F6E5D8', primary: 'E5654F', accent: 'E0B450', onPrimary: '2A100F' },
  },
};

/** 舊版 3 主題 → 新色系別名（向後相容） */
export const THEME_ALIASES = {
  'Edu Warm': '語文',
  'edu-warm': '語文',
  'Tech Dark': '科技',
  'tech-dark': '科技',
  'Academic Clean': '學術',
  'academic-clean': '學術',
};

/** 取色系（含別名解析），預設語文 */
export function getTheme(name) {
  const key = THEME_ALIASES[name] || name;
  return THEMES[key] || THEMES['語文'];
}

export const THEME_KEYS = Object.keys(THEMES);

// ── WCAG 對比工具 ────────────────────────────────────────────
function _lin(c) { c /= 255; return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; }
/** 相對亮度 */
export function luminance(hex) {
  const h = hex.replace('#', '');
  const r = parseInt(h.slice(0, 2), 16), g = parseInt(h.slice(2, 4), 16), b = parseInt(h.slice(4, 6), 16);
  return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b);
}
/** 對比比值（1–21） */
export function contrastRatio(hexA, hexB) {
  const a = luminance(hexA), b = luminance(hexB);
  const hi = Math.max(a, b), lo = Math.min(a, b);
  return +((hi + 0.05) / (lo + 0.05)).toFixed(2);
}
/** 依背景挑黑或白文字（取對比較高者） */
export function bestTextOn(bgHex) {
  return contrastRatio('FFFFFF', bgHex) >= contrastRatio('111111', bgHex) ? 'FFFFFF' : '111111';
}
