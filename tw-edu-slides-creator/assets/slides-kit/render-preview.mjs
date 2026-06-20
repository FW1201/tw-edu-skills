// render-preview.mjs — 截圖視覺測試：pptx → PDF → PNG（每張）＋ N-up 縮圖總覽
// 用法：node render-preview.mjs <deck.pptx> [outDir=preview]
// 轉 PDF 引擎自動偵測：① LibreOffice(soffice) ② Microsoft PowerPoint（macOS, AppleScript）。
// 再用 poppler(pdftoppm) 切成每張 PNG。
//
// 註：用 PowerPoint 路徑時，macOS 會要求一次「自動化」權限（System Settings ›
//     Privacy & Security › Automation）。互動執行時核准即可；headless/CI 建議裝 LibreOffice。

import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { basename, join } from 'node:path';
import { tmpdir } from 'node:os';

const SOFFICE_CANDIDATES = [
  'soffice', 'libreoffice',
  '/Applications/LibreOffice.app/Contents/MacOS/soffice',
  '/opt/homebrew/bin/soffice', '/usr/local/bin/soffice', '/usr/bin/soffice',
];
function findSoffice() {
  for (const c of SOFFICE_CANDIDATES) {
    try { execSync(`command -v "${c}" >/dev/null 2>&1 || test -x "${c}"`, { stdio: 'ignore' }); return c; }
    catch { /* next */ }
  }
  return null;
}
function which(cmd) { try { execSync(`command -v ${cmd}`, { stdio: 'ignore' }); return true; } catch { return false; } }
function hasPowerPoint() { return existsSync('/Applications/Microsoft PowerPoint.app'); }

/** 用 LibreOffice 轉 PDF */
function sofficeToPdf(soffice, pptx, outDir) {
  execSync(`"${soffice}" --headless --convert-to pdf --outdir "${outDir}" "${pptx}"`, { stdio: 'inherit' });
  return join(outDir, `${basename(pptx).replace(/\.pptx$/i, '')}.pdf`);
}

/** 用 PowerPoint(AppleScript) 轉 PDF。為避免雲端硬碟路徑逾時，先複製到本機暫存。 */
function powerpointToPdf(pptx, outDir) {
  const tmpPptx = join(tmpdir(), 'slideskit-render.pptx');
  const tmpPdf = join(tmpdir(), 'slideskit-render.pdf');
  execSync(`cp "${pptx}" "${tmpPptx}"`);
  const scpt = join(tmpdir(), 'slideskit-render.applescript');
  writeFileSync(scpt, [
    'on run argv',
    '  set inP to item 1 of argv',
    '  set outP to item 2 of argv',
    '  tell application "Microsoft PowerPoint"',
    '    activate',
    '    with timeout of 200 seconds',
    '      open POSIX file inP',
    '      set pres to active presentation',
    '      save pres in POSIX file outP as save as PDF',
    '      close pres saving no',
    '    end timeout',
    '  end tell',
    '  return "ok"',
    'end run',
  ].join('\n'));
  execSync(`osascript "${scpt}" "${tmpPptx}" "${tmpPdf}"`, { stdio: 'inherit' });
  const finalPdf = join(outDir, `${basename(pptx).replace(/\.pptx$/i, '')}.pdf`);
  execSync(`cp "${tmpPdf}" "${finalPdf}"`);
  return finalPdf;
}

// ── main ─────────────────────────────────────────────────────
const pptx = process.argv[2];
const outDir = process.argv[3] || 'preview';
if (!pptx || !existsSync(pptx)) { console.error('用法：node render-preview.mjs <deck.pptx> [outDir]'); process.exit(2); }
if (!which('pdftoppm')) { console.error('❌ 找不到 pdftoppm，請安裝 poppler：brew install poppler'); process.exit(3); }

mkdirSync(outDir, { recursive: true });
const soffice = findSoffice();
let pdf;
try {
  if (soffice) { console.log(`① pptx → pdf（LibreOffice）…`); pdf = sofficeToPdf(soffice, pptx, outDir); }
  else if (hasPowerPoint()) { console.log('① pptx → pdf（Microsoft PowerPoint）…'); pdf = powerpointToPdf(pptx, outDir); }
  else {
    console.error('❌ 找不到 PDF 轉檔引擎。\n   裝 LibreOffice：brew install --cask libreoffice\n   或於有 Microsoft PowerPoint 的 macOS 互動執行（會要求一次自動化權限）。');
    process.exit(3);
  }
} catch (e) {
  console.error('❌ 轉 PDF 失敗：', e.message);
  console.error('   若用 PowerPoint：請到 System Settings › Privacy & Security › Automation 允許控制 PowerPoint，或改裝 LibreOffice。');
  process.exit(4);
}

console.log('② pdf → png（每張，150dpi）…');
execSync(`rm -f "${outDir}"/slide-*.png "${outDir}"/overview.png`);
execSync(`pdftoppm -png -r 150 "${pdf}" "${outDir}/slide"`, { stdio: 'inherit' });

if (which('montage')) {
  console.log('③ 產生 N-up 縮圖總覽 overview.png …');
  try { execSync(`montage "${outDir}"/slide-*.png -tile 3x -geometry 480x270+6+6 -background gray "${outDir}/overview.png"`, { stdio: 'inherit' }); }
  catch { console.warn('  montage 失敗，略過總覽'); }
} else {
  console.log('③ （未裝 ImageMagick montage，略過 N-up 總覽；單張 PNG 已足夠審圖）');
}

console.log(`\n✅ 截圖完成 → ${outDir}/slide-*.png`);
console.log('   下一步：用 subagent 以「假設一定有錯」的心態逐張審圖（見 SKILL.md QA 清單）。');
