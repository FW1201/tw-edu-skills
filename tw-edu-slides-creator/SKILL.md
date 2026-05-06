---
name: tw-edu-slides-creator
description: >
  上傳任何教材（Word/PDF/文字/網址）後，自動生成視覺化精美教學簡報（.pptx）。
  依年級自動調整字體大小、資訊密度與視覺風格。11 種版型 × 9 種教育色盤。
  純 Python stdlib，無外部依賴，品質穩定。
  當使用者提及「幫我做簡報」「上傳教材做簡報」「把文件轉成投影片」
  「製作教學簡報」「做PPT」「做投影片」「教學PPT」「課程簡報」
  「把這份資料做成簡報」「簡報製作」「製作投影片」時觸發。
version: 3.0.0
author: 奇老師・數位敘事力社群
allowed-tools: "Bash, Read, Write, WebFetch, WebSearch"
---

# 教材轉視覺化教學簡報 V3.0

---

## Step 1：資訊收集（最多問 3 個）

| 問題 | 必填 |
|------|------|
| 教學主題或課文是什麼？ | ✅ |
| 給哪個年級的學生？ | ✅ |
| 有現成教材嗎？（文字/Word/PDF/網址） | 選填 |

收集後輸出確認摘要：主題、年級、色盤、約幾張。

---

## Step 2：年級規格 + 色盤選擇

### 年級對應表
| 學習階段 | grade 參數 | 標題 pt | 內文 pt | 每頁上限 |
|---------|-----------|--------|--------|---------|
| 國小低年級 1-2 | elementary_low | 40 | 28 | 3 條 |
| 國小中高年 3-6 | elementary_high | 36 | 24 | 4 條 |
| 國中 7-9 | junior（預設） | 32 | 22 | 5 條 |
| 高中 10-12 | senior | 28 | 20 | 6 條 |

### 色盤選擇
| edu_theme | 適用情境 |
|-----------|---------|
| edu-warm（預設）| 人文/國語文/溫暖教室 |
| modern | 正式課堂/全校公開課 |
| colorful | 低年級/互動課 |
| dark | 高中/程式/電競課 |
| local | 本土文化/歷史/鄉土 |
| nature | 自然/環境/健康 |
| tech | 資訊/AI/STEM |
| warm | 藝術/社會/SEL |
| purple | 文學/哲學/研究 |

---

## Step 3：生成 JSON 規格並執行腳本

### 3-A. 輸出 JSON 規格存為 `/tmp/slides_spec.json`

```json
{
  "meta": {"title": "課文名稱", "subject": "科目", "grade": "年級"},
  "edu_theme": "edu-warm",
  "grade_stage": "junior",
  "slides": [
    {"layout": "cover",       "title": "...", "subtitle": "...", "meta": "年級・設計者"},
    {"layout": "objectives",  "title": "學習目標", "bullets": ["認知：能...", "情意：能...", "態度：能養成..."]},
    {"layout": "section",     "title": "章節名稱", "subtitle": "副標"},
    {"layout": "bullets",     "title": "...", "bullets": ["重點一", "重點二"]},
    {"layout": "two-column",  "title": "...", "left_title": "...", "left": [...], "right_title": "...", "right": [...]},
    {"layout": "compare",     "title": "...", "left_title": "...", "left": [...], "right_title": "...", "right": [...]},
    {"layout": "vocab",       "title": "詞彙", "items": [{"word":"蹣跚","reading":"ㄆㄢˊㄕㄢ","definition":"行走困難"}]},
    {"layout": "activity",    "title": "活動", "steps": ["步驟1", "步驟2"]},
    {"layout": "discussion",  "question": "思考問題句...？", "timer_min": 5, "hint": "提示（選填）"},
    {"layout": "hero",        "headline": "大標語", "subline": "副標（選填）"},
    {"layout": "summary",     "title": "重點整理", "pairs": [["詞", "說明"], ["詞", "說明"]]}
  ]
}
```

**版型節奏規則**：
- 不得 3 張以上連續同版型
- 每 5 張至少 1 張重版型（cover / section / hero / discussion）
- 10 張以上須有 ≥1 hero 或 section

### 3-B. 執行腳本

```bash
python3 scripts/generate_slides.py \
  --spec /tmp/slides_spec.json \
  --edu_theme edu-warm \
  --grade junior \
  --output "/mnt/user-data/outputs/[主題]_教學簡報.pptx"
```

---

## Step 4：品質確認

**P0（不達到不交付）**
- [ ] 無 Emoji（一律用全形括號【】或 Unicode 幾何符號）
- [ ] layout 值必須在 11 種版型內（cover/section/bullets/two-column/compare/objectives/vocab/activity/discussion/hero/summary）
- [ ] 年級字體規格已套用
- [ ] 輸出 .pptx 可正常解壓（unzip -l 驗證有 ppt/slides/slide*.xml）

**P1（影響教學效果）**
- [ ] 版型種類 ≥ 4 種
- [ ] 學習目標使用認知／情意／態度三維格式
- [ ] 注音使用 ㄅㄆㄇ 符號（vocab 版型）

---

## Step 5：輸出摘要

交付時提供：
1. 下載連結（.pptx）
2. 版型清單（#張 × 版型名）
3. 建議調整方向（針對班級特性）

---

## Canva 路徑（高設計感版本）

使用者說「Canva 版」或「更精美的」時，若 Canva MCP 已連線：
```
canva: generate-design(design_type="presentation", query="[主題] [年級]教學簡報 [色盤風格]，共[N]頁")
```
未連線時：告知需啟用 Canva Connector，並切換路徑 A 繼續。

---

## 微調模式

生成後，用一字動詞觸發 delta 更新：

| 動詞 | 動作 |
|------|------|
| 換 | 替換指定張次的 layout/內容 |
| 改 | 修改色盤（--edu_theme）或年級（--grade） |
| 加 | 插入新投影片到指定位置 |
| 刪 | 移除指定張次 |
