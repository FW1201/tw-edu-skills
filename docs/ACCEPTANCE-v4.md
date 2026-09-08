# v4 驗收紀錄

2026-09-08。依使用者要求「變更完畢就好，不用過多額外驗收」，停止擴大驗收，未執行項目不標示通過。

| 驗證 | 實際結果 |
|---|---|
| 21 技能、metadata、資源、同步 | 通過 |
| 回歸、安裝、封裝 | 74 passed；包含生成器、錯誤輸入、備份回復、路徑越界、ZIP 獨立性 |
| Codex／Claude Code 單項及全套安裝 | 兩組隔離目錄通過，未覆蓋既有安裝 |
| 真實 Codex 任務 | 讀取教師設定，產出 40 分鐘自然科學教案、2 題 10 分學生／教師卷、3 頁可編輯簡報與備註，內容核對通過 |
| 真實 Claude Code 任務 | 未完成：auth status 回報 loggedIn=false |
| Chrome 四種小程式 | 答題計分與重設、翻卡與標記安全、抽選、計時暫停／重設／結束通過；無頁面錯誤 |
| PPTX 結構 | 原生文字、表格、圖表、備註、16:9；圖片模式缺圖、比例、重複與頁碼驗證通過 |
| DOCX 視覺 | 教案代表樣本已渲染檢查；指定可用 Noto TC 字型目錄後中文正常。後續排版修改僅完成回歸，未再做全頁視覺驗收 |
| Office 全套／長文壓力／外部生圖 | 未執行，依使用者要求不追加 |
| Linux/macOS × Python 3.10/3.12 | 首次分支 CI 四組全部成功；最新提交以 GitHub Actions 為準 |
| 教師接受／課綱與文獻查證 | 由各教學任務個別確認，不由 repo 測試替代 |

測試：`python -m pytest -q`、`python scripts/validate_skills.py`、`python scripts/sync_assets.py --check`。

選用瀏覽器重現：先執行 `python scripts/acceptance_fixtures.py`，再於已有 Playwright 與 Chrome 的環境執行 `node scripts/browser_smoke.cjs`。不自動安裝全域套件。

[首次升級 CI](https://github.com/FW1201/tw-edu-skills/actions/runs/34166227656)；[最新執行](https://github.com/FW1201/tw-edu-skills/actions)。
