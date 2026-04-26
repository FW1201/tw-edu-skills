---
name: tw-edu-parent-communication
description: >
  撰寫親師溝通文件，包含班訊、聯絡簿訊息、關懷信函、行為記錄函。
  當使用者提及「親師溝通」「班訊」「聯絡家長」「通知信」
  「給家長的信」「寫班訊」「家長通知」「家長聯絡」時觸發。
version: 1.0.0
allowed-tools: "Bash, Read, Write"
disable-model-invocation: true
---

# 親師溝通文件生成工具

## Step 0：讀取文件
- `references/communication_templates.md`
- `/mnt/skills/public/docx/SKILL.md`


**概念對齊協議（必要前置步驟）：**
`../../tw_edu_concept_alignment.md`
→ 在執行任何工作前，先完成概念對齊確認卡。


## Step 1：資訊收集
1. 文件類型？
   - 班訊（定期通知）
   - 活動通知（戶外教學/運動會/成果展）
   - 個別關懷信函（學生表現/特殊狀況）
   - 行為問題記錄函
   - 成績說明函
2. 主要訊息內容？
3. 需要 Line 訊息簡短版嗎？

## Step 2：生成文件

```bash
python scripts/generate_parent_comm.py \
  --type "[newsletter/activity/care/behavior/grade]" \
  --content "[主要訊息摘要]" \
  --teacher "[教師姓名]" --class_name "[班級]" \
  --output "/mnt/user-data/outputs/親師溝通_[類型].docx"
```

## 書信格式規範（臺灣）
- 稱謂：「XX家長您好：」
- 自稱：「老師」
- 結語：「敬祝 闔家平安」或「順頌 時祺」
- 署名：「XXX老師 敬上」
- 日期：民國年格式（民國XXX年XX月XX日）
- 語氣：溫和、正向、具體、避免評判性語言

---

## 年級適應 + 引導式收集（v2.0 更新）

### 年級偵測
從使用者輸入自動辨識學段。若無法辨識，詢問：
「這份通知是給哪個年級的家長？（影響書信語氣與用詞）」

### 年級對應語氣調整
| 學習階段 | 語氣特性 | 用詞範例 |
|---------|---------|---------|
| 國小 | 溫暖、家庭感、具體說明 | 「小朋友」「請協助準備」 |
| 國中 | 正式但親切、尊重家長 | 「學生」「煩請配合」 |
| 高中 | 較正式、學生自主性高 | 「同學」「請自行」 |

### 引導式收集（第一輪）
```
Q1: 「這封信的主要目的是什麼？（一句話說明）」
Q2: 「是哪個班的家長通知？（班級名稱）」
```

### 引導式收集（第二輪，選填）
```
Q3: 「需要家長回條嗎？（切割線 + 簽名欄）」
Q4: 「需要同時生成 Line 訊息短版嗎？」
```

---

## MCP 連接器（平台差異）

### Claude Code ／ Claude.ai（Pro/Team/Enterprise）

**Gmail MCP（若已連接）：**
```
用途：直接從 Claude 草擬親師溝通郵件存入 Gmail 草稿
啟用：Settings → Connectors → 啟用 Gmail

流程：
  1. Claude 生成通知文件
  2. 詢問使用者：「要幫你把這封信存到 Gmail 草稿嗎？
                   請提供家長的 Email 地址。」
  3. 若確認：呼叫 gmail_create_draft(
                to: [家長信箱],
                subject: "[班級] [通知類型]",
                body: [生成的信件內容]
             )
  4. 使用者在 Gmail 中確認後自行發送
  ⚠️ Claude 只存草稿，絕不自動發送
```

### Codex 平台
MCP Connectors 透過 `~/.codex/config.toml` 設定（`codex mcp add` 指令或手動編輯）。
未設定時自動降級：請參閱上方降級方案。

### Antigravity 平台（Google AI IDE）
MCP 透過 MCP Server Hub（1,500+ servers）或 `~/.gemini/antigravity/mcp_config.json` 設定。
支援 Jupyter Notebook 整合。未設定時自動降級：請參閱上方降級方案。
