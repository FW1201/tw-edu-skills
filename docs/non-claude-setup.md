# tw-edu-skills — Codex & Antigravity 安裝指南

適用平台：**OpenAI Codex CLI** 和 **Google Antigravity IDE**  
版本：V3.1（2026-04-26）

---

## Codex 安裝

### Skills 路徑

Codex 從以下路徑自動掃描 Skills（從當前工作目錄向上至 repo root）：

```
<your-project>/.agents/skills/<skill-name>/SKILL.md   ← 專案層（推薦）
~/.codex/skills/<skill-name>/SKILL.md                  ← 全域層
```

### 安裝步驟

```bash
# Clone tw-edu-skills repo
git clone https://github.com/FW1201/tw-edu-skills.git

# 方式 1：安裝到專案目錄（推薦）
mkdir -p <your-project>/.agents/skills
cp -r tw-edu-skills/tw-edu-*/ <your-project>/.agents/skills/

# 方式 2：全域安裝
mkdir -p ~/.codex/skills
cp -r tw-edu-skills/tw-edu-*/ ~/.codex/skills/

# 安裝學習類 Skills
cp -r tw-edu-skills/tw-stu-*/ ~/.codex/skills/

# 安裝所有 Skills
cp -r tw-edu-skills/tw-*/  ~/.codex/skills/
```

### 使用方式

安裝後，在 Codex 的 prompt 中直接描述任務，Codex 自動匹配並啟用對應 Skill：

```
"幫我設計一份國中國語文新詩欣賞的素養導向教案"
→ 自動啟用 tw-edu-lesson-plan-108

"設計108課綱素養命題的試卷"
→ 自動啟用 tw-edu-exam-generator

"幫我製作一份學習單"
→ 自動啟用 tw-edu-worksheet-creator
```

### MCP Connectors 設定

Codex 原生支援 MCP 協議。在 `~/.codex/config.toml` 設定：

```toml
# Google Drive（教案上傳、學習單儲存）
[mcp_servers.google-drive]
command = "npx"
args = ["-y", "@google/mcp-server-googledrive"]

# Canva（教學簡報、視覺設計）
[mcp_servers.canva]
url = "https://mcp.canva.com/mcp"
headers = { Authorization = "Bearer ${CANVA_TOKEN}" }

# Google Calendar（會議記錄、行事曆）
[mcp_servers.google-calendar]
url = "https://gcal.mcp.claude.com/mcp"
headers = { Authorization = "Bearer ${GCAL_TOKEN}" }

# Notion（知識庫管理）
[mcp_servers.notion]
command = "npx"
args = ["-y", "@notionhq/notion-mcp-server"]
env = { NOTION_API_KEY = "${NOTION_API_KEY}" }

# Vercel（mini-app 部署）
[mcp_servers.vercel]
url = "https://mcp.vercel.com"
headers = { Authorization = "Bearer ${VERCEL_TOKEN}" }
```

或使用指令行：

```bash
codex mcp add google-drive --command "npx -y @google/mcp-server-googledrive"
codex mcp add canva --url "https://mcp.canva.com/mcp" --header "Authorization: Bearer $CANVA_TOKEN"
codex mcp list
```

### Skills × MCP 需求對照

| Skill | 必要 MCP | 選用 MCP |
|-------|---------|---------|
| tw-edu-lesson-plan-108 | WebSearch（內建）| Google Drive, Canva |
| tw-edu-exam-generator | WebSearch | Google Drive |
| tw-edu-slides-creator | — | Canva, Figma |
| tw-edu-meeting-facilitator | — | Google Calendar, Drive, Gmail |
| tw-edu-mini-app | — | Vercel |

---

## Antigravity 安裝（Google AI IDE）

### Skills 路徑

```
~/.gemini/antigravity/skills/<skill-name>/SKILL.md   ← 全域層
<project>/.agent/skills/<skill-name>/SKILL.md         ← 專案層（推薦）
```

注意：路徑是 `.agent`（單數），不是 `.agents`。

### 安裝步驟

```bash
# 全域安裝
mkdir -p ~/.gemini/antigravity/skills
cp -r tw-edu-skills/tw-edu-*/ ~/.gemini/antigravity/skills/

# 專案層安裝（推薦，避免污染全域）
mkdir -p <project>/.agent/skills
cp -r tw-edu-skills/tw-edu-*/ <project>/.agent/skills/
```

### MCP Connectors 設定

**方式 1：MCP Server Hub（推薦）**

在 Antigravity 介面中：
1. 點擊側邊欄 **MCP Server Hub**
2. 搜尋服務（Notion, Google Drive, Canva 等）
3. 點選 **Enable**

**方式 2：JSON 設定檔**

```json
// ~/.gemini/antigravity/mcp_config.json
{
  "mcpServers": {
    "google-drive": {
      "command": "npx",
      "args": ["-y", "@google/mcp-server-googledrive"]
    },
    "canva": {
      "url": "https://mcp.canva.com/mcp",
      "headers": { "Authorization": "Bearer ${CANVA_TOKEN}" }
    },
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": { "NOTION_API_KEY": "${NOTION_API_KEY}" }
    }
  }
}
```

### Antigravity 特有優勢

- **Jupyter Notebook 整合**：AI 可直接讀取、編輯、執行 `.ipynb` cells
- **MCP Server Hub**：1,500+ 預建 Connectors，免手動設定大多數常用服務
- **Skills 自動發現**：啟動時自動掃描所有 Skills 目錄

---

## 常見問題

| 問題 | 解決方案 |
|------|---------|
| Codex 找不到 Skill | 確認路徑為 `.agents/skills/`（複數），且 SKILL.md 在 skill 目錄內 |
| Antigravity 找不到 Skill | 確認路徑為 `.agent/skills/`（單數），不是 `.agents` |
| MCP Connector 認證失敗 | 確認環境變數已設定（`echo $NOTION_API_KEY`） |
| Frontmatter 欄位警告 | `allowed-tools`、`disable-model-invocation` 是 Claude Code 專屬欄位，Codex/Antigravity 忽略即可 |

---

## 相關資源

- [完整安裝指南](../wiki/開發者/skills-installation-guide.md)
- [Skills 全覽地圖](../wiki/開發者/skills-map.md)
- [GitHub Issues](https://github.com/FW1201/tw-edu-skills/issues)
