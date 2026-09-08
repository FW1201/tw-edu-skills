# tw-edu-skills v4.0.0

重新啟用原專案，保留 21 個獨立技能與既有名稱，不依賴 Harness。

- 19 個內容驅動生成器：版本化 JSON、驗證、明確範例與成品驗證紀錄。
- Codex／Claude Code 單項或全套安裝、預覽、自訂內容衝突、備份與失敗回復。
- 簡報預設原生可編輯，可選圖片模式；試卷學生卷與教師卷分開。
- quiz、flashcard、lottery、timer 實作並以 Chrome 操作檢查。
- 共用來源同步成技能內實體檔案；21 份獨立 ZIP、全套 ZIP 與 SHA256SUMS。
- 自動 CI：Linux/macOS，Python 3.10/3.12。

遷移：舊範例式 CLI 改用 `--input JSON`；`--example` 只用於明確示範。
省略 `--output` 時寫入目前工作區 `artifacts/<skill>/<task-id>/`，不覆寫既有成品。
圖片路徑相對於輸入 JSON；中文字型需在開啟／渲染環境可用。

驗證範圍：74 項測試、Codex 代表流程與瀏覽器操作完成。Claude Code 已驗證安裝，但實際任務受未登入阻擋；未做完整 Office 視覺驗收。依使用者要求不再追加驗收，細節見 ACCEPTANCE-v4.md。
