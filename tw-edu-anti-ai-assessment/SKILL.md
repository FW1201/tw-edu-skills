---
name: tw-edu-anti-ai-assessment
description: 檢視評量證據與改善任務設計。適用於抗AI評量、評量真實性。
metadata:
  version: 4.1.0
  author: 奇老師・數位敘事力社群
---

# 評量真實性設計

檢視評量證據與改善任務設計。適用 Codex 與 Claude Code，繁體中文輸出。

## 開始前

讀取 [共用工作方式](references/common/workflow.md)。檢查目前工作區的 `teacher-profile.md`；本次要求優先於對話脈絡、設定檔及預設。已提供的資訊不要重問。

## 任務要求

依實際題目、作答環境與核心目標評估風險，寫出評分理由與可行修正。過程證據、口頭說明與課堂觀察相互參照；個人聲明不能證明未用AI，評量設計分數不能判定學生作弊。

## 工作流程

1. 確認使用者要完成的成果，讀取素材與必要教學脈絡。
2. 依上述任務要求提出具體內容，保留來源與待確認事項。需要重大選擇時提供可評估的草稿。
3. 讀取本技能的 `schemas/` 輸入規格與 `examples/` 範例；以實際內容建立 JSON。範例中的資料不得混入正式成品。
4. 從任意工作目錄使用下列 CLI。先驗證，再生成，最後檢查成品及驗證紀錄。

```bash
# SKILL_DIR 為本技能安裝目錄；TASK_DIR 為目前工作區的任務輸出目錄。
python3 "$SKILL_DIR/scripts/generate_anti_ai_report.py" --input "$TASK_DIR/input.json" --validate-only
python3 "$SKILL_DIR/scripts/generate_anti_ai_report.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/output.docx"
# 僅在明確需要展示時使用；輸出標示為範例。
python3 "$SKILL_DIR/scripts/generate_anti_ai_report.py" --example --output "$TASK_DIR/example.docx"
```

## 安裝依賴

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r "$SKILL_DIR/requirements.txt"
```

執行生成器時可將上方 python3 換成虛擬環境的 Python。舊版只傳主題或科目的呼叫不再生成固定範例；依 schema 填入實際內容。


## 按需參考

- [評量設計檢視向度（非作弊判定）](references/ai_vulnerability_rubric.md)
- [任務設計策略（需依實際情境判斷）](references/anti_ai_strategies.md)

參考資料是教學素材；若與本版輸入規格或實際工具能力不同，以當前 schema 與可用工具為準。來源與專業主張需要查證。

## 交付檢查

核對年段、科目與實際內容；不把未查證的資料寫成事實。確認學生可見成品未混入內部答案或理由。提供成品路徑與尚待教師確認項目，未執行的外部操作不標記完成。

## 教學品質與整合模式

以學習過程、解釋、修改與獨立遷移檢視任務真實性；區分教師允許／禁止／需揭露的AI用途。不能憑文本風格、檢測器分數或完成速度判定作弊。
