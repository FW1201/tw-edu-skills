# 貢獻指南 — tw-edu-skills

感謝你有興趣為 **tw-edu-skills（K-12 教學 Skills 套組）** 貢獻或提交客製化作品！  
本指南說明如何製作符合規格的 Skill，以及如何將成果分享給數位敘事力期刊。

---

## 🌱 貢獻方式

| 方式 | 說明 |
|------|------|
| **提交新 Skill** | 製作 Skill 後郵寄給維護者審核 |
| **回報問題** | 在 GitHub Issues 描述 Bug 或改善建議 |
| **改善現有 Skill** | Fork → 修改 → 提交 Pull Request |
| **客製化自用** | Fork 自行維護，只需在 README 標註來源 |

---

## 🛠 如何製作一個 Skill

### 方法一：使用 Claude Skills Creator（推薦）

**Claude Skills Creator** 是 Anthropic 官方的 Skill 製作工具，在 Claude Code 中操作。

**步驟：**

1. 開啟 Claude Code（`claude` 指令或桌面應用程式）
2. 輸入以下提示詞啟動製作流程：

   ```
   請幫我製作一個新的 Claude Skill，名稱是 tw-edu-[你的功能名稱]，
   功能是[描述你想要的教學輔助功能]，目標使用者是[教師/學校行政]。
   ```

3. Claude 會引導你完成：
   - SKILL.md 的 frontmatter（name、description、version、allowed-tools）
   - Skill 的執行步驟與提示詞設計
   - 概念對齊確認卡（Concept Alignment Protocol）
   - references/ 參考文件（108課綱條文、評量規範等）

4. 完成後，儲存至本機資料夾，資料夾名稱即為 Skill ID（如 `tw-edu-my-skill/`）

**SKILL.md 最低規格：**

```yaml
---
name: tw-edu-[your-skill-name]
description: >
  一句話描述功能 + 觸發詞清單
version: 1.0.0
author: 你的名稱・數位敘事力期刊
allowed-tools: "Bash, Read, Write, WebSearch"
disable-model-invocation: true
---

# Skill 標題

[執行步驟...]
```

---

### 方法二：使用 Codex Skills Creator

**Codex Skills Creator** 是 OpenAI Codex 環境中的 Skill 建構工具。

**步驟：**

1. 在 Codex CLI 環境中輸入：

   ```
   /create-skill tw-edu-[你的功能名稱]
   ```

2. 依照提示填寫 Skill 的描述、觸發詞、執行邏輯

3. Codex 生成的 SKILL.md 需手動補充以下欄位（以符合本套組規格）：
   - `disable-model-invocation: true`
   - 概念對齊確認卡（Concept Alignment Protocol）段落
   - AI 輸出查核三問（每個 Skill 末段必備）

> ⚠️ **注意**：Codex 環境不支援 MCP Connectors，若你的 Skill 需要整合 Notion、Google Drive、Gmail、Google Calendar、Canva 等服務，需在 Claude Code 環境中補充 `allowed-tools` 設定。

---

## 📋 Skill 品質檢核清單

提交前請確認：

- [ ] **命名規範**：`tw-edu-[功能名]`（全小寫、連字號分隔）
- [ ] **SKILL.md 完整**：包含所有必要 frontmatter 欄位
- [ ] **概念對齊確認卡**：Skill 執行前有對齊機制
- [ ] **108 課綱對應**：說明對應哪些核心素養指標（若適用）
- [ ] **AI 輸出查核三問**：Skill 末段包含三問確認
- [ ] **觸發詞清單**：description 中列出至少 5 個中文觸發詞
- [ ] **版本號**：遵循 SemVer（major.minor.patch）
- [ ] **作者欄位**：填寫姓名 + 數位敘事力期刊

---

## 📧 如何提交給維護者

製作完成後，請將 Skill 資料夾（包含 SKILL.md 及所有子目錄）壓縮後寄至：

**📮 kevinwu@gtrainerdemo.jdn2023.com**

郵件主旨格式：
```
[Skill 貢獻] tw-edu-[你的 Skill 名稱] — [你的姓名]
```

郵件內容請包含：
1. Skill 名稱與功能簡介（100字以內）
2. 目標使用情境（哪個學段、哪個科目）
3. 製作工具（Claude Skills Creator / Codex Skills Creator / 手動編寫）
4. 你的 GitHub 帳號（若有，將列入貢獻者名單）
5. 壓縮附件：`tw-edu-[功能名].zip`

收到後，維護者將於 **7 個工作天**內回覆審核結果。

---

## 📜 Citation 規範

Fork 或衍生本套組時，請在你的作品中標註：

```
基於 吳奇（Kevin Wu）. (2025). tw-edu-skills: K-12 教學 Claude Skills 套組 [Software].
數位敘事力期刊. https://github.com/FW1201/tw-edu-skills
受 曾慶良老師（GitHub: @ChatGPT3a01）啟發。
```

---

## 🤝 行為準則

- 尊重所有使用者與貢獻者
- 提交內容不得包含任何歧視性語言或不適合教育場域的內容
- 所有 Skills 必須以學習者福祉為優先，不得設計為替代學生思考

---

## 📬 聯絡資訊

**數位敘事力期刊**

📮 kevinwu@gtrainerdemo.jdn2023.com  
📘 [Facebook](https://www.facebook.com/Journal.of.Digital.Narrative)  
▶️ [YouTube](https://www.youtube.com/@Journal_of_Digital_Narrative)  
📸 [Instagram](https://www.instagram.com/journal_of_digital_narrative/)  
💻 GitHub：[@FW1201](https://github.com/FW1201)
