# 開發與發布

Python 3.10+，在虛擬環境安裝 requirements-dev.txt。

## 維護原則

- skills-manifest.json 是技能清單、版本及依賴的來源。
- shared/runtime/edu_runtime 是生成器共用程式來源；shared/references 是共同規範來源。使用 scripts/sync_assets.py 同步實體副本。
- 每個 Skill 攜帶必要規範、schemas、examples、程式及 requirements.txt。
- CLI 修改需同步 schema、示例、說明及回歸測試。正式模式不得使用固定範例或忽略輸入。
- 保留技能各自教學目的，不加入統一任務狀態機或模型／API 設定服務。

## 驗證

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/sync_assets.py
.venv/bin/python scripts/sync_assets.py --check
.venv/bin/python scripts/validate_skills.py
.venv/bin/python -m pytest -q
.venv/bin/python scripts/package_skills.py
```

CI 在 Linux/macOS、Python 3.10/3.12 執行結構與回歸測試。中文字型由平台提供；無可用 CJK 字型時明示失敗。

## 發布

功能分支與 PR 整合；自動測試及雙宿主／視覺驗收後一般合併，禁止 force push。版本與 CHANGELOG 一致。package_skills.py 產生 21 個單項 ZIP、全套 ZIP 與 SHA256SUMS。發布後回讀 GitHub commit、CI、技能清單及資產。
