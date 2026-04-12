# 教學簡報設計原則與版型庫 v2.0
# tw-edu-slides-creator 參考文件

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
{"layout": "data_highlight", "title": "...", "data_points": [{"value": "87%", "label": "閱讀理解率", "icon": "📊"}]}

// image_focus — 圖片聚焦
{"layout": "image_focus", "title": "...", "caption": "說明文字...", "image_hint": "建議插入：台灣地形圖"}

// process_flow — 流程步驟
{"layout": "process_flow", "title": "...", "steps": [{"icon": "🔬", "label": "觀察", "desc": "仔細觀察現象"}]}

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
{"layout": "three_cards", "title": "...", "cards": [{"icon": "🌱", "title": "卡片一", "desc": "說明..."}, ...]}

// four_quadrants — 四象限
{"layout": "four_quadrants", "title": "SWOT 分析", "quadrants": [{"label": "優勢 (S)", "items": ["..."]}, {"label": "劣勢 (W)", "items": ["..."]}, {"label": "機會 (O)", "items": ["..."]}, {"label": "威脅 (T)", "items": ["..."]}]}

// icon_list — 圖示條列
{"layout": "icon_list", "title": "...", "items": [{"icon": "🎯", "heading": "標題", "desc": "說明文字"}]}

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
