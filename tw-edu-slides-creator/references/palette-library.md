# 學科色系庫（鎖定 design token）

12+ 組學科色系，每組 6 色 token＋深底 premium 變體，全部通過 WCAG AA（≥4.5:1）。
`meta.theme` 填**色系名**即可；renderer 自動套用，**schema 內絕不寫 raw hex**。

舊名對應：`Edu Warm→語文`、`Tech Dark→科技`、`Academic Clean→學術`。

| 色系 | bg | text | primary | secondary | accent | surface | text/bg | 深底 premium |
|------|----|----|---------|-----------|--------|---------|---------|------|
| **語文** | #FFFBF5 | #2D1A0E | #C2410C | #3F6FA3 | #B45309 | #F5EDE0 | 16.09:1 | bg #2A1A12 / primary #E9885F |
| **數學** | #F7F8FC | #1B1F3B | #4338CA | #0E7490 | #D97706 | #EAEDF7 | 15.15:1 | bg #14152B / primary #8B83F0 |
| **自然** | #F4FBF6 | #13261A | #15803D | #0E7490 | #CA8A04 | #E1F1E6 | 15.14:1 | bg #0F2419 / primary #4FB477 |
| **社會** | #FBF7F0 | #2B2114 | #B45309 | #1D5FA0 | #7C5E3C | #EFE5D4 | 14.78:1 | bg #241B10 / primary #D9913F |
| **英語** | #FFF7FA | #2B0F1C | #BE185D | #6D28D9 | #D97706 | #F6E2EB | 16.78:1 | bg #2A0F1B / primary #E96CA0 |
| **藝術** | #FBF7FF | #241433 | #7C3AED | #DB2777 | #0D9488 | #EDE4F8 | 16.23:1 | bg #1E1330 / primary #A985F0 |
| **科技** | #0D1117 | #E6EDF3 | #00D4FF | #7B2FFF | #FF6B35 | #161B22 | 16.02:1 | bg #0D1117 / primary #00D4FF |
| **SEL** | #F4FAF7 | #16271F | #2F6F5E | #6F9C8B | #D98A3D | #E1F0EA | 14.78:1 | bg #12241D / primary #5FAE96 |
| **體育** | #FFF6F4 | #2B1416 | #E11D48 | #0E8F8E | #D97706 | #F8E1DB | 16.26:1 | bg #2A1113 / primary #F2607E |
| **生活** | #FAF6F0 | #271E14 | #9A6A3A | #4F8060 | #C2410C | #EEE4D6 | 15.21:1 | bg #21190F / primary #C49364 |
| **學術** | #FAF9F5 | #1A1814 | #34539C | #5C84B8 | #B45309 | #EBE9E1 | 16.83:1 | bg #15171C / primary #7AA0D8 |
| **節慶** | #FFF8F2 | #2B1412 | #B91C1C | #B7892B | #0E7490 | #F6E4D6 | 16.48:1 | bg #2A100F / primary #E5654F |

## 用法
```jsonc
"meta": { "theme": "自然" }   // 換色系只改這個欄位（Delta 改風格）
```

## 規則
- **dominance over equality**：primary 佔 60–70% 視覺權重，secondary/accent 點綴。
- 深底版型（cover/section/hero/quote/closing）自動套 premium 變體。
- 新增色系：在 `assets/slides-kit/tokens.mjs` 加一組並跑對比檢查（見該檔尾的 contrastRatio）。
