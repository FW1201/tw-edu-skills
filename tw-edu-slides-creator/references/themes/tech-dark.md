# 主題：Tech Dark（科技深色）

> 適用：AI 課程、程式設計、資訊科技、Vibe Coding、期末發表、高中進階
> 風格：深色、科技感、未來感，適合國中以上

## CSS 變數

```css
:root {
  --bg:      #0D1117;   /* GitHub 深夜模式底色 */
  --surface: #161B22;   /* 卡片底色 */
  --primary: #00D4FF;   /* 主色：電藍（標題、重點） */
  --accent:  #7B2FFF;   /* 強調色：紫（tag、按鈕） */
  --text:    #E6EDF3;   /* 正文：淺灰白 */
  --muted:   #8B949E;   /* 次要文字：中灰 */
  --border:  #30363D;   /* 分隔線 */
}
```

## 字型設定

```css
:root {
  --font-heading: 'Tektur', 'Noto Sans TC', sans-serif;
  --font-body:    'Noto Sans TC', monospace;
}
```

Google Fonts 引入：
```html
<link href="https://fonts.googleapis.com/css2?family=Tektur:wght@600;700;900&family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
```

## 年段字級（配合此主題）

| 年段 | --sz-title | --sz-h2 | --sz-body | --sz-small |
|------|-----------|---------|-----------|-----------|
| 國中 | 2.4rem | 1.8rem | 1.5rem | 1.1rem |
| 高中 | 2.0rem | 1.6rem | 1.3rem | 1.0rem |

> 此主題不建議用於國小低年級（深色背景對幼童較不友善）

## 推薦版型順序（12 張範例）

cover → hero → section → bullets → two-column → data → timeline → activity → quote → pros-cons → discussion → summary

## 對比度驗證

- `--text` (#E6EDF3) 對 `--bg` (#0D1117)：14.3:1 ✅ AAA
- `--primary` (#00D4FF) 對 `--bg` (#0D1117)：9.8:1 ✅ AAA
- `--text` 對 `--surface` (#161B22)：13.1:1 ✅ AAA
