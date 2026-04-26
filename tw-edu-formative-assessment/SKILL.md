---
name: tw-edu-formative-assessment
description: >
  設計課堂形成性評量工具，包含出口票、KWL表、概念圖提示、診斷測驗等。
  當使用者提及「形成性評量」「出口票」「exit ticket」「KWL」
  「課前測」「診斷評量」「即時評量」「學習檢核」時觸發。
version: 1.0.0
allowed-tools: "Bash, Read, Write"
disable-model-invocation: true
---

# 形成性評量工具生成器

## Step 0：讀取文件
- `/mnt/skills/public/docx/SKILL.md`


**概念對齊協議（必要前置步驟）：**
`../../tw_edu_concept_alignment.md`
→ 在執行任何工作前，先完成概念對齊確認卡。


## Step 1：資訊收集
0. **先確認兩件事再選工具**：
   - 這節課的**學習意圖**是什麼？（這堂課結束後，學生應該能做到什麼？）
   - **成功標準**是什麼？（學生達成目標時，會有什麼可觀察的表現？）
   → 學習意圖和成功標準不清楚，評量收集到的資料就沒有方向。
1. 科目、年級、主題？
2. 評量目的（課前診斷/課中監控/課後出口）？
3. 工具類型？
   - 出口票（Exit Ticket）
   - KWL 表（Know-Want-Learned）
   - 概念理解自評量表
   - 課前知識診斷測驗（3-5 題）
   - 學習收穫與困惑記錄單

## Step 2：生成評量工具

```bash
python scripts/generate_formative.py \
  --subject "[科目]" --grade "[年級]" --topic "[主題]" \
  --type "[exit_ticket/kwl/self_check/diagnostic]" \
  --output "/mnt/user-data/outputs/[主題]_形成性評量.docx"
```

## 輸出設計
- 每份評量工具設計**三個節點**：
  - **課前**（了解起點）→ 學生帶著哪些先備知識進來？
  - **課中**（即時偵測）→ 學生卡在哪裡？哪裡需要即時調整？
  - **課後**（確認理解）→ 學生達成學習意圖了嗎？
  - 每個節點都要有「**教師觀察後如何調整**」的記錄欄
- 一頁排版 2-4 份（方便裁切分發）
- 留白足夠學生書寫
- 包含教師觀察記錄表（另一頁）

### KWL 表設計提醒
傳統 KWL 的 W 欄（Want to know）效果有限，建議改為：
- W 欄 → **「這節課我預計達成的目標是…」**
- 讓學生在學習前主動設定意圖，而非被動等待老師說什麼

### 出口票必備欄位
出口票務必包含**兩個欄位**（而非只問「你今天學到什麼」）：
- 「我現在確認理解了…」
- 「我還不確定的是…」

→ 讓評量結果對**學生本人**也可見——他們能看見自己的掌握程度，而不只是給老師打分。

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
