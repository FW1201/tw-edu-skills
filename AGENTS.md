# tw-edu-skills

21 個獨立臺灣 K-12 Skills，適用 Codex 與 Claude Code，繁體中文。保留 skills-manifest.json 中的名稱與獨立安裝能力。

修改共用邏輯請編輯 shared/runtime，並執行 scripts/sync_assets.py；不要手動編輯生成副本。各技能的 schema、示例與教學規範須對齊。正式生成不得使用未標示的範例資料，來源及學生事實不得虛構。

驗證：scripts/validate_skills.py、scripts/sync_assets.py --check、pytest。測試需檢查成品內容與資料流，不能只判斷檔案存在或大小。宿主實測、Office 視覺、外部工具驗收另行記錄，不冒充 CI 通過。

不修改使用者原有未提交內容。外部發布與同步遵循使用者已授權的範圍。開發流程見 CONTRIBUTING.md。
