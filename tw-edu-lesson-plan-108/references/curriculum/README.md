# 課綱資料快照

9 個 JSON 逐 byte 取自 FW1201/twa-edu-harness 的既有官方 PDF 抽取資料，來源 commit、每檔 SHA-256、分類筆數在 snapshot-manifest.json。原資料整理日期為 2026-09-08。本套件帶入的是靜態資料，不需要安裝或匯入任何 Harness 套件。

[教育部公告領綱入口](https://www.naer.edu.tw/PageSyllabus?fid=52)。本次已確認官方入口可用；完整 3460 筆未在本次重新逐頁比對 PDF。正式送件請核對當次官方領綱與適用學段。抽取資料可能保留格式正規化與既有抽取限制，不代表官方全文或人工驗收。

只載入當次需要的領域。lookup_curriculum.py 支援代碼、類型、關鍵字查詢；description 為快照原文，不是模型摘要。驗證器會檢查檔案雜湊、欄位、筆數及核心素養 Markdown 與 JSON 的一致性。後續替換快照必須一併更新來源證據、manifest 與生成表，不只修改 SHA-256。
