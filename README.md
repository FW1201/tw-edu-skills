# 臺灣 K-12 教育 Claude Code Skills 套組

> 專為臺灣中小學教師設計的 20 種 AI 輔助教學技能，以「**教師素養為主、AI 為輔**」為核心哲學，全面對應 108 課綱。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform: Claude Code](https://img.shields.io/badge/Platform-Claude%20Code-orange)](https://code.claude.com)
[![Agent Skills Standard](https://img.shields.io/badge/Standard-Agent%20Skills%20Open%20Standard-blue)](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

---

## ✨ 功能一覽

| 類別 | Skill 名稱 | 主要輸出 | 說明 |
|------|-----------|---------|------|
| **A 課程設計** | tw-edu-lesson-plan-108 | .docx | 108課綱素養導向教案（各領域） |
| | tw-edu-curriculum-mapper | .xlsx | 課程地圖與學習表現對應 |
| | tw-edu-differentiated | .docx | 差異化教學設計（三層次） |
| | tw-edu-interdisciplinary | .docx + .pptx | 跨領域/彈性課程設計 |
| **B 評量命題** | tw-edu-rubric-designer | .docx | 評量規準（整體式/分析式） |
| | tw-edu-exam-generator | .docx | 各科試卷（含答案卷） |
| | tw-edu-formative-assessment | .docx | 形成性評量工具包 |
| **C 教材資源** | tw-edu-worksheet-creator | .docx | 素養導向學習單 |
| | tw-edu-reading-scaffold | .docx | 閱讀理解鷹架 |
| | tw-edu-vocab-material | .docx | 字詞教學材料 |
| **D 學生表現** | tw-edu-feedback-writer | .docx | 學生作業/作文評語 |
| | tw-edu-learning-portfolio | .docx | 學習歷程檔案輔助 |
| | tw-edu-student-iep | .docx | 個別化教育計畫框架 |
| **E 班級行政** | tw-edu-parent-communication | .docx | 親師溝通文件 |
| | tw-edu-classroom-culture | .docx | 班級經營策略 |
| | tw-edu-school-document | .docx | 校園公文與計畫書 |
| | tw-edu-meeting-facilitator | .docx | 會議議程與記錄 |
| **F AI素養** | tw-edu-ai-literacy | .pptx | AI素養融入教學方案 |
| | tw-edu-digital-story | .pptx | 數位敘事力教學 |
| | tw-edu-pbl-designer | .docx | 專題式學習（PBL）設計 |

---

## 🚀 快速安裝

### 方式一：一鍵安裝（推薦）

```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/tw-edu-skills/main/install.sh | bash
```

### 方式二：手動安裝全套

```bash
git clone https://github.com/YOUR_USERNAME/tw-edu-skills.git
cd tw-edu-skills
bash install.sh
```

### 方式三：安裝單一 Skill

```bash
bash install.sh tw-edu-lesson-plan-108
```

### 方式四：學校/組織統一部署

```bash
# 在專案 .claude/skills/ 目錄加入 submodule
git submodule add https://github.com/YOUR_USERNAME/tw-edu-skills .claude/skills/tw-edu-bundle
```

---

## 📋 系統需求

| 項目 | 需求 |
|------|------|
| Claude Code | 最新版本（Pro / Max / Team / Enterprise） |
| Python | 3.9 以上 |
| Python 套件 | `pip install -r requirements.txt` |
| 中文字型 | 標楷體（macOS 內建）或 Noto Serif CJK TC |

```bash
pip install -r requirements.txt
```

---

## 💡 使用方式

安裝後，在 Claude Code 中直接用中文描述需求：

```
# 教案生成
請幫我做一份《背影》的教案，國中八年級，翰林版，3節課

# 出題
幫我出一份國中九年級數學二次方程式的段考題，30題，含選擇和計算

# 評量規準
設計一份議論文寫作的評量規準，高中二年級

# 親師溝通
幫我寫一封給家長的班訊，說明下週戶外教學的注意事項
```

Claude 會自動辨識情境，載入對應 skill，引導你輸入必要參數，產出完整 .docx / .pptx / .xlsx 文件。

---

## 🏗️ 專案結構

```
tw-edu-skills/
├── tw-edu-lesson-plan-108/
│   ├── SKILL.md          # 核心指令（Claude 讀取）
│   ├── references/        # 108課綱指標、格式規範
│   ├── scripts/           # Python 文件生成腳本
│   └── assets/            # 樣板、圖示
├── tw-edu-exam-generator/
│   └── ...
├── install.sh             # 安裝腳本
├── requirements.txt       # Python 依賴
└── README.md
```

---

## 📐 設計原則

1. **漸進揭露**：SKILL.md 僅載核心邏輯，細節參考置於 `references/`
2. **直覺引導**：每個 skill 啟動後主動詢問年級、科目、版本等參數
3. **108課綱原生**：使用素養導向、學習表現等臺灣教育術語
4. **跨平台相容**：遵循 Agent Skills Open Standard，相容 Claude Code / Claude.ai / API
5. **美觀文件**：產出符合臺灣教師習慣的精美排版文件

---

## 🤝 貢獻指南

歡迎教師社群參與改善！
1. Fork 此專案
2. 建立功能分支：`git checkout -b feature/改善XX教案格式`
3. 提交變更：`git commit -m 'feat: 新增高中英文教案模板'`
4. 推送分支並建立 Pull Request

---

## 📄 授權

MIT License © 2026 奇老師 · 數位敘事力社群

---

## 🙏 致謝

- 臺灣教育部 108 課綱相關文件
- Anthropic Agent Skills Open Standard
- 翻轉教育、數位敘事力期刊教師社群

> 「AI 是工具，教師才是靈魂。」——奇老師
