# tw-edu-skills

35 個獨立臺灣 K-12 教師 Skills（8 個面向），適用 Codex 與 Claude Code，繁體中文。保留 skills-manifest.json 中的名稱、面向與獨立安裝能力。

修改共用邏輯請編輯 shared/runtime、shared/references 或 shared/curriculum，並執行 scripts/sync_assets.py；不要手動編輯生成副本。各技能的 schema、示例與 SKILL.md 思維路線須對齊。新增或改寫技能依 docs/SKILL-AUTHORING-v5.md。正式生成不得使用未標示的範例資料，來源及學生事實不得虛構。

法規、時限、官方規範的主張必須記錄於 CITATIONS.md（來源、條次、查核日期、狀態），技能內的情境要點須與其一致；無法查證的標待查，不寫成事實。涉及學生安全的紅旗一律先導向 shared/references/safety-red-flags.md。

驗證：scripts/validate_skills.py、scripts/sync_assets.py --check、scripts/verify_curriculum_snapshot.py、pytest。測試需檢查成品內容與資料流，不能只判斷檔案存在或大小。宿主實測、Office 視覺、外部工具驗收另行記錄，不冒充 CI 通過。

不修改使用者原有未提交內容。外部發布與同步遵循使用者已授權的範圍。開發流程見 CONTRIBUTING.md。
