---
name: tw-edu-lesson-plan-108
description: 依課程目標安排活動、時間與評量。適用於教案、備課、108課綱。
metadata:
  version: 4.1.0
  author: 奇老師・數位敘事力社群
---

# 108 課綱教案

依課程目標安排活動、時間與評量。適用 Codex 與 Claude Code，繁體中文輸出。

## 開始前

讀取 [共用工作方式](references/common/workflow.md)。檢查目前工作區的 `teacher-profile.md`；本次要求優先於對話脈絡、設定檔及預設。已提供的資訊不要重問。

## 任務要求

提供學段、科目、主題、總時間與教材；先讀來源再設計。每個目標有可觀察行為，活動與評量對應目標 ID，活動分鐘加總等於總時間。課綱代碼需對照官方來源、科目與學段，無法查證時標示待確認。

## 工作流程

1. 確認使用者要完成的成果，讀取素材與必要教學脈絡。
2. 依上述任務要求提出具體內容，保留來源與待確認事項。需要重大選擇時提供可評估的草稿。
3. 讀取本技能的 `schemas/` 輸入規格與 `examples/` 範例；以實際內容建立 JSON。範例中的資料不得混入正式成品。
4. 從任意工作目錄使用下列 CLI。先驗證，再生成，最後檢查成品及驗證紀錄。

```bash
# SKILL_DIR 為本技能安裝目錄；TASK_DIR 為目前工作區的任務輸出目錄。
python3 "$SKILL_DIR/scripts/generate_lesson_plan.py" --input "$TASK_DIR/input.json" --validate-only
python3 "$SKILL_DIR/scripts/generate_lesson_plan.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/output.docx"
# 僅在明確需要展示時使用；輸出標示為範例。
python3 "$SKILL_DIR/scripts/generate_lesson_plan.py" --example --output "$TASK_DIR/example.docx"
```

## 安裝依賴

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r "$SKILL_DIR/requirements.txt"
```

執行生成器時可將上方 python3 換成虛擬環境的 Python。舊版只傳主題或科目的呼叫不再生成固定範例；依 schema 填入實際內容。


## 按需參考

- [課綱指標資料（使用前回查官方版本）](references/108_subject_indicators.md)
- [認知層次與教學目標](references/bloom_taxonomy_tw.md)

參考資料是教學素材；若與本版輸入規格或實際工具能力不同，以當前 schema 與可用工具為準。來源與專業主張需要查證。

## 交付檢查

核對年段、科目與實際內容；不把未查證的資料寫成事實。確認學生可見成品未混入內部答案或理由。提供成品路徑與尚待教師確認項目，未執行的外部操作不標記完成。

## 教學品質與整合模式

教學試作模式：明示待改善問題、學生觀察、短期試作、再檢核與停止條件。雙語模式分開內容與語言目標，不將語言流利度當領域理解。科學活動列變因、測量與證據解釋，安全條件依實際來源及學校規則確認。
