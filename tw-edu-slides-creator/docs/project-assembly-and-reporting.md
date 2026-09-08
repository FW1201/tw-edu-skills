# 組裝與驗收

使用本技能 generate_slides.py，以 --input 提供版本化 JSON、--output 指定 PPTX。
先執行 --validate-only。命令完整範例與依賴見 SKILL.md。

## Editable（預設）

content.mode 為 editable。slides 依序提供 id、title、body、notes，並可加入 schema 支援的 table、chart、image。
文字、表格、圖表必須保留原生可編輯物件；notes 寫入同頁講者備註。
先做一頁樣張確認後，再填寫全套輸入。

## Image（選用）

content.mode 為 image，每頁提供圖片路徑與同頁 notes。
圖片需 16:9、頁碼連續且不可重複。所有路徑按生成器的輸入路徑規則解析。
沿用逐頁生圖時，可使用 slide-generation-state.md 的選用工作紀錄。
不要將圖片式 PPTX 宣稱為文字可編輯。

## 視覺檢查

實際開啟或渲染每頁：繁體中文與中文字型、截斷／溢出、圖表標籤、表格密度、圖片比例、投影可讀性、16:9 與備註對應。
內容需符合大綱與年段，不出現虛構課綱代碼、無關裝飾或未授權素材。
修復嚴重問題後才交付；超長內容需拆頁或請使用者核准精簡，不靜默刪文。

## 交付

列出 PPTX、輸入 JSON、大綱、樣張與驗證紀錄的實際路徑，
說明模式、頁數、哪些項目已檢查、哪些仍待教師／平台確認。
生成器的結構檢查不等於 Office 視覺驗收。
