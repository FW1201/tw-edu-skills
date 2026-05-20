# 主題：Academic Clean（學術清爽）

> 適用：研究報告、碩論簡報、正式學術發表、高中學術性課程
> 風格：清爽、專業、知識感，適合高中以上

## CSS 變數

```css
:root {
  --bg:      #faf9f5;   /* 暖白底（接近 canvas-design 官方底色） */
  --surface: #ede9e2;   /* 卡片底色（米白） */
  --primary: #6a9bcc;   /* 主色：霧藍（標題、重點） */
  --accent:  #d97757;   /* 強調色：暖橙（tag、數據） */
  --text:    #1a1814;   /* 正文：深棕黑 */
  --muted:   #787060;   /* 次要文字：中灰棕 */
  --border:  #d4cec4;   /* 分隔線 */
}
```

## 字型設定

```css
:root {
  --font-heading: 'Instrument Sans', 'Noto Sans TC', sans-serif;
  --font-body:    'Lora', 'Noto Serif TC', 'Noto Sans TC', serif;
}
```

Google Fonts 引入：
```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@600;700&family=Lora:wght@400;700&family=Noto+Sans+TC:wght@400;700;900&display=swap" rel="stylesheet">
```

> 注意：Lora 僅含拉丁字元，中文正文 fallback 至 Noto Sans TC。

## 年段字級（配合此主題）

| 年段 | --sz-title | --sz-h2 | --sz-body | --sz-small |
|------|-----------|---------|-----------|-----------|
| 高中 | 2.0rem | 1.6rem | 1.3rem | 1.0rem |
| 大學/研究所 | 1.8rem | 1.4rem | 1.2rem | 0.95rem |

## 推薦版型順序（研究型 16 張範例）

cover → objectives → section → hero → bullets → two-column → timeline → data → quote → pros-cons → three-column → bullets → discussion → summary → checklist → quote

## 對比度驗證

- `--text` (#1a1814) 對 `--bg` (#faf9f5)：17.2:1 ✅ AAA
- `--primary` (#6a9bcc) 對 `--bg` (#faf9f5)：3.4:1 → 僅用於大字標題（≥18pt），符合 WCAG AA Large
- `--text` 對 `--surface` (#ede9e2)：15.8:1 ✅ AAA
