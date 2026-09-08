---
name: tw-edu-interdisciplinary
description: "整合不同學科的概念與探究任務。適用於跨領域、跨科。"
version: 4.0.0
author: 奇老師・數位敘事力社群
---

# 跨領域課程

整合不同學科的概念與探究任務。適用 Codex 與 Claude Code，繁體中文輸出。

## 開始前

讀取 [共用工作方式](references/common/workflow.md)。檢查目前工作區的 `teacher-profile.md`；本次要求優先於對話脈絡、設定檔及預設。已提供的資訊不要重問。

## 任務要求

從共同問題出發，說明每科不可替代的貢獻、概念關係、時程、活動與共同評量。不是將不同科目活動並列；引用資料與課綱需可追溯。

## 工作流程

1. 確認使用者要完成的成果，讀取素材與必要教學脈絡。
2. 依上述任務要求提出具體內容，保留來源與待確認事項。需要重大選擇時提供可評估的草稿。
3. 讀取本技能的 `schemas/` 輸入規格與 `examples/` 範例；以實際內容建立 JSON。範例中的資料不得混入正式成品。
4. 從任意工作目錄使用下列 CLI。先驗證，再生成，最後檢查成品及驗證紀錄。

```bash
# SKILL_DIR 為本技能安裝目錄；TASK_DIR 為目前工作區的任務輸出目錄。
python3 "$SKILL_DIR/scripts/generate_interdisciplinary.py" --input "$TASK_DIR/input.json" --validate-only
python3 "$SKILL_DIR/scripts/generate_interdisciplinary.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/output.docx"
# 僅在明確需要展示時使用；輸出標示為範例。
python3 "$SKILL_DIR/scripts/generate_interdisciplinary.py" --example --output "$TASK_DIR/example.docx"
```

## 安裝依賴

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r "$SKILL_DIR/requirements.txt"
```

執行生成器時可將上方 python3 換成虛擬環境的 Python。舊版只傳主題或科目的呼叫不再生成固定範例；依 schema 填入實際內容。

## 交付檢查

核對年段、科目與實際內容；不把未查證的資料寫成事實。確認學生可見成品未混入內部答案或理由。提供成品路徑與尚待教師確認項目，未執行的外部操作不標記完成。
