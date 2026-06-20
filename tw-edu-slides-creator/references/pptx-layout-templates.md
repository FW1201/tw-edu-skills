# 版型 schema 規格（deck.json）

每張投影片 = 一個 `slide` 物件，必有 `layout`，其餘欄位依版型而定。
共用選用欄位：`kicker`（小標籤）、`tone`（`"dark"`/`"light"`，覆寫預設深淺底）、`notes`（講者備註）。

**只填欄位，不要寫座標或 hex。** 座標/字級/色彩由 `assets/slides-kit/` 依 `meta.grade`、`meta.theme` 自動套用。

## meta
```jsonc
"meta": {
  "course": "課程全名（出現在頁尾）",
  "grade": "國小低 | 國小中高 | 國中 | 高中 | 大學",
  "theme": "語文 | 數學 | 自然 | 社會 | 英語 | 藝術 | 科技 | SEL | 體育 | 生活 | 學術 | 節慶",
  "instructor": "講師",
  "date": "2026/06/18"
}
```

## 21 種版型

| layout | 用途 | 主要欄位 | 預設深淺底 |
|--------|------|----------|-----------|
| `cover` | 封面 | `subject`, `title`, `instructor`, `date` | 深 |
| `section` | 章節分隔 | `number`, `kicker`, `title` | 深 |
| `objectives` | 三向學習目標 | `title`, `items:[{kind,text}]`（≤3） | 淺 |
| `bullets` | 條列重點 | `title`, `items:[string]`（依年級上限） | 淺 |
| `two-column` | 雙欄對比 | `title`, `columns:[{heading,items:[]}]`（2） | 淺 |
| `vocab` | 詞彙卡（含注音） | `title`, `items:[{word,zhuyin,def}]`（≤6） | 淺 |
| `activity` | 課堂活動步驟 | `title`, `time`, `group`, `steps:[string]`（≤5） | 淺 |
| `discussion` | 討論提問 | `question`, `thinkTime` | 淺 |
| `hero` | 大字強調 | `kicker`, `text` | 自帶 primary 底 |
| `data` | 數據展示 | `title`, `stats:[{value,label,desc}]`（≤4） | 淺 |
| `summary` | 重點回顧 | `title`, `items:[{key,value}]`（≤5） | 淺 |
| `timeline` | 時間軸 | `title`, `points:[{year,event}]`（≤4） | 淺 |
| `quote` | 名言引用 | `text`, `cite` | 深 |
| `three-column` | 三欄卡片 | `title`, `cards:[{icon,title,body}]`（3） | 淺 |
| `image-hero` | 圖文分割 | `title`, `body`, `image`（路徑/URL，缺則佔位） | 淺 |
| `pros-cons` | 優缺點 | `title`, `pros:[]`, `cons:[]`, `prosLabel`, `consLabel` | 淺 |
| `checklist` | 學習自評 | `title`, `items:[string]`（≤6）, `reflect` | 淺 |
| `matrix` | 2×2 象限 | `title`, `quadrants:[{heading,text}]`（4） | 淺 |
| `process-flow` | 流程圖 | `title`, `steps:[{label}]`（≤4） | 淺 |
| `concept-web` | 概念網 | `title`, `center`, `nodes:[string]`（≤6） | 淺 |
| `closing` | 結語 | `kicker`, `title`, `subtitle` | 深 |

## 內容類型 → 版型 對應（含 Bloom 分層）

| 內容特徵 | 建議版型 | Bloom |
|----------|----------|-------|
| 名言一句 | `quote` | 理解 |
| 步驟/程序 | `process-flow` / `activity` | 應用 |
| ≥3 時間點 | `timeline` | 分析 |
| 詞語需解釋 | `vocab` | 記憶 |
| A vs B | `two-column` / `pros-cons` | 分析 |
| ≤4 數據 | `data` | 理解 |
| 三個並列概念 | `three-column` | 理解 |
| 四象限/矩陣 | `matrix` | 分析 |
| 概念關係網 | `concept-web` | 分析/創造 |
| 課堂活動 | `activity` | 應用/創造 |
| 開放討論 | `discussion` | 評鑑/創造 |
| 自我檢核 | `checklist` | 評鑑 |

## 範例
完整可建置範例見 `assets/slides-kit/examples/guoyu-7.json`（七年級國文・10 張）。

## 每張的 notes（講者備註）
任何 slide 加 `"notes": "..."` 即寫入 PowerPoint 講者備註（Delta `加稿N`）。
