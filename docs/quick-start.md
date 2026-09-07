# 快速開始

需要 Git、Python 3.10+，以及已登入的 Codex 或 Claude Code。

```bash
git clone https://github.com/FW1201/tw-edu-skills.git
cd tw-edu-skills
bash install.sh --agent codex --dry-run
bash install.sh --agent codex
# Claude Code 全套
bash install.sh --agent claude-code
# 只安裝評量技能
bash install.sh tw-edu-exam-generator --agent claude-code
```

預設安裝至使用者的 ~/.codex/skills 或 ~/.claude/skills。--dest 可指定測試或其他目錄；自訂目錄需依宿主設定為可發現位置。dry-run 不產生安裝目錄。若偵測已自訂內容，先比較，再明確加 --force；更新保留舊目錄備份。

在目前工作區告訴 Agent 使用技能並提供素材，例如：「使用 tw-edu-lesson-plan-108，國中八年級國語文，兩節各45分鐘，根據附件設計教案。」已提供的資訊不用重答。

想保存偏好可使用 tw-edu-synchronizer，建立工作區 teacher-profile.md。本次要求優先。設定檔不要放學生名單或診斷資訊。

需要文件輸出時建立虛擬環境，依該技能 requirements.txt 安裝套件。Agent 讀 schemas 與 examples，建立實際內容 JSON，先 --validate-only 再生成。--example 只用於示範，成品會標示為範例。

正式成品預設位於目前工作區 artifacts/教師/<task-name>/，可指定其他目的地。完成後檢查驗證紀錄與成品；教學適切性與 Office 視覺需實際確認。
