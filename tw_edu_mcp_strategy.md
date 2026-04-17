# tw-edu-skills MCP 整合策略全域指南
# MCP Integration Strategy — All 19 Skills
# 版本：3.0

---

## 可用 MCP 清單（依使用者環境）

| MCP 名稱 | 端點 | 核心能力 | 支援平台 |
|---------|------|---------|---------|
| **Excalidraw** | excalidraw-mcp-app.vercel.app/mcp | 手繪風格互動圖表 | Claude Code / Claude.ai |
| **Gmail** | gmail.mcp.claude.com/mcp | 草擬/讀取郵件 | Claude Code / Claude.ai |
| **Canva** | mcp.canva.com/mcp | 設計簡報/視覺材料 | Claude Code / Claude.ai |
| **Figma** | mcp.figma.com/mcp | 精確設計稿/標注 | Claude Code / Claude.ai |
| **Vercel** | mcp.vercel.com | 部署靜態/動態網站 | Claude Code |
| **Google Calendar** | gcal.mcp.claude.com/mcp | 行事曆建立/查詢 | Claude Code / Claude.ai |
| **Consensus** | mcp.consensus.app/mcp | 學術論文搜尋 | Claude Code / Claude.ai |
| **Three.js 3D Viewer** | — | 3D 互動視覺化 | Claude Code / Claude.ai |
| **WebSearch** | (內建) | 網路搜尋 | 全平台 |
| **Google Drive** | (需另外設定) | 雲端儲存/讀取 | Claude Code / Claude.ai |

---

## 19 個 Skills 的 MCP 分配矩陣

| Skill | WebSearch | Canva | Excalidraw | Gmail | Calendar | Drive | Vercel | Consensus | Figma | Three.js |
|-------|-----------|-------|-----------|-------|----------|-------|--------|-----------|-------|---------|
| A1 教案 | ✅ 必要 | ⭕ 選用 | — | — | — | ⭕ 選用 | — | — | — | — |
| A2 課程地圖 | ✅ 必要 | — | ⭕ 選用 | — | — | ⭕ 選用 | — | — | — | — |
| A3 差異化 | ✅ | — | ⭕ 選用 | — | — | — | — | — | — | — |
| A4 跨領域 | ✅ | — | ⭕ 選用 | — | ⭕ 選用 | ⭕ 選用 | — | — | — | — |
| B1 評量規準 | ✅ | — | — | — | — | ⭕ 選用 | — | — | — | — |
| B2 試卷 | ✅ 必要 | — | — | — | — | ⭕ 選用 | — | — | — | — |
| B3 形成性評量 | ✅ | — | ⭕ 選用 | — | — | — | — | — | — | — |
| C1 學習單 | ✅ | — | ⭕ 選用 | — | — | — | — | — | — | — |
| D1 回饋評語 | — | — | — | ✅ 核心 | — | ⭕ 選用 | — | — | — | — |
| D2 學習歷程 | ✅ | ⭕ 選用 | — | — | — | ⭕ 選用 | — | — | — | — |
| E1 親師溝通 | — | — | — | ✅ 核心 | — | — | — | — | — | — |
| E2 班級經營 | ✅ | — | ⭕ 選用 | — | — | — | — | — | — | — |
| E3 行政文書 | — | — | — | — | — | ⭕ 選用 | — | — | — | — |
| **E4 會議** | — | — | — | ✅ 核心 | **✅ 核心** | **✅ 核心** | — | — | — | — |
| F1 PBL | ✅ | — | ✅ 核心 | — | — | — | — | — | — | — |
| F2 slides | ✅ | **✅ 優先** | — | — | — | ⭕ 選用 | — | — | ⭕ 選用 | — |
| G1 mini-app | — | — | — | — | — | — | **✅ 核心** | — | — | ⭕ 選用 |
| **R1 研究視覺化** | ✅ | ⭕ 選用 | **✅ 優先** | — | — | — | — | — | ⭕ 選用 | ⭕ 選用 |
| **R2 文獻查核** | **✅ 必要** | — | — | — | — | — | — | **✅ 核心** | — | — |
| **G2 直式短影音** | ✅ 必要 | ⭕ 選用 | — | — | — | ⭕ 選用 | — | — | — | — |

圖例：✅ 必要/核心 | ⭕ 選用/可選 | — 不適用

---

## 各 Skill 的 MCP 最佳化更新說明

### A1 教案（lesson-plan-108）
- **WebSearch**：搜尋課文資料（現有，已實作）
- **Canva MCP（新增建議）**：若使用者說「幫我做美觀教案封面」，呼叫 Canva 生成封面設計
- **Google Drive（新增建議）**：完成後提供上傳到 Drive 選項

### A2 課程地圖（curriculum-mapper）
- **Excalidraw（新增建議）**：除 .xlsx 外，可呼叫 Excalidraw 生成視覺化課程地圖
- **Google Drive（新增建議）**：自動上傳到學校共用 Drive

### A4 跨領域（interdisciplinary）
- **Google Calendar（新增建議）**：為各里程碑建立行事曆提醒
- **Excalidraw（新增建議）**：生成跨科學習地圖的視覺化版本

### D1 回饋評語（feedback-writer）
- **Gmail（既有，強化）**：批量草擬家長通知信

### E4 會議（meeting-facilitator）
- **Google Calendar（v2.1 核心功能）**：建立本次/下次會議 + 查詢空閒時間
- **Google Drive（v2.1 核心功能）**：上傳記錄 + 取得分享連結
- **Gmail（v2.1 核心功能）**：草擬摘要 + 行動清單

### F2 slides（slides-creator）
- **Canva MCP（優先）**：若可用，優先呼叫 Canva 生成高設計感簡報
- **Figma（選用）**：若需要精確設計規格，呼叫 Figma

### G1 mini-app（mini-app）
- **Vercel（核心）**：一鍵部署
- **Three.js（選用）**：3D 資料視覺化小程式

### G2 直式短影音（remotion-shorts）
- **WebSearch（必要）**：查官方 Remotion / ElevenLabs 文件與更新設定
- **Google Drive（選用）**：若使用者要保存腳本、分鏡或輸出清單，可上傳到 Drive
- **Canva（選用）**：若需要封面、縮圖或教學用視覺素材，可延伸使用

### R1 研究視覺化（research-viz）
- **Excalidraw（優先）**：生成可編輯的研究架構圖
- **Three.js（選用）**：3D 文獻關係網絡圖
- **Figma（選用）**：精確學術圖表標注

### R2 文獻查核（citation-checker）
- **Consensus（核心）**：學術論文搜尋與驗證
- **WebSearch（必要）**：CrossRef、DOI 解析、期刊官網

---

## MCP 安全原則（全 Skills 通用）

### 絕對不做的事
1. **不自動發送 Email**：Gmail MCP 只存草稿，使用者確認後自行發送
2. **不修改分享權限**：Drive 上傳後不修改權限設定
3. **不刪除任何行事曆事件**：只建立，不刪除
4. **不代表使用者同意條款**：不自動點擊同意按鈕
5. **不存取其他使用者的資料**：只操作使用者自己的帳號資源

### 確認機制（必須的）
每次呼叫 MCP 執行寫入操作前，Claude 必須：
1. 顯示「將要執行的操作」摘要
2. 詢問「確認嗎？」
3. 等待使用者明確回覆「確認」/「是」/「好」
4. 收到確認後才執行

### 降級方案（MCP 不可用時）
| MCP | 降級方案 |
|-----|---------|
| Excalidraw | SVG 代碼 / Mermaid 語法 / draw.io XML |
| Gmail | 格式化 Email 文字（主旨+內文） |
| Google Calendar | .ics 檔案 |
| Google Drive | 本地文件 + 上傳步驟說明 |
| Canva | python-pptx 生成 .pptx |
| Vercel | 部署腳本 + 說明文件 |
| Consensus | WebSearch 多源驗證 |
| Three.js | matplotlib 靜態圖表 |
