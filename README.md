# tw-edu-skills v5.0.1

臺灣 K-12 教師的 35 個獨立 AI Skills，分 8 個面向：課程設計、評量命題、教材資源、學生表現、班級經營、教育行政、教師專業、套組設定。適用 Codex 與 Claude Code。各技能可單獨安裝；Agent 依技能內的思維路線讀教材與實際資料、撰寫內容，Python 驗證並排版。教師保有教學判斷權。

v5 重點：每支技能改寫為「定位與邊界 → 開始前 → 思維路線 → 台灣情境要點 → 產出 → 品質關卡 → 交接」七段式；新增班級經營（導師事務、行為支持、事件應變與通報分流、學生輔導建議、輔導與特教協作）、教育行政（校園公文）與教師專業（公開授課、校事會議應對、教師壓力支持）等 12 支；法規與時限主張集中記錄於 [CITATIONS.md](CITATIONS.md)。遷移見 [v5 遷移指南](docs/MIGRATION-v5.md)；舊版見 [v4 遷移指南](docs/MIGRATION-v4.md)。

## 安裝

需要 Git 與 Python 3.10+。先檢視原始碼，再安裝：

```bash
git clone https://github.com/FW1201/tw-edu-skills.git
cd tw-edu-skills
# 預覽，不修改安裝目錄
bash install.sh --agent codex --dry-run
# Codex 全套
bash install.sh --agent codex
# Claude Code 全套
bash install.sh --agent claude-code
# 單項：只安裝教案技能
bash install.sh tw-edu-lesson-plan-108 --agent codex
```

Codex 預設使用者目錄為 `~/.codex/skills`，Claude Code 為 `~/.claude/skills`。既有自訂內容會阻止覆蓋；檢查後可加 `--force`，舊目錄仍保留為同層隱藏備份。安裝器不執行全域 pip。完整說明見 [快速開始](docs/quick-start.md)。

## 使用

告訴 Agent：「使用 tw-edu-lesson-plan-108，根據這份教材設計國中八年級國語文兩節課教案。」

技能讀取目前工作區的 `teacher-profile.md`；本次要求優先。Agent 先檢查來源、補足必要脈絡，再依技能 schema 建立內容。產出檔案前先驗證，正式內容不混入示範資料。未提供來源或未查證課綱時明示待確認。

生成器共同介面：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r tw-edu-lesson-plan-108/requirements.txt
.venv/bin/python tw-edu-lesson-plan-108/scripts/generate_lesson_plan.py --input input.json --validate-only
.venv/bin/python tw-edu-lesson-plan-108/scripts/generate_lesson_plan.py --input input.json --output artifacts/lesson.docx
```

各技能的 `schemas/` 與 `examples/` 提供輸入格式；`--example` 明確產生有標記的示範成品。只有主題、科目等舊參數的呼叫會提示遷移，不再生成看似正式的固定範本。

## 技能清單

<!-- inventory:start -->
共 35 個獨立 Skills，分 8 個面向。

### 課程設計（7）

| Skill | 用途 | 主要輸出 |
|---|---|---|
| `tw-edu-lesson-plan-108` | 108 課綱教案：以學習重點逆向設計目標、評量與活動，課綱代碼回查 | docx |
| `tw-edu-curriculum-mapper` | 課程地圖：跨單元安排學期進度、課綱對應與評量，檢查校行事衝突 | xlsx |
| `tw-edu-differentiated` | 差異化教學：依學習證據調整任務與支持 | docx |
| `tw-edu-interdisciplinary` | 跨領域課程：整合不同學科的概念與探究任務 | docx |
| `tw-edu-pbl-designer` | 專題式學習：設計驅動問題、探究歷程與真實成果 | docx |
| `tw-edu-lesson-design-brainstorm` | 課程設計發想引導：從議題或課題發散到收斂，引導教師構築教學設計構想 | docx |
| `tw-edu-school-curriculum-plan` | 學校課程計畫：規劃校訂與彈性學習課程架構、目標對應與審議流程 | docx |

### 評量命題（4）

| Skill | 用途 | 主要輸出 |
|---|---|---|
| `tw-edu-exam-generator` | 試卷命題：製作有答案、解析與配分的評量 | docx |
| `tw-edu-rubric-designer` | 評量規準：建立任務專屬的表現描述與評分方式 | docx |
| `tw-edu-formative-assessment` | 形成性評量：收集課中證據並決定教學調整 | docx |
| `tw-edu-anti-ai-assessment` | 評量真實性設計：檢視評量證據與改善任務設計 | docx |

### 教材資源（4）

| Skill | 用途 | 主要輸出 |
|---|---|---|
| `tw-edu-worksheet-creator` | 學習單：編排學生可完成的練習與思考任務 | docx |
| `tw-edu-slides-creator` | 教學簡報：製作可編輯投影片與教師講稿 | pptx |
| `tw-edu-mini-app` | 教學小程式：產出可本機開啟的互動教學網頁 | html |
| `tw-edu-material-reviewer` | 教材與評量品質審查：檢查既有教材、試卷或簡報的可定位缺陷，提出局部修正並複查 | docx |

### 學生表現（4）

| Skill | 用途 | 主要輸出 |
|---|---|---|
| `tw-edu-feedback-writer` | 學生回饋：根據作品證據撰寫具體可行的回饋 | docx |
| `tw-edu-learning-portfolio` | 學習歷程指導：協助整理學習證據、反思與成果 | docx |
| `tw-edu-learning-evidence-analyzer` | 學習證據分析：以匿名作答判讀班級學習證據，區分缺答、題目疑義與待驗證錯因 | docx |
| `tw-edu-conduct-comments` | 日常生活表現評語：依行為事實撰寫不標籤化的日常生活表現評語 | docx |

### 班級經營（7）

| Skill | 用途 | 主要輸出 |
|---|---|---|
| `tw-edu-parent-communication` | 親師溝通：依對象與敏感程度選擇管道，先事實後關切，提出具體合作請求 | docx |
| `tw-edu-classroom-culture` | 班級規範與文化：以安全底線、共同協議、可選擇事項三層規範，設計儀式、關係經營與修復路徑 | docx |
| `tw-edu-homeroom-operations` | 導師日常與學期事務：規劃開學建班、幹部職務、出缺勤預警、聯絡簿與學期交接 | docx |
| `tw-edu-behavior-support` | 學生行為支持：以觀察紀錄與功能假設設計正向行為支持計畫 | docx |
| `tw-edu-incident-response` | 事件應變與通報分流：處理同儕衝突並以紅旗閘門分流霸凌、性平、兒少保護與自傷通報 | docx |
| `tw-edu-student-guidance-advice` | 學生輔導建議：依匿名學生概況、時間序事件與教師看法提供分析與分層建議 | docx |
| `tw-edu-guidance-collaboration` | 輔導轉介與特教協作：準備三級輔導轉介、IEP 會議與最小必要資料分享 | docx |

### 教育行政（3）

| Skill | 用途 | 主要輸出 |
|---|---|---|
| `tw-edu-school-document` | 校務計畫與成果文書：撰寫活動計畫、補助申請、成果報告與校內辦法草案，經費與成果可檢核 | docx |
| `tw-edu-meeting-facilitator` | 校內會議議程與紀錄：排定議程時間，區分報告事項與討論事項決議，追蹤執行單位與期限 | docx |
| `tw-edu-official-document` | 校園公文：依文書處理手冊撰寫或修改學校簽、函、便簽、開會通知單與公告 | docx |

### 教師專業（5）

| Skill | 用途 | 主要輸出 |
|---|---|---|
| `tw-edu-research-viz` | 教學研究視覺化：以真實數據製作研究圖表 | png |
| `tw-edu-citation-checker` | 教育文獻查核：核實文獻存在性與引用資訊 | markdown |
| `tw-edu-open-lesson` | 公開授課與觀議課：規劃共同備課、低推論觀課紀錄與議課下一輪試作 | docx |
| `tw-edu-school-affairs-meeting` | 校事會議應對準備：整理校事會議程序權利、時程、陳述意見書與訪談準備 | docx |
| `tw-edu-teacher-wellbeing` | 教師壓力與職場支持：面對申訴與調查壓力時建立支持資源、界線與自我照顧計畫 | docx |

### 套組設定（1）

| Skill | 用途 | 主要輸出 |
|---|---|---|
| `tw-edu-synchronizer` | 教師偏好設定：建立與更新可供技能讀取的教師偏好 | markdown |
<!-- inventory:end -->

Markdown 型技能由 Agent 產出查核表或設定檔，其餘技能有本機內容驗證／渲染 CLI。簡報預設原生可編輯文字、圖形、表格與圖表；完整圖片簡報須選用 image 模式。試卷分成學生卷與教師答案卷。

## 能力與驗證

- [技能參考](docs/skill-reference.md)：輸入、輸出與驗收。
- [健檢報告](docs/AUDIT-v4.md)：原問題與修復證據。
- [驗收紀錄](docs/ACCEPTANCE-v4.md)：本機、CI、雙宿主與視覺檢查分別記錄。
- [開發與發布](CONTRIBUTING.md)：單一來源、封裝與測試方式。
- [v5 撰寫規範](docs/SKILL-AUTHORING-v5.md)：思維路線七段式與新增技能門檻。
- [路由案例](docs/eval/v5-routing-cases.md)：每支技能的正例與近似反例。
- [引據查核](CITATIONS.md)：法規與官方規範的條次與查核日期。

需要的外部工具依當次宿主能力使用；未連接工具時不承諾外部同步、部署或搜尋完成。來源查證與教學適切性仍需教師確認。

## 授權

[MIT License](LICENSE)。第三方參考與授權見 [NOTICE.md](NOTICE.md)。作者：吳奇（Kevin Wu）・數位敘事力社群。引用：吳奇（2026）。tw-edu-skills：臺灣 K-12 教學 Skills [Software]。https://github.com/FW1201/tw-edu-skills
