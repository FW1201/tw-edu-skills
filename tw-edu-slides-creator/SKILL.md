---
name: tw-edu-slides-creator
description: 教學簡報製作。依教學流程（引入、示例、解析、練習、統整）規劃每頁的教學功能，先確認大綱、風格與一張樣張再全套製作，預設可編輯 PPTX（原生文字、表格、圖表、講者備註），圖片模式需使用者選用。適用於簡報、投影片、PPT、上課簡報、研習簡報。
metadata:
  version: 5.2.0
  author: 奇老師・數位敘事力社群
  category: 教材資源
---

# 教學簡報

教學簡報不是講稿的投影版。每一頁都要回答：這頁在學生學習流程中扮演什麼角色？學生看到這頁要做什麼？

## 定位與邊界

- **做**：教學流程規劃、逐頁教學功能、大綱與樣張確認、可編輯 PPTX、表格與資料圖表、講者備註、可及性檢查、圖片模式的逐頁工作追蹤。
- **不做**：教案本體（→ `tw-edu-lesson-plan-108`）、學生學習單（→ `tw-edu-worksheet-creator`）、既有簡報審查（→ `tw-edu-material-reviewer` 的 slides 模式）。

## 開始前

讀取 [共用工作方式](references/common/workflow.md)，檢查 `teacher-profile.md`（科目、學段、慣用風格）。沿用已核准的大綱與風格，不重複詢問。

必要情境：學習目標、教學時間、教材內容、使用場合（上課、研習、家長會）、要用 editable 還是 image 模式。

## 思維路線

1. **教學流程**：依學習目標排出引入 → 示例 → 解析 → 練習 → 統整。先示例再提問，練習頁要有學生任務與時間。
2. **逐頁功能**：每頁標明功能（展示內容、學生任務、教師講解）；學生任務頁寫清楚要做什麼、多久、怎麼回報。
3. **大綱確認**：產出 outline，逐頁列教學目的、實際文字、活動與評量，請老師確認。
4. **風格與樣張**：選色彩、字型、密度與圖像處理，製作一張代表性樣張，確認後才全套製作。
5. **內容密度**：一頁一個重點；長文改成條列或圖解；數據用原生圖表並附來源。
6. **講者備註**：寫教師要說的關鍵句、提問、預期學生回答與轉換語，放在對應頁。
7. **可及性**：閱讀順序、文字與背景對比、圖片替代文字、字級足夠在教室後排閱讀。
8. **模式**：editable 為預設；image 模式每頁是整張圖片，文字無法直接編輯，開始前說明限制，逐頁圖片需 16:9、連續且不重複。

## 台灣情境要點

- 教學視覺原則見 [簡報設計原則](references/slide_design_principles.md)；版面見 [版面格線](references/layout-grid.md)、[版面範本](references/pptx-layout-templates.md)；配色見 [色票庫](references/palette-library.md)；風格見 [風格選擇](references/presentation-style-library.md)；樣張確認見 [樣張範本](references/sample-approval-template.md)。
- 流程關卡與進度：[流程關卡](docs/workflow-gates-and-progress.md)、[大綱範例](docs/outline-style-sample.md)、[生成狀態](docs/slide-generation-state.md)、[組裝與回報](docs/project-assembly-and-reporting.md)。
- 圖片模式的逐頁工作者提示：[slide worker](prompts/slide-worker.md)。

## 產出

依 [輸入規格](schemas/input.schema.json) 建立 JSON，[範例](examples/example.json) 只看結構。

```bash
python3 "$SKILL_DIR/scripts/generate_slides.py" --input "$TASK_DIR/input.json" --validate-only
python3 "$SKILL_DIR/scripts/generate_slides.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/slides.pptx"
```

圖片模式的工作追蹤：

```bash
python3 "$SKILL_DIR/scripts/init_slide_jobs.py" "$TASK_DIR/deck" --slide-count 12
python3 "$SKILL_DIR/scripts/slide_job_status.py" "$TASK_DIR/deck"
```

語意閘門會擋下：頁碼不連續、圖表類別與數值長度不一致；圖片模式會檢查缺頁與重複。

## 品質關卡

- 每頁都有教學功能，練習頁有學生任務。
- 樣張經確認才全套製作。
- 圖表數值與來源一致。
- 講者備註在對應頁面。
- 實際開啟或渲染檢查過，不以檔案存在代替視覺檢查。

## 交接

- 配套學習單 → `tw-edu-worksheet-creator`。
- 簡報中的檢核題 → `tw-edu-formative-assessment`。
- 完成後審查 → `tw-edu-material-reviewer`。
