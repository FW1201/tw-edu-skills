---
name: tw-edu-classroom-culture
description: >
  提供班級經營策略，包含班規設計、積極行為支持(PBS)方案、
  導師週記、班級氣氛建立活動。
  當使用者提及「班級經營」「班規」「PBS」「導師週記」
  「班會」「班級文化」「班級公約」「獎懲制度」「正向管教」時觸發。
version: 1.0.0
allowed-tools: "Bash, Read, Write"
disable-model-invocation: true
---

# 班級經營與文化建立工具

## Step 0：讀取文件
- `references/classroom_management.md`
- `/mnt/skills/public/docx/SKILL.md`


**概念對齊協議（必要前置步驟）：**
`../../tw_edu_concept_alignment.md`
→ 在執行任何工作前，先完成概念對齊確認卡。


## Step 1：資訊收集
1. 目前需要協助的面向？
   - 學期初班規設計
   - PBS 積極行為支持方案
   - 導師週記撰寫
   - 班會活動設計
   - 學生衝突調解流程
2. 年級與班級特性（普通班/特殊班/混齡）？
3. 目前遇到的主要挑戰？

## Step 2：生成班級經營文件

```bash
python scripts/generate_classroom.py \
  --type "[rules/pbs/weekly/meeting/conflict]" \
  --grade "[年級]" --challenge "[主要挑戰描述]" \
  --output "/mnt/user-data/outputs/班級經營_[類型].docx"
```

## 各類型重點
- **班規設計**：正向語言、學生共同制定、具體行為描述
- **PBS 方案**：預防/教導/增強三層架構
- **導師週記**：觀察記錄、個別輔導記錄、班級氣氛評估
- **班會設計**：民主討論流程、學生自治能力培養

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
