# Tailwind CSS Theme Reference（open-slide v2.0）

open-slide 使用標準 Tailwind CSS。所有顏色使用 arbitrary values（`bg-[#hex]`）確保精確色值，無需額外 config。

---

## 1. Edu Warm（教育暖色）

適用：語文、社會、SEL、一般教學 ｜ 年級：**全部**

| Token | 色值 | Tailwind Class |
|-------|------|----------------|
| 背景 bg | `#fffbf5` | `bg-[#fffbf5]` |
| 表面 surface | `#f5ede0` | `bg-[#f5ede0]` |
| 主色 primary | `#d97757` | `bg-[#d97757]` / `text-[#d97757]` / `border-[#d97757]` |
| 輔色 accent | `#6a9bcc` | `bg-[#6a9bcc]` / `text-[#6a9bcc]` |
| 主文字 text | `#2d1a0e` | `text-[#2d1a0e]` |
| 次文字 muted | `#987b63` | `text-[#987b63]` |
| 邊框 border | `#e8d5bf` | `border-[#e8d5bf]` |
| 標題字型 | Work Sans | `font-[Work_Sans]` |

**Google Fonts import（加入 open-slide `layout.tsx` 或 `globals.css`）：**
```html
<link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;600;700;900&family=Noto+Sans+TC:wght@400;700&display=swap" rel="stylesheet">
```

---

## 2. Tech Dark（科技深色）

適用：AI、資訊、程式、科技 ｜ 年級：**國中以上**（不建議國小低年級）

| Token | 色值 | Tailwind Class |
|-------|------|----------------|
| 背景 bg | `#0D1117` | `bg-[#0D1117]` |
| 表面 surface | `#161B22` | `bg-[#161B22]` |
| 主色 primary | `#00D4FF` | `bg-[#00D4FF]` / `text-[#00D4FF]` / `border-[#00D4FF]` |
| 輔色 accent | `#7B2FFF` | `bg-[#7B2FFF]` / `text-[#7B2FFF]` |
| 主文字 text | `#E6EDF3` | `text-[#E6EDF3]` |
| 次文字 muted | `#8B949E` | `text-[#8B949E]` |
| 邊框 border | `#30363D` | `border-[#30363D]` |
| 標題字型 | Tektur | `font-[Tektur]` |

**Google Fonts import：**
```html
<link href="https://fonts.googleapis.com/css2?family=Tektur:wght@400;700;900&family=Noto+Sans+TC:wght@400;700&display=swap" rel="stylesheet">
```

---

## 3. Academic Clean（學術清爽）

適用：研究、論文、正式報告 ｜ 年級：**高中 / 大學**

| Token | 色值 | Tailwind Class |
|-------|------|----------------|
| 背景 bg | `#faf9f5` | `bg-[#faf9f5]` |
| 表面 surface | `#ede9e2` | `bg-[#ede9e2]` |
| 主色 primary | `#6a9bcc` | `bg-[#6a9bcc]` / `text-[#6a9bcc]` / `border-[#6a9bcc]` |
| 輔色 accent | `#d97757` | `bg-[#d97757]` / `text-[#d97757]` |
| 主文字 text | `#1a1814` | `text-[#1a1814]` |
| 次文字 muted | `#787060` | `text-[#787060]` |
| 邊框 border | `#d4cec4` | `border-[#d4cec4]` |
| 標題字型 | Instrument Sans | `font-[Instrument_Sans]` |

**Google Fonts import：**
```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;600;700&family=Noto+Sans+TC:wght@400;700&display=swap" rel="stylesheet">
```

---

## 年級字型大小（px，1920×1080 畫布）

> open-slide 的 1920×1080 畫布由框架自動縮放，px 值即為設計稿實際值，無需轉換 rem/em。

| 年級 | title | h2 | body | small | max bullets |
|------|-------|----|------|-------|-------------|
| 國小低（1-2） | `text-[96px]` | `text-[72px]` | `text-[56px]` | `text-[40px]` | 3 |
| 國小中高（3-6） | `text-[84px]` | `text-[60px]` | `text-[48px]` | `text-[36px]` | 4 |
| 國中 | `text-[72px]` | `text-[52px]` | `text-[40px]` | `text-[32px]` | 5 |
| 高中 | `text-[64px]` | `text-[48px]` | `text-[36px]` | `text-[28px]` | 6 |
| 大學 | `text-[56px]` | `text-[44px]` | `text-[32px]` | `text-[24px]` | 6 |

---

## 快速替換指南（主題切換）

Tech Dark 版本的版型只需將 Edu Warm 色值替換：

| Edu Warm | Tech Dark |
|----------|-----------|
| `bg-[#fffbf5]` | `bg-[#0D1117]` |
| `bg-[#f5ede0]` | `bg-[#161B22]` |
| `text-[#2d1a0e]` | `text-[#E6EDF3]` |
| `text-[#987b63]` | `text-[#8B949E]` |
| `text-[#d97757]` / `bg-[#d97757]` | `text-[#00D4FF]` / `bg-[#00D4FF]` |
| `border-[#e8d5bf]` | `border-[#30363D]` |
