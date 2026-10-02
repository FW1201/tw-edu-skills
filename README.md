# tw-edu-skills v4.1.0

臺灣 K-12 教師的 23 個獨立 AI Skills，適用 Codex 與 Claude Code。各技能可單獨安裝；Agent 根據教材與實際資料撰寫內容，Python 驗證並排版。教師保有教學判斷權。

本 repo 已重新啟用，安裝與更新來源為 **FW1201/tw-edu-skills**。v3.1-final 保留供舊版查閱，新版遷移見 [v4 遷移指南](docs/MIGRATION-v4.md)。

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
| Skill | 用途 | 主要輸出 |
|---|---|---|
| `tw-edu-lesson-plan-108` | 108 課綱教案 | docx |
| `tw-edu-curriculum-mapper` | 課程地圖 | xlsx |
| `tw-edu-differentiated` | 差異化教學 | docx |
| `tw-edu-interdisciplinary` | 跨領域課程 | docx |
| `tw-edu-exam-generator` | 試卷命題 | docx |
| `tw-edu-rubric-designer` | 評量規準 | docx |
| `tw-edu-formative-assessment` | 形成性評量 | docx |
| `tw-edu-worksheet-creator` | 學習單 | docx |
| `tw-edu-slides-creator` | 教學簡報 | pptx |
| `tw-edu-feedback-writer` | 學生回饋 | docx |
| `tw-edu-learning-portfolio` | 學習歷程指導 | docx |
| `tw-edu-parent-communication` | 親師溝通 | docx |
| `tw-edu-classroom-culture` | 班級經營 | docx |
| `tw-edu-school-document` | 校園文書 | docx |
| `tw-edu-meeting-facilitator` | 會議引導 | docx |
| `tw-edu-pbl-designer` | 專題式學習 | docx |
| `tw-edu-mini-app` | 教學小程式 | html |
| `tw-edu-research-viz` | 教學研究視覺化 | png |
| `tw-edu-citation-checker` | 教育文獻查核 | markdown |
| `tw-edu-anti-ai-assessment` | 評量真實性設計 | docx |
| `tw-edu-synchronizer` | 教師偏好設定 | markdown |
| `tw-edu-learning-evidence-analyzer` | 學習證據分析 | docx |
| `tw-edu-material-reviewer` | 教材與評量品質審查 | docx |
<!-- inventory:end -->

Markdown 型技能由 Agent 產出查核表或設定檔，其餘技能有本機內容驗證／渲染 CLI。簡報預設原生可編輯文字、圖形、表格與圖表；完整圖片簡報須選用 image 模式。試卷分成學生卷與教師答案卷。

## 能力與驗證

- [技能參考](docs/skill-reference.md)：輸入、輸出與驗收。
- [健檢報告](docs/AUDIT-v4.md)：原問題與修復證據。
- [驗收紀錄](docs/ACCEPTANCE-v4.md)：本機、CI、雙宿主與視覺檢查分別記錄。
- [開發與發布](CONTRIBUTING.md)：單一來源、封裝與測試方式。

需要的外部工具依當次宿主能力使用；未連接工具時不承諾外部同步、部署或搜尋完成。來源查證與教學適切性仍需教師確認。

## 授權

[MIT License](LICENSE)。作者：吳奇（Kevin Wu）・數位敘事力社群。引用：吳奇（2026）。tw-edu-skills：臺灣 K-12 教學 Skills [Software]。https://github.com/FW1201/tw-edu-skills
