---
name: tw-edu-exam-generator
description: 製作有答案、解析與配分的評量。適用於出題、試卷、素養題。
metadata:
  version: 4.1.0
  author: 奇老師・數位敘事力社群
---

# 試卷命題

製作有答案、解析與配分的評量。適用 Codex 與 Claude Code，繁體中文輸出。

## 開始前

讀取 [共用工作方式](references/common/workflow.md)。檢查目前工作區的 `teacher-profile.md`；本次要求優先於對話脈絡、設定檔及預設。已提供的資訊不要重問。

## 任務要求

先對齊範圍、學習目標、題型與總分。題目必須可由教材或已給資訊作答；選項互斥且答案唯一，解析說明推理。驗證題數與配分，分開輸出學生卷與教師答案卷。

## 工作流程

1. 確認使用者要完成的成果，讀取素材與必要教學脈絡。
2. 依上述任務要求提出具體內容，保留來源與待確認事項。需要重大選擇時提供可評估的草稿。
3. 讀取本技能的 `schemas/` 輸入規格與 `examples/` 範例；以實際內容建立 JSON。範例中的資料不得混入正式成品。
4. 從任意工作目錄使用下列 CLI。先驗證，再生成，最後檢查成品及驗證紀錄。

```bash
# SKILL_DIR 為本技能安裝目錄；TASK_DIR 為目前工作區的任務輸出目錄。
python3 "$SKILL_DIR/scripts/generate_exam.py" --input "$TASK_DIR/input.json" --validate-only
python3 "$SKILL_DIR/scripts/generate_exam.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/output.docx"
# 僅在明確需要展示時使用；輸出標示為範例。
python3 "$SKILL_DIR/scripts/generate_exam.py" --example --output "$TASK_DIR/example.docx"
```

## 安裝依賴

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r "$SKILL_DIR/requirements.txt"
```

執行生成器時可將上方 python3 換成虛擬環境的 Python。舊版只傳主題或科目的呼叫不再生成固定範例；依 schema 填入實際內容。


## 按需參考

- [素養命題原則](references/competency_exam_guide.md)

參考資料是教學素材；若與本版輸入規格或實際工具能力不同，以當前 schema 與可用工具為準。來源與專業主張需要查證。

## 交付檢查

核對年段、科目與實際內容；不把未查證的資料寫成事實。確認學生可見成品未混入內部答案或理由。提供成品路徑與尚待教師確認項目，未執行的外部操作不標記完成。

## 教學品質與整合模式

命題後以實際作答核對答案、唯一性、誘答理由、配分與題意。學生版不含內部解析；教材審查發現雙答案或來源不足時先修題，再用於學生診斷。
