---
name: tw-edu-lesson-plan-108
description: 108 課綱素養導向教案。依學習重點（學習表現×學習內容）以逆向設計排出目標、評量與活動，活動分鐘數加總等於總時間，課綱代碼用隨包快照回查，可融入議題與差異化。適用於教案、備課、單元設計、公開授課教案、108課綱教學設計。
metadata:
  version: 5.0.0
  author: 奇老師・數位敘事力社群
  category: 課程設計
---

# 108 課綱教案

把一節或一個單元的教學，寫成目標、評量、活動彼此對得起來的素養導向教案。教案的核心不是活動多精彩，而是每個活動都在產生學生達成目標的證據。

## 定位與邊界

- **做**：學習重點對應、可觀察的學習目標、評量設計、活動流程與分鐘數、課綱代碼查核、議題融入、差異化掛點、教學試作與雙語模式。
- **不做**：還沒想法時的發想（→ `tw-edu-lesson-design-brainstorm`）、一學期進度（→ `tw-edu-curriculum-mapper`）、學校課程計畫（→ `tw-edu-school-curriculum-plan`）、完整差異化方案（→ `tw-edu-differentiated`）。

## 開始前

讀取 [共用工作方式](references/common/workflow.md)，檢查 `teacher-profile.md`（科目、學段、教材版本、慣用格式）。本次要求優先。

必要情境：學段與年級、科目、主題或課文、總節數或總分鐘、教材來源、學生先備。缺少教材時先請老師提供，不憑記憶寫課文內容。

## 思維路線

1. **選模式**：單節（一節課的完整流程）、單元（數節課的架構與每節重點）、多節（跨週的連續設計）。
2. **定學習重點**：從領綱找學習表現與學習內容，各選 1–3 條。用課綱查詢器回查代碼與敘述；同一代碼在不同領域敘述不同，查詢一定指定領域。
3. **寫學習目標**：每個目標是學生可被觀察的表現（動詞＋內容＋條件），對應到學習重點。避免「了解」「體會」這類無法觀察的動詞，參考 [認知層次](references/bloom_taxonomy_tw.md)。
4. **先設計評量**：每個目標用什麼證據判斷學生達成？寫出方法與成功準則。每個目標都要被評量。
5. **再設計活動**：引起動機 → 發展 → 綜合。每個活動標明對應的目標編號，確保每個目標都被教到。素養導向檢核：是否連結真實情境、是否讓學生用方法解決問題、是否有表現機會。
6. **時間配置**：活動分鐘加總必須等於總時間。轉換、收拾、說明都要算進去。
7. **議題與差異化**：相關議題寫具體融入點，不只列名稱；需要支持的學生寫一兩個掛點（鷹架、分層任務），細節交給差異化技能。
8. **選用模式**：
   - 教學試作：寫出想改善的問題、短期試作、要看的學生證據、再檢核與停止條件。
   - 雙語：內容目標與語言目標分開，不把語言流利度當成學科理解。
   - 科學活動：列變因、測量與證據解釋，安全條件依學校規定確認。

## 台灣情境要點

- 教案格式參考 [教案格式](references/lesson_plan_format.md)；核心素養表見 [核心素養](references/108_core_competencies.md)。
- 課綱代碼查詢（隨包 9 領域 3460 筆快照）：

```bash
python3 "$SKILL_DIR/scripts/lookup_curriculum.py" --domain 國語文 --code 5-IV-2
python3 "$SKILL_DIR/scripts/lookup_curriculum.py" --domain 英語文 --kind performance --keyword 聆聽 --limit 10
```

查詢說明與快照限制見 [課綱指標查詢](references/108_subject_indicators.md)。快照不是官方全文，正式送件回查教育部公告版本。

## 產出

依 [輸入規格](schemas/input.schema.json) 建立 JSON，[範例](examples/example.json) 只看結構。v5 新增選填欄位：`mode`、`learning_focus`（performance、content）、`issues`、`differentiation`。

```bash
# SKILL_DIR 為本技能安裝目錄；TASK_DIR 為目前工作區的任務輸出目錄。
python3 "$SKILL_DIR/scripts/generate_lesson_plan.py" --input "$TASK_DIR/input.json" --validate-only
python3 "$SKILL_DIR/scripts/generate_lesson_plan.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/lesson-plan.docx"
```

依賴：`python3 -m pip install -r "$SKILL_DIR/requirements.txt"`。語意閘門會擋下：編號重複、活動分鐘不等於總時間、有目標沒被教或沒被評量、引用不存在的目標、未查核的課綱代碼沒有說明。

## 品質關卡

- 每個目標都能被觀察，且同時出現在活動與評量。
- 分鐘數加總正確。
- 課綱代碼都有查核狀態；待確認的不寫成已查核。
- 學生版材料（學習單、簡報）不含教師答案。
- 教材內容來自老師提供或可查證來源。

## 交接

- 學習單 → `tw-edu-worksheet-creator`；簡報 → `tw-edu-slides-creator`；評量 → `tw-edu-exam-generator`、`tw-edu-rubric-designer`。
- 分層支持 → `tw-edu-differentiated`（帶目標與學生證據）。
- 公開授課 → `tw-edu-open-lesson`（帶目標與想觀察的焦點）。
