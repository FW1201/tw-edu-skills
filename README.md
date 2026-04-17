# tw-edu-skills — K-12 教學 Claude Skills 套組

> **臺灣 K-12 教師專用 AI 技能套組**  
> 基於 108 課綱素養導向設計，涵蓋備課、命題、評量、班級經營、親師溝通等完整教學流程。

[![Skills](https://img.shields.io/badge/Skills-19-green)](https://github.com/FW1201/tw-edu-skills)
[![Version](https://img.shields.io/badge/Version-3.1-blue)](https://github.com/FW1201/tw-edu-skills)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 📦 套組概覽

本套組包含 **19 個 Skills**，面向臺灣 K-12 各學段教師，深度整合：
- 108 課綱核心素養三面九項
- 十大學習領域 × 各版本教科書（南一/翰林/康軒）
- SDGs / ESG 跨領域議題
- 差異化教學（NESA 特教規範）

> **相關套組**：[tw-stu-skills（學生）](https://github.com/FW1201/tw-stu-skills) ｜ [tw-research-skills（學術研究）](https://github.com/FW1201/tw-research-skills)

---

## 🛠 Skills 清單

### 課程設計
| Skill | 功能說明 |
|-------|---------|
| `tw-edu-lesson-plan-108` | 依 108 課綱生成素養導向教案（.docx），支援所有學習領域 |
| `tw-edu-curriculum-mapper` | 繪製課程地圖，對應核心素養指標 |
| `tw-edu-differentiated` | 差異化教學設計，依學生程度分組教學策略 |
| `tw-edu-interdisciplinary` | 跨領域/跨科課程設計，整合 SDGs 議題 |
| `tw-edu-pbl-designer` | 專題式學習（PBL）完整設計，含驅動問題、任務鷹架、成果展示 |

### 評量命題
| Skill | 功能說明 |
|-------|---------|
| `tw-edu-exam-generator` | 素養導向試題生成，支援會考/學測題型，含閱讀素材 |
| `tw-edu-rubric-designer` | 評量規準（Rubric）設計，布魯姆認知層次對應 |
| `tw-edu-formative-assessment` | 形成性評量工具設計（提問策略、出口票、同儕互評） |
| `tw-edu-anti-ai-assessment` | 抗 AI 作弊評量設計，確保學習真實性 |

### 教材資源
| Skill | 功能說明 |
|-------|---------|
| `tw-edu-worksheet-creator` | 學習單製作，支援引導式問題設計與素養題型 |
| `tw-edu-slides-creator` | 教學簡報製作，含視覺化架構建議 |
| `tw-edu-mini-app` | 生成互動式教學小程式（HTML Artifact），無需寫程式 |
| `tw-edu-remotion-shorts` | 直式短影音學習動畫製作，含分鏡、風格與 Remotion 設定 |

### 學生表現
| Skill | 功能說明 |
|-------|---------|
| `tw-edu-feedback-writer` | 學生評語撰寫，個人化、具體描述學習表現 |

### 班級行政
| Skill | 功能說明 |
|-------|---------|
| `tw-edu-classroom-culture` | 班級經營計畫、班規設計、導師輔導策略 |
| `tw-edu-parent-communication` | 親師溝通信件、聯絡簿回覆、家長說明文件 |
| `tw-edu-school-document` | 校園公文寫作（會議記錄、申請表、活動計畫） |
| `tw-edu-meeting-facilitator` | 教師會議引導，生成會議議程、摘要與行動事項 |

### 套組設定
| Skill | 功能說明 |
|-------|---------|
| `tw-edu-synchronizer` | 個人化套組設定助手，根據科別/年段/教學風格客製化所有 Skills 行為 |

---

## 🚀 安裝方式

### Claude Code（推薦）

Claude Code 是本套組設計的**主要平台**，所有功能完整支援。

```bash
# 安裝全套組（19 個 Skills）
npx skills add FW1201/tw-edu-skills --all -a claude-code

# 安裝單一 Skill
npx skills add FW1201/tw-edu-skills tw-edu-lesson-plan-108 -a claude-code

# 確認安裝
npx skills list -a claude-code

# 更新套組
npx skills update -a claude-code
```

安裝後，在 Claude Code 中直接輸入觸發詞即可啟動（例如：「幫我寫一份教案」、「設計一份試卷」）。

### Codex CLI

```bash
# 安裝（需先有 Codex CLI 環境）
npx skills add FW1201/tw-edu-skills --all -a codex
```

> ⚠️ **Codex 限制**：
> - `Bash` 工具不支援（無法執行 Python/R 程式碼）
> - MCP Connectors（Notion、Google Drive、Gmail、Google Calendar、Canva）**不可用**
> - 涉及 `.docx` / `.pdf` 生成的功能需搭配 `docx`、`pdf` Skill

### Antigravity

```bash
# 安裝
npx skills add FW1201/tw-edu-skills --all -a antigravity
```

> ⚠️ **Antigravity 限制**：
> - MCP Connectors 支援程度依個人環境而定
> - 互動式 HTML Artifact（`tw-edu-mini-app`）需確認瀏覽器預覽功能已啟用
> - 部分 `WebSearch` 功能依連線狀態而定

---

## 🔌 MCP Connectors 整合

本套組部分 Skills 可連接以下 MCP Connectors（需在 Claude Code 中設定）：

| Connector | 應用 Skills | 功能 |
|-----------|------------|------|
| Google Drive | 所有 Skills | 讀取已有素材、儲存生成文件 |
| Gmail | `tw-edu-parent-communication` | 直接生成信件草稿 |
| Google Calendar | `tw-edu-lesson-plan-108`, `tw-edu-worksheet-creator` | 課程排程自動建立 |
| Notion | 所有 Skills | 知識庫存檔、教案管理 |
| Canva | `tw-edu-slides-creator`, `tw-edu-worksheet-creator` | 設計模板套用 |
| Gamma | `tw-edu-slides-creator` | AI 生成教學簡報 |

---

## 💡 第一次使用建議

1. **執行 `tw-edu-synchronizer`**（輸入「我要設定教師套組」）  
   → 完成 10 分鐘問卷，系統自動記住你的科別、年段、教學偏好
2. **嘗試 `tw-edu-remotion-shorts`**（輸入「幫我做一支 9:16 的國中自然短影音學習動畫」）
3. **再試 `tw-edu-lesson-plan-108`**（輸入「幫我設計一份國文教案」）
4. 依需求使用其他 Skills

---

## 📐 設計理念

- **素養優先**：所有輸出對應 108 課綱核心素養三面九項
- **教師主導**：AI 提供草稿與架構，教師保有最終判斷權
- **概念對齊**：每個 Skill 執行前確認使用者意圖，避免誤解
- **本土深度**：台灣版本教科書（南一/翰林/康軒）+ 本土文化語境

---

## ⚠️ 重要聲明

### 鼓勵共創與客製化

本套組以開放精神釋出，**歡迎所有人 Fork、客製化、延伸開發**。  
唯使用或衍生本套組時，請務必遵守以下 Citation 規範：

```
吳奇（Kevin Wu）. (2026). tw-edu-skills: K-12 教學 Claude Skills 套組 [Software].
數位敘事力期刊. https://github.com/FW1201/tw-edu-skills
```

> 本套組的設計理念深受 **曾慶良老師**（GitHub：[@ChatGPT3a01](https://github.com/ChatGPT3a01)）啟發，  
> 在此致上誠摯謝意。

如需提交貢獻或客製化 Skills，請參閱 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 👨‍💻 作者

**奇老師・數位敘事力期刊**  
GitHub：[@FW1201](https://github.com/FW1201)

📘 [Facebook](https://www.facebook.com/Journal.of.Digital.Narrative) ｜
▶️ [YouTube](https://www.youtube.com/@Journal_of_Digital_Narrative) ｜
📸 [Instagram](https://www.instagram.com/journal_of_digital_narrative/)

---

*本套組採 MIT 授權。歡迎 Fork、提 Issue、或 PR 貢獻新 Skill。使用時請標註來源。*
