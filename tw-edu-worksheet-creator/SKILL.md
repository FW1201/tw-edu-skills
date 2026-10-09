---
name: tw-edu-worksheet-creator
description: 學習單製作。依學習目標安排示例、引導練習、獨立練習與反思，設計鷹架與作答空間，檢查閱讀負荷、材料是否足以完成任務與可及性，學生版不含教師解答。適用於學習單、練習單、閱讀學習單、課堂任務單、分層學習單。
metadata:
  version: 4.2.0
  author: 奇老師・數位敘事力社群
  category: 教材資源
---

# 學習單

學習單是學生自己能完成的思考路徑，不是把課本內容挖空。每一題都要能從學習單上的材料完成，並朝學習目標前進一步。

## 定位與邊界

- **做**：任務序列設計、鷹架、作答空間、反思題、閱讀負荷檢查、可及性與分層版本、學生版與教師參考答案分離。
- **不做**：試卷（→ `tw-edu-exam-generator`）、形成性評量的判讀規則（→ `tw-edu-formative-assessment`）。

## 開始前

讀取 [共用工作方式](references/common/workflow.md)，檢查 `teacher-profile.md`。

必要情境：學習目標、學段、使用時機（課堂、回家）、時間長度、教材原文。引用的圖片與文本要有來源與使用權。

## 思維路線

1. **學習目標 → 學生任務**：學生完成這張學習單後，能做到什麼？倒推需要哪些任務。
2. **任務序列**：
   - 示例：一個完整的示範。
   - 引導練習：附提示或半完成的鷹架。
   - 獨立練習：撤除提示。
   - 反思：學生說出自己的做法或卡住的地方。
3. **鷹架設計**：句型框架、步驟提示、圖表組織、關鍵字表；鷹架逐步減少。
4. **材料足夠嗎**：每題需要的資訊都在學習單或指定教材中；不要求學生回答沒教過或沒給資料的內容。
5. **閱讀負荷**：指令簡短、一題一件事；文本長度與字詞難度符合學段。
6. **作答空間**：依預期回答長度留行數，不讓學生擠在小格子裡。
7. **可及性與分層**：提供放大字、圖示、替代表達方式；分層版本保留相同核心目標，不在學生版標示層級高低。
8. **答案分離**：學生版不含解答或教師內部理由；教師參考答案另存。

## 台灣情境要點

- 依教材版本（翰林、南一、康軒、龍騰等）調整用詞，但不複製教科書受著作權保護的大段內容；引用短文需標示出處。
- 課綱學習重點與目標的對應見 `tw-edu-lesson-plan-108`。

## 產出

依 [輸入規格](schemas/input.schema.json) 建立 JSON，[範例](examples/example.json) 只看結構。重點欄位：`instructions`、`prompts`（題目與 `response_space_lines`）、`reflection`。

```bash
python3 "$SKILL_DIR/scripts/generate_worksheet.py" --input "$TASK_DIR/input.json" --validate-only
python3 "$SKILL_DIR/scripts/generate_worksheet.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/worksheet.docx"
```

## 品質關卡

- 每題都對應學習目標，且材料足以作答。
- 有從示範到獨立的鷹架遞減。
- 學生版沒有答案。
- 來源與圖片用途可查核。

## 交接

- 分層需求 → `tw-edu-differentiated`。
- 印前檢查 → `tw-edu-material-reviewer`。
- 學生作品回饋 → `tw-edu-feedback-writer`。
