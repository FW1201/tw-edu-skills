---
name: tw-edu-curriculum-mapper
description: >
  輸入學習主題或課程單元，自動對應108課綱各領域學習表現、學習內容代碼，
  並生成課程地圖視覺化表格（.xlsx）。
  當使用者提及「課程地圖」「學習表現對應」「課綱對應」「課程規劃」
  「學期課程」「課程架構」「學習地圖」「學年計畫」時觸發。
version: 1.0.0
author: 奇老師・數位敘事力社群
allowed-tools: "Bash, Read, Write"
disable-model-invocation: true
---

# 課程地圖生成器

## 哲學定位
協助教師將「課程直覺」轉化為可視化的結構，作為課程審視與討論的基礎。

---

## Step 0：讀取參考文件
- `references/curriculum_map_format.md` — 課程地圖格式規範
- `/mnt/skills/public/xlsx/SKILL.md` — Excel 文件生成規範
- `tw-edu-lesson-plan-108/references/108_subject_indicators.md` — 課綱指標

---


**概念對齊協議（必要前置步驟）：**
`../../tw_edu_concept_alignment.md`
→ 在執行任何工作前，先完成概念對齊確認卡。


## Step 1：引導資訊收集

詢問使用者：
1. 學期或學年？（上學期／下學期／全學年）
2. 科目與年級？
3. 有幾個單元/章節？（請列出名稱）
4. 是否要對應課綱學習表現代碼？

---

## Step 2：生成課程地圖 Excel

```bash
python scripts/generate_curriculum_map.py \
  --subject "[科目]" \
  --grade "[年級]" \
  --semester "[學期]" \
  --units "[單元1,單元2,...]" \
  --output "/mnt/user-data/outputs/[科目]課程地圖.xlsx"
```

---

## 課程地圖四個工作表

### 工作表1：學期總覽
| 週次 | 單元名稱 | 教學主題 | 節數 | 核心素養 | 重大議題 | **遷移情境** |

**遷移情境說明**：每個單元除了名稱，還需填寫「學生學完這個單元後，在什麼**真實情境**中能用到這個學習？」
- 不只是「學分數」，而是「能在日常情境中判斷半份與四分之一份的大小」
- 填不出遷移情境，代表這個單元的學習目標可能還不夠具體

### 工作表2：學習表現對應
| 單元 | 學習表現代碼 | 說明 | 布魯姆層次 | **評量任務** |

**評量任務說明**：每個素養代碼旁標注「要用什麼具體表現（作業/活動/測驗）來驗證學生真的達成了？」
- 先想好驗收方式，再回頭設計教學活動——避免教學和評量脫節

### 工作表3：學習內容對應
| 單元 | 學習內容代碼 | 說明 | 教學材料 |

### 工作表4：跨域連結圖 + 核心概念累積軌跡
視覺化矩陣：單元 × 相關科目，標示連結強度

**核心概念累積說明**：標示哪些跨單元、跨學期的課程服務相同的「核心概念」——讓老師看見學習的**累積軌跡**，避免每個單元都像孤立的知識塊。

---

## 樣式規範
- 主色：`#1A5276`（臺灣教育藍）
- 表頭：深藍底白字，粗體 12pt
- 字型：新細明體（Microsoft JhengHei 備用）
- 凍結首行首列，啟用自動篩選
- 格線清晰，奇偶列交替底色

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
