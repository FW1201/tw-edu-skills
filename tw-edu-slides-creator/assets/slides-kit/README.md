# slides-kit — tw-edu-slides-creator v3.0 渲染套件

投影片結構 schema（JSON）→ 原生可編輯 `.pptx`。純 node、零 build。

## 安裝（一次）
```bash
cd assets/slides-kit
npm install                     # 只裝 pptxgenjs
# 截圖 QA 需要（選用）：
brew install --cask libreoffice # soffice
brew install poppler            # pdftoppm（多半已有）
```

## 四步流程
```bash
# 1) schema → pptx
node build.mjs examples/guoyu-7.json deck.pptx

# 2) 品質閘門（P0 必須清零）+ OOXML
node validate-deck.mjs examples/guoyu-7.json deck.pptx

# 3) 內容 QA（抽文字核對漏字/錯序/殘留佔位）
python3 -m markitdown deck.pptx

# 4) 截圖視覺 QA（需 LibreOffice）→ preview/slide-*.png
node render-preview.mjs deck.pptx preview
#    然後用 subagent「假設一定有錯」逐張審圖（清單見 SKILL.md）
```

## 檔案
| 檔 | 角色 |
|----|------|
| `tokens.mjs` | 12+ 學科鎖定色系 token＋WCAG 對比工具 |
| `grid.mjs` | 版面網格契約：座標常數、年級字級、8pt 間距、溢出估算 |
| `masters.mjs` | LIGHT/DARK slide master（含母題、頁尾） |
| `layouts.mjs` | 21 版型 renderer（schema → PptxGenJS 元素） |
| `build.mjs` | 編排器：deck.json → deck.pptx |
| `validate-deck.mjs` | 品質閘門 P0–P3 + OOXML |
| `render-preview.mjs` | pptx→PDF→PNG 截圖（+ N-up 總覽） |
| `examples/guoyu-7.json` | 範例 deck（七年級國文・10 張） |

## schema 規格
見 `../../references/pptx-layout-templates.md`（21 版型欄位）、`palette-library.md`（色系）、`layout-grid.md`（網格/字級）。

## 驗收基準（baseline）
首次以 `examples/guoyu-7.json` 跑完四步、視覺全清的 `preview/` 截圖，存為 baseline；
日後改 renderer 後重跑比對，避免版面回歸退化。
