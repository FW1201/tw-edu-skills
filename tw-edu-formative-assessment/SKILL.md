---
name: tw-edu-formative-assessment
description: 形成性評量設計。從學習目標寫出成功準則，設計課中檢核點（出口票、提問、小白板、同儕互評），預先訂好判讀規則與對應的教學決策，並安排短期再檢核。適用於形成性評量、出口票、課堂提問、學習檢核、即時回饋、補救前診斷。
metadata:
  version: 4.2.0
  author: 奇老師・數位敘事力社群
  category: 評量命題
---

# 形成性評量

形成性評量的價值在於「看到證據之後，教學會改變」。只設計題目、不設計判讀與調整，就只是小考。

## 定位與邊界

- **做**：學習目標與成功準則、檢核點設計、證據蒐集方式、判讀規則、教學決策、再檢核。
- **不做**：原始作答的統計分析（→ `tw-edu-learning-evidence-analyzer`）、段考命題（→ `tw-edu-exam-generator`）。

## 開始前

讀取 [共用工作方式](references/common/workflow.md)，檢查 `teacher-profile.md`。

必要情境：這節課的學習目標、學生先備、可用時間（形成性評量通常 3–10 分鐘）、可用工具（紙本、小白板、平板）。

## 思維路線

1. **學習目標 → 成功準則**：用學生聽得懂的話寫出「做到什麼就代表學會了」。
2. **選檢核點時機**：課前（先備）、課中（關鍵概念後）、課末（出口票）。
3. **設計檢核任務**：一到三題，直接對準最常見的誤解；能在短時間內看完全班的回答。
4. **預先寫判讀規則**：例如「八成以上答對 → 進入下一段；答錯集中在 B 選項 → 代表把分子分母倒置，重新用圖示示範」。判讀規則要在上課前就決定。
5. **教學決策**：全班再教、分組支持、個別追問、繼續前進，各對應一個判讀結果。
6. **再檢核**：調整後用一題相似但不同的題目確認；不因一次答對就宣稱已精熟。
7. **學生參與**：讓學生用成功準則自評或互評，知道自己的下一步。

## 台灣情境要點

- 國中小學習評量辦法將平時評量與定期評量並列；形成性評量多屬平時評量的一部分，結果用於調整教學，是否計分依學校規定。

## 產出

依 [輸入規格](schemas/input.schema.json) 建立 JSON，[範例](examples/example.json) 只看結構。重點欄位：`learning_target`、`checks`（題目、成功準則、證據蒐集方式）、`response_rules`（證據 → 行動）。

```bash
python3 "$SKILL_DIR/scripts/generate_formative.py" --input "$TASK_DIR/input.json" --validate-only
python3 "$SKILL_DIR/scripts/generate_formative.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/formative.docx"
```

## 品質關卡

- 每個檢核點都有對應的判讀規則與教學行動。
- 檢核題目對準常見誤解，而不是只問記憶。
- 有再檢核的安排。
- 只設計檢核時，不宣稱學生已經改善。

## 交接

- 收回的作答要分析 → `tw-edu-learning-evidence-analyzer`。
- 需要分組支持 → `tw-edu-differentiated`。
- 個別回饋 → `tw-edu-feedback-writer`。
