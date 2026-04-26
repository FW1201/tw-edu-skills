---
name: tw-edu-school-document
description: >
  協助撰寫校園行政公文與教育文書，包含簽呈、計畫書、成果報告、
  研習申請、課程計畫，符合教育部公文格式。
  當使用者提及「公文」「簽呈」「計畫書」「成果報告」「申請書」
  「教學研究」「課程計畫」「學校文件」「行政文書」時觸發。
version: 1.0.0
allowed-tools: "Bash, Read, Write"
disable-model-invocation: true
---

# 校園行政文書生成工具

## Step 0：讀取文件
- `references/official_document_format.md`
- `/mnt/skills/public/docx/SKILL.md`


**概念對齊協議（必要前置步驟）：**
`../../tw_edu_concept_alignment.md`
→ 在執行任何工作前，先完成概念對齊確認卡。


## Step 1：資訊收集
1. 文件類型？
   - 簽呈（校內行政簽核）
   - 計畫書（教學計畫/活動計畫/研習計畫）
   - 成果報告（活動/研習/研究成果）
   - 教師研習申請函
   - 課程計畫（學期/學年）
2. 事由與主要內容？
3. 呈報對象（校長/主任/教務處）？

## Step 2：生成行政文書

```bash
python scripts/generate_school_doc.py \
  --type "[memo/plan/report/application/curriculum]" \
  --subject "[事由]" --content "[主要內容摘要]" \
  --author "[撰文者]" --school "[學校名稱]" \
  --output "/mnt/user-data/outputs/行政文書_[類型].docx"
```

## 公文格式規範
- 段落標號：一、（一）1.（1）
- 民國年格式
- 正式公文用語（「函復」「敬請 核示」等）
- 標準主旨/說明/辦法三段式格式

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
