---
name: tw-edu-mini-app
description: 互動教學小程式。依教學目的選擇互動測驗、單字卡、抽籤或計時器，用老師提供的實際題目與名單產出可離線開啟的單一 HTML，檢查答案、計分、鍵盤操作、空清單與安全輸出。適用於互動測驗、學習卡、抽籤、計時器、課堂小遊戲。
metadata:
  version: 4.2.0
  author: 奇老師・數位敘事力社群
  category: 教材資源
---

# 教學小程式

小程式要解決一個具體的課堂需求：快速檢核、反覆練習、公平抽人、掌握時間。它是工具，內容仍要正確，而且學生資料不能外流。

## 定位與邊界

- **做**：quiz、flashcard、lottery、timer 四種模式；內容驗證；鍵盤與觸控操作；本機離線開啟。
- **不做**：需要登入或資料庫的平台、蒐集學生個資的表單、自動部署到公開網址。

## 開始前

讀取 [共用工作方式](references/common/workflow.md)，檢查 `teacher-profile.md`。

必要情境：教學目的、模式、實際題目或卡片內容、使用裝置（教室電腦、學生平板）。抽籤名單建議用座號，不放學生全名。

## 思維路線

1. **選模式**：
   - quiz：檢核理解，需要題目、選項、答案、解析。
   - flashcard：記憶與練習，需要正反面內容。
   - lottery：公平抽人或抽題，需要名單或題目。
   - timer：活動計時，需要秒數。
2. **內容來自教學**：題目與答案依教材與學習目標，答案唯一，解析說明為什麼。
3. **檢查互動**：計分正確、空清單時有提示、重新開始能清空狀態、鍵盤可操作、按鈕有清楚標籤。
4. **安全**：文字以安全節點呈現，不執行輸入內容中的程式碼；學生姓名不傳到外部服務。
5. **使用情境**：投影時字級夠大；學生平板使用時不依賴網路。
6. **部署**：預設只產生本機檔案；需要放到網路上時，由老師在已授權的位置上傳，見部署說明。

## 台灣情境要點

- 校園網路與平板管理依學校資訊組規定；外部平台使用前確認學校是否同意。
- 部署選項與注意事項見 [部署說明](references/deployment_guide.md)。

## 產出

依 [輸入規格](schemas/input.schema.json) 建立 JSON，[範例](examples/example.json) 只看結構。

```bash
python3 "$SKILL_DIR/scripts/generate_mini_app.py" --input "$TASK_DIR/input.json" --validate-only
python3 "$SKILL_DIR/scripts/generate_mini_app.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/app.html"
```

語意閘門會擋下：quiz 模式題號重複、選項編號重複、答案不在選項中。

## 品質關卡

- 答案與解析正確。
- 在瀏覽器實際開啟並操作過一輪。
- 不含學生全名或個資。
- 沒有自動上傳或部署。

## 交接

- 正式評量 → `tw-edu-exam-generator`。
- 形成性評量的判讀與調整 → `tw-edu-formative-assessment`。
