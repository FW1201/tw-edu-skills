# 教學小程式部署指南

## 方式一：Vercel（推薦）

### 準備工作
1. 前往 https://vercel.com 建立免費帳號
2. 在 Claude Code 中連接 Vercel MCP：
   `claude mcp add vercel`

### 透過 Vercel MCP 自動部署（Claude Code 用戶）
Claude Code 中說：「幫我把這個小程式部署到 Vercel」
→ Claude 自動執行 deploy_to_vercel()
→ 返回永久連結（如 https://edu-quiz-abc123.vercel.app）

### 手動部署（其他平台）
```bash
# 安裝 Vercel CLI
npm i -g vercel

# 部署單一 HTML 檔案
echo '{"rewrites":[{"source":"/(.*)", "destination":"/index.html"}]}' > vercel.json
vercel --prod
```

## 方式二：GitHub Pages（免費）

### 步驟
1. 建立 GitHub repository（public）
2. 將 HTML 檔案命名為 `index.html`
3. 推送到 GitHub
4. 在 repository Settings → Pages 選擇 main branch
5. 約 2 分鐘後可訪問 https://[帳號].github.io/[repo名]/

### 快速腳本
```bash
git init
git add index.html
git commit -m "教學小程式初始版本"
git branch -M main
git remote add origin https://github.com/你的帳號/小程式名稱.git
git push -u origin main
# 然後到 GitHub 網站啟用 Pages
```

## 方式三：本地使用（最簡單）

直接在瀏覽器開啟 .html 檔案，投影給學生使用。
不需要網路，學生不需要手機。
適合：計時器、隨機分組等教師操作型工具。

## 更新小程式內容

### 修改題目
在 HTML 檔案中找到 `const questions = [...]` 區塊，
直接修改題目、選項和答案。
或請 Claude 「幫我更新第 3 題的選項」。

### 重新部署
修改後執行 `vercel --prod` 或 `git push`，連結不變。
