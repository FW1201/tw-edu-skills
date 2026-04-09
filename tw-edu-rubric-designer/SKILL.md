---
name: tw-edu-rubric-designer
description: >
  依據學習目標設計完整評量規準（Rubric），支援整體式與分析式兩種格式。
  當使用者提及「評量規準」「rubric」「評分標準」「評量表」
  「作業規準」「口頭報告評分」「實作評量」時觸發。
version: 1.0.0
allowed-tools: "Bash, Read, Write"
disable-model-invocation: true
---

# 評量規準設計工具

## Step 0：讀取參考文件
- `references/rubric_design_guide.md`
- `/mnt/skills/public/docx/SKILL.md`


**概念對齊協議（必要前置步驟）：**
`../../tw_edu_concept_alignment.md`
→ 在執行任何工作前，先完成概念對齊確認卡。


## Step 1：資訊收集
1. 評量的任務/作業名稱？
2. 科目與年級？
3. 整體式（Holistic）or 分析式（Analytic）規準？
4. 評量向度有哪些？（教師可自訂，或由 Claude 建議）
5. 幾個等第？（建議 4 等第：傑出/精熟/基礎/待加強）

## Step 2：生成評量規準文件

```bash
python scripts/generate_rubric.py \
  --task "[任務名稱]" \
  --subject "[科目]" --grade "[年級]" \
  --type "[holistic/analytic]" \
  --dimensions "[向度1,向度2,向度3]" \
  --output "/mnt/user-data/outputs/[任務]_評量規準.docx"
```

## 文件結構
- 封面：任務說明 + 評量規準用途說明
- 分析式規準表（各向度 × 4 等第 × 描述語）
- 教師評量記錄區
- 學生自評 / 同儕評量區
- 評量規準設計說明（給家長）

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
