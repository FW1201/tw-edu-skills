# 貢獻指南（Contributing Guide）

感謝你有興趣為「臺灣 K-12 教育 Claude Code Skills 套組」做出貢獻！
這份指南說明如何參與改善這個專案。

---

## 🎯 我們歡迎的貢獻類型

### 1. 改善現有 Skills
- 修正錯誤的課綱代碼
- 改善生成文件的格式與美觀度
- 補充更多 references 說明文件
- 新增更多範例資料

### 2. 新增 Skill 功能
- 新增支援高中各科的教案變體
- 新增英語教學專用 skill
- 新增特定議題融入設計（如性別平等、環境教育）

### 3. 修復問題
- Python 腳本 bug
- SKILL.md 觸發描述不準確
- 中文字型顯示問題

### 4. 改善文件
- 更新 README 說明
- 翻譯文件（英文版）
- 補充使用教學影片

---

## 🔧 開發流程

### 環境設定

```bash
# 1. Fork 並 clone
git clone https://github.com/YOUR_USERNAME/tw-edu-skills.git
cd tw-edu-skills

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 測試現有 skills
python3 tw-edu-lesson-plan-108/scripts/generate_lesson_plan.py \
  --subject 國語文 --title 測試課文 --grade 國中八年級 \
  --output /tmp/test_output.docx
```

### Skill 開發規範

#### SKILL.md 必要欄位
```yaml
---
name: tw-edu-[功能名稱]
description: >
  中文描述（包含觸發關鍵詞）
  觸發詞必須包含至少 5 個臺灣教育情境相關的詞語
version: X.X.X
author: 你的名字
allowed-tools: "Bash, Read, Write"
disable-model-invocation: true  # 任務型 skill 必填
---
```

#### Python 腳本規範
- 使用 `tw_edu_doc_utils.py` 共用工具庫
- 文件色彩系統使用品牌色（臺灣教育藍 `#1A5276`）
- 字型：`.docx` 使用標楷體，`.pptx` 使用微軟正黑體
- 紙張：A4，上下邊距 2cm，左右邊距 2.5cm
- 每個腳本必須有 `--output` 參數
- 包含 `argparse` 命令列介面

#### 測試要求
提交前請確認：
```bash
# 腳本可正常執行
python3 your-skill/scripts/generate_xxx.py --output /tmp/test.docx

# 輸出檔案可正常開啟（不為空、不報錯）
ls -lh /tmp/test.docx  # 應 > 20K
```

### 提交 Pull Request

1. 從 `main` 建立功能分支
   ```bash
   git checkout -b feature/改善國語文教案格式
   ```

2. 依照規範修改/新增檔案

3. 撰寫清楚的 commit message（中英文皆可）
   ```
   feat: 新增高中英文教案 skill
   fix: 修正國中數學試卷選擇題編號錯誤
   docs: 更新 README 安裝說明
   ```

4. 推送並建立 Pull Request
   - 標題請用中文說明變更內容
   - 附上測試截圖（文件截圖或終端機輸出）

---

## 📋 Skill 審查標準

Pull Request 合併前，維護者會確認：

| 項目 | 標準 |
|------|------|
| SKILL.md 格式 | 符合 Agent Skills Open Standard |
| 觸發詞 | 包含臺灣教育常用語彙 |
| 輸出品質 | 文件格式美觀、內容正確 |
| 108課綱 | 對應代碼正確（-J- / -E- / -U-） |
| 注音符號 | 使用 ㄅㄆㄇ（非漢語拼音） |
| 測試通過 | 腳本可正常執行 |
| 無個資 | 不包含真實學生資料 |

---

## 💬 聯絡與社群

- GitHub Issues：回報問題或提出建議
- 數位敘事力社群：奇老師主編
- 翻轉教育：https://flipedu.parenting.com.tw

---

> 「每一位願意改善這份工具的教師，都是在為更多孩子創造更好的學習機會。」
> —— 奇老師
