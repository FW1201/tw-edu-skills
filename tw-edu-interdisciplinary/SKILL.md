---
name: tw-edu-interdisciplinary
description: 跨領域課程設計。從共同問題或大概念出發，寫出每個領域不可替代的知識與方法貢獻、協同時數與分工、學習活動與共同評量，各領域學習重點可回查課綱。適用於跨領域、跨科協同、主題課程、素養導向跨科教學、議題探究。
metadata:
  version: 4.2.0
  author: 奇老師・數位敘事力社群
  category: 課程設計
---

# 跨領域課程

好的跨領域課程是「沒有這個科目，問題就解不了」，而不是把幾個科目的活動放在同一個主題下並列。

## 定位與邊界

- **做**：共同問題與大概念、各領域貢獻矩陣、協同時數與分工、活動序列、共同成果與評量、課綱回查。
- **不做**：單一科目教案（→ `tw-edu-lesson-plan-108`）、完整專題流程管理（→ `tw-edu-pbl-designer`）、學校總體課程計畫（→ `tw-edu-school-curriculum-plan`）。

## 開始前

讀取 [共用工作方式](references/common/workflow.md)，檢查 `teacher-profile.md`。

必要情境：參與的科目與教師、學段、可用節數（各科分別）、共同主題或問題。協同教師的實際時數未知時標待確認，不假設全員都能共同授課。

## 思維路線

1. **共同問題**：一個需要多領域才能回答的問題，例如「學校午餐的食材該從哪裡來？」。
2. **大概念**：學生學完能遷移到其他情境的理解。
3. **各領域貢獻**：每科寫「提供什麼知識」與「提供什麼方法」。若拿掉某科，問題仍能完整回答，代表那科只是點綴，要重新設計或移除。
4. **學習重點回查**：每科列學習表現或學習內容代碼，用查詢器回查，指定領域。
5. **協同方式**：各科分開教再整合、協同教學、輪流主導；寫出每科實際節數與誰負責哪一段。
6. **活動序列**：各科活動之間如何接力；前一科的產出是否成為下一科的輸入。
7. **共同成果與評量**：一個整合的成果，評量分成共同能力（如問題解決、溝通）與各科目標兩部分，避免只評作品外觀。

## 台灣情境要點

- 課綱代碼查詢：

```bash
python3 "$SKILL_DIR/scripts/lookup_curriculum.py" --domain 自然科學 --keyword 能量 --limit 10
```

查詢說明見 [課綱指標查詢](references/108_subject_indicators.md)；核心素養見 [核心素養](references/108_core_competencies.md)。
- 國中小常在彈性學習課程的統整性主題或議題探究中實施；與校訂課程的關係見 `tw-edu-school-curriculum-plan`。

## 產出

依 [輸入規格](schemas/input.schema.json) 建立 JSON，[範例](examples/example.json) 只看結構。重點欄位：`driving_question`、`discipline_contributions`（每科 knowledge 與 method）、`activities`、`product`。

```bash
python3 "$SKILL_DIR/scripts/generate_interdisciplinary.py" --input "$TASK_DIR/input.json" --validate-only
python3 "$SKILL_DIR/scripts/generate_interdisciplinary.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/interdisciplinary.docx"
```

## 品質關卡

- 每科都有不可替代的知識與方法。
- 協同時數與分工可以實際執行。
- 共同評量同時看到共同能力與各科目標。
- 課綱代碼有查核狀態。

## 交接

- 各科教案 → `tw-edu-lesson-plan-108`。
- 長期專題的里程碑管理 → `tw-edu-pbl-designer`。
- 共同評量規準 → `tw-edu-rubric-designer`。
