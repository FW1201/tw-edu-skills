# tw-edu-skills 全專案健檢

2026-09-07；基準 d19f192（遠端）／1cff78d（原本機）。本文件記錄真實問題，修復與驗證仍以測試及 ACCEPTANCE-v4.md 為準。

| 原問題 | 證據 | 修復方向 |
|---|---|---|
| 必要規範無法載入 | 19 個 SKILL.md 使用 ../../tw_edu_*.md，超出 repo 根目錄 | 獨立技能內的 references/common/workflow.md |
| 共用維護重複 | 16 份 tw_edu_doc_utils.py SHA-256 完全相同 | shared/runtime 單一來源與 CI 同步驗證 |
| 清單錯誤 | README／安裝器／CLAUDE.md 宣稱數量不一致，追蹤實際 21 個 | manifest 驅動清單、安裝、打包、文件 |
| 安裝破壞自訂資料 | install.sh 未驗證名字直接 rm -rf，漏 synchronizer | 白名單、dry-run、備份替換與失敗回復 |
| CI 過期且停用 | workflow 指向已刪除 generate_slides.py；9/5 改成 workflow_dispatch | 新生成器、跨平台 regression、自動 CI |
| 輸入未使用 | --students、--assessment_text、--content、--types、rubric --type 被忽略 | task-specific schema 與實際內容驗收 |
| 試卷不一致 | 選擇題標 20 題，迴圈實際最多 3 題 | 實際題目清單／分數守恆；學生卷、答案卷分開 |
| mini-app 任務錯誤 | flashcard 落入 lottery 分支；錯誤 JSON 改成範例 | 四種類型明確分支與輸入驗證 |
| 年段錯誤 | get_stage('高中一年級') 與國中一年級皆回 elementary | 先辨識學段再辨識年級 |
| HTML 執行風險 | JSON 直接嵌入 script、使用者文字進 innerHTML | 安全序列化、文字節點及攻擊字串測試 |
| 不實內容 | 固定學生／班級觀察、國語文代碼與誇張 AI 能力斷言 | 實際內容輸入、來源狀態、去除無證據斷言 |
| 中文圖表失敗 | PRISMA 指定 DejaVu Sans，requirements 缺 matplotlib | CJK 字型檢查、依賴及數量驗證 |
| 偏好功能不完整 | synchronizer 寫設定，其他技能沒有共同讀取規則 | 所有技能明確讀取工作區 teacher-profile.md |
| 簡報不可編輯 | 每頁僅完整圖片，預設輸出綁定個人 Wiki | 原生可編輯 PPTX，圖片模式可選，工作區輸出 |
| 參考與腳本不存在 | 多技能提及未提供的 references 與生成腳本 | 新入口僅引用已打包資源，保留可用教學資料 |

原工作區 README 修改、四支腳本權限修改與未追蹤短影音目錄均保留。新版在獨立 checkout 開發，不把這些產出納入發布。

## 範圍判斷

保留 21 個入口及其不同教學目的。文獻查核、研究視覺化、學習歷程保留教師支援角色。未新增 README 曾列出但未實作的三個技能，不涉及其他專案。Markdown 型技能不新增無必要的生成器。
