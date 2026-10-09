---
name: tw-edu-research-viz
description: 教學研究視覺化。為教師行動研究、課程評鑑與研習成果製作 PRISMA 簡化流程圖與流程架構圖，數量必須守恆、中文可讀，記錄資料來源與設計限制，不冒充完整系統性回顧。適用於行動研究流程圖、PRISMA、研究架構圖、成果簡報圖表、教學研究視覺化。
metadata:
  version: 4.2.0
  author: 奇老師・數位敘事力社群
  category: 教師專業
---

# 教學研究視覺化

圖表要讓讀者一眼看懂研究或課程歷程，而且每個數字都能回到資料。圖畫得漂亮但數字對不上，比沒有圖更糟。

## 定位與邊界

- **做**：PRISMA 簡化流程圖（文獻篩選數量守恆）、簡易流程或架構圖（行動研究循環、課程實施流程）、中文字型處理、來源與限制說明。
- **不做**：完整系統性回顧報告、統計分析、資料圖表的詳細設計（長條圖、折線圖可用簡報技能的原生圖表）。

## 開始前

讀取 [共用工作方式](references/common/workflow.md)，檢查 `teacher-profile.md`。

必要情境：圖的用途（投稿、研習、成果報告）、資料與單位、樣本或文獻數量、來源。

## 思維路線

1. **確認目的**：讀者是誰？這張圖要回答什麼問題？
2. **選圖型**：文獻篩選 → PRISMA 簡化流程；研究或課程歷程 → 流程圖（節點與數值）。圖型選擇參考 [視覺化類型](references/academic_viz_types.md)。
3. **檢查數量守恆**（PRISMA）：辨識數 = 移除重複數 + 篩選數；篩選數 = 篩選排除數 + 全文評估數；全文評估數 = 全文排除數 + 納入數。對不上就先回頭查資料。
4. **區分單位**：records、reports、studies 的計數不同時，標明需要完整研究模式，不在簡化圖中混用。
5. **中文可讀**：使用系統中的繁體中文字型；字型不可用時停止並說明，不輸出方框字。
6. **註明限制**：資料來源、時間、這是簡化圖而非完整 PRISMA 2020 報告。

## 台灣情境要點

- 教師行動研究常用「問題 → 計畫 → 行動 → 觀察 → 反思」循環，可用流程圖呈現每一輪的重點與證據。
- 研習成果圖不放學生個資與可辨識照片。

## 產出

依 [輸入規格](schemas/input.schema.json) 建立 JSON，[範例](examples/example.json) 只看結構。`type` 為 prisma 時填 `prisma` 各數值，simple_diagram 時填 `nodes`。

```bash
python3 "$SKILL_DIR/scripts/generate_prisma.py" --input "$TASK_DIR/input.json" --validate-only
python3 "$SKILL_DIR/scripts/generate_prisma.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/diagram.png"
```

語意閘門會擋下 PRISMA 三個階段任一數量不守恆。

## 品質關卡

- 數量守恆，與資料表一致。
- 中文正常顯示。
- 圖說寫出資料來源與限制。

## 交接

- 文獻查核 → `tw-edu-citation-checker`。
- 放進簡報 → `tw-edu-slides-creator`。
- 公開授課的試作循環 → `tw-edu-open-lesson`。
