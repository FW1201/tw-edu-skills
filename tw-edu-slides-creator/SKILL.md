---
name: tw-edu-slides-creator
description: |
  台灣 K-12 教育簡報生成器（v2.0）。使用 open-slide 框架（React + TypeScript + Tailwind CSS，1920×1080 畫布），
  支援 17 種教學版型、3 主題色系、Bloom 分層設計。輸出可直接 pnpm dev 預覽、pnpm build 匯出 HTML/PDF。
  由 Claude Code 負責生成 TSX 投影片元件，open-slide 框架處理縮放與演示。
version: 2.0
tags: [education, slides, Taiwan, React, TypeScript, open-slide, Tailwind, K-12]
capabilities:
  - open-slide 專案自動建立（npx @open-slide/cli init）
  - 17 種 TSX 投影片版型
  - 3 Tailwind CSS 主題（Edu Warm / Tech Dark / Academic Clean）
  - 年級自適應字型大小（國小低/中高/國中/高中/大學）
  - Bloom 分類法版型選擇邏輯
  - 演示者模式（open-slide 內建）
  - HTML/PDF 匯出（pnpm build）
  - Delta 更新模式（換N / 改風格 / 加N / 刪N / 加稿N）
references:
  - references/tsx-layout-templates.md
  - references/tailwind-themes.md
  - references/slide_design_principles.md
---

# tw-edu-slides-creator v2.0

台灣 K-12 教育簡報生成 Skill，使用 open-slide 框架。
Claude Code 負責生成 TSX 元件；open-slide 負責預覽、縮放、PDF 匯出。

---

## 📋 工作流程（5 步驟）

### 步驟 0：確認環境

檢查使用者環境：
- Node.js 是否安裝（`node --version`）
- 當前目錄是否已有 open-slide 專案（`package.json` 含 `@open-slide/core`）
- 若無專案：提示將自動 `npx @open-slide/cli init <slug>` 建立

### 步驟 1：收集資訊

詢問以下資訊（可一次問完）：

| 欄位 | 說明 | 預設值 |
|------|------|--------|
| 課程/主題名稱 | 投影片標題 | 必填 |
| 年級 | 國小低（1-2）/ 國小中高（3-6）/ 國中 / 高中 / 大學 | 國中 |
| 張數 | 預計投影片總數（含封面） | 10 |
| 主題色系 | Edu Warm / Tech Dark / Academic Clean | Edu Warm |
| 講稿模式 | 是否需要演講備註（speaker notes） | 否 |
| 輸出目錄名稱 | open-slide 專案資料夾名稱 | slides-`<課程slug>` |

### 步驟 2：規劃投影片結構

依據「25 種內容類型 → 17 種版型」對應規則（見 `slide_design_principles.md`），
加上 Bloom 分類年級規則，生成投影片大綱：

```
投影片大綱（國中・10張・Edu Warm）
01 cover      ← 封面（必有）
02 objectives ← 學習目標（必有）
03 section    ← 第一章
04 bullets    ← 核心重點
05 vocab      ← 詞彙卡
06 activity   ← 課堂活動
07 discussion ← 討論提示
08 summary    ← 重點回顧
09 checklist  ← 學習自評
10 hero       ← 結語強調
```

向使用者確認大綱後繼續。

### 步驟 3：建立 open-slide 專案

```bash
# 若無現有 open-slide 專案：
npx @open-slide/cli init <目錄名稱>
cd <目錄名稱>
pnpm install
```

若已有 open-slide 專案，直接在 `slides/` 目錄下新增。

### 步驟 4：生成 TSX 投影片元件

為每張投影片建立獨立檔案：

```
slides/
  01-cover/index.tsx
  02-objectives/index.tsx
  03-section/index.tsx
  ...
```

每個檔案格式（完整版型範例見 `references/tsx-layout-templates.md`）：

```tsx
// slides/01-cover/index.tsx
import type { Page } from '@open-slide/core';

const Cover: Page = () => (
  <div className="relative flex h-full w-full flex-col items-center justify-center bg-[#fffbf5]">
    {/* 主題色系底線裝飾 */}
    <div className="absolute inset-x-0 bottom-0 h-3 bg-[#d97757]" />
    {/* 科目標籤 */}
    <span className="mb-4 text-[32px] font-medium tracking-widest text-[#987b63] uppercase">
      七年級國文
    </span>
    {/* 課程標題 */}
    <h1 className="text-[72px] font-bold leading-tight text-[#2d1a0e] text-center max-w-[1400px]">
      課程名稱
    </h1>
    {/* 講師與日期 */}
    <p className="mt-8 text-[40px] text-[#987b63]">吳老師 ｜ 2026/05/23</p>
  </div>
);

export default [Cover];
export const meta = { title: '01 封面' };
```

### 步驟 5：完成提示

```
✅ 已生成 {N} 張投影片

📁 專案路徑：./{project-name}/
▶  預覽：pnpm dev
📤 匯出 HTML/PDF：pnpm build

🎨 主題：{theme}  ｜  📐 畫布：1920×1080px
```

---

## 🎨 主題系統（Tailwind CSS）

完整色值與 utility class 對照見 `references/tailwind-themes.md`。

### Edu Warm（教育暖色）
適用：語文、社會、SEL、一般教學（所有年級）
```
bg-[#fffbf5]  text-[#2d1a0e]  primary: #d97757  accent: #6a9bcc
heading font: Work Sans
```

### Tech Dark（科技深色）
適用：AI、資訊、程式、科技主題（不建議國小低年級）
```
bg-[#0D1117]  text-[#E6EDF3]  primary: #00D4FF  accent: #7B2FFF
heading font: Tektur
```

### Academic Clean（學術清爽）
適用：研究、論文、正式報告（高中/大學）
```
bg-[#faf9f5]  text-[#1a1814]  primary: #6a9bcc  accent: #d97757
heading font: Instrument Sans
```

---

## 📐 年級自適應字型（px，1920×1080 畫布）

| 年級 | 標題 Title | 副標 H2 | 內文 Body | 說明 Small | max bullets |
|------|-----------|---------|----------|-----------|-------------|
| 國小低（1-2） | 96px | 72px | 56px | 40px | 3 |
| 國小中高（3-6） | 84px | 60px | 48px | 36px | 4 |
| 國中 | 72px | 52px | 40px | 32px | 5 |
| 高中 | 64px | 48px | 36px | 28px | 6 |
| 大學 | 56px | 44px | 32px | 24px | 6 |

Tailwind 用法：`text-[72px]`（國中標題）、`text-[40px]`（國中內文）

> 1920×1080 畫布由 open-slide 自動處理縮放，px 值即為實際設計值，無需轉換 rem。

---

## 🔄 Delta 更新模式

生成後可用單字指令修改，無需重新生成整份簡報：

| 指令 | 說明 | 範例 |
|------|------|------|
| `換N` | 替換第 N 張版型 | `換3`（改用 quote 版型）|
| `改風格` | 切換主題色系 | `改風格 → Tech Dark` |
| `加N` | 在第 N 張後插入新投影片 | `加5` |
| `刪N` | 刪除第 N 張 | `刪7` |
| `加稿N` | 為第 N 張加入演講備註 | `加稿2 備註內容...` |

---

## 🚫 常見問題（Anti-Patterns）

1. **內容溢出畫布**：1920×1080 是固定畫布，所有內容必須在框架內。bullets 版型最多 5 條（國中）
2. **字型過小**：最小字型 24px（大學 Small），低年級請用 40px 以上
3. **連續同版型**：超過 3 張連續同版型，改用 section 分割
4. **中文字型缺失**：open-slide 預設支援 Noto Sans TC，無需額外設定
5. **圖片路徑錯誤**：圖片使用相對路徑或完整 URL；open-slide 不自動處理本機絕對路徑

---

## 🔗 相關資源

- open-slide GitHub：https://github.com/1weiho/open-slide
- open-slide 文檔：https://open-slide.vercel.app
- 版型完整範例：`references/tsx-layout-templates.md`（17 種版型 TSX 程式碼）
- 主題 Tailwind 對照：`references/tailwind-themes.md`
- 內容設計原則：`references/slide_design_principles.md`
