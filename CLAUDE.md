# tw-edu-skills — Claude Code 專案設定
# K-12 教學 Skills Repo
# 最後更新：2026-04-26

---

## Repo 定位

此 repo 包含 **18 個 K-12 教學 Skills**，目標用戶為台灣教師與學校行政人員。

---

## 工具許可

### 允許（無需確認）
- `WebSearch`：搜尋課綱資料、教材資源
- `Read`：讀取 SKILL.md 和 references/ 文件
- `Bash`：執行 Python/Node.js 生成腳本

### 需確認
- `Write`：寫入 SKILL.md 或 references/
- GitHub push：任何 commit 推送前需確認

---

## 輸出規範

### 文件格式
- 教案：.docx（標楷體 12pt，1.5 倍行距）
- 試卷：.docx 或 .pdf
- 學習單：.docx

### 設計皮膚
- 教學類：**Edu Warm**（`--edu-warm-bg: #fffbf5`）
- 學習單：素雅白底配色

---

## Skill 開發規範

### Frontmatter 必要欄位
```yaml
name: tw-edu-<name>
description: >
  [功能描述，包含觸發詞]
version: x.x.x
author: 奇老師・數位敘事力社群
allowed-tools: "<必要工具清單>"
```

### MCP 聲明方式
- 不在 frontmatter 宣告 MCP
- 在 skill 內文的 `## MCP 整合` 節描述
- 必須有降級方案（MCP 未連接時的替代做法）

### 版本命名
- 功能更新：`x.y.0`（如 `2.1.0`）
- 文件修正：`x.y.z`（如 `2.0.1`）

---

## 測試

```bash
# 驗證所有 SKILL.md 格式
node tests/skills-validation.js

# 安裝到 Claude Code 測試
npx skills add . --all -a claude-code
```
