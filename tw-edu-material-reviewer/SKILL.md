---
name: tw-edu-material-reviewer
description: 檢查既有教材、試卷或簡報的可定位缺陷，提出局部修正並複查；生成器負責編排審查報告。
metadata:
  version: 1.0.0
  author: 奇老師・數位敘事力社群
---

# 教材與評量品質審查

讀取 [工作方式](references/common/workflow.md) 與目前工作區 `teacher-profile.md`，缺設定仍可工作。

先選教材／評量／簡報模式，檢查知識與來源、目標、材料是否支持解答、答案唯一性、線索洩漏、負荷與可及性。每個問題有素材ID、原文摘錄、理由、嚴重度、修正與未知項；不憑風格判重大錯誤。腳本只驗證定位及編排，不會自動完成知識審查。修正交給原生成技能可選，修後複查；文字檢查與實際版面分開。

依 [輸入規格](schemas/input.schema.json) 建立實際 JSON，使用 [範例](examples/example.json) 只看結構。

```bash
python3 "$SKILL_DIR/scripts/generate_review.py" --input "$TASK_DIR/input.json" --validate-only
python3 "$SKILL_DIR/scripts/generate_review.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/report.docx"
```

交付可編輯報告、來源／計數／定位與待教師確認事項。
