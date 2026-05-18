# HTML Layout Templates v1.0
# tw-edu-slides-creator 版型骨架參考庫

> Claude 在 Step 4 生成 HTML 時讀取此文件，作為 11 個版型的 CSS 與 HTML 骨架標準。
> **規則**：直接使用此骨架，依內容填入 `{佔位符}`，不得自行發明新 class 名稱。

---

## 通用規則

- 所有版型容器必須是 `<div class="slide layout-{key}">` 結構
- 動畫靠 `.slide.active` + `nth-child delay` 自動觸發，無需手動加 class
- 圖片佔位用 `<figure class="img-placeholder"><p>[在此插入圖片]</p></figure>`，不使用 Emoji
- 全形符號列表：【】、▪ ▸ ▶ ★ ◆ ◎ ○ ● ■ □ — 可任意使用

---

## 01 cover — 封面

**用途**：每份簡報第一張，呈現課程名稱、年段、教師。

```html
<div class="slide layout-cover" id="slide-{N}">
  <p class="cover-meta">{年段} ・ {科目}</p>
  <h1 class="cover-title">{主標題}</h1>
  <p class="cover-subtitle">{副標題（選填，可省略）}</p>
  <p class="cover-author">{教師姓名（選填，可省略）}</p>
</div>
```

**CSS 要點（已含於 SKILL.md 主樣式）：**
- `cover-title`：最大字體 `--sz-title`，字重 900，顏色 `--primary`
- `::after` 偽元素：右下角大圓形裝飾（accent 色，opacity 0.08）
- 整體左對齊（`align-items: flex-start`）

---

## 02 objectives — 學習目標

**用途**：呈現認知／情意／態度三維學習目標，通常排在封面後。

```html
<div class="slide layout-objectives" id="slide-{N}">
  <h2 class="slide-title">學習目標</h2>
  <ul class="objectives-list">
    <li><span class="obj-tag">認知</span>能{Bloom 動詞}......</li>
    <li><span class="obj-tag">情意</span>能{Bloom 動詞}......</li>
    <li><span class="obj-tag">態度</span>能養成{習慣/態度}......</li>
  </ul>
</div>
```

**Bloom 動詞參考（依年段）：**
- 國小低：說出、指出、做做看、比一比
- 國小中高：列舉、解釋、使用、分析
- 國中：記憶、摘要、應用、評估、設計
- 高中：定義、詮釋、實作、批判、建構

---

## 03 section — 段落分隔

**用途**：單元過渡、章節開頭，視覺重版型，每 5 張一次。

```html
<div class="slide layout-section" id="slide-{N}">
  <div class="section-num">{數字，如 01 02}</div>
  <div class="section-inner">
    <p class="section-label">{UNIT / PART / 單元等上層標籤}</p>
    <h2 class="section-title">{段落主標題}</h2>
    <p class="section-sub">{副標（選填）}</p>
  </div>
</div>
```

**CSS 要點：**
- `section-num`：極大字體（18vw），`--accent` 色，opacity 0.18，position absolute 置中背景
- `section-inner`：position relative，z-index 1，遮蓋數字背景
- 整體水平垂直置中

---

## 04 bullets — 條列重點

**用途**：一般概念說明、重點列舉，最常用版型，上限依年段 `--max-bullets`。

```html
<div class="slide layout-bullets" id="slide-{N}">
  <h2 class="slide-title">{標題}</h2>
  <ul class="bullets-list">
    <li>{重點一（簡短，單行原則）}</li>
    <li>{重點二}</li>
    <li>{重點三（國小低年級最多 3 條）}</li>
    <!-- 依年段控制條數，不超過 --max-bullets -->
  </ul>
</div>
```

**CSS 要點：**
- 每條前置彩色圓點（`::before`，accent 色）
- 字體 `--sz-body`，行高 1.5

---

## 05 two-column — 雙欄比較

**用途**：概念 vs 例子、文言 vs 白話、兩種方法比較。適合國中以上。

```html
<div class="slide layout-two-column" id="slide-{N}">
  <h2 class="slide-title">{整體標題}</h2>
  <div class="col-wrap">
    <div class="col">
      <p class="col-title">{左欄標題}</p>
      <ul>
        <li>{左欄項目一}</li>
        <li>{左欄項目二}</li>
      </ul>
    </div>
    <div class="col">
      <p class="col-title">{右欄標題}</p>
      <ul>
        <li>{右欄項目一}</li>
        <li>{右欄項目二}</li>
      </ul>
    </div>
  </div>
</div>
```

**替代用法**：右欄可用 `<p>` 段落取代 `<ul>`，適合長文本對照。

---

## 06 vocab — 詞彙定義

**用途**：生字詞彙、術語解釋，國語文/文學課必備，含注音符號。

```html
<div class="slide layout-vocab" id="slide-{N}">
  <h2 class="slide-title">{標題，如「本課生字」「關鍵詞彙」}</h2>
  <div class="vocab-grid">
    <div class="vocab-card">
      <p class="vocab-word">{詞語，如：蹣跚}</p>
      <p class="vocab-phonetic">{注音，如：ㄆㄢˊ ㄕㄢ}</p>
      <p class="vocab-def">{定義：行走不穩、搖晃貌}</p>
      <p class="vocab-example">{例句（選填）}</p>
    </div>
    <!-- 重複 vocab-card，最多 6 張卡片（依螢幕空間自動排列） -->
  </div>
</div>
```

**注音格式規則**：
- 使用 ㄅㄆㄇㄈ 注音符號，聲調符號（ˊˋˇ˙）加在最後一個符號後
- 不用羅馬拼音代替

---

## 07 activity — 課堂活動

**用途**：步驟性任務、實作流程，含時間與分組說明。

```html
<div class="slide layout-activity" id="slide-{N}">
  <h2 class="slide-title">{活動名稱}</h2>
  <p class="activity-meta">◎ {時間，如：5 分鐘} ・ {分組，如：個人 / 小組}</p>
  <ol class="steps-list">
    <li>
      <span class="step-num">1</span>
      <span>{步驟說明（動詞開頭，簡短）}</span>
    </li>
    <li>
      <span class="step-num">2</span>
      <span>{步驟說明}</span>
    </li>
    <!-- 最多 5 個步驟；國小低年級最多 3 個 -->
  </ol>
</div>
```

**CSS 要點：**
- `step-num`：圓形徽章，accent 背景，白字

---

## 08 discussion — 思考討論

**用途**：核心提問、反思題、辯論導入，重版型，視覺焦點強。

```html
<div class="slide layout-discussion" id="slide-{N}">
  <div class="discussion-inner">
    <span class="discussion-timer">思考時間：{N} 分鐘</span>
    <h2 class="discussion-question">{問題句，結尾加「？」}</h2>
    <p class="discussion-hint">{提示文字（選填，如：可以從...角度思考）}</p>
  </div>
</div>
```

**CSS 要點：**
- `discussion-question`：`--sz-h2`，字重 900，`--primary` 色
- `discussion-timer`：邊框徽章樣式（accent 色 border）
- 整體水平垂直置中，最大寬度 80%

---

## 09 hero — 核心訊息大字

**用途**：衝擊開場、名言金句、章節過渡揭示，重版型。

```html
<div class="slide layout-hero" id="slide-{N}">
  <div class="hero-inner">
    <div class="hero-bar"></div>
    <h1 class="hero-headline">{核心訊息或名言（建議 ≤30 字）}</h1>
    <p class="hero-subline">{副標說明（選填，可省略）}</p>
  </div>
</div>
```

**應用場景：**
- 課文精華句：`"天行健，君子以自強不息"`（附來源於副標）
- 核心主張：`「閱讀是最廉價的旅行」`
- 過渡提問（較短）：`「你有多了解台灣？」`（詳細提問用 discussion 版型）

---

## 10 data — 數據/統計亮點

**用途**：統計數字、百分比、量化事實；也可用於三要素並列呈現。

```html
<div class="slide layout-data" id="slide-{N}">
  <h2 class="slide-title">{標題}</h2>
  <div class="data-grid">
    <div class="data-item">
      <span class="data-value">{數字，如：87%}</span>
      <span class="data-label">{指標名稱}</span>
      <span class="data-desc">{一行補充說明（選填）}</span>
    </div>
    <div class="data-item">
      <span class="data-value">{數字}</span>
      <span class="data-label">{指標名稱}</span>
    </div>
    <!-- 最多 4 個 data-item，自動 grid 排列 -->
  </div>
</div>
```

**三要素用法（無數字時）：**
將 `data-value` 改為大型圖示符號（如 ★ ◆ ▶），`data-label` 為要素名稱，`data-desc` 為說明文字。

---

## 11 summary — 重點整理

**用途**：課程尾段複習，以關鍵詞 + 說明的格式整理要點。

```html
<div class="slide layout-summary" id="slide-{N}">
  <h2 class="slide-title">{標題，如「本節重點」}</h2>
  <div class="summary-list">
    <div class="summary-item">
      <span class="summary-key">{關鍵詞}</span>
      <span class="summary-val">{一句說明}</span>
    </div>
    <div class="summary-item">
      <span class="summary-key">{關鍵詞}</span>
      <span class="summary-val">{一句說明}</span>
    </div>
    <!-- 建議 3–6 個項目，依年段調整 -->
  </div>
</div>
```

---

## 12 timeline — 時間軸

**用途**：歷史事件、人物傳記、故事發展順序，需 ≥ 3 個帶年份/日期的節點。

```html
<div class="slide layout-timeline" id="slide-{N}">
  <h2 class="slide-title">{標題，如「台灣 AI 發展里程碑」}</h2>
  <div class="timeline-track">
    <div class="tl-item">
      <div class="tl-dot"></div>
      <div class="tl-year">{年份，如：2022}</div>
      <div class="tl-content">
        <p class="tl-label">{事件名稱}</p>
        <p class="tl-desc">{一行說明（選填）}</p>
      </div>
    </div>
    <div class="tl-item">
      <div class="tl-dot"></div>
      <div class="tl-year">{年份}</div>
      <div class="tl-content">
        <p class="tl-label">{事件名稱}</p>
      </div>
    </div>
    <!-- 建議 3–6 個 tl-item；超過 6 個改用 bullets 版型 -->
  </div>
</div>
```

**CSS 要點：**
```css
/* layout-timeline */
.layout-timeline { align-items: flex-start; }
.timeline-track {
  position: relative; width: 100%;
  display: flex; flex-direction: column; gap: 1.5rem;
  padding-left: 2.5rem;
}
.timeline-track::before {
  content: ''; position: absolute; left: 0.55rem; top: 0.4rem; bottom: 0.4rem;
  width: 2px; background: var(--accent); opacity: 0.4;
}
.tl-item { display: flex; align-items: flex-start; gap: 1.25rem; position: relative; }
.tl-dot {
  position: absolute; left: -2.07rem; top: 0.35rem;
  width: 0.9rem; height: 0.9rem; border-radius: 50%;
  background: var(--accent); flex-shrink: 0;
  box-shadow: 0 0 0 3px var(--bg), 0 0 0 5px var(--accent);
}
.tl-year {
  font-size: var(--sz-small); font-weight: 700; color: var(--accent);
  white-space: nowrap; min-width: 3.5rem; padding-top: 0.1rem;
}
.tl-content { flex: 1; }
.tl-label { font-size: var(--sz-body); font-weight: 700; color: var(--text); line-height: 1.4; }
.tl-desc { font-size: var(--sz-small); color: var(--muted); margin-top: 0.25rem; line-height: 1.5; }
```

---

## 13 quote — 大字金句

**用途**：名言、課文精華句、核心主張、人物引言，最多 1 句，需附出處。

```html
<div class="slide layout-quote" id="slide-{N}">
  <div class="quote-inner">
    <div class="quote-mark">&#8220;</div>
    <p class="quote-text">{金句正文（建議 ≤ 40 字）}</p>
    <div class="quote-source">
      <span class="quote-author">{人物/作品名稱，如：孔子《論語》}</span>
      <span class="quote-context">{出處補充（選填，如：學而篇）}</span>
    </div>
  </div>
</div>
```

**CSS 要點：**
```css
/* layout-quote */
.layout-quote { justify-content: center; align-items: center; text-align: center; }
.quote-inner { max-width: 82%; position: relative; }
.quote-mark {
  font-size: clamp(5rem, 12vw, 9rem); font-weight: 900;
  color: var(--accent); opacity: 0.18; line-height: 1;
  position: absolute; top: -1.5rem; left: -1rem;
  pointer-events: none; user-select: none;
  font-family: Georgia, serif;
}
.quote-text {
  font-size: var(--sz-h2); font-weight: 700; color: var(--primary);
  line-height: 1.7; position: relative; z-index: 1; margin-bottom: 1.5rem;
}
.quote-source {
  display: flex; flex-direction: column; align-items: center; gap: 0.25rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
}
.quote-author { font-size: var(--sz-body); font-weight: 700; color: var(--text); }
.quote-context { font-size: var(--sz-small); color: var(--muted); }
```

---

## 14 three-column — 三欄並列

**用途**：同層級的三個概念/要素/步驟，橫向並列，視覺對等。

```html
<div class="slide layout-three-column" id="slide-{N}">
  <h2 class="slide-title">{標題}</h2>
  <div class="three-col-wrap">
    <div class="three-col">
      <div class="col3-icon">{符號，如 ▶ ★ ◆ ●}</div>
      <p class="col3-title">{欄標題}</p>
      <p class="col3-body">{說明文字（1–3 行）}</p>
    </div>
    <div class="three-col">
      <div class="col3-icon">{符號}</div>
      <p class="col3-title">{欄標題}</p>
      <p class="col3-body">{說明文字}</p>
    </div>
    <div class="three-col">
      <div class="col3-icon">{符號}</div>
      <p class="col3-title">{欄標題}</p>
      <p class="col3-body">{說明文字}</p>
    </div>
  </div>
</div>
```

**CSS 要點：**
```css
/* layout-three-column */
.layout-three-column { align-items: flex-start; }
.three-col-wrap {
  display: grid; grid-template-columns: 1fr 1fr 1fr;
  gap: 1.25rem; width: 100%;
}
.three-col {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 0.875rem;
  padding: 1.5rem 1.25rem;
  display: flex; flex-direction: column; align-items: center;
  text-align: center; gap: 0.75rem;
  position: relative; overflow: hidden;
}
.three-col::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--accent), var(--primary));
}
.col3-icon {
  font-size: var(--sz-title); color: var(--accent); line-height: 1;
}
.col3-title { font-size: var(--sz-body); font-weight: 700; color: var(--primary); }
.col3-body { font-size: var(--sz-small); color: var(--muted); line-height: 1.6; }
```

---

## 15 image-hero — 圖片全版

**用途**：需要圖片輔助說明的版型，如地圖、插圖、照片、視覺引導。無圖時顯示佔位框。

```html
<div class="slide layout-image-hero" id="slide-{N}">
  <div class="img-hero-box">
    <!-- 有圖片時：<img src="{路徑}" alt="{描述}"> -->
    <!-- 無圖片時（預設）： -->
    <div class="img-hero-placeholder">[在此插入圖片]<br><span>{建議插入：圖片描述，如「台灣地形圖」}</span></div>
  </div>
  <div class="img-hero-caption">
    <h2 class="img-hero-title">{圖片標題（選填）}</h2>
    <p class="img-hero-desc">{說明文字（選填，1–2 行）}</p>
    <p class="img-hero-source">{來源 · 說明（選填）}</p>
  </div>
</div>
```

**CSS 要點：**
```css
/* layout-image-hero */
.layout-image-hero { justify-content: flex-start; align-items: stretch; gap: 1.25rem; }
.img-hero-box {
  flex: 0 0 65%; border-radius: 0.875rem; overflow: hidden;
  background: var(--surface); border: 1px solid var(--border);
}
.img-hero-box img { width: 100%; height: 100%; object-fit: cover; }
.img-hero-placeholder {
  width: 100%; height: 100%; min-height: 200px;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center; gap: 0.5rem;
  color: var(--muted); font-size: var(--sz-body);
  border: 2px dashed var(--border);
  border-radius: 0.875rem;
}
.img-hero-placeholder span { font-size: var(--sz-small); opacity: 0.7; }
.img-hero-caption {
  flex: 1; display: flex; flex-direction: column;
  justify-content: center; gap: 0.5rem;
}
.img-hero-title { font-size: var(--sz-h2); font-weight: 700; color: var(--primary); }
.img-hero-desc { font-size: var(--sz-body); color: var(--text); line-height: 1.6; }
.img-hero-source { font-size: var(--sz-small); color: var(--muted); margin-top: 0.25rem; }
```

---

## 16 pros-cons — 優劣分析

**用途**：正反立場、優缺點比較、議題討論，適合議論文教學或辯論導入。

```html
<div class="slide layout-pros-cons" id="slide-{N}">
  <h2 class="slide-title">{議題標題}</h2>
  <div class="pc-wrap">
    <div class="pc-col pc-pros">
      <p class="pc-header">&#9650; 支持 / 優點</p>
      <ul class="pc-list">
        <li>{優點一}</li>
        <li>{優點二}</li>
        <li>{優點三（選填）}</li>
      </ul>
    </div>
    <div class="pc-divider"></div>
    <div class="pc-col pc-cons">
      <p class="pc-header">&#9660; 反對 / 缺點</p>
      <ul class="pc-list">
        <li>{缺點一}</li>
        <li>{缺點二}</li>
        <li>{缺點三（選填）}</li>
      </ul>
    </div>
  </div>
</div>
```

**CSS 要點：**
```css
/* layout-pros-cons */
.layout-pros-cons { align-items: flex-start; }
.pc-wrap {
  display: grid; grid-template-columns: 1fr auto 1fr;
  gap: 0; width: 100%; align-items: stretch;
}
.pc-col {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 0.875rem;
  padding: 1.25rem 1.5rem;
  display: flex; flex-direction: column; gap: 0.75rem;
}
.pc-divider {
  width: 1px; background: var(--border);
  margin: 0 1.25rem; flex-shrink: 0;
}
.pc-header {
  font-size: var(--sz-small); font-weight: 700;
  letter-spacing: 0.08em; margin-bottom: 0.25rem;
}
.pc-pros .pc-header { color: var(--accent); }
.pc-cons .pc-header { color: var(--muted); }
.pc-list { list-style: none; display: flex; flex-direction: column; gap: 0.6rem; }
.pc-list li {
  font-size: var(--sz-body); padding-left: 1.1em;
  position: relative; line-height: 1.5; color: var(--text);
}
.pc-pros .pc-list li::before {
  content: '+'; position: absolute; left: 0;
  color: var(--accent); font-weight: 700;
}
.pc-cons .pc-list li::before {
  content: '-'; position: absolute; left: 0;
  color: var(--muted); font-weight: 700;
}
```

---

## 17 checklist — 學習清單

**用途**：課堂任務確認、學習評量項目、課後作業、自我評估量表。

```html
<div class="slide layout-checklist" id="slide-{N}">
  <h2 class="slide-title">{清單標題，如「今日學習任務」「學習自我評量」}</h2>
  <ul class="checklist-list">
    <li class="checklist-item">
      <span class="check-box">&#9744;</span>
      <span class="check-label">{任務/評量項目說明}</span>
    </li>
    <li class="checklist-item">
      <span class="check-box">&#9744;</span>
      <span class="check-label">{任務/評量項目說明}</span>
    </li>
    <li class="checklist-item">
      <span class="check-box">&#9744;</span>
      <span class="check-label">{任務/評量項目說明}</span>
    </li>
    <!-- 建議 3–6 項；依年段控制項目數 -->
  </ul>
  <p class="checklist-note">{底部備注（選填，如：完成後請舉手 / 截止時間）}</p>
</div>
```

**CSS 要點：**
```css
/* layout-checklist */
.layout-checklist { align-items: flex-start; }
.checklist-list { list-style: none; width: 100%; display: flex; flex-direction: column; gap: 0.75rem; }
.checklist-item {
  display: flex; align-items: center; gap: 1rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 0.75rem; padding: 0.9rem 1.25rem;
  cursor: default;
  transition: border-color 0.2s;
}
.checklist-item:hover { border-color: var(--accent); }
.check-box {
  font-size: var(--sz-h2); color: var(--accent);
  flex-shrink: 0; line-height: 1;
  transition: all 0.2s;
}
.checklist-item:hover .check-box::before { content: '&#9745;'; }
.check-label { font-size: var(--sz-body); color: var(--text); line-height: 1.5; }
.checklist-note {
  font-size: var(--sz-small); color: var(--muted);
  margin-top: 0.75rem; padding-left: 0.5rem;
  border-left: 3px solid var(--accent);
}
```

---

## 版型選擇快速決策

```
素材含步驟/流程         → activity（≤5步）
素材含年份/日期序列     → timeline（≥3 個時間點）
素材含提問/反思         → discussion
素材含名言/金句/人物引言 → quote
素材含詞彙/生字         → vocab（含注音）
素材含數字/統計         → data
素材含 A vs B 比較      → two-column
素材含正反立場/優缺點   → pros-cons
素材含 3 個同層級概念   → three-column
素材需圖片輔助說明      → image-hero
課堂任務清單/評量項目   → checklist
條列重點（一般）         → bullets
章節/單元過渡           → section
課程開始                 → cover + objectives
課程結束                 → summary
```

---

## 圖片佔位規範

當版型需要圖片但無實際圖檔時：

```html
<figure class="img-placeholder">
  <div class="img-placeholder-box">[在此插入圖片]</div>
  <figcaption>{來源 · 圖片說明（可省略）}</figcaption>
</figure>
```

補充 CSS（加入 `<style>` 內）：
```css
.img-placeholder-box {
  background: var(--surface);
  border: 2px dashed var(--border);
  border-radius: 0.5rem;
  display: flex; align-items: center; justify-content: center;
  min-height: 200px;
  color: var(--muted); font-size: var(--sz-small);
}
figcaption { font-size: var(--sz-small); color: var(--muted); margin-top: 0.5rem; }
```
