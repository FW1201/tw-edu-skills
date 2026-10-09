---
name: tw-edu-learning-evidence-analyzer
description: 學習證據分析。以匿名的實際作答（CSV 或 JSON）與作品判讀班級學習狀況：先查題目與答案、資料完整性，正式數值由腳本計數（全班與已答分母分開，未核答案不計正確率），區分缺答、題目疑義與待驗證錯因，給出下一堂課的教學決策。適用於考後分析、作答分析、錯題分析、全班學習狀況判讀。
metadata:
  version: 1.1.0
  author: 奇老師・數位敘事力社群
  category: 學生表現
---

# 學習證據分析

把全班的作答變成「明天怎麼教」的依據。數字由腳本算，判讀由老師與技能一起做，而且每個判讀都能回到原始資料。

## 定位與邊界

- **做**：資料完整性檢查、題目與答案核對、計數與正確率（全班與已答分母分開）、選項分布、作品判讀與原文定位、待驗證錯因、教學決策與再檢核建議。
- **不做**：鑑別度等需較大樣本的統計（樣本不適合時不硬算）、把一次作答當成固定能力、宣稱介入有效。
- **近似反例**：只想設計下一次的檢核 → `tw-edu-formative-assessment`。

## 開始前

讀取 [共用工作方式](references/common/workflow.md)，檢查 `teacher-profile.md`。缺設定仍可工作。

必要資料：題目與標準答案（含答案是否已核實）、匿名作答。學生用代碼，空白代表缺答。

## 思維路線

1. **先查題目**：答案是否核實？有沒有題目可能有兩個答案或題意不清？有疑義的題目標 ambiguous，不計正確率。
2. **查資料**：學生代碼是否重複、有無多餘欄位、缺答比例。缺答多的題目先想是時間不夠、題目太難還是排版問題。
3. **讓腳本計數**：已答人數、缺答、答對、全班正確率、已答正確率、選項分布。兩種分母都呈現，不擇一。
4. **看分布找線索**：答錯集中在同一個選項，可能是共同迷思；分散則可能是猜測或題目問題。
5. **錯因只列候選**：同一個錯誤可能有不同原因，列出 2–3 個候選，並寫出怎麼確認（追問、看算式、請學生說明）。
6. **個別觀察**：標出需要追問的學生，不給能力標籤。
7. **教學決策**：全班再教、分組支持、個別追問、題目修正；每個決策指回證據。
8. **再檢核**：建議一個短期的檢核方式；第二次作答進步也只描述變化，不推論是某個介入造成的。

## 台灣情境要點

- 成績與分析結果不公開個別學生排名（國中小學習評量辦法第11條）。
- 作答資料去識別後再交給 AI，避免上傳姓名與學號。

## 產出

依 [輸入規格](schemas/input.schema.json) 建立 JSON，[範例](examples/example.json) 只看結構。

CSV 匯入（欄位為 student_id 與每題 ID，空白是缺答；不接受多餘欄位或重複學生代碼）：

```bash
python3 "$SKILL_DIR/scripts/import_responses.py" --csv 作答.csv --items 題目輸入.json --output 合併輸入.json
python3 "$SKILL_DIR/scripts/generate_evidence.py" --input "$TASK_DIR/input.json" --validate-only
python3 "$SKILL_DIR/scripts/generate_evidence.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/report.docx"
```

另會輸出 `.analysis.json` 供回查。

## 品質關卡

- 正確率的分母寫清楚。
- 答案未核實或有疑義的題目沒有被算進正確率。
- 每個教學建議都對應到資料。
- 沒有能力標籤或因果宣稱。

## 交接

- 分組支持 → `tw-edu-differentiated`。
- 個別回饋 → `tw-edu-feedback-writer`。
- 題目修正 → `tw-edu-material-reviewer` 或 `tw-edu-exam-generator`。
- 再檢核設計 → `tw-edu-formative-assessment`。
