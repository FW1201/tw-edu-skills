---
name: tw-edu-curriculum-mapper
description: 學期課程地圖。把一學期或一學年的單元排進週次與節數，對應學習目標、課綱代碼與評量，並和段考、校慶、連假等校行事交叉檢查進度衝突，輸出 Excel。適用於課程地圖、學期進度表、教學計畫進度、學年規劃。
metadata:
  version: 5.0.0
  author: 奇老師・數位敘事力社群
  category: 課程設計
---

# 學期課程地圖

把一學期的教學放在同一張表上：每個單元在哪幾週、幾節、要達成什麼、對應哪些課綱代碼、怎麼評量，並且避開校行事造成的進度斷裂。

## 定位與邊界

- **做**：單元與週次節數配置、目標與課綱對應、評量分布、校行事衝突檢查、先備與進階關係。
- **不做**：單節教案（→ `tw-edu-lesson-plan-108`）、全校課程計畫（→ `tw-edu-school-curriculum-plan`）。

## 開始前

讀取 [共用工作方式](references/common/workflow.md)，檢查 `teacher-profile.md`（科目、學段、教材版本、每週節數）。

必要情境：學期週數、每週節數、教材單元清單、校行事曆（段考週、校慶、連假、畢業旅行）。校行事未提供時，表格仍可產出，但在待確認中列出。

## 思維路線

1. **算可用節數**：學期週數 × 每週節數 − 段考、活動、連假占用。先算總量，再分配。
2. **單元排序**：依教材順序與先備關係；需要前一單元概念的單元不能排在前面。
3. **配置節數**：重點單元給足時間，複習與評量也要占節數。總配置不能超過可用節數。
4. **目標與課綱**：每個單元寫 1–3 個學習目標，對應課綱代碼並回查；同一代碼跨領域敘述不同，查詢指定領域。
5. **評量分布**：形成性評量分散在單元中，總結性評量對齊段考範圍；避免同一週多科大考（若有跨科資訊）。
6. **校行事衝突**：段考前一週是否還在教新單元？連假前後是否切斷一個單元？衝突處提出調整建議。
7. **檢視覆蓋**：一學期下來，課綱的學習表現是否集中在少數幾條？是否有該教卻沒排到的？

## 台灣情境要點

- 課綱代碼查詢：

```bash
python3 "$SKILL_DIR/scripts/lookup_curriculum.py" --domain 數學 --keyword 分數 --limit 10
```

查詢說明見 [課綱指標查詢](references/108_subject_indicators.md)；核心素養見 [核心素養](references/108_core_competencies.md)。

## 產出

依 [輸入規格](schemas/input.schema.json) 建立 JSON，[範例](examples/example.json) 只看結構。v5 新增選填 `school_events`（週次、校行事），會輸出成第二張工作表「校行事對照」。

```bash
python3 "$SKILL_DIR/scripts/generate_curriculum_map.py" --input "$TASK_DIR/input.json" --validate-only
python3 "$SKILL_DIR/scripts/generate_curriculum_map.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/curriculum-map.xlsx"
```

語意閘門：未查核的課綱代碼必須附查核說明。

## 品質關卡

- 總節數不超過可用節數。
- 每個單元都有目標、代碼查核狀態與評量。
- 段考範圍與單元進度一致。
- 校行事衝突已標出並有調整建議。

## 交接

- 單元展開成教案 → `tw-edu-lesson-plan-108`。
- 全校層級的課程架構 → `tw-edu-school-curriculum-plan`。
