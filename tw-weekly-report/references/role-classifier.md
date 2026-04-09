# 角色分類指南

## 四角色關鍵詞對照表

### 🟣 主編 / 社群管理者
**核心關鍵詞：**
數位敘事力、期刊、圖卡、infocard、social-infocard、Canva、Neon Circuit、
社群媒體、FB、Threads、Instagram、翻轉教育、投稿、媒體策劃、議題選題、
Prompt Injection 圖卡、AI安全圖卡、AI瀏覽器、Zero Trust、
tw-social-infocard、canvas-design、排程、發文、選題

**主要產出物：** PNG 圖卡、文章草稿、社群貼文、發文排程表

---

### 🔵 學術研究者
**核心關鍵詞：**
碩論、論文、語料庫、Sinica Corpus、中央研究院、一直、向來、
文獻回顧、APA 7th、研究計畫、TCSL 研究、對應分析、Correspondence Analysis、
Cohen's kappa、標注框架、偏誤分析、SLA、二語習得、中介語、化石化、
tw-research-proposal-diamond、tw-academic-double-diamond、
tw-edu-research-viz、tw-edu-citation-checker、Consensus MCP

**注意：**TCSL「研究」（語言學/文獻）→ 研究者；TCSL「教學設計」（課堂）→ 教師

**主要產出物：** .docx 論文草稿、研究架構圖、標注框架、引用清單

---

### 🟢 教師 / 教育設計者
**核心關鍵詞：**
教案、試卷、學習單、評量規準、rubric、課綱、108課綱、備課、K-12、
國中、高中、成語、國語文、差異化教學、PBL、班級經營、親師溝通、
出題、月考、段考、學習歷程、課程地圖、Google認證、培訓師、
tw-edu-lesson-plan-108、tw-edu-exam-generator、tw-edu-worksheet-creator、
華語文教學（課堂設計面）、TOCFL 等級對應、師資培訓

**主要產出物：** 教案 .docx、試卷 PDF、學習單、評量規準、教學簡報

---

### 🟩 Vibe Coding 開發者
**核心關鍵詞：**
Extension、Chrome、chrome-extension、Gemini EDU、NotebookLM、
Skill、skill-creator、tw-edu-skills、SKILL.md、package_skill、
Vibe Coding、mini-app、React、Vite、Vercel、部署、deploy、
GitHub、程式、code、前端、HTML、CSS、JavaScript、
SDD、規格書、Manifest V3、CLAUDE.md、tw-edu-mini-app、
web-artifacts-builder、frontend-design、Claude Code CLI

**主要產出物：** 部署 URL、.skill 套件、程式碼、Chrome Extension 檔案

---

### ⚙️ 系統 / 其他
**歸入條件：**
- 建構工作系統本身（角色設計、架構規劃、週報）
- 純概念討論、問答（無明確產出物）
- 跨越多角色且無法判定主角色

---

## 分類衝突解決規則

```
優先順序：主要產出物 > 對話標題關鍵詞 > 對話摘要關鍵詞
```

| 衝突情境 | 解決方式 |
|---------|---------|
| 同時有圖卡 + 研究內容 | 以主要產出物判定（PNG → 主編；.docx → 研究者） |
| TCSL 話題 | 看目的：語言學分析 → 研究者；課堂教學 → 教師 |
| Skill 開發 + 教育內容 | 開發者（因為在建構工具） |
| 無法判定 | ⚙️ 系統，附「無法分類原因」說明 |

---

## 跨角色機會矩陣

| 來源角色 | 本週產出類型 | 可轉化為 | 具體轉化建議 |
|---------|------------|---------|------------|
| 🔵 研究者 | 研究結論/論文章節 | 🟣 主編 | 拆解為3-5張期刊科普圖卡 |
| 🔵 研究者 | 文獻整理/理論框架 | 🟢 教師 | 教學補充材料、課堂講義 |
| 🟢 教師 | 教學設計/課堂案例 | 🟣 主編 | 翻轉教育投稿題材、AI教育推文 |
| 🟢 教師 | 工具需求/痛點發現 | 🟩 開發者 | Mini-App 構想、Extension 功能需求 |
| 🟩 開發者 | 工具發布/功能更新 | 🟣 主編 | 社群分享貼文、Threads 宣傳 |
| 🟩 開發者 | Skill 設計完成 | 🟢 教師 | 推廣至教師社群、培訓素材 |
| 🟣 主編 | 社群留言/受眾回饋 | 🔵 研究者 | 研究問題線索、田野材料 |

**使用規範：**
- 只在確實有高品質轉化價值時提示，最多 3 個機會
- 每個機會必須附「具體下一步」（例：「可調用 tw-social-infocard 生成3張圖卡」）
- 避免為湊數而提出低價值的轉化建議
