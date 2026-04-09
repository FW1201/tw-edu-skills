---
name: tw-edu-differentiated
description: >
  為同一節課設計差異化教學方案，提供基礎/標準/進階三層次學習任務，
  整合通用設計學習（UDL）框架，支援融合教育與特殊需求情境。
  當使用者提及「差異化」「分層教學」「UDL」「不同程度學生」
  「特殊需求」「融合教育」「適性教學」「因材施教」時觸發。
version: 1.0.0
allowed-tools: "Bash, Read, Write"
disable-model-invocation: true
---

# 差異化教學設計工具

## Step 0：讀取參考文件
- `references/udl_framework.md` — UDL 通用設計學習三原則
- `references/differentiation_strategies.md` — 差異化策略庫
- `/mnt/skills/public/docx/SKILL.md`


**概念對齊協議（必要前置步驟）：**
`../../tw_edu_concept_alignment.md`
→ 在執行任何工作前，先完成概念對齊確認卡。


## Step 1：資訊收集
1. 課文/單元名稱與年級科目？
2. 這節課的核心學習目標？
3. 班上學生組成？（一般生/資優/學習障礙/新住民/其他）
4. 主要差異化向度？（學習內容/學習過程/學習成果/學習環境）

## Step 2：生成差異化文件
```bash
python scripts/generate_differentiated.py \
  --subject "[科目]" --title "[課文]" --grade "[年級]" \
  --needs "[學生需求說明]" \
  --output "/mnt/user-data/outputs/[課文]_差異化設計.docx"
```

## 文件結構
### 封面：差異化教學設計摘要
### 表格一：三層次學習任務對照
| 層次 | 目標修訂 | 學習活動 | 支援策略 | 評量調整 |
|基礎層（Essential）|降低認知負荷|...|鷹架支援|...|
|標準層（Core）|課綱標準|...|適度引導|...|
|進階層（Advanced）|延伸深化|...|開放探究|...|

### 表格二：UDL 三原則應用
| 原則 | 設計重點 | 具體做法 |
|提供多元表徵方式|如何呈現資訊|...|
|提供多元行動與表達方式|學生如何學習|...|
|提供多元參與方式|如何激發動機|...|

### 表格三：個別學生調整建議
（依教師輸入的特殊需求填入）

### 表格四：差異化評量規準
（各層次對應不同評量期待）

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
