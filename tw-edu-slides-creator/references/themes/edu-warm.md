# 主題：Edu Warm（教育暖色）

> 適用：一般教學、國語文、社會課、藝術、SEL、親師溝通
> 風格：溫暖、親切、清晰，適合全年段

## CSS 變數

```css
:root {
  --bg:      #fffbf5;   /* 暖白底色 */
  --surface: #f5ede0;   /* 卡片底色（比 bg 暗 8%） */
  --primary: #d97757;   /* 主色：暖橙（標題、重點） */
  --accent:  #6a9bcc;   /* 強調色：霧藍（按鈕、tag） */
  --text:    #2d1a0e;   /* 正文：深棕 */
  --muted:   #987b63;   /* 次要文字：中棕 */
  --border:  #e8d5bf;   /* 分隔線 */
}
```

## 字型設定

```css
:root {
  --font-heading: 'Work Sans', 'Noto Sans TC', sans-serif;
  --font-body:    'Noto Sans TC', sans-serif;
}
```

Google Fonts 引入：
```html
<link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@600;700;900&family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
```

## 年段字級（配合此主題）

| 年段 | --sz-title | --sz-h2 | --sz-body | --sz-small |
|------|-----------|---------|-----------|-----------|
| 國小低 | 3.2rem | 2.4rem | 2.0rem | 1.4rem |
| 國小中高 | 2.8rem | 2.0rem | 1.7rem | 1.3rem |
| 國中 | 2.4rem | 1.8rem | 1.5rem | 1.1rem |
| 高中 | 2.0rem | 1.6rem | 1.3rem | 1.0rem |

## 推薦版型順序（15 張範例）

cover → objectives → section → bullets → vocab → activity → discussion → hero → bullets → two-column → data → quote → three-column → summary → checklist

## 對比度驗證

- `--text` (#2d1a0e) 對 `--bg` (#fffbf5)：16.8:1 ✅ AAA
- `--primary` (#d97757) 對 `--bg` (#fffbf5)：3.1:1 → 僅用於大字標題（≥18pt），符合 WCAG AA Large
- `--text` 對 `--surface` (#f5ede0)：14.5:1 ✅ AAA
