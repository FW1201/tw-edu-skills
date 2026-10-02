---
name: tw-edu-learning-evidence-analyzer
description: 以匿名實際作答與作品判讀班級學習證據，區分缺答、題目疑義與待驗證錯因。
metadata:
  version: 1.0.0
  author: 奇老師・數位敘事力社群
---

# 學習證據分析

讀取 [工作方式](references/common/workflow.md) 與目前工作區 `teacher-profile.md`，缺設定仍可工作。

收到實際作答後先查題目／答案與資料完整性。正式數值由生成器計數，全班與已答分母分開；未核答案不計正確率。作品判讀保留原文位置，錯因只列待驗證候選；不能由一次作答固定能力或推介入效果。輸出證據摘要與教師下一步，形成性評量／差異化／回饋交接可選。

依 [輸入規格](schemas/input.schema.json) 建立實際 JSON，使用 [範例](examples/example.json) 只看結構。

```bash
python3 "$SKILL_DIR/scripts/generate_evidence.py" --input "$TASK_DIR/input.json" --validate-only
python3 "$SKILL_DIR/scripts/generate_evidence.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/report.docx"
```

交付可編輯報告、來源／計數／定位與待教師確認事項。

CSV 匯入：欄位為 student_id 與每題ID，空白是缺答；以 scripts/import_responses.py --csv 作答.csv --items 題目輸入.json --output 合併輸入.json 轉成標準輸入，不接受多餘欄位或重複學生ID。
