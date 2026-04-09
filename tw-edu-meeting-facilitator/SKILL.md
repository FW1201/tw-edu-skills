---
name: tw-edu-meeting-facilitator
description: >
  為教師專業學習社群(PLC)、課發會、行政會議、共同備課設計議程與記錄模板，
  並透過 Google Calendar MCP 建立會議提醒、Google Drive MCP 儲存紀錄、
  Gmail MCP 發送摘要給與會者。
  當使用者提及「PLC」「課發會」「會議記錄」「教師社群」「備課會議」
  「教學研討」「共備」「專業社群」「行政會議」「教師會議」「開會」時觸發。
version: 2.1.0
author: 奇老師・數位敘事力社群
allowed-tools: "Bash, Read, Write"
disable-model-invocation: true
---

# 教師會議全流程輔助系統 v2.1

## 哲學定位
「好的會議不是開完就算，而是有決議、有追蹤、有下次的延續。」

---

## Step 0：讀取必要文件

1. `../../tw_edu_guided_collection.md` — 引導式收集框架
2. `/mnt/skills/public/docx/SKILL.md` — Word 文件生成

---


**概念對齊協議（必要前置步驟）：**
`../../tw_edu_concept_alignment.md`
→ 在執行任何工作前，先完成概念對齊確認卡。


## Step 1：引導式資訊收集

### 第一輪問題（最多 3 個）
```
Q1: 「會議類型是什麼？
    A. PLC 教師專業學習社群
    B. 課程發展委員會（課發會）
    C. 行政會議
    D. 共同備課（lesson study）
    E. 其他（請描述）」

Q2: 「這次的討論主題是什麼？（一句話說明）」

Q3: 「要生成議程（會前）還是會議記錄（會後）？」
```

### 第二輪（選填，影響 MCP 功能）
```
Q4: 「會議時間和地點？
    （提供了才能建立 Google Calendar 提醒）」

Q5: 「與會者信箱？
    （提供了才能寄發記錄摘要和建立共享行事曆）」

Q6: 「已確認下次會議時間嗎？
    （若有，一併建立行事曆提醒）」
```

### 確認摘要
```
✅ 類型：{會議類型}
📋 主題：{討論主題}
⏱ 時間：{時間/地點}
📄 輸出：{議程/記錄/兩者} → .docx
🔗 MCP 服務：{列出可用 MCP}
```

---

## Step 2：生成會議文件

```bash
python scripts/generate_meeting.py \
  --type "[plc/curriculum/admin/lesson_study]" \
  --topic "[主題]" \
  --duration "[分鐘]" \
  --date "[日期時間]" \
  --location "[地點]" \
  --mode "[agenda/minutes/both]" \
  --output "/mnt/user-data/outputs/會議文件_[主題].docx"
```

---

## Step 3：各類型議程設計

### PLC（60-90 分鐘）
```
00-05  Check-in：每人一句話說今天的期待
05-20  共同閱讀/案例分析
20-45  深度討論（3 個引導問題）：
  P1. 開放性：「在這個主題上，你最近觀察到什麼？」
  P2. 挑戰性：「什麼證據讓你確認學生真的學會了？」
  P3. 行動性：「你願意在下週嘗試什麼具體改變？」
45-60  行動規劃（承諾下次嘗試的策略）
60-65  Check-out：每人一個行動承諾
```

### 課發會（90-120 分鐘）
```
報到 + 確認出席（5 分）
主席開場 + 確認議程（5 分）
各年段課程計畫報告（每段 10-15 分）
跨領域/彈性課程討論（20 分）
行政宣達（10 分）
決議確認（10 分）
```

### 共同備課（60 分鐘）
```
單元目標確認（10 分）：最關鍵的學習轉折點
教案細節討論（20 分）：逐段過教學步驟
觀課焦點設定（15 分）：我們要觀察什麼
教材準備確認（15 分）：學習單/教具清單
```

---

## Step 4：會議記錄規範

### 文件結構
```
封面（會議基本資料：時間/地點/主席/記錄/出席）
↓
各議程項目摘要（依討論順序）
↓
決議事項清單
↓
行動追蹤表（Action Items）
  | # | 行動事項 | 負責人 | 期限 | 狀態 |
  | 1 | ...     | ...   | ... | 待辦 |
↓
下次會議預告
↓
附件清單
```

### 記錄品質標準
- 每個決議必須有「負責人」和「完成日期」
- 討論摘要用第三人稱（「林師提出」而非「老師說」）
- 行動事項在散會前確認一次
- 24 小時內完成並發送給與會者

---

## Step 5：MCP 整合（Google Calendar + Drive + Gmail）

### ══════════════════════════════════════════
### Google Calendar MCP
### 建立會議行事曆 + 查詢空閒時間
### ══════════════════════════════════════════

**Claude Code：** `claude mcp add google-calendar`
**Claude.ai：** Settings → Connectors → Google Calendar

#### A. 建立本次會議事件
```
觸發：使用者提供了會議時間

詢問：
「要幫您在 Google Calendar 建立這次會議嗎？
  📅 {會議類型} — {主題}
  ⏰ {開始} — {結束}
  📍 {地點}
  👥 {與會者}」

確認後執行：
gcal_create_event(
  summary: "{會議類型} — {主題}",
  start: { dateTime: "{ISO 時間}", timeZone: "Asia/Taipei" },
  end:   { dateTime: "{ISO 時間}", timeZone: "Asia/Taipei" },
  location: "{地點}",
  description: "【議程】\n{議程摘要}\n\n【引導問題】\n{3個問題}\n\n【預期產出】\n{本次會議目標}",
  attendees: [{ email: "{信箱}" }, ...],
  reminders: {
    useDefault: false,
    overrides: [
      { method: "email", minutes: 1440 },   // 前一天 Email 提醒
      { method: "popup", minutes: 15 }       // 前 15 分鐘彈窗
    ]
  }
)
```

#### B. 建立下次會議事件（包含行動追蹤）
```
觸發：記錄中確認了下次會議時間

執行：
gcal_create_event(
  summary: "下次 {會議類型} — {下次主題}",
  start: { dateTime: "{下次時間}", timeZone: "Asia/Taipei" },
  description: "【上次行動事項追蹤】\n{Action Items 清單}\n\n【預定議題】\n{下次討論主題}",
  attendees: [{ email: "{信箱}" }, ...]
)
```

#### C. 查詢與會者共同空閒時間
```
觸發：「幫我找大家都有空的時間」

執行：
gcal_find_meeting_times(
  attendees: [{ email: "{信箱}" }, ...],
  duration: { minutes: 60 },
  timeMin: "{最早時間 ISO}",
  timeMax: "{最晚時間 ISO}"
)
→ 返回 3 個可行時段供選擇
```

---

### ══════════════════════════════════════════
### Google Drive（透過 WebSearch/Bash 或 Drive MCP）
### 儲存會議記錄 + 建立共享連結
### ══════════════════════════════════════════

**若 Google Drive MCP 已連接：**
```
觸發：.docx 文件生成後

詢問：
「要把會議記錄上傳到 Google Drive 嗎？
  📁 建議路徑：教師文件/PLC記錄/{學年}/
  📄 {日期}_{類型}_{主題}.docx」

確認後執行：
gdrive_upload_file(
  file_path: "{本地 .docx 路徑}",
  folder_name: "PLC記錄/{學年}",
  file_name: "{日期}_{主題}.docx"
)
→ 返回 Google Drive 可分享連結

注意：
  上傳後的預設權限為「知道連結者可查看」
  如需調整，請使用者在 Drive 中自行修改
  Claude 不修改任何 Drive 分享權限設定
```

**若 Drive MCP 未連接（降級方案）：**
```
生成 .docx 後告知使用者：
「會議記錄已儲存為本地文件。
  建議上傳步驟：
  1. 前往 https://drive.google.com
  2. 拖曳文件到 [教師文件/PLC記錄] 資料夾
  3. 右鍵 → 取得連結 → 選擇「知道連結者可檢視」
  4. 複製連結附在 Email 中」
```

---

### ══════════════════════════════════════════
### Gmail MCP
### 草擬摘要 Email 給與會者
### ══════════════════════════════════════════

```
觸發：記錄完成 + 使用者說「寄給大家」

詢問：
「要草擬一封摘要 Email 嗎？
  收件人：{與會者清單}
  主旨：[會議記錄] {日期} {類型}：{主題}」

確認後執行：
gmail_create_draft(
  to: ["{信箱1}", "{信箱2}", ...],
  subject: "[會議記錄] {日期} {類型}：{主題}",
  body: """各位好，

附上今日 {類型} 會議摘要，請查閱。

【決議事項】
{決議清單（條列）}

【行動追蹤清單】
{Action Items 表格（文字版）}

【下次會議】
時間：{下次時間}
主題：{下次主題}
行事曆邀請：已發送 / 請確認

完整記錄：{Google Drive 連結（若有）}

如有問題，請直接回覆此信。

{記錄者姓名} 敬上
{日期}"""
)
→ 只存草稿，顯示草稿連結給使用者確認後自行發送

⚠️ Claude 只存草稿，絕不自動發送
```

---

### 完整 MCP 整合流程圖（會後）

```
會議結束
    │
    ▼
[生成] .docx 會議記錄 + Action Items 表格
    │
    ├─────────────────────────────────┐
    ▼                                 ▼
[Drive MCP 可用]                  [無 Drive MCP]
上傳 → 取得 Drive 連結             輸出本地檔案
    │                                 │
    ▼                                 ▼
[Calendar MCP] 建立下次會議行事曆（含 Action Items + Drive 連結）
    │
    ▼
[Gmail MCP] 草擬摘要 Email（含 Drive 連結 + Calendar 邀請說明）
    │
    ▼
使用者確認 → 自行發送
```

---

## Step 6：各平台 MCP 差異對照

| 功能 | Claude Code | Claude.ai Pro/Team | Codex / gemini-cli |
|------|------------|-------------------|-------------------|
| 生成 .docx | ✅ | ✅ | ✅ |
| Google Calendar 建立事件 | ✅ MCP | ✅ Connectors | ❌ → 輸出 .ics |
| Google Calendar 查空閒 | ✅ MCP | ✅ Connectors | ❌ |
| Google Drive 上傳 | ✅ MCP | ✅ Connectors | ❌ → 本地檔案 |
| Gmail 草稿 | ✅ MCP | ✅ Connectors | ❌ → 複製文字 |

### 無 MCP 降級方案
- **Calendar**：生成 `.ics` 文件（雙擊即可匯入 Google Calendar）
- **Drive**：輸出本地 .docx + 上傳步驟說明
- **Gmail**：輸出格式化 Email 文字（含主旨）供手動複製

---

## Step 7：品質確認清單

- [ ] 議程有明確時間分配（分鐘數加總等於會議總時長）
- [ ] 引導問題具體、可討論
- [ ] 行動追蹤表每項有負責人和期限
- [ ] 決議用主動句記錄
- [ ] Google Calendar 事件已建立（若 MCP 可用）
- [ ] Drive 記錄已上傳（若 MCP 可用）
- [ ] Gmail 草稿已存（使用者自行確認發送）
- [ ] .ics 文件已備份（無 MCP 時）
