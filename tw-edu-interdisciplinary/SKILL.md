---
name: tw-edu-interdisciplinary
description: >
  設計跨領域/跨科課程，整合108課綱彈性學習課程與校本課程框架。
  當使用者提及「跨領域」「彈性課程」「校本課程」「跨科」
  「統整課程」「專題課程設計」「核心問題」「essential question」時觸發。
version: 1.0.0
allowed-tools: "Bash, Read, Write"
disable-model-invocation: true
---

# 跨領域課程設計工具

## Step 0：讀取參考文件
- `references/interdisciplinary_framework.md`
- `/mnt/skills/public/docx/SKILL.md`
- `/mnt/skills/public/pptx/SKILL.md`


**概念對齊協議（必要前置步驟）：**
`../../tw_edu_concept_alignment.md`
→ 在執行任何工作前，先完成概念對齊確認卡。


## Step 1：資訊收集
1. 核心問題（Essential Question）是什麼？
2. 涉及哪些科目？各科教師協作還是單科融入？
3. 年級與學習階段？
4. 時數安排（幾週、幾節）？
5. 最終成品/發表形式？

## Step 2：生成跨領域課程文件

```bash
python scripts/generate_interdisciplinary.py \
  --question "[核心問題]" \
  --subjects "[科目1,科目2]" \
  --grade "[年級]" \
  --weeks [週數] \
  --output "/mnt/user-data/outputs/跨領域課程設計.docx"
```

也可生成簡報供課程說明：
```bash
python scripts/generate_interdisciplinary_pptx.py \
  --question "[核心問題]" --output "/mnt/user-data/outputs/跨領域課程簡報.pptx"
```

## 文件結構
1. 課程概述（核心問題、課程理念、參與科目）
2. 跨科學習地圖（各科貢獻矩陣）
3. 學習活動序列（時間軸）
4. 素養對應說明
5. 評量設計（真實性評量）
6. 實施注意事項

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
