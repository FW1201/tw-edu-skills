---
name: tw-edu-slides-creator
description: >
  上傳任何教材（Word/PDF/文字/網址）後，自動生成視覺化精美教學簡報（.pptx）。
  依年級自動調整字體大小、資訊密度與視覺風格。支援 25 種版型 × 8 種色盤。
  提供 Claude 內建（.pptx 直接下載）與 Canva 高設計感兩條路徑。
  當使用者提及「幫我做簡報」「上傳教材做簡報」「把文件轉成投影片」
  「製作教學簡報」「做PPT」「做投影片」「教學PPT」「課程簡報」
  「把這份資料做成簡報」「簡報製作」「製作投影片」時觸發。
version: 2.0.0
author: 奇老師・數位敘事力社群
allowed-tools: "Bash, Read, Write, WebFetch, WebSearch"
---

# 教材轉視覺化教學簡報 v2.0

## 哲學定位
「好的教學簡報不是把文字搬上投影片，而是把複雜知識視覺化。」
→ 25 種版型 × 8 種色盤 × 智慧內容分析，讓每張投影片都有最適合的呈現方式。

---

## Step 0：讀取必要參考文件

依序讀取以下四個文件，作為後續步驟的知識基礎：

1. `references/slide_design_principles.md` — 25 種版型庫 + 選版型規則 + 色盤配對指南
2. `../../tw_edu_grade_adapter.md` — 年級偵測與內容難度適應系統
3. `../../tw_edu_guided_collection.md` — 引導式資訊收集框架
4. `../../tw_edu_concept_alignment.md` — 概念對齊協議（確認方向一致再執行）

---

## Step 1：年級偵測 + 路徑選擇 + 引導式資訊收集

### 1-A. 雙路徑選擇（第一個問題）
```
🛤️ 請問您想用哪種方式製作簡報？

A. 🖥️ Claude 內建（直接生成 .pptx 檔案，可立即下載，適合快速製作）
B. 🎨 Canva 路徑（呼叫 Canva 生成高設計感版本，視覺效果更精美）

→ 請輸入 A 或 B，或直接描述您的需求（我會自動判斷）
```

### 1-B. 核心資訊收集（最多 3 個必填問題）
```
Q1: 「這份簡報的教學主題或課文是什麼？」
Q2: 「給哪個年級的學生使用？」（若未偵測到）
Q3: 「您有現成的教材想提供嗎？（可貼文字、上傳 Word/PDF、提供網址）」

提示：您可以直接貼上文字內容、上傳 Word 或 PDF、
      提供網頁連結，或用文字描述想要什麼內容。
```

### 1-C. 風格選擇（選填）
```
Q4: 「想要哪種色盤？
    A. 簡約現代（白底深藍，正式課堂）
    B. 活潑彩色（鮮明藍橘，低年級互動）
    C. 深色沉穩（深藍底，高中/程式/專業）
    D. 台灣特色（棕紅米色，本土文化課）
    E. 自然清新（綠色系，自然/環境/健康）
    F. 科技感 （靛青深底，資訊/AI課程）
    G. 溫暖橙調（橙色系，藝術/社會/SEL）
    H. 學術紫  （深紫系，文學/哲學/研究）」

Q5: 「圖示風格？
    A. Emoji（輕量預設，零依賴）
    B. SVG 圖示（需要網路，下載 Iconify 公開資源）
    C. 純文字（無圖示）」

Q6: 「幾張投影片？（預設依內容自動判斷，通常 12-18 張）」
```

### 1-D. 確認摘要（執行前輸出）
```
✅ 主題：{主題}
🎓 年級：{年級}（→ 字體/密度已自動調整）
🛤️ 路徑：{A. Claude 內建 / B. Canva}
🎨 色盤：{色盤選擇}
🖼️ 圖示：{emoji / svg / none}
📊 張數：約 {N} 張（含封面/目標/內容/結尾）
📄 輸出：{主題}_教學簡報.pptx
```

---

## Step 2：年級對應簡報規格

| 學習階段 | 每頁字數上限 | 圖文比例 | 字體大小 | 動畫建議 |
|---------|------------|---------|---------|---------|
| 國小低年級（1-2年）| 20字 | 圖 70% | 標題 40pt / 內文 28pt | 多（出現動畫）|
| 國小中高年級（3-6年）| 40字 | 圖 55% | 標題 36pt / 內文 24pt | 適中 |
| 國中（7-9年）| 80字 | 圖 40% | 標題 32pt / 內文 22pt | 少 |
| 高中（10-12年）| 120字 | 圖 30% | 標題 28pt / 內文 20pt | 無或極少 |

---

## Step 2.5：內容智慧分析（核心步驟）

**依輸入素材類型，先做前處理：**

| 輸入類型 | 前處理方式 |
|---------|-----------|
| 直接貼入文字/課文 | 直接進入分析 |
| Word/PDF 上傳 | `python3 -m markitdown /mnt/user-data/uploads/[檔名]` 轉成文字後分析 |
| 只給主題（無素材）| 依主題＋年級＋108課綱脈絡自行生成完整內容 |
| 網頁 URL | WebFetch 抓取正文後分析 |

**內容分析輸出（JSON 格式）：**

根據輸入素材與 `references/slide_design_principles.md` 的版型選擇規則，
輸出以下結構化 JSON（存為 `/tmp/slides_content.json`）：

```json
{
  "title": "課文/主題名稱",
  "subject": "科目",
  "grade": "年級",
  "objectives": [
    "能（布魯姆動詞）...",
    "能（布魯姆動詞）...",
    "能（布魯姆動詞）..."
  ],
  "slides": [
    {
      "layout": "hero_message",
      "headline": "開場大標語",
      "subtext": "副標題或引導語"
    },
    {
      "layout": "content",
      "title": "概念標題",
      "bullets": ["重點一", "重點二", "重點三"],
      "note": "教師提示"
    },
    {
      "layout": "two_column",
      "title": "比較標題",
      "left_title": "左欄標題",
      "left_bullets": ["..."],
      "right_title": "右欄標題",
      "right_text": "..."
    }
    // ... 依內容自動選擇最適版型
  ],
  "discussion_question": "思考提問句",
  "summary": [
    ["關鍵詞一", "說明一"],
    ["關鍵詞二", "說明二"],
    ["關鍵詞三", "說明三"],
    ["關鍵詞四", "說明四"]
  ],
  "homework": "課後任務說明"
}
```

**版型多樣性要求**：一份簡報應包含 ≥4 種不同版型，
避免連續 3 張以上使用相同版型。

---

## Step 3：路徑分歧

### 路徑 A：Claude 內建 .pptx

執行腳本：
```bash
python scripts/generate_slides.py \
  --title "[主題名稱]" \
  --subject "[科目]" \
  --grade "[年級]" \
  --stage "[elementary_low|elementary_high|junior|senior]" \
  --style "[modern|colorful|dark|local|nature|tech|warm|purple]" \
  --icons "[emoji|svg|none]" \
  --content_file "/tmp/slides_content.json" \
  --slides_count [張數] \
  --output "/mnt/user-data/outputs/[主題]_教學簡報.pptx"
```

### 路徑 B：Canva 高設計感版本

若 Canva MCP 可用：
```
呼叫 Canva MCP：
generate-design(
  design_type="presentation",
  query="[主題] [年級]教學簡報，[色盤風格]，共[N]頁，
         包含：[slide titles 列表]"
)
```

若 Canva MCP 不可用：
```
⚠️ 偵測到 Canva MCP 未連線

→ 請至 Claude Code 設定 → Connectors → 啟用 Canva
→ 或切換到「路徑 A - Claude 內建」繼續製作
  （內容分析已完成，可直接執行 .pptx 生成）
```

---

## Step 4：25 種版型說明（摘要）

詳細版型規格見 `references/slide_design_principles.md`。

| 版型 | 用途摘要 |
|------|---------|
| `content` | 條列文字（預設）|
| `discussion` | 思考提問 + 計時器 |
| `two_column` | 左右雙欄說明 |
| `activity` | 步驟卡 + 時間/分組 |
| `vocab` | 詞彙格子（注音+釋義）|
| `timeline` | 橫向時間軸節點 |
| `comparison` | 雙色對照欄 |
| `big_quote` | 大字金句居中 |
| `data_highlight` | 大數字統計卡 |
| `image_focus` | 圖片佔位框 + 說明 |
| `process_flow` | 橫向箭頭流程 |
| `kanban` | 三欄 KWL 分類 |
| `concept_web` | 放射狀概念圖 |
| `pros_cons` | ✅優/❌缺 雙欄 |
| `section_cover` | 章節分隔頁 |
| `hero_message` | 全版大標語 |
| `three_cards` | 三卡並列 |
| `four_quadrants` | 四象限矩陣 |
| `icon_list` | 圖示條列清單 |
| `stat_bar` | 文字進度條比較 |
| `pyramid` | 金字塔層次 |
| `agenda` | 議程目錄 |
| `testimonial` | 人物引言卡 |
| `split_screen` | 非對稱分割 |
| `blank_canvas` | 空白模板 |

---

## Step 5：品質確認清單

- [ ] 封面有完整資訊（主題/科目/年級）
- [ ] 學習目標頁使用布魯姆動詞
- [ ] 每頁字數符合年級規格
- [ ] 版型種類 ≥ 4 種（視覺多樣性）
- [ ] 無連續 3 張相同版型
- [ ] 主色調一致，最多使用 3 種顏色
- [ ] 重要概念有視覺化呈現
- [ ] 至少一張互動/提問投影片（discussion）
- [ ] 結尾頁有重點整理（summary）
- [ ] 無「相關概念一」等通用佔位符

---

## MCP 整合說明

### Canva MCP（路徑 B）
- 連線方式：Claude Code 設定 → Connectors → Canva
- 呼叫方式：`generate-design(design_type="presentation", query="...")`
- 適合需要精美設計感的簡報（品牌感、行銷型）

### Google Drive MCP（若已連接）
- 直接讀取 Drive 中的教材文件
- 完成後直接儲存回 Drive
- 觸發：使用者提供 Google Drive 連結
