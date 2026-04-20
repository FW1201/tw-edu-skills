---
name: tw-edu-mini-app
description: >
  開發互動式教學小程式（測驗/遊戲/計時器/隨機分組等），
  並自動部署到 Vercel 或 GitHub Pages，生成可分享的永久連結。
  當使用者提及「做一個小程式」「教學遊戲」「互動測驗」「線上測驗」
  「做個抽籤程式」「隨機分組工具」「計時器」「Kahoot 替代」
  「教學工具開發」「幫我做一個能分享的教學頁面」「部署到網路」時觸發。
  技術棧：React + Tailwind CSS → Vercel（優先）或 GitHub Pages
version: 1.0.0
author: 奇老師・數位敘事力社群
allowed-tools: "Bash, Read, Write, WebSearch"
disable-model-invocation: true
---

# 教學小程式開發 + 自動部署 v1.0

## 哲學定位
「讓每位教師都能有自己的教學工具，無需程式背景。」

---

## 設計系統 V2.0：Edu Warm

> 基於 Claude Design（2026-04-17）+ canvas-design 字型庫（Work Sans + Noto Sans TC）

### Edu Warm CSS Token
```css
:root {
  --bg: #fffbf5;      --surface: #f5f0e8;
  --text: #141413;    --text-muted: #6B6B6B;
  --primary: #d97757; --primary-hover: #c4664a;
  --secondary: #6a9bcc; --accent: #788c5d;
  --radius: 12px;     --shadow: 0 4px 24px rgba(0,0,0,0.08);
  --font-heading: 'Work Sans', 'Noto Sans TC', sans-serif;
  --font-body: 'Noto Sans TC', sans-serif;
}
```

> **禁用字型**：Inter、Roboto、Arial — 改用 Work Sans（標題）+ Noto Sans TC（內文）  
> **禁用模式**：border-left accent callout（視覺陳腐）、漸層轟炸、SVG 插圖嘗試  
> **色彩延伸**：`oklch(72% 0.13 50)` 可衍生 Edu Warm 暖色中間色

### Edu Warm 元件規格（canvas-design 共用元件庫）
```css
/* 按鈕 */
.btn-primary { background: #d97757; color: white; border-radius: 8px; 
               padding: 12px 24px; font: Work Sans Bold 16px; }

/* 卡片 */
.card { background: white; border-radius: 12px; padding: 24px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.08); }

/* 強調框 */
.callout { border-left: 4px solid #d97757; background: rgba(217,119,87,0.08);
           padding: 16px 20px; border-radius: 0 8px 8px 0; }

/* 進度徽章 */
.badge { background: #d97757; color: white; border-radius: 50%;
         width: 32px; height: 32px; display: flex; align-items: center; 
         justify-content: center; font: Work Sans Bold 14px; }
```

### 版面：HTML artifact 輸出標準
所有小程式以 **HTML artifact** 形式輸出（可即時預覽），確保：
- Google Fonts 載入：Work Sans + Noto Sans TC
- CSS token 完整定義（:root 變數）
- 響應式設計（max-width: 720px 居中）
- 微調模式支援：用戶說「換主色」只更新 --primary 變數
- `text-wrap: pretty` 用於所有段落文字，防止孤字

### React HTML artifact 技術規格（固定版本）
使用 React 時，CDN 版本必須固定，避免外部變動影響：
```html
<script crossorigin src="https://unpkg.com/react@18.3.1/umd/react.development.js"></script>
<script crossorigin src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js"></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js"></script>
```
**樣式物件命名規則**（避免 Babel scope 衝突）：
```javascript
// ❌ 錯誤：const styles = {...} 在多個 Babel 腳本中會衝突
// ✅ 正確：使用唯一名稱
const quizStyles = { container: {...}, question: {...} };
const timerStyles = { display: {...}, controls: {...} };
// 組件跨腳本共享
Object.assign(window, { QuizCard, TimerDisplay });
```

### 狀態持久化（LocalStorage）
需要記憶進度的工具（測驗/學習卡/計時設定）必須加 LocalStorage：
```javascript
// 儲存狀態
localStorage.setItem('app_state', JSON.stringify({ score, currentQ, settings }));
// 恢復狀態（頁面重載後繼續）
const saved = JSON.parse(localStorage.getItem('app_state') || '{}');
```

---

---

## Step 0：讀取必要文件

1. `references/mini_app_types.md` — 常見教學小程式類型與規格
2. `../../tw_edu_grade_adapter.md` — 年級適應系統
3. `../../tw_edu_guided_collection.md` — 引導式收集框架
4. `references/deployment_guide.md` — Vercel + GitHub Pages 部署指南

---


**概念對齊協議（必要前置步驟）：**
`../../tw_edu_concept_alignment.md`
→ 在執行任何工作前，先完成概念對齊確認卡。


## Step 1：年級偵測 + 引導式資訊收集

### 第一輪問題（最多 3 個）
```
Q1: 「想要什麼類型的教學小程式？
    常見類型（可多選或描述你的想法）：
    🎯 A. 互動測驗（選擇題/是非題，含計分）
    🎲 B. 隨機抽籤/分組工具
    ⏱ C. 課堂計時器（含倒數音效）
    🃏 D. 字詞/概念記憶卡（翻牌遊戲）
    🎮 E. 填字/配對遊戲
    📊 F. 即時投票/情緒溫度計
    🔧 G. 其他（請描述）」

Q2: 「給哪個年級的學生使用？」（若未偵測到）
Q3: 「需要學生輸入資料/名字嗎？（若有，我會設計輸入區塊）」
```

### 第二輪問題（選填）
```
Q4: 「有具體的題目、詞語或內容要放進去嗎？
    （可以直接貼上，或告訴我主題由我設計範例內容）」
    
Q5: 「部署偏好？
    A. Vercel（推薦，更快更穩定，需要 Vercel 帳號）
    B. GitHub Pages（免費，需要 GitHub 帳號）
    C. 只需要 HTML 檔案，我自己部署」
```

### 確認摘要
```
✅ 小程式類型：{類型}
🎓 適用年級：{年級}
📝 內容：{主題/題目說明}
🚀 部署方式：{Vercel/GitHub Pages/本地}
🔗 完成後：生成可分享的永久連結
```

---

## Step 2：技術架構規範

### 技術選擇原則
```
單頁互動工具（測驗/遊戲/計時器）：
  → 純 HTML + CSS + Vanilla JS（單一 .html 檔）
  → 無需 npm、無需框架，方便教師直接使用

複雜互動工具（多頁面/後端資料）：
  → React + Tailwind CSS
  → 部署至 Vercel

資料持久化工具（需儲存結果）：
  → React + localStorage（不需後端）
  → 或 Vercel + KV store（需後端）
```

### 設計系統（教育用）
```css
/* 主色 */
--edu-blue:   #1A5276;   /* 主要操作按鈕 */
--edu-green:  #1E8449;   /* 正確/完成 */
--edu-orange: #CA6F1E;   /* 警示/進行中 */
--edu-gold:   #D4AC0D;   /* 獎勵/高亮 */

/* 字型 */
--font-main: 'Noto Sans TC', 'Microsoft JhengHei', sans-serif;

/* 年級字體大小 */
國小低：  標題 2.5rem / 內文 1.5rem / 按鈕 1.3rem
國小中高：標題 2rem   / 內文 1.3rem / 按鈕 1.1rem
國中：    標題 1.8rem / 內文 1.1rem / 按鈕 1rem
高中：    標題 1.5rem / 內文 1rem   / 按鈕 0.9rem
```

---

## Step 3：各類型小程式規格

### A. 互動測驗（最常用）
```
功能規格：
- 題目逐一顯示，選完後即時回饋（正確/錯誤 + 解析）
- 進度條顯示（第 X 題 / 共 X 題）
- 計分系統（答對 +10 分，可設定時間加分）
- 完成後顯示總分 + 成績評語
- 可重新作答按鈕
- 題目/選項支援直接修改（教師模式）

資料格式（Claude 自動填入或依使用者提供）：
const questions = [
  {
    id: 1,
    question: "題目文字",
    options: ["選項A", "選項B", "選項C", "選項D"],
    answer: 0, // 答案索引
    explanation: "解析說明",
    difficulty: 1 // 1=★☆☆ 2=★★☆ 3=★★★
  }
];
```

### B. 隨機抽籤/分組
```
功能規格：
- 輸入學生名單（每行一個名字）
- 設定分組數目或每組人數
- 隨機分組動畫效果
- 一鍵重新分組
- 複製結果按鈕

額外功能：
- 冷卻模式（被抽過的暫時不再被抽）
- 轉盤抽籤視覺效果（可選）
```

### C. 課堂計時器
```
功能規格：
- 多段計時模式（思考 1 分/討論 3 分/發表 2 分）
- 大字顯示倒數時間
- 最後 10 秒變色提示
- 音效提示（完成時）
- 課堂情境預設：
  * 小組討論、個人思考、上台發表、課前複習、考試

視覺：
- 全螢幕顯示（方便投影）
- 深色模式（不刺眼）
```

### D. 記憶卡翻牌遊戲
```
功能規格：
- 翻牌配對（詞語+定義、問題+答案、圖+字）
- 計時 + 配對次數記錄
- 完成動畫
- 自訂卡片內容

適用：字詞學習、公式記憶、歷史事件配對
```

### E. 即時投票/情緒溫度計
```
功能規格：
- 教師端：顯示問題 + QR Code
- 學生端（手機掃碼）：點選答案
- 即時顯示統計圖表
注意：此功能需後端支援，推薦使用 Vercel + Upstash Redis
```

---

## Step 4：開發 + 部署流程

### 方案A：純 HTML 單檔（最簡單）
```bash
# 生成單一 HTML 檔
python scripts/generate_mini_app.py \
  --type "[quiz/lottery/timer/flashcard]" \
  --grade "[年級]" \
  --content "[題目/內容 JSON]" \
  --output "/mnt/user-data/outputs/[名稱].html"

# 使用者可直接在瀏覽器開啟，或上傳到任何靜態伺服器
```

### 方案B：Vercel 自動部署（推薦）

**需要的 MCP：Vercel MCP**

```
若 Vercel MCP 可用時的流程：

1. Claude 生成 React 專案原始碼（/tmp/mini-app-[名稱]/）
2. 呼叫 Vercel MCP 部署：
   deploy_to_vercel(project_dir="/tmp/mini-app-[名稱]")
3. Vercel MCP 返回永久連結（https://xxx.vercel.app）
4. Claude 輸出連結給使用者

⚠️ 需要使用者已在 Claude Code 中連接 Vercel MCP
```

若 Vercel MCP 不可用：
```bash
# 生成 React 專案 + vercel.json
python scripts/generate_mini_app_react.py \
  --type "[類型]" --grade "[年級]" \
  --output_dir "/mnt/user-data/outputs/mini-app-[名稱]/"

# 輸出部署說明給使用者
echo "請執行以下指令部署：
cd mini-app-[名稱]
npx vercel --prod"
```

### 方案C：GitHub Pages
```bash
python scripts/generate_github_pages.py \
  --type "[類型]" --grade "[年級]" \
  --output_dir "/mnt/user-data/outputs/mini-app-[名稱]/"

# 輸出部署說明：
echo "請將資料夾推送到 GitHub，並在 Settings > Pages 啟用部署"
```

---

## Step 5：品質確認清單

- [ ] 行動裝置友善（手機/平板可正常使用）
- [ ] 字體大小符合年級規格
- [ ] 支援觸控操作
- [ ] 色彩對比度符合可及性標準（WCAG AA）
- [ ] 有返回/重置功能
- [ ] 無需帳號即可使用（學生端）
- [ ] 中文顯示正常（字型已嵌入或指定備用字型）
- [ ] 部署成功並測試連結可訪問
- [ ] React 版本已固定（18.3.1 + Babel 7.29.0）？
- [ ] 樣式物件名稱唯一（非 `const styles`）？
- [ ] 需要記憶進度的工具已加 LocalStorage？
- [ ] 無漸層轟炸、無 SVG 插圖嘗試、無 border-left accent callout？
- [ ] `text-wrap: pretty` 已套用？

---

## MCP 連接器（平台差異，核心功能）

### Claude Code（完整支援）
```
Vercel MCP（若已連接）：
  用途：一鍵將小程式部署到 Vercel，生成可分享連結
  啟用：claude mcp add vercel
  
  使用時機：使用者說「部署到 Vercel」或「生成可分享連結」
  MCP 呼叫：deploy_to_vercel(project_path, project_name)
  返回值：{ url: "https://xxx.vercel.app", deployment_id: "..." }

GitHub MCP / Filesystem（若已連接）：
  用途：建立 GitHub repository 並啟用 Pages
  使用時機：使用者說「放到 GitHub Pages」
```

### Claude.ai（設定頁啟用）
```
目前 Vercel MCP 需在 Claude Code 環境使用。
Claude.ai 使用者建議：
1. Claude 生成完整 HTML 單檔
2. 使用者手動上傳到 Vercel / Netlify / GitHub Pages
```

### 其他平台（Codex / gemini-cli）
```
支援 Vercel CLI 和 GitHub Pages 部署腳本生成，
但需使用者手動執行部署指令。
Claude 會生成完整的 deploy.sh 腳本。
```

### 部署 MCP 調用範例（Claude Code）

```
# 若 Vercel MCP 已連接
[Claude 生成程式碼後]
[呼叫 Vercel MCP 部署]
→ 返回 https://edu-quiz-xxxxx.vercel.app
→ Claude 輸出：「✅ 已部署！分享連結：https://edu-quiz-xxxxx.vercel.app」
```
