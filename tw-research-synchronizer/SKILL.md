---
name: tw-research-synchronizer
description: >
  學術研究套組客製化工具，幫助研究者根據個人情境調整所有 tw-research-* Skills
  的預設行為。輸入研究背景後生成 researcher-profile.md 設定檔，
  後續所有 tw-research-* Skills 可讀取此設定檔自動客製化。
  當使用者提及「設定研究偏好」「客製化學術工具」「研究者設定」
  「設定我的研究領域」「個人化學術設定」時觸發。
  分類：學術研究（tw-research-*）
version: 1.0.0
author: 奇老師・數位敘事力社群
allowed-tools: "Bash, Read, Write, Notion"
disable-model-invocation: true
---

# 學術研究套組客製化工具 v1.0

## 核心目的
「**讓每個 tw-research-* Skill 都了解你的研究情境。**
設定一次，整個學術研究工作流都變成你的專屬工具。」

---

## Step 0：讀取所有 tw-research-* Skills 的 frontmatter

讀取以下 Skills 的可客製化參數：
- `../tw-research-proposal-diamond/SKILL.md`
- `../tw-research-citation-checker/SKILL.md`
- `../tw-research-viz/SKILL.md`
- `../tw-research-lit-review/SKILL.md`
- `../tw-research-stat-consultant/SKILL.md`
- `../tw-research-citation-proofer/SKILL.md`
- `../tw-research-dialectics/SKILL.md`

---

## Step 1：概念對齊確認卡

```
╔══════════════ 概念對齊確認 ══════════════╗
📌 任務：學術研究套組個人化設定
🎯 目標：建立你的研究者設定檔
👤 建立後：所有 tw-research-* Skills 自動讀取你的設定
⏱️ 所需時間：約 10-15 分鐘
開始設定了嗎？
╚═══════════════════════════════════════════╝
```

---

## Step 2：系統性問卷（15 題）

### 研究者基本資料
```
Q1：「你的稱呼或姓名？（讓 AI 稱呼你）」
Q2：「你目前的身份？
    A. 碩士生（哪年級？）   B. 博士生（哪年級？）
    C. 大學生（畢業論文）   D. 學術研究者/教師
    E. 其他：___」
Q3：「你的學術領域（請盡量具體）？
    例：「應用語言學、語料庫語言學」
    例：「教育心理學、科技教育」」
Q4：「你就讀/任職的機構？（選填）」
```

### 研究情境
```
Q5：「你目前的研究主題是什麼？（一句話）」
Q6：「你的研究方法取向？
    A. 量化研究（統計為主）
    B. 質性研究（訪談/觀察為主）
    C. 混合研究
    D. 語料庫/計算研究
    E. 理論/文獻研究」
Q7：「你使用的主要統計工具？（若有）
    A. SPSS    B. R    C. Python    D. SAS
    E. 其他    F. 不用統計」
Q8：「你的目標出版/發表場域？
    A. 台灣國內學位論文（碩/博士）
    B. 台灣本土期刊（TSSCI/台灣教育研究）
    C. 國際期刊（SSCI/SCI/A&HCI）
    D. 研討會論文（AERA / CASLAR 等）
    E. 尚未確定」
```

### 學術規範偏好
```
Q9：「你主要使用的引用格式？
    A. APA 7th   B. MLA 9th   C. 台灣學位論文格式
    D. Chicago   E. Vancouver  F. 依期刊而定」
Q10：「你偏好的學術書寫語言？
     A. 中文為主      B. 英文為主
     C. 中英文混合    D. 依場合而定」
Q11：「你的指導教授/學術導師的風格是？
     A. 強調嚴謹方法論
     B. 強調理論框架
     C. 強調實用性與創新
     D. 不確定/無指導教授」
```

### 工作習慣
```
Q12：「你通常在什麼軟體中寫作？
     A. Word（.docx）  B. LaTeX  C. Google Docs
     D. Overleaf       E. 其他」
Q13：「你的文獻管理工具？
     A. Zotero  B. Mendeley  C. EndNote
     D. Notion  E. 手動管理」
Q14：「你最常遇到的研究困難？（前三名）
     A. 文獻搜尋與整理
     B. 統計分析
     C. 論文寫作（架構/語言）
     D. 引用格式
     E. 論點不夠強（邏輯）
     F. 研究設計」
Q15：「有什麼是你希望 AI 特別注意的？（自由填寫）」
```

---

## Step 3：生成 researcher-profile.md

```markdown
# 研究者設定檔
# 建立日期：[YYYY-MM-DD]
# tw-research-synchronizer v1.0

---

## 研究者資料
- 稱呼：[名字]
- 身份：[身份]
- 領域：[領域（具體）]
- 機構：[機構]（若有）

## 研究情境
- 研究主題：[主題]
- 方法取向：[量化/質性/混合/語料庫]
- 統計工具：[工具]
- 目標場域：[發表目標]

## 學術規範設定
- 引用格式：[格式]
- 書寫語言：[語言]
- 導師風格：[風格]

## 工作環境
- 寫作軟體：[軟體]
- 文獻管理：[工具]
- 主要困難：[困難列表]

## 各 Skill 客製化參數

### tw-research-lit-review
- 搜尋語言優先：[中文/英文/雙語]
- 主要資料庫：[列表]
- 年份範圍：[範圍]

### tw-research-stat-consultant
- 慣用程式語言：[Python/R/SPSS]
- 研究方法：[主要方法]
- 效果量報告：[Cohen's d / η² / 其他]

### tw-research-citation-proofer
- 預設格式：[格式]
- 特殊台灣本土規範：[若有]

### tw-research-dialectics
- 辯證強度預設：[輕度/中度/嚴格]
- 學科批判傳統：[領域特有的批判框架]

### tw-research-viz
- 圖表風格：[學術期刊/論文/研討會簡報]
- 慣用工具：[Excalidraw/matplotlib/R ggplot]
```

---

## Step 4：輸出已啟動的自訂項目

```
✅ 已客製化的項目（[N] 項）：

1. AI 稱呼你為「[名字]」
2. 所有分析採用 [引用格式] 規範
3. 統計程式碼優先使用 [程式語言]
4. 文獻搜尋優先涵蓋 [語言] 資料庫
5. 辯證預設強度：[強度]
6. 書寫語言：[語言]

📁 設定檔已存入：./researcher-profile.md
   （所有 tw-research-* Skills 啟動時會自動讀取此檔案）
```

---

## Step 5：Notion 設定檔備份

```
若使用者同意存入 Notion：
→ 建立「研究者設定檔」Notion 頁面
→ 方便在不同裝置或工作階段取用
```
