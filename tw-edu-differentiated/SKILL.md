---
name: tw-edu-differentiated
description: 差異化教學設計。在共同學習目標下，依學生學習證據從內容、過程、成果、環境四面向調整任務與支持，涵蓋學習扶助（補救）與加深加廣，並寫出調組依據與支持撤除條件。適用於差異化、分層任務、UDL、學習扶助、資優加深、融合班級調整。
metadata:
  version: 4.2.0
  author: 奇老師・數位敘事力社群
  category: 課程設計
---

# 差異化教學

差異化不是把學生分成好、中、差三組做不同的事，而是讓所有學生朝同一個學習目標前進，只是路徑、支持與表現方式不同，而且分組會隨證據改變。

## 定位與邊界

- **做**：共同目標、依證據的學習需求分組、四面向調整、學習扶助與加深加廣、UDL 選擇、調組與撤除支持條件。
- **不做**：特教 IEP 本身（→ `tw-edu-guidance-collaboration`）、全班作答分析（→ `tw-edu-learning-evidence-analyzer`）、診斷或標籤化分組。

## 開始前

讀取 [共用工作方式](references/common/workflow.md)，檢查 `teacher-profile.md`。

必要情境：學習目標、學生的學習證據（前測、作業、觀察；匿名）、班級人數、可用時間與資源。沒有證據時，先建議用一個快速檢核取得證據，不憑印象分組，也不補造學生人數或表現。

## 思維路線

1. **鎖定共同目標**：寫出所有學生都要達成的核心目標；差異化調整的是路徑，不是降低目標。
2. **讀證據分需求**：依證據把學生分成幾種「需求」（例如：概念未建立、程序不穩、已熟練可延伸），每組寫出依據的證據。分組名稱描述需求，不描述能力高低。
3. **選調整面向**：
   - 內容：不同難度或形式的材料（文本、圖像、操作物）。
   - 過程：鷹架、示範、分段任務、同儕協作。
   - 成果：不同表現方式（口說、圖解、書寫、作品）。
   - 環境：座位、時間、工具、噪音與視覺干擾。
4. **學習扶助**：針對先備缺口設計短介入（10–15 分鐘的再教或練習），並安排再檢核。
5. **加深加廣**：已達標的學生做更複雜的應用、遷移或探究，不是做更多同樣的題目。
6. **UDL**：提供多種參與、表徵與表達方式，讓需要的學生自己選，不只給特定學生。
7. **調組與撤除支持**：寫出何時重新分組（例如每次形成性評量後）、支持在學生能獨立表現後如何逐步撤除。

## 台灣情境要點

- 普通班中的特教學生：調整依 IEP 與特教老師建議；導師與任課教師的合作見 `tw-edu-guidance-collaboration`。
- 學習扶助：依學校學習扶助方案的篩選與追蹤機制；本技能處理課堂內的即時調整。

## 產出

依 [輸入規格](schemas/input.schema.json) 建立 JSON，[範例](examples/example.json) 只看結構。重點欄位：`shared_goal`、`learner_groups`（每組的 `evidence` 與 `support`）、`activities`。

```bash
python3 "$SKILL_DIR/scripts/generate_differentiated.py" --input "$TASK_DIR/input.json" --validate-only
python3 "$SKILL_DIR/scripts/generate_differentiated.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/differentiated.docx"
```

## 品質關卡

- 每組都朝同一個共同目標，沒有組別被降低目標。
- 每組的依據是學習證據，不是印象或標籤。
- 至少一個面向提供學生選擇。
- 有調組時間點與撤除支持的條件。
- 學生可見材料不出現組別的能力標記。

## 交接

- 需要判讀全班作答 → `tw-edu-learning-evidence-analyzer`。
- 分層學習單 → `tw-edu-worksheet-creator`；分層試題 → `tw-edu-exam-generator`。
- 再檢核設計 → `tw-edu-formative-assessment`。
