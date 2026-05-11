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

## 版型選擇快速決策

```
素材含步驟/流程         → activity（≤5步）
素材含提問/反思         → discussion
素材含名言/金句         → hero
素材含詞彙/生字         → vocab（含注音）
素材含數字/統計         → data
素材含 A vs B 比較      → two-column
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
