# 5.0.1 — 2026-10-09

manifest 顯示名稱與用途對齊 v5 SKILL.md（classroom-culture、parent-communication、school-document、meeting-facilitator、lesson-plan-108、curriculum-mapper、material-reviewer、learning-evidence-analyzer），README 與技能參考重新產生。各技能內容與個別版本不變。

# 5.0.0 — 2026-10-09

**面向重整、思維路線深化、12 支新技能。共 35 支，分 8 個面向。**

- 面向：manifest 新增 `category`（課程設計、評量命題、教材資源、學生表現、班級經營、教育行政、教師專業、套組設定），README 與技能參考依面向分組。原「班級行政」拆為班級經營與教育行政。
- 思維路線：35 支 SKILL.md 全部改寫為七段式（定位與邊界、開始前、思維路線、台灣情境要點、產出、品質關卡、交接），由驗證器強制檢查；撰寫規範見 docs/SKILL-AUTHORING-v5.md。
- 新增：lesson-design-brainstorm、school-curriculum-plan、conduct-comments、homeroom-operations、behavior-support、incident-response、student-guidance-advice、guidance-collaboration、official-document、open-lesson、school-affairs-meeting、teacher-wellbeing（各 1.0.0）。
- 輸入規格不相容變更：classroom-culture、parent-communication、school-document、meeting-facilitator（各 5.0.0），見 docs/MIGRATION-v5.md。lesson-plan-108、curriculum-mapper 新增選填欄位（5.0.0，向下相容）。其餘既有技能改寫思維路線，升 minor。
- 語意閘門：新增 shared/runtime/edu_runtime/semantics.py（學生代碼、體罰與羞辱措施、診斷與標籤用語、紅旗通報、公文用語、經費與節數守恆、議程時間、評語證據等），非阻擋提醒寫入 `.validation.json` 的 `advisories`。
- 版面：新增宣告式 docx 版面（layouts.py）與公文版面（official.py）。
- 共用參考：新增 safety-red-flags.md（紅旗與通報分流），workflow.md 加入紅旗優先與四欄區分。
- 課綱快照移至 shared/curriculum，同步到 5 支課程設計技能。
- 引據：新增 CITATIONS.md，51 項法規與官方規範主張逐條記錄條次與查核日期（2026-10-09）；新增 NOTICE.md（tw-formal-writing，MIT）。
- 開發：移除 build_runtime_assets.py；驗證器不再寫死技能數；測試的生成器清單改由 manifest 推導。
- 未完成：宿主上的模型選用與多輪行為、Office 視覺全面驗收、課堂有效性；路由案例已建立但未批次實測。

# 4.1.1 — 2026-10-03

課綱參考移除舊代碼與未查證改寫，改為隨包9領域靜態快照及獨立查詢器；驗證快照雜湊、分類筆數與229條核心素養表。

# Changelog

## 4.1.0 — 2026-10-02

教師23入口：新增實際學習證據分析與素材品質審查；21既有入口加入教學品質、UDL、校準、觀課與選用跨域交接。現有JSON/CLI向下相容，新增入口各1.0；所有既有入口依實際內容改動升minor。

# Changelog

## 4.0.0 — 2026-09-08

- Reactivate this repository as 21 independent Taiwan K-12 Skills for Codex and Claude Code.
- Manifest-driven packaging, self-contained resources and recoverable installer updates.
- Versioned task inputs and content-driven document generation; explicit example mode.
- Editable slides by default, optional validated image decks.
- Separate student and teacher exam outputs, actual feedback records, four mini-app modes.
- Restore CI; record structural, host and visual verification separately.

The v3.1-final tag remains available. See docs/MIGRATION-v4.md for breaking CLI changes.
