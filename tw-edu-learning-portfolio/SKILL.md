---
name: tw-edu-learning-portfolio
description: >
  引導學生整理學習歷程檔案（108課綱大學申請入學用），
  包含課程學習成果說明、多元表現敘述、自我評述框架。
  當使用者提及「學習歷程」「備審資料」「課程學習成果」
  「多元表現」「自我評述」「學習歷程檔案」「大學申請」時觸發。
version: 1.0.0
allowed-tools: "Bash, Read, Write"
disable-model-invocation: true
---

# 學習歷程檔案輔助工具

## Step 0：讀取文件
- `references/portfolio_guide.md`
- `/mnt/skills/public/docx/SKILL.md`


**概念對齊協議（必要前置步驟）：**
`../../tw_edu_concept_alignment.md`
→ 在執行任何工作前，先完成概念對齊確認卡。


## Step 1：資訊收集
1. 學生年級（高一/高二/高三）？
2. 要撰寫哪類文件？
   - 課程學習成果說明（每份800字內）
   - 多元表現綜整心得
   - 自傳/自我陳述
   - 大學科系對應說明
3. 學生提供的關鍵內容（活動、作品、心得）？

## Step 2：生成學習歷程文件

```bash
python scripts/generate_portfolio.py \
  --grade "[高一/高二/高三]" \
  --type "[course_result/diverse/autobiography]" \
  --content "[學生提供的內容摘要]" \
  --target_dept "[目標科系（選填）]" \
  --output "/mnt/user-data/outputs/學習歷程_[類型].docx"
```

## 重要提醒
- 本工具提供框架與引導，最終內容須由學生自己撰寫
- 輸出為草稿，需學生大量修改使其個人化
- 強調真實性：鼓勵學生寫真實的學習歷程

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
