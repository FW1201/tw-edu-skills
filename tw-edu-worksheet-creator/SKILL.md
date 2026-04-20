---
name: tw-edu-worksheet-creator
description: >
  依課文、主題、年級生成素養導向學習單，整合提問鷹架與圖表填寫。
  當使用者提及「學習單」「任務單」「工作單」「練習單」
  「活動學習單」「課堂學習單」「設計學習單」時觸發。
version: 1.0.0
allowed-tools: "Bash, Read, Write"
disable-model-invocation: true
---

# 學習單生成工具

---

## 設計系統 V2.0：Edu Warm × A4 格線

> 基於 Claude Design（2026-04-17）+ canvas-design 最少裝飾原則

### A4 版面格線系統（595×842pt）
```
所有邊距: 72pt（1英寸）
內容欄寬: 451pt
格線 base unit: 8pt
行距建議: 1.75（閱讀舒適）
```

### Edu Warm 學習單字型
```
主標題（學習單名稱）: Work Sans Bold 18pt / color: #d97757
小節標題:            Work Sans SemiBold 14pt
正文/問題:           Noto Sans TC Regular 12pt / line-height: 1.75
填答空格標示:        Noto Sans TC Regular 12pt / color: #6B6B6B
頁碼:                Noto Sans TC Regular 10pt
```

> **禁用字型**：Inter、Roboto、Arial — 缺乏教育溫感，改用 Work Sans + Noto Sans TC  
> **禁用模式**：每題加邊框裝飾色條、漸層背景 — 學習單以留白與對齊勝出

### HTML artifact 輸出（A4 可列印版）
學習單優先輸出為 **HTML artifact**（A4 比例，可直接列印）：
```css
.worksheet { width: 595px; min-height: 842px; padding: 72pt;
             font-family: 'Noto Sans TC', sans-serif;
             background: white; }
.worksheet p, .worksheet li { text-wrap: pretty; }  /* 防止孤字 */
@media print { .worksheet { page-break-inside: avoid; } }
```

### canvas-design 最少裝飾原則
- 格線輔助：8pt 格線保持元素對齊，不顯示格線本身
- 色彩克制：最多 3 種顏色（Edu Warm 主色 #d97757 + 黑 + 灰）
- 空間留白：每個問題區塊之間保持 16pt 間距

---

## Step 0：讀取文件
- `/mnt/skills/public/docx/SKILL.md`


**概念對齊協議（必要前置步驟）：**
`../../tw_edu_concept_alignment.md`
→ 在執行任何工作前，先完成概念對齊確認卡。


## Step 1：資訊收集
1. 科目、年級、課文/主題？
2. 這份學習單的目的（預習/課中/複習/作業）？
3. 需要哪類活動設計？
   - 閱讀理解提問（三層次：字面/推論/評鑑）
   - 概念圖/心智圖填寫框架
   - 表格比較分析
   - 仿作/創作引導
   - 反思與自評

## Step 2：生成學習單

```bash
python scripts/generate_worksheet.py \
  --subject "[科目]" --grade "[年級]" --topic "[主題]" \
  --purpose "[preview/inclass/review/homework]" \
  --activities "[comprehension,concept_map,compare,writing]" \
  --output "/mnt/user-data/outputs/[主題]_學習單.docx"
```

## 設計規範
- A4 直向，留白充足（學生書寫空間 > 50%）
- 標題明確，每個活動有清楚的任務說明
- 提供布魯姆層次提示（讓學生了解思考深度）
- 頁尾有班級/姓名/日期填寫欄
- 美觀排版：使用線框、底色區塊區隔不同活動

### 設計原則（影響學習效果的關鍵）

**每頁聚焦一個核心任務**
若學習單涵蓋多個概念，請切分為多頁或明確的多段。學生的注意力一次能有效處理的訊息有限，把多個任務塞進同一頁會讓他們來回切換、反而每個都學得淺。

**圖文相鄰原則**
說明文字與對應圖表放在**相鄰位置**，不分頁。純裝飾性插圖（不傳達概念的插圖）省略，視覺裝飾分散注意力而非幫助理解。

**三層次題目設計邏輯**
- 基礎題：確認學生是否具備先備知識
- 核心題：落在「有引導就能完成、無引導則困難」的區間
- 延伸題：讓能力較強的學生繼續探索

**鷹架是可以撤除的支持**
句型提示、部分填寫示例設計為可逐步移除：第一次使用 → 完整鷹架；熟悉後 → 只保留問題引導；最終目標是學生能獨立完成。

---

## 年級適應 + 引導式收集（v2.0 更新）

### 自動年級偵測
從使用者輸入辨識學習階段（國小/國中/高中），自動調整：
- 教學語言複雜度與詞彙難度
- 布魯姆認知層次分布
- 活動設計的自主程度
- 課綱代碼學段後綴（-E- / -J- / -U-）

詳見：`../../tw_edu_grade_adapter.md`

### 引導式資訊收集
啟動時執行漸進式三輪問答，確保取得充足資訊再開始任務。
詳見：`../../tw_edu_guided_collection.md`

---

## MCP 連接器

### Claude Code ／ Claude.ai（Pro/Team/Enterprise）
```
WebSearch（自動啟用）：
  搜尋最新課綱資料、教材資源、時事素材

Google Drive（若已連接，Settings → Connectors）：
  直接從 Drive 讀取現有教材
  完成後直接儲存輸出文件到 Drive
```

### 其他平台（Codex / gemini-cli）
MCP 不可用，Claude 使用訓練知識執行，並提示使用者手動儲存。

---

## MCP 整合更新（v3.0）

**讀取全域策略文件：`../../tw_edu_mcp_strategy.md`**

### 本 Skill 適用的 MCP 最佳化

**WebSearch（已啟用）：**
搜尋最新課綱資料、教學素材、時事情境。

**Canva MCP（若已連接）：**
使用者說「幫我做更美觀的版本」或「Canva 設計」時：
→ 呼叫 Canva:generate-design 生成高設計感版本
→ 優先適用：教案封面、簡報、學習單封面

**Google Drive（若已連接）：**
文件生成後詢問：「要上傳到 Google Drive 嗎？」
→ 確認後上傳，返回分享連結
→ 不修改任何現有檔案的分享權限

**安全原則：**
所有 MCP 寫入操作執行前，必須顯示確認摘要並等待使用者確認。
