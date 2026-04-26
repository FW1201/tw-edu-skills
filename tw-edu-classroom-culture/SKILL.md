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
  - 每條班規讓學生看見**它在培養什麼能力**（例：「輪流發言」= 練習傾聽與自我管理；不只是遵守秩序）
  - 能力可見，學生才不只是「服從規定」，而是**理解規定的意義**
- **PBS 方案**：預防/教導/增強三層架構
- **導師週記**：觀察記錄、個別輔導記錄、班級氣氛評估
- **班會設計**：民主討論流程、學生自治能力培養
  - 每次會議議程最後加入**反思問句**（例：「這場討論中，你怎麼管理自己的不同意見？」）
  - 不只討論議題，也練習討論**過程中**的自我管理
- **衝突調解**：引導學生用以下步驟處理衝突——
  1. 說出你感受到的情緒（用具體詞彙，不是「我很不爽」）
  2. 說出你理解對方的感受是什麼
  3. 你們的需求在哪裡重疊？
  4. 可以試試什麼解決方法？
  5. 執行後回來討論結果

### 每日情緒 Check-in（建議加入班級日常）

在開始上課或班級活動前，保留 2 分鐘：
- 使用**情緒詞彙輪**（提供超過 10 個選項，不只是「好/不好」）
- 引導學生說出具體情緒詞，而非只說「還好」
- 具體詞彙 → 準確理解 → 才有可能調節情緒

這個習慣不需要花大量時間，但能顯著提升學生在課堂中的投入感與班級安全感。

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

### Codex 平台
MCP Connectors 透過 `~/.codex/config.toml` 設定（`codex mcp add` 指令或手動編輯）。
未設定時自動降級：請參閱上方降級方案。

### Antigravity 平台（Google AI IDE）
MCP 透過 MCP Server Hub（1,500+ servers）或 `~/.gemini/antigravity/mcp_config.json` 設定。
支援 Jupyter Notebook 整合。未設定時自動降級：請參閱上方降級方案。

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
