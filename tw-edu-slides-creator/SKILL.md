---
name: tw-edu-slides-creator
description: >
  上傳任何教材（Word/PDF/文字/網址）後，自動生成視覺化教學簡報（.html）。
  依年段自動調整字體大小與資訊密度，使用者輸入風格描述詞，Claude 動態解讀為 CSS 設計系統。
  17 種 HTML 版型，純 CSS 動畫，無外部依賴，任何瀏覽器直接開啟投影。
  保留 Canva 高設計感路徑（Canva MCP）。
  當使用者提及「幫我做簡報」「上傳教材做簡報」「把文件轉成投影片」
  「製作教學簡報」「做PPT」「做投影片」「教學PPT」「課程簡報」
  「把這份資料做成簡報」「簡報製作」「製作投影片」時觸發。
version: 4.1.0
author: 奇老師・數位敘事力社群
allowed-tools: "Read, Write, WebFetch, WebSearch"
---

# 教材轉視覺化教學簡報 V4.1

---

## Step 1：資訊收集（最多問 3 個）

| 問題 | 必填 |
|------|------|
| 教學主題或課文是什麼？有現成教材嗎？（文字/Word/PDF/網址） | ✅ |
| 給哪個年段的學生？ | ✅ |
| 視覺風格是什麼感覺？請用 2–4 個詞描述，例如：「科技感 深色」「溫暖活潑」「簡約清晰」 | ✅ |

收集後輸出確認摘要：主題、年段、風格方向、預計張數。

---

## Step 2：風格解讀 + CSS 設計系統配置

### 2-A. 風格描述詞解讀

根據使用者的描述詞，自行判斷並決定以下 CSS 變數值。
**不得使用固定預設色盤**——每次都要根據描述詞做原創判斷。

**常見描述詞 → CSS 配置參考（僅供啟發，非窮舉）：**

| 描述詞範例 | --bg | --primary | --accent | --text |
|-----------|------|-----------|---------|--------|
| 科技感 深色 未來 | #0D1117 | #00D4FF | #7B2FFF | #E6EDF3 |
| 溫暖 活潑 色彩 | #FFFAF0 | #FF8C42 | #FFD166 | #2D2D2D |
| 簡約 專業 清晰 | #FFFFFF | #1A73E8 | #34A853 | #202124 |
| 清新 自然 生態 | #F0FAF4 | #2D9E6B | #7BC67E | #1A2E25 |
| 典雅 學術 沉穩 | #F8F6F2 | #2C3E6D | #C0392B | #1A1A2E |
| 活潑 低年級 遊戲 | #FFF8E1 | #E91E8C | #FF9800 | #212121 |
| 沉穩 高中 深灰 | #1C1C1E | #F5F5F5 | #FF9F0A | #EBEBEB |
| 台灣本土 文化 | #FEF3E2 | #C0392B | #E67E22 | #2C1A0E |

**完整 CSS 變數宣告範本：**
```css
:root {
  --bg: #...;         /* 背景色（投影片底色） */
  --surface: #...;    /* 卡片/區塊底色（比 bg 調深或淺 10-15%） */
  --primary: #...;    /* 主色（標題、重點強調） */
  --accent: #...;     /* 強調色（按鈕、highlight、圓點） */
  --text: #...;       /* 正文主色 */
  --muted: #...;      /* 次要文字（副標、提示） */
  --border: #...;     /* 分隔線（text 的 15% opacity 參考值） */
}
```

**對比度規則：**
- `--text` 對 `--bg` 的對比度必須 ≥ 4.5:1（WCAG AA）
- 深色背景配淺色文字；淺色背景配深色文字
- `--surface` 比 `--bg` 明度差 10–15%，確保區塊可辨

### 2-B. 年段字級配置

在 `:root` 中加入年段字級變數：

| 年段 | --sz-title | --sz-h2 | --sz-body | --sz-small | --max-bullets |
|------|-----------|---------|-----------|-----------|--------------|
| 國小低 (1-2) | 3.2rem | 2.4rem | 2.0rem | 1.4rem | 3 |
| 國小中高 (3-6) | 2.8rem | 2.0rem | 1.7rem | 1.3rem | 4 |
| 國中 (7-9) | 2.4rem | 1.8rem | 1.5rem | 1.1rem | 5 |
| 高中 (10-12) | 2.0rem | 1.6rem | 1.3rem | 1.0rem | 6 |

---

## Step 3：內容分析 + 投影片規劃

### 3-A. 讀取教材

讀取使用者提供的素材（文字輸入、Read 工具讀取檔案、或 WebFetch 抓取網址）。

### 3-B. 版型分配

依 `references/slide_design_principles.md` 的「內容特徵 → 版型映射規則」，將內容分配到以下 **17 個 HTML 版型**。
詳細 CSS class 與 HTML 骨架請參照 `references/html-layout-templates.md`。

| 版型 key | 用途 | 對應舊版型 |
|---------|------|----------|
| `cover` | 封面（課名・年段・教師） | cover |
| `objectives` | 學習目標（三維格式） | objectives |
| `section` | 段落分隔（編號 + 主題） | section_cover |
| `bullets` | 條列重點 | content / icon_list |
| `two-column` | 雙欄比較 | two_column / comparison |
| `vocab` | 詞彙定義（含注音） | vocab |
| `activity` | 課堂活動步驟 | activity / process_flow |
| `discussion` | 思考討論題 | discussion |
| `hero` | 核心訊息大字 | hero_message |
| `data` | 數據/統計亮點 | data_highlight / three_cards |
| `summary` | 重點整理 | summary / kanban |
| `timeline` | 時間軸（歷史/傳記/事件，≥3 時間點） | timeline |
| `quote` | 大字金句（名言/課文精華/人物引言） | big_quote / testimonial |
| `three-column` | 三欄並列（三要素/三特徵） | three_cards / kanban |
| `image-hero` | 圖片全版（地圖/插圖/視覺引導） | image_focus |
| `pros-cons` | 優劣分析（正反立場/優缺點） | pros_cons |
| `checklist` | 學習清單（任務確認/評量項目） | blank_canvas |

**版型節奏規則：**
- 不得 3 張以上連續同版型
- 每 5 張至少 1 張重版型（cover / section / hero / discussion）
- 10 張以上須有 ≥1 hero 或 section

### 3-C. 輸出大綱供確認

**生成 HTML 前，先輸出文字大綱給教師確認：**

```
投影片大綱（共 N 張）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 #1  [cover]       課程名稱
 #2  [objectives]  學習目標（認知・情意・態度）
 #3  [section]     第一部分名稱
 #4  [bullets]     重點一標題
 ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
確認後請說「生成」，我就輸出完整 HTML 檔。若需調整，請指示後再生成。
```

---

## Step 4：生成完整 HTML

收到「生成」指令後，用 `Write` 工具輸出完整自含式 HTML：
```
/tmp/{主題slug}_教學簡報.html
```

### 4-A. HTML 完整架構

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{課程標題}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=Noto+Serif+TC:wght@400;700&display=swap" rel="stylesheet">
  <style>
    /* === 1. Reset === */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    /* === 2. CSS 變數（Step 2 風格解讀） === */
    :root {
      --bg: #...;
      --surface: #...;
      --primary: #...;
      --accent: #...;
      --text: #...;
      --muted: #...;
      --border: #...;
      --sz-title: ...rem;
      --sz-h2: ...rem;
      --sz-body: ...rem;
      --sz-small: ...rem;
      --font-tc: 'Noto Sans TC', sans-serif;
    }

    /* === 3. 投影片容器 === */
    html, body { height: 100%; overflow: hidden; background: var(--bg); }
    .deck {
      height: 100svh;
      overflow-y: scroll;
      scroll-snap-type: y mandatory;
      scrollbar-width: none;
    }
    .deck::-webkit-scrollbar { display: none; }
    .slide {
      height: 100svh;
      scroll-snap-align: start;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: clamp(2rem, 5vw, 4rem);
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-tc);
      position: relative;
      overflow: hidden;
    }

    /* === 4. 共用元件 === */
    .slide-title {
      font-size: var(--sz-h2);
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 1.5rem;
      align-self: flex-start;
      max-width: 90%;
      line-height: 1.3;
    }
    .surface-card {
      background: var(--surface);
      border-radius: 1rem;
      padding: 1.5rem 2rem;
    }
    .tag {
      display: inline-block;
      padding: 0.2em 0.6em;
      border-radius: 0.4em;
      font-size: var(--sz-small);
      font-weight: 700;
      background: var(--accent);
      color: var(--bg);
    }

    /* === 5. 11 個版型（參照 html-layout-templates.md 貼入完整 CSS） === */

    /* layout-cover */
    .layout-cover { justify-content: center; align-items: flex-start; }
    .layout-cover .cover-meta {
      font-size: var(--sz-small); color: var(--muted);
      letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 1rem;
    }
    .layout-cover .cover-title {
      font-size: var(--sz-title); font-weight: 900; color: var(--primary);
      line-height: 1.15; max-width: 80%; margin-bottom: 1rem;
    }
    .layout-cover .cover-subtitle {
      font-size: var(--sz-body); color: var(--text); margin-bottom: 2rem;
    }
    .layout-cover .cover-author {
      font-size: var(--sz-small); color: var(--muted);
    }
    .layout-cover::after {
      content: '';
      position: absolute; bottom: -5%; right: -5%;
      width: 40vw; height: 40vw;
      border-radius: 50%;
      background: var(--accent);
      opacity: 0.08;
      pointer-events: none;
    }

    /* layout-objectives */
    .layout-objectives { align-items: flex-start; }
    .objectives-list { list-style: none; width: 100%; display: flex; flex-direction: column; gap: 1rem; }
    .objectives-list li {
      display: flex; align-items: flex-start; gap: 0.75rem;
      font-size: var(--sz-body); background: var(--surface);
      border-radius: 0.75rem; padding: 1rem 1.25rem;
    }
    .obj-tag {
      flex-shrink: 0; font-size: var(--sz-small); font-weight: 700;
      padding: 0.15em 0.5em; border-radius: 0.35em;
      background: var(--accent); color: var(--bg);
    }

    /* layout-section */
    .layout-section { justify-content: center; align-items: center; text-align: center; }
    .section-num {
      font-size: clamp(5rem, 18vw, 12rem); font-weight: 900;
      color: var(--accent); opacity: 0.18; line-height: 1;
      position: absolute; left: 50%; top: 50%;
      transform: translate(-50%, -50%);
      pointer-events: none; user-select: none;
    }
    .section-inner { position: relative; z-index: 1; text-align: center; }
    .section-label {
      font-size: var(--sz-small); color: var(--muted);
      letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 0.75rem;
    }
    .section-title {
      font-size: var(--sz-title); font-weight: 900; color: var(--primary); line-height: 1.2;
    }
    .section-sub { font-size: var(--sz-body); color: var(--muted); margin-top: 0.75rem; }

    /* layout-bullets */
    .layout-bullets { align-items: flex-start; }
    .bullets-list { list-style: none; width: 100%; display: flex; flex-direction: column; gap: 0.9rem; }
    .bullets-list li {
      display: flex; align-items: flex-start; gap: 0.75rem;
      font-size: var(--sz-body); line-height: 1.5;
    }
    .bullets-list li::before {
      content: ''; flex-shrink: 0;
      width: 0.5rem; height: 0.5rem; border-radius: 50%;
      background: var(--accent); margin-top: 0.5em;
    }

    /* layout-two-column */
    .layout-two-column { align-items: flex-start; }
    .col-wrap {
      display: grid; grid-template-columns: 1fr 1fr;
      gap: 1.5rem; width: 100%;
    }
    .col { background: var(--surface); border-radius: 0.75rem; padding: 1.25rem; }
    .col-title {
      font-size: var(--sz-small); font-weight: 700; color: var(--accent);
      text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.75rem;
    }
    .col ul { list-style: none; display: flex; flex-direction: column; gap: 0.6rem; }
    .col ul li { font-size: var(--sz-body); padding-left: 1em; position: relative; line-height: 1.5; }
    .col ul li::before {
      content: '▸'; position: absolute; left: 0; color: var(--accent);
    }

    /* layout-vocab */
    .layout-vocab { align-items: flex-start; }
    .vocab-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(min(100%, 280px), 1fr));
      gap: 1rem; width: 100%;
    }
    .vocab-card {
      background: var(--surface); border-radius: 0.75rem; padding: 1rem 1.25rem;
      border-left: 4px solid var(--accent);
    }
    .vocab-word { font-size: var(--sz-h2); font-weight: 900; color: var(--primary); }
    .vocab-phonetic { font-size: var(--sz-small); color: var(--muted); margin: 0.2rem 0 0.5rem; }
    .vocab-def { font-size: var(--sz-body); line-height: 1.6; }
    .vocab-example { font-size: var(--sz-small); color: var(--muted); margin-top: 0.4rem; }

    /* layout-activity */
    .layout-activity { align-items: flex-start; }
    .activity-meta {
      font-size: var(--sz-small); color: var(--accent);
      font-weight: 700; margin-bottom: 1.25rem; margin-top: -0.75rem;
    }
    .steps-list { list-style: none; width: 100%; display: flex; flex-direction: column; gap: 0.85rem; }
    .steps-list li {
      display: flex; align-items: flex-start; gap: 1rem;
      background: var(--surface); border-radius: 0.75rem; padding: 1rem 1.25rem;
      font-size: var(--sz-body);
    }
    .step-num {
      flex-shrink: 0; width: 2em; height: 2em;
      border-radius: 50%; background: var(--accent); color: var(--bg);
      font-weight: 900; font-size: var(--sz-small);
      display: flex; align-items: center; justify-content: center;
    }

    /* layout-discussion */
    .layout-discussion { justify-content: center; align-items: center; text-align: center; }
    .discussion-inner { max-width: 80%; display: flex; flex-direction: column; align-items: center; gap: 1.5rem; }
    .discussion-timer {
      font-size: var(--sz-small); color: var(--accent);
      font-weight: 700; letter-spacing: 0.1em;
      border: 2px solid var(--accent); padding: 0.3em 0.8em; border-radius: 2em;
    }
    .discussion-question {
      font-size: var(--sz-h2); font-weight: 900; color: var(--primary);
      line-height: 1.4;
    }
    .discussion-hint {
      font-size: var(--sz-body); color: var(--muted); line-height: 1.6;
    }

    /* layout-hero */
    .layout-hero { justify-content: center; align-items: center; text-align: center; }
    .hero-inner { max-width: 85%; }
    .hero-headline {
      font-size: var(--sz-title); font-weight: 900; color: var(--primary);
      line-height: 1.2; margin-bottom: 1.25rem;
    }
    .hero-subline { font-size: var(--sz-body); color: var(--muted); line-height: 1.7; }
    .hero-bar {
      width: 4rem; height: 4px; background: var(--accent);
      margin: 0 auto 1.5rem; border-radius: 2px;
    }

    /* layout-data */
    .layout-data { align-items: flex-start; }
    .data-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(min(100%, 200px), 1fr));
      gap: 1.25rem; width: 100%;
    }
    .data-item {
      background: var(--surface); border-radius: 0.75rem; padding: 1.25rem 1.5rem;
      display: flex; flex-direction: column; gap: 0.4rem;
    }
    .data-value {
      font-size: var(--sz-title); font-weight: 900; color: var(--accent);
      line-height: 1;
    }
    .data-label { font-size: var(--sz-small); color: var(--muted); }
    .data-desc { font-size: var(--sz-body); color: var(--text); line-height: 1.5; }

    /* layout-summary */
    .layout-summary { align-items: flex-start; }
    .summary-list { width: 100%; display: flex; flex-direction: column; gap: 0.75rem; }
    .summary-item {
      display: grid; grid-template-columns: auto 1fr;
      gap: 1rem; align-items: center;
      background: var(--surface); border-radius: 0.65rem; padding: 0.9rem 1.25rem;
    }
    .summary-key {
      font-weight: 900; color: var(--accent); font-size: var(--sz-body);
      white-space: nowrap;
    }
    .summary-val { font-size: var(--sz-body); color: var(--text); line-height: 1.5; }

    /* === 6. 進場動畫（純 CSS） === */
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes slideUp {
      from { opacity: 0; transform: translateY(1.5rem); }
      to   { opacity: 1; transform: none; }
    }
    @keyframes scaleIn {
      from { opacity: 0; transform: scale(0.95); }
      to   { opacity: 1; transform: scale(1); }
    }
    .slide > * { opacity: 0; }
    .slide.active > * { animation: slideUp 0.45s ease forwards; }
    .slide.active > *:nth-child(1) { animation-delay: 0s; }
    .slide.active > *:nth-child(2) { animation-delay: 0.08s; }
    .slide.active > *:nth-child(3) { animation-delay: 0.16s; }
    .slide.active > *:nth-child(4) { animation-delay: 0.24s; }
    .slide.active > *:nth-child(n+5) { animation-delay: 0.3s; }

    /* === 7. 導航 UI === */
    .nav-dots {
      position: fixed; right: 1.5rem; top: 50%;
      transform: translateY(-50%);
      display: flex; flex-direction: column; gap: 0.5rem; z-index: 100;
    }
    .nav-dot {
      width: 8px; height: 8px; border-radius: 50%;
      background: var(--muted); cursor: pointer;
      transition: background 0.2s, transform 0.2s;
      border: none; padding: 0;
    }
    .nav-dot.active { background: var(--accent); transform: scale(1.5); }
    .slide-counter {
      position: fixed; bottom: 1.5rem; right: 1.5rem;
      font-size: 0.8rem; color: var(--muted); z-index: 100;
      font-family: monospace; letter-spacing: 0.05em;
    }
    /* G 鍵縮圖預覽 */
    .grid-preview {
      display: none; position: fixed; inset: 0;
      background: rgba(0,0,0,0.92); z-index: 200;
      padding: 2rem;
      grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
      gap: 0.75rem; overflow-y: auto;
    }
    .grid-preview.visible { display: grid; }
    .grid-thumb {
      background: var(--surface); border-radius: 0.5rem;
      aspect-ratio: 16/9; display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      cursor: pointer; padding: 0.75rem; gap: 0.4rem;
      transition: outline 0.15s;
    }
    .grid-thumb:hover { outline: 2px solid var(--accent); }
    .grid-thumb-num { font-size: 0.65rem; color: var(--muted); font-family: monospace; }
    .grid-thumb-title { font-size: 0.7rem; color: var(--text); text-align: center; line-height: 1.4; }
  </style>
</head>
<body>
  <div class="deck" id="deck">

    <!-- === 封面 === -->
    <div class="slide layout-cover" id="slide-1">
      <p class="cover-meta">{年段} ・ {科目}</p>
      <h1 class="cover-title">{課程標題}</h1>
      <p class="cover-subtitle">{副標題（選填）}</p>
      <p class="cover-author">{教師姓名（選填）}</p>
    </div>

    <!-- === 學習目標 === -->
    <div class="slide layout-objectives" id="slide-2">
      <h2 class="slide-title">學習目標</h2>
      <ul class="objectives-list animate-list">
        <li><span class="obj-tag">認知</span>能{動詞}...</li>
        <li><span class="obj-tag">情意</span>能{動詞}...</li>
        <li><span class="obj-tag">態度</span>能養成{習慣/態度}...</li>
      </ul>
    </div>

    <!-- === 其他投影片依大綱生成 === -->

  </div>

  <nav class="nav-dots" id="navDots"></nav>
  <div class="slide-counter" id="counter">1 / N</div>
  <div class="grid-preview" id="gridPreview"></div>

  <script>
    const deck = document.getElementById('deck');
    const slides = Array.from(document.querySelectorAll('.slide'));
    const dotsContainer = document.getElementById('navDots');
    const counter = document.getElementById('counter');
    const gridPreview = document.getElementById('gridPreview');
    const total = slides.length;
    let current = 0;

    // 建立導航點
    slides.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.className = 'nav-dot' + (i === 0 ? ' active' : '');
      dot.setAttribute('aria-label', `投影片 ${i+1}`);
      dot.addEventListener('click', () => goTo(i));
      dotsContainer.appendChild(dot);
    });

    // 建立縮圖預覽
    slides.forEach((s, i) => {
      const thumb = document.createElement('div');
      thumb.className = 'grid-thumb';
      const title = s.querySelector('h1,h2,.slide-title,.cover-title,.section-title,.hero-headline,.discussion-question');
      thumb.innerHTML = `<span class="grid-thumb-num">#${i+1}</span><span class="grid-thumb-title">${title ? title.textContent.slice(0,30) : ''}</span>`;
      thumb.addEventListener('click', () => { goTo(i); toggleGrid(false); });
      gridPreview.appendChild(thumb);
    });

    function goTo(n) {
      current = Math.max(0, Math.min(n, total - 1));
      slides[current].scrollIntoView({ behavior: 'smooth' });
    }

    function toggleGrid(force) {
      const show = force !== undefined ? force : !gridPreview.classList.contains('visible');
      gridPreview.classList.toggle('visible', show);
    }

    // IntersectionObserver 追蹤當前頁
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.intersectionRatio >= 0.5) {
          const idx = slides.indexOf(e.target);
          current = idx;
          document.querySelectorAll('.nav-dot').forEach((d, i) =>
            d.classList.toggle('active', i === idx));
          counter.textContent = `${idx + 1} / ${total}`;
          // 觸發進場動畫
          if (!e.target.classList.contains('active')) {
            e.target.classList.remove('active');
            void e.target.offsetWidth; // reflow
            e.target.classList.add('active');
          }
        }
      });
    }, { threshold: 0.5 });

    slides.forEach(s => io.observe(s));
    slides[0].classList.add('active');

    // 鍵盤導航
    document.addEventListener('keydown', e => {
      if (['ArrowRight', 'ArrowDown', ' '].includes(e.key)) {
        e.preventDefault(); goTo(current + 1);
      } else if (['ArrowLeft', 'ArrowUp'].includes(e.key)) {
        e.preventDefault(); goTo(current - 1);
      } else if (e.key === 'g' || e.key === 'G') {
        toggleGrid();
      } else if (e.key === 'Escape') {
        toggleGrid(false);
      }
    });
  </script>
</body>
</html>
```

### 4-B. 品質自檢（輸出前）

**P0（不達到不輸出）：**
- [ ] 所有 CSS 變數已定義，對比度符合 WCAG AA
- [ ] 年段字級已套用（sz-title / sz-h2 / sz-body 對應表格）
- [ ] 使用的版型 CSS class 完整定義於 `<style>` 內（17 種版型：cover/objectives/section/bullets/two-column/vocab/activity/discussion/hero/data/summary/timeline/quote/three-column/image-hero/pros-cons/checklist）
- [ ] `<script>` 導航功能語法正確
- [ ] 無 Emoji（用全形【】或 ▪ ★ ◆ 等 Unicode 幾何符號代替）
- [ ] 版型種類 ≥ 4 種

**P1（影響教學效果）：**
- [ ] 版型具多樣性（非連續 3 張以上相同版型）
- [ ] 學習目標使用認知／情意／態度三維格式
- [ ] vocab 版型包含注音（ㄅㄆㄇ 符號）

---

## Step 5：交付 + 微調

交付時提供：
1. 下載連結（.html 檔）
2. 投影片清單（#編號 × [版型] × 標題）
3. 使用提示：「在瀏覽器開啟後按 ← → 或空格換頁，按 G 鍵查看縮圖總覽」

---

## Canva 路徑（高設計感版本）

使用者說「Canva 版」「更精美的」「用 Canva 做」時，若 Canva MCP 已連線：
```
canva: generate-design(design_type="presentation", query="[主題] [年段]教學簡報 [風格描述]，共[N]頁")
```
未連線時：告知需啟用 Canva Connector，並切換 HTML 路徑繼續。

---

## 微調模式

生成後，用一字動詞觸發 delta 更新（直接用 `Write` 修改 HTML 檔）：

| 動詞 | 動作 |
|------|------|
| 換 N | 替換第 N 張的版型或內容 |
| 改 風格 | 重新解讀風格描述詞，更新 `:root` CSS 變數 |
| 加 N | 在第 N 張後插入新投影片 |
| 刪 N | 移除第 N 張 |
