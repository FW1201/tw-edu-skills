# 教學簡報設計原則與版型庫 v2.0
# tw-edu-slides-creator 參考文件

> **v2.0 更新（2026-05-23）**：本檔案原有的「HTML layout key」（如 `layout-bullets`、CSS class 選擇器）已遷移為 TSX 元件對應（如 `04-bullets/index.tsx`）。所有 17 種版型的完整 TSX 程式碼範例見 `tsx-layout-templates.md`；Tailwind 色值與字型對照見 `tailwind-themes.md`。

> Claude 在 Step 2.5 內容分析時讀取此文件，作為版型選擇與設計判斷的依據。

---

## 一、25 種版型速查表

| # | 版型鍵值 | 中文名稱 | 最適內容類型 | 適用年級 |
|---|---------|---------|------------|---------|
| 1 | `content` | 條列文字 | 一般概念說明、重點列舉 | 全年級 |
| 2 | `discussion` | 思考討論 | 提問、反思、辯論題 | 全年級 |
| 3 | `two_column` | 左右雙欄 | 概念+例子、中英對照、補充說明 | 國中↑ |
| 4 | `activity` | 課堂活動 | 步驟性任務、實作流程（≤4步）| 全年級 |
| 5 | `vocab` | 生字詞彙 | 詞彙列表、生字、術語 | 國小↑ |
| 6 | `timeline` | 時間軸 | 有年份/日期的歷史/傳記/事件 | 全年級 |
| 7 | `comparison` | 比較對照 | A vs B、文言白話、兩種方法 | 全年級 |
| 8 | `big_quote` | 大字金句 | 名言、課文精華句、核心主張 | 全年級 |
| 9 | `data_highlight` | 數據亮點 | 統計數字、百分比、量化事實（≤4個）| 國中↑ |
| 10 | `image_focus` | 圖片聚焦 | 需要圖片說明的概念、地圖、照片 | 全年級 |
| 11 | `process_flow` | 流程步驟 | 科學實驗、操作程序（含箭頭關係，≤5步）| 全年級 |
| 12 | `kanban` | 三欄分類 | KWL表、分類整理、三類對比 | 全年級 |
| 13 | `concept_web` | 概念放射 | 核心概念+子概念（4-6個分支）| 全年級 |
| 14 | `pros_cons` | 優劣分析 | 正反立場、優缺點、議題討論 | 國中↑ |
| 15 | `section_cover` | 章節封面 | 單元分隔、章節開頭 | 全年級 |
| 16 | `hero_message` | 英雄訊息 | 衝擊開場、主題揭示、章節過渡 | 全年級 |
| 17 | `three_cards` | 三卡並列 | 三要素、三特徵、三步驟（同層級）| 全年級 |
| 18 | `four_quadrants` | 四象限矩陣 | SWOT、2×2分析、四向度比較 | 高中↑ |
| 19 | `icon_list` | 圖示條列 | 特徵列舉、原則清單（帶視覺標記）| 全年級 |
| 20 | `stat_bar` | 數據長條 | 量化比較（≤5項，有相對大小關係）| 國中↑ |
| 21 | `pyramid` | 金字塔層次 | 優先級、馬斯洛需求、層次概念 | 國中↑ |
| 22 | `agenda` | 議程目錄 | 課程開頭目錄、複習大綱 | 全年級 |
| 23 | `testimonial` | 人物引言 | 真實案例、見證、人物觀點 | 國中↑ |
| 24 | `split_screen` | 非對稱分割 | 強視覺對比、主從關係呈現 | 全年級 |
| 25 | `blank_canvas` | 空白模板 | 需要師生現場填寫的互動投影片 | 全年級 |

---

## 二、內容特徵 → 版型映射規則

Claude 在分析輸入素材時，依以下規則判斷每張投影片的最佳版型：

```
輸入特徵                        → 建議版型
────────────────────────────────────────────────
含名言/精華句子（1句，強調）      → big_quote
含步驟/程序（含箭頭、先後順序）  → process_flow 或 activity
含年份/日期序列（≥3個時間點）    → timeline
含詞彙/生字需解釋                → vocab
含比較（A vs B 結構）            → comparison 或 pros_cons
含圖表/統計數據（≤4個數字）      → data_highlight
含統計比較（有大小關係）          → stat_bar
含課堂任務/操作步驟              → activity
含3個並列概念（同層級）          → three_cards
含4個面向/象限                   → four_quadrants
含層次/優先級（上寬下窄）        → pyramid
含核心概念+子概念（放射狀）      → concept_web
含正反立場/優缺點                → pros_cons
含需要圖片輔助的概念             → image_focus
含人物/真實案例引言              → testimonial
分類整理（3類）                  → kanban
需要視覺衝擊/過渡                → hero_message 或 section_cover
需要師生共同填寫                 → blank_canvas
含課程目錄/大綱                  → agenda
一般概念說明（2欄）              → two_column
一般概念說明（1欄）              → content
提問/反思                        → discussion
```

---

## 三、一堂課簡報的典型結構示例

```
封面（title）
↓
目錄（agenda）                ← 可選
↓
學習目標（objectives）
↓
先備知識激活（hero_message）  ← 大字提問 或 image_focus
↓
概念一（content / two_column）
↓
概念二（concept_web / timeline / comparison）
↓
數據/圖表（data_highlight / stat_bar）← 若有
↓
詞彙整理（vocab）              ← 國語文必有
↓
課堂活動（activity）
↓
思考討論（discussion）
↓
重點整理（summary）
↓
課後任務（closing）
```

**版型多樣性原則**：一份 15 張的簡報，應包含 ≥4 種不同版型，避免連續 3 張以上使用相同版型。

---

## 四、色盤 × 課程類型配對指南

| 色盤 | 鍵值 | 最適課程類型 |
|------|------|------------|
| 簡約現代 | `modern` | 正式課堂、考試複習、一般教學 |
| 活潑彩色 | `colorful` | 低年級、遊戲化學習、互動課 |
| 深色沉穩 | `dark` | 高中進階、程式設計、期末報告 |
| 台灣特色 | `local` | 本土語言、文化課、鄉土教育 |
| 自然清新 | `nature` | 自然科學、環境教育、健康課 |
| 科技感 | `tech` | 資訊科技、Vibe Coding、AI課程 |
| 溫暖橙調 | `warm` | 藝術、社會、生活科技、SEL課程 |
| 學術紫 | `purple` | 文學、哲學、研究報告、碩論簡報 |

---

## 五、布魯姆動詞對照表（學習目標撰寫參考）

| 認知層次 | 國小低年級 | 國小中高年級 | 國中 | 高中 |
|---------|-----------|------------|------|------|
| 記憶 | 說出、指出 | 列舉、認識 | 記憶、背誦 | 確認、定義 |
| 理解 | 說明、比一比 | 解釋、描述 | 解釋、摘要 | 詮釋、整理 |
| 應用 | 做做看、試試看 | 使用、操作 | 應用、執行 | 實作、使用 |
| 分析 | 找一找不同 | 分析、比較 | 分析、比較 | 區辨、組織 |
| 評鑑 | 說說為什麼好/不好 | 判斷、選擇 | 評估、判斷 | 批判、論證 |
| 創造 | 畫一畫、做一個 | 設計、創作 | 設計、規劃 | 建構、提案 |

---

## 六、各版型的 JSON 資料格式規範

供 Step 2.5 輸出 JSON 時參照：

```json
// content — 一般條列
{"layout": "content", "title": "...", "bullets": ["...", "..."], "note": "..."}

// discussion — 思考提問
{"layout": "discussion", "question": "...", "thinking_time": "2"}

// two_column — 左右雙欄
{"layout": "two_column", "title": "...", "left_title": "...", "left_bullets": ["..."], "right_title": "...", "right_text": "..."}

// activity — 課堂活動
{"layout": "activity", "title": "...", "steps": ["步驟一...", "步驟二..."], "time_min": "5", "grouping": "個人/小組"}

// vocab — 生字詞彙
{"layout": "vocab", "title": "生字詞彙", "vocab_list": [{"word": "...", "phonetic": "...", "definition": "...", "example": "..."}]}

// timeline — 時間軸
{"layout": "timeline", "title": "...", "events": [{"year": "1895", "label": "馬關條約"}]}

// comparison — 比較對照
{"layout": "comparison", "title": "...", "left_label": "文言文", "left_items": ["..."], "right_label": "白話文", "right_items": ["..."]}

// big_quote — 大字金句
{"layout": "big_quote", "quote": "天行健，君子以自強不息", "source": "《易經》乾卦"}

// data_highlight — 數據亮點
{"layout": "data_highlight", "title": "...", "data_points": [{"value": "87%", "label": "閱讀理解率", "icon": "[#]"}]}

// image_focus — 圖片聚焦
{"layout": "image_focus", "title": "...", "caption": "說明文字...", "image_hint": "建議插入：台灣地形圖"}

// process_flow — 流程步驟
{"layout": "process_flow", "title": "...", "steps": [{"icon": "01", "label": "觀察", "desc": "仔細觀察現象"}]}

// kanban — 三欄分類
{"layout": "kanban", "title": "KWL 學習地圖", "columns": [{"header": "已知 (K)", "items": ["..."]}, {"header": "想知道 (W)", "items": ["..."]}, {"header": "學到 (L)", "items": ["..."]}]}

// concept_web — 概念放射
{"layout": "concept_web", "center": "核心概念", "branches": [{"label": "子概念一", "detail": "說明..."}, ...]}

// pros_cons — 優劣分析
{"layout": "pros_cons", "title": "...", "pros": ["優點一", "優點二"], "cons": ["缺點一", "缺點二"]}

// section_cover — 章節封面
{"layout": "section_cover", "section_num": "第二單元", "section_title": "唐詩賞析"}

// hero_message — 英雄訊息
{"layout": "hero_message", "headline": "「你有多了解台灣？」", "subtext": "今天，我們一起探索這片土地的故事"}

// three_cards — 三卡並列
{"layout": "three_cards", "title": "...", "cards": [{"icon": "▪", "title": "卡片一", "desc": "說明..."}, ...]}

// four_quadrants — 四象限
{"layout": "four_quadrants", "title": "SWOT 分析", "quadrants": [{"label": "優勢 (S)", "items": ["..."]}, {"label": "劣勢 (W)", "items": ["..."]}, {"label": "機會 (O)", "items": ["..."]}, {"label": "威脅 (T)", "items": ["..."]}]}

// icon_list — 圖示條列
{"layout": "icon_list", "title": "...", "items": [{"icon": "★", "heading": "標題", "desc": "說明文字"}]}

// stat_bar — 數據長條
{"layout": "stat_bar", "title": "...", "bars": [{"label": "項目一", "value": 75, "unit": "%"}]}

// pyramid — 金字塔層次
{"layout": "pyramid", "title": "...", "levels": [{"label": "最高層", "desc": "說明"}, ...]}

// agenda — 議程目錄
{"layout": "agenda", "title": "本節課程大綱", "items": [{"num": "01", "title": "先備知識", "time": "5分鐘"}]}

// testimonial — 人物引言
{"layout": "testimonial", "quote": "...", "person": "孔子", "role": "春秋時期思想家", "context": "《論語》學而篇"}

// split_screen — 非對稱分割
{"layout": "split_screen", "left_text": "大標題", "left_sub": "副標題", "right_bullets": ["重點一", "重點二"]}

// blank_canvas — 空白模板
{"layout": "blank_canvas", "title": "請填寫你的想法", "prompt": "（留空供師生現場填寫）"}
```

---

## 六、25 版型 → 17 HTML 版型對應表

V4.1 擴充為 17 個 HTML 版型，覆蓋 99% 教學場景：

| HTML 版型 key | 對應舊版型 | 說明 |
|-------------|-----------|------|
| `cover` | cover | 課程封面 |
| `objectives` | objectives | 三維學習目標 |
| `section` | section_cover | 章節過渡 |
| `bullets` | content, icon_list | 條列重點 |
| `two-column` | two_column, comparison | 雙欄比較 |
| `vocab` | vocab | 詞彙定義（含注音） |
| `activity` | activity, process_flow | 步驟性任務 |
| `discussion` | discussion | 思考提問 |
| `hero` | hero_message | 核心大字 |
| `data` | data_highlight, stat_bar | 數據亮點 |
| `summary` | summary, agenda, four_quadrants, pyramid | 整理複習 |
| `timeline` | timeline | 時間軸（≥3 時間點） |
| `quote` | big_quote, testimonial | 大字金句/人物引言 |
| `three-column` | three_cards, kanban | 三欄並列/分類 |
| `image-hero` | image_focus | 圖片全版 |
| `pros-cons` | pros_cons | 優劣正反分析 |
| `checklist` | blank_canvas | 學習清單/任務確認 |

> 若教材有 concept_web、split_screen 等特殊需求，
> 於 `bullets` 或 `two-column` 版型內以 CSS inline style 局部調整。

---

## 七、風格描述詞 → CSS 變數對應示例表

| 描述詞 | --bg | --surface | --primary | --accent | --text | --muted |
|--------|------|-----------|-----------|---------|--------|---------|
| 科技感 深色 未來 | #0D1117 | #161B22 | #00D4FF | #7B2FFF | #E6EDF3 | #8B949E |
| 溫暖 活潑 色彩 | #FFFAF0 | #FFF3D6 | #E8541A | #FFD166 | #2D2D2D | #888070 |
| 簡約 專業 清晰 | #FFFFFF | #F4F6F8 | #1A73E8 | #34A853 | #202124 | #9AA0A6 |
| 清新 自然 生態 | #F0FAF4 | #DFF2E8 | #1B7A4E | #7BC67E | #1A2E25 | #6A9E7E |
| 典雅 學術 沉穩 | #F8F6F2 | #EDE9E2 | #2C3E6D | #C0392B | #1A1A2E | #787060 |
| 活潑 低年級 遊戲 | #FFF8E1 | #FFE8A8 | #D81B60 | #FF9800 | #212121 | #888060 |
| 沉穩 高中 深灰 | #1C1C1E | #2C2C2E | #F5F5F5 | #FF9F0A | #EBEBEB | #8E8E93 |
| 台灣本土 文化 | #FEF3E2 | #F5E4C8 | #B03020 | #E67E22 | #2C1A0E | #907850 |
| 海洋 藍調 開闊 | #EBF5FB | #D6EAF8 | #1565C0 | #00ACC1 | #0D2137 | #5E8BAA |
| 夢幻 柔和 粉色 | #FDF0F5 | #FAE0EB | #C2185B | #F48FB1 | #2D1520 | #A07080 |

**使用原則**：
- 此表僅供風格解讀時啟發參考，不是強制映射
- 若描述詞混合多種感覺（如「清新 科技」），融合兩組配色方向，自行判斷
- 最重要規則：`--text` 對 `--bg` 對比度 ≥ 4.5:1

---

## 八、圖片處理規範（v2.1 新增，參考 guizang-ppt-skill 標準）

### 比例標準（依版型）

| 版型 | 建議圖片比例 | 錯誤用法 |
|------|------------|---------|
| `split_screen` 左圖 | 16:9 或 4:3 | 任意比例 |
| `image_focus` 主圖 | 16:10 或 16:9 | 正方形 |
| `three_cards` 縮圖 | 4:3 或 1:1 | 同頁不一致混用 |
| `data_highlight` 圖標 | 1:1（正方形） | 矩形 |

### 裁切規則
- 圖片預設從底部裁切，保留頂部主體（人臉、標題、品牌識別）
- 禁止側面裁切（左右）：在 PPTX 中透過 crop_top / crop_bottom 控制
- 同一頁的多張圖片必須使用相同高度（不可混用 5cm 與 8cm）

### 圖片說明格式（三段式）
使用第三層字型（微軟正黑體 Italic 12pt），位於圖片下方 0.3cm：
```
來源 · 說明文字（中文）
```

### 無圖片時的佔位方式
使用 `[在此插入圖片]` 純文字佔位，配合色塊背景（`c['light']`），
不使用 Emoji 或 SVG 圖示。

---

## 九、垂直預算計算方法（V5.0 新增）

> 原則：投影片不能捲動，溢出內容在投影時消失。生成前務必估算。

### 計算公式

```
可用高度 ≈ 100svh × (1 - 上下 padding 比例)
         ≈ 100svh - clamp(2rem, 5vw, 4rem) × 2
         ≈ 約 88%–90% 的視窗高度
```

### 工作範例（高中年段，標準版心）

| 元素 | 計算方式 | 高度 |
|------|---------|------|
| slide-title（sz-h2 = 1.6rem） | 1.6rem × 1.3 × 1行 + 1.5rem margin | ~3.6rem |
| bullets-list × 5 項（sz-body = 1.3rem） | 1.3rem × 1.6 × 1行 × 5 + 0.9rem gap × 4 | ~14.0rem |
| 上下 padding（clamp 2–4rem 各） | 4rem × 2 | 8rem |
| **合計** | | **~25.6rem** |

90svh ≈ 90% × 視窗高度，通常 26–30rem。若超出，**拆頁**，不縮字級或隱藏溢出。

### 拆頁時機

- bullets 超過 --max-bullets（依年段：3/4/5/6）→ 拆為「重點（上）」「重點（下）」
- 單頁元素超過 4 種類型（標題 + 說明 + 圖片 + 按鈕）→ 拆頁
- 感覺塞滿時：一定溢出，直接拆

---

## 十、反模式清單（V5.0 新增，借鑒 open-slide）

以下情況會直接導致簡報失效或教學效果下降，生成前自檢：

| 反模式 | 後果 | 正確做法 |
|--------|------|---------|
| overflow:hidden 遮溢出 | 投影時部分內容消失，教師不知情 | 拆頁 |
| 文字牆（>120字/張） | 學生無法跟上，注意力流失 | 拆頁或改 hero 大字版型 |
| 連續 3 張同版型 | 視覺單調，學生失去方向感 | 插入 section / hero 過渡 |
| 條列項換行 | 字級太大或文字太長 | 縮短文字或降低字級 |
| 正文 < 1.5rem | 後排看不清 | 調高 sz-body |
| Emoji 當圖片佔位 | 呈現不一致，列印失真 | 用 `[在此插入圖片]` 文字佔位 |
| 跳過大綱確認直接生成 | 返工率高，浪費 token | 必須先確認大綱 |
| vocab 無注音 | 國語文課失去教學功能 | 補上 ㄅㄆㄇ 符號 |
