---
name: tw-research-viz
description: >
  將學術研究資料（文獻關係、研究架構、概念框架、資料流程、統計結果）
  視覺化為精確的學術圖表，優先調用 Excalidraw MCP 生成手繪風格圖，
  或生成可嵌入論文的 SVG/PNG 圖表。
  當使用者提及「研究架構圖」「概念框架」「文獻關係圖」「理論模型」
  「研究流程圖」「資料視覺化」「畫圖」「論文圖表」「研究地圖」
  「系統性文獻回顧」「SLR 流程」「PRISMA」時觸發。
  適用情境：碩博士論文、期刊論文、研討會論文、研究計畫書。
version: 1.0.0
author: 奇老師・數位敘事力社群
allowed-tools: "Bash, Read, Write, WebSearch"
disable-model-invocation: true
---

# 學術論文資料視覺化工具 v1.0

## 哲學定位
「一張好的學術圖表，能讓審稿人在 30 秒內理解你的研究邏輯。」

---

## Step 0：讀取必要文件

1. `references/academic_viz_types.md` — 學術圖表類型與規範
2. `references/apa7_figure_format.md` — APA/APA 7th 圖表格式要求
3. `../../tw_edu_guided_collection.md` — 引導式收集框架

若 Excalidraw MCP 可用：
→ 優先使用 Excalidraw 生成可編輯圖表
→ 調用 `Excalidraw:create_view` 工具

---


**概念對齊協議（必要前置步驟）：**
`../../tw_edu_concept_alignment.md`
→ 在執行任何工作前，先完成概念對齊確認卡。


## Step 1：引導式資訊收集（三輪）

### 第一輪（核心，必問）
```
Q1: 「要視覺化什麼類型的內容？
    A. 研究架構 / 概念框架
    B. 文獻關係圖（如：文獻引用網絡、主題分群）
    C. 研究流程圖（含 PRISMA/SLR 流程）
    D. 理論模型（變數關係、路徑圖）
    E. 統計數據視覺化（長條圖/折線/雷達圖）
    F. 心智圖 / 主題概念地圖
    G. 其他（請描述）」

Q2: 「請提供核心資料：
    ・研究題目 / 主題
    ・要呈現的主要元素（節點/變數/步驟等）
    ・元素之間的關係（A→B、A←→B、A包含B）」
```

### 第二輪（細節，選填）
```
Q3: 「圖的最終用途？
    A. 嵌入 Word/PDF 論文（需高解析度）
    B. 學術報告/簡報（.pptx）
    C. 研討會海報
    D. 線上分享 / 可編輯版本」

Q4: 「有沒有特定的學術格式要求？
    APA 7th / 臺灣學位論文格式 / 期刊特定格式」

Q5: 「色彩偏好？
    A. 黑白（適合列印）
    B. 有限色彩（2-3 色，正式感）
    C. 全彩（簡報/海報用）」
```

### 確認摘要
```
✅ 圖表類型：{類型}
📐 元素數量：{N 個節點/步驟}
🎨 風格：{黑白/有限色/全彩}
🔧 生成工具：{Excalidraw MCP / SVG / matplotlib}
📄 輸出格式：{svg/png/pptx 嵌入}
```

---

## Step 2：圖表類型規範

### A. 研究架構圖 / 概念框架
```
適用：展示研究的整體架構、各構念之間的關係

Excalidraw 元素設計：
  ・矩形（圓角）= 構念/變數
  ・箭頭 = 影響方向（實線 = 假設正向影響）
  ・虛線箭頭 = 調節/中介關係
  ・雙向箭頭 = 相關但無因果方向

分層建議：
  ├── 前置變數（左側或上方）
  ├── 核心構念（中央）
  └── 結果變數（右側或下方）

標記規範（APA 7th）：
  H1, H2... = 假設編號（在箭頭旁標注）
  β = 標準化路徑係數（若有統計結果）
```

### B. PRISMA 系統性文獻回顧流程圖
```
標準 4 階段結構（PRISMA 2020）：

識別（Identification）
  │ 資料庫搜尋（N = ）
  │ 移除重複（n = ）
  ↓
篩選（Screening）
  │ 標題/摘要篩選（n = 排除 / 原因）
  ↓
資格審查（Eligibility）
  │ 全文審查（n = 排除 / 原因清單）
  ↓
納入（Included）
  └── 最終納入文獻（n = ）

Excalidraw 樣式：
  ・識別 = 藍色框
  ・篩選 = 黃色框
  ・資格 = 橘色框
  ・納入 = 綠色框
  ・排除原因 = 側邊虛線框
```

### C. 文獻關係圖 / 主題群聚
```
適用：展示不同文獻/學者之間的引用關係或主題分群

元素設計：
  ・圓形節點 = 重要文獻/學者
  ・節點大小 = 被引用次數（越大越重要）
  ・線條粗細 = 關係強度
  ・色彩分群 = 研究主題/時期

若文獻數量 > 20：建議使用 Python 腳本生成圖表（matplotlib + networkx）
```

### D. 路徑模型圖（SEM / 迴歸）
```
元素設計：
  ・橢圓 = 潛在變數（latent variable）
  ・矩形 = 觀測變數（observed variable）
  ・單向箭頭 = 因果路徑（標注路徑係數）
  ・雙向彎曲箭頭 = 相關/共變
  ・小圓圈 e = 誤差項

標注規範：
  顯著路徑：β = .XX, p < .001（標注 ***）
  非顯著路徑：β = .XX, ns（虛線箭頭）
```

### E. 統計數據視覺化
```
圖表選擇指南：
  比較多組 → 長條圖（bar chart）
  趨勢/時序 → 折線圖（line chart）
  比例/組成 → 圓餅圖/環形圖
  多維度比較 → 雷達圖（spider chart）
  相關關係 → 散佈圖（scatter plot）
  分佈情況 → 箱形圖（box plot）

生成工具：
  → Python matplotlib / seaborn 腳本
  → 或呼叫 Three.js 3D Viewer（3D 資料呈現）
```

---

## Step 3：Excalidraw MCP 調用規範

### 優先使用 Excalidraw MCP 的情境
```
✅ 研究架構圖、概念框架
✅ PRISMA 流程圖
✅ 文獻關係圖（< 20 節點）
✅ 心智圖
✅ 任何需要「可編輯」的圖表
```

### Excalidraw 調用前的準備
```
Step 1：讀取 Excalidraw read_me
  → 呼叫 Excalidraw:read_me 取得元素格式規範

Step 2：設計元素結構（JSON）
  元素類型：rectangle / ellipse / arrow / text / diamond
  元素屬性：x, y, width, height, backgroundColor, strokeColor, label

Step 3：呼叫 create_view
  Excalidraw:create_view(elements: JSON 陣列字串)
```

### 學術圖表元素設計原則
```
顏色系統（學術正式用）：
  主要節點：#1A5276（深藍）
  次要節點：#2471A3（中藍）
  強調節點：#D4AC0D（金色）
  邊界節點：#1E8449（綠色）
  背景色：#EBF5FB（淺藍，避免純白）
  文字：#1C2A35（深色）

字型：
  節點標題：14px 粗體
  路徑標注：12px 細體
  圖注：12px 斜體

連接器：
  因果關係：實線箭頭
  相關關係：雙向箭頭
  包含關係：虛線框
  調節關係：虛線箭頭
```

---

## Step 4：Python 輔助腳本（無 Excalidraw MCP 時）

```bash
# 生成 PRISMA 流程圖
python scripts/generate_prisma.py \
  --identified [N] \
  --duplicates [n] \
  --screened [n] \
  --eligible [n] \
  --included [n] \
  --output "/mnt/user-data/outputs/PRISMA流程圖.png"

# 生成研究架構圖
python scripts/generate_framework.py \
  --nodes "[節點1:類型,節點2:類型,...]" \
  --edges "[節點1->節點2:標籤,...]" \
  --output "/mnt/user-data/outputs/研究架構圖.svg"
```

---

## Step 5：APA 7th 圖表格式規範

```
圖注格式（Figure caption）：

Figure X
[圖表標題（首字大寫，不加句點）]
注意。[說明文字，如有]。[資料來源，如改編自其他研究]

範例：
Figure 1
Conceptual Framework of Teacher AI Competency and Student Learning Outcomes
注意。本架構整合 Davis (1989) 科技接受模型與 Bandura (1977) 自我效能理論。

圖表編號規則：
  ・全論文連續編號（Figure 1, 2, 3...）
  ・圖注置於圖的正下方
  ・圖標題與論文正文字體一致（通常為 Times New Roman 12pt）
```

---

## Step 6：MCP 整合對照表

| 功能 | Claude Code | Claude.ai | Codex/gemini-cli |
|------|------------|-----------|-----------------|
| Excalidraw 互動圖 | ✅ MCP | ✅ MCP（若連接） | ❌ → SVG 輸出 |
| 統計圖（matplotlib） | ✅ Bash | ✅ Bash | ✅ |
| 匯出為 .png/.svg | ✅ | ✅ | ✅ |
| Three.js 3D 視覺化 | ✅ MCP | ✅ MCP（若連接） | ❌ |

### Excalidraw MCP 未連接時的降級方案
1. 使用 Python `matplotlib` 生成 `.png` 靜態圖表
2. 生成 SVG 代碼（可貼入 Inkscape 或 Figma 繼續編輯）
3. 生成 Mermaid 語法（flowchart/graph）輸出供用戶複製
4. 提供 draw.io XML（可匯入 diagrams.net 編輯）

---

## Step 7：品質確認清單

- [ ] 圖表邏輯清晰，看圖能理解研究核心
- [ ] 元素大小與字型符合學術出版標準
- [ ] 顏色不超過 3 種（印刷版需考慮灰階辨識度）
- [ ] 箭頭方向明確、無歧義
- [ ] 有 APA 7th 格式的圖注
- [ ] 高解析度輸出（≥ 300 DPI 印刷用，≥ 150 DPI 螢幕用）
- [ ] Excalidraw 版本可供後續編輯（若 MCP 可用）
