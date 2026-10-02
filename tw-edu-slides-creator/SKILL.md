---
name: tw-edu-slides-creator
description: 製作可編輯投影片與教師講稿。適用於簡報、投影片、PPT。預設可編輯 PPTX，圖片模式可選。
metadata:
  version: 5.1.0
  author: 奇老師・數位敘事力社群
---

# 教學簡報

製作可編輯投影片與教師講稿。適用 Codex 與 Claude Code，繁體中文輸出。

## 開始前

讀取 [共用工作方式](references/common/workflow.md)。檢查目前工作區的 `teacher-profile.md`；本次要求優先於對話脈絡、設定檔及預設。已提供的資訊不要重問。

## 任務要求

先確認教學大綱、風格與一張代表性樣張，沿用既有核准。每頁服務引入、示例、解析、練習或統整；先示例再提問。editable 為預設，原生文字、圖表、表格可編輯；image 必須使用者選用，逐頁圖像需16:9、連續且不重複，備註正確對頁。

## 工作流程

1. 確認使用者要完成的成果，讀取素材與必要教學脈絡。
2. 依上述任務要求提出具體內容，保留來源與待確認事項。需要重大選擇時提供可評估的草稿。
3. 讀取本技能的 `schemas/` 輸入規格與 `examples/` 範例；以實際內容建立 JSON。範例中的資料不得混入正式成品。
4. 從任意工作目錄使用下列 CLI。先驗證，再生成，最後檢查成品及驗證紀錄。

```bash
# SKILL_DIR 為本技能安裝目錄；TASK_DIR 為目前工作區的任務輸出目錄。
python3 "$SKILL_DIR/scripts/generate_slides.py" --input "$TASK_DIR/input.json" --validate-only
python3 "$SKILL_DIR/scripts/generate_slides.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/output.pptx"
# 僅在明確需要展示時使用；輸出標示為範例。
python3 "$SKILL_DIR/scripts/generate_slides.py" --example --output "$TASK_DIR/example.pptx"
```

## 安裝依賴

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r "$SKILL_DIR/requirements.txt"
```

執行生成器時可將上方 python3 換成虛擬環境的 Python。舊版只傳主題或科目的呼叫不再生成固定範例；依 schema 填入實際內容。


## 按需參考

- [教學視覺原則](references/slide_design_principles.md)
- [視覺風格選擇](references/presentation-style-library.md)
- [樣張確認](references/sample-approval-template.md)

參考資料是教學素材；若與本版輸入規格或實際工具能力不同，以當前 schema 與可用工具為準。來源與專業主張需要查證。

## 交付檢查

核對年段、科目與實際內容；不把未查證的資料寫成事實。確認學生可見成品未混入內部答案或理由。提供成品路徑與尚待教師確認項目，未執行的外部操作不標記完成。

## 教學品質與整合模式

內容可編輯為預設；圖表附來源與數值。教學投影片分辨展示內容、學生任務與教師講稿；可及性檢查閱讀順序、對比與文字替代，圖片模式明示編輯限制。
