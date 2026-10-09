---
name: tw-edu-meeting-facilitator
description: 校內會議議程與紀錄。依會議類型（校務會議、行政會議、課程發展委員會、領域教學研究會、學生事務會議、班親會）排議程與時間，紀錄區分報告事項（決定）與討論事項（案由、說明、決議），追蹤執行單位與期限，未決議事項不寫成通過。適用於會議議程、會議紀錄、課發會、領域會議、班親會流程。
metadata:
  version: 5.0.0
  author: 奇老師・數位敘事力社群
  category: 教育行政
---

# 校內會議議程與紀錄

會議紀錄最重要的是讓沒出席的人也知道：決定了什麼、誰要做、什麼時候做完。沒有決議的事，就不能寫成已決議。

## 定位與邊界

- **做**：議程與時間配置、報告事項與討論事項的結構、紀錄草稿、執行追蹤、會議前後的狀態區分。
- **不做**：開會通知單（→ `tw-edu-official-document`）、公開授課的觀議課紀錄（→ `tw-edu-open-lesson`）、替會議做決定。

## 開始前

讀取 [共用工作方式](references/common/workflow.md)，檢查 `teacher-profile.md`。

必要情境：會議類型、日期、會議總時長、出席人員、議題與提案單位。若是寫紀錄，需要實際的會議內容（筆記、錄音逐字稿摘要）；沒有提供的決議一律寫〔待會議決議〕。

## 思維路線

1. **會議類型**：決定議程結構與出席者（例如課發會需有家長代表、校務會議有特定組成）。
2. **議程時間**：報告事項短、討論事項長、臨時動議預留；各項分鐘數加總必須等於會議總時長。
3. **報告事項**：各單位報告摘要；需要時記「決定」（如「洽悉」或指示事項）。
4. **討論事項**：每案寫案次、提案單位、案由、說明、決議。會前是議程草案，決議一律〔待會議決議〕；會後依實際結果寫通過、修正通過、不通過或保留。
5. **紀錄原則**：記重點與決議，不逐字記錄；發言者意見需要時摘要，不加評價。
6. **執行追蹤**：每項決議的執行單位與期限；下次會議報告「上次會議決議執行情形」。
7. **狀態**：議程草案、紀錄草稿、已確認紀錄分開；紀錄需經主席或與會者確認後才算確認。
8. **班親會**：流程、分工、班級經營說明、親師互動時間；不討論個別學生。

## 台灣情境要點

- 課程發展委員會、校務會議等的組成與議決方式依學校組織規程與相關規定；本技能不判斷會議是否合法召開。
- 公開授課的議課改用 `tw-edu-open-lesson`。

## 產出

依 [輸入規格](schemas/input.schema.json) 建立 JSON，[範例](examples/example.json) 只看結構。v5 必填 `meeting_type`、`date`、`duration_minutes`、`agenda`（含 `kind`）、`record_status`；選填 `reports`、`discussions`。

```bash
python3 "$SKILL_DIR/scripts/generate_meeting.py" --input "$TASK_DIR/input.json" --validate-only
python3 "$SKILL_DIR/scripts/generate_meeting.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/meeting.docx"
```

需要建立行事曆時，參考 [ICS 範本](references/ics_template.md)；實際建立行程或寄送需老師授權。

語意閘門會擋下：議程分鐘加總不等於會議時長、待決議事項寫了決議或已決議事項仍是〔待會議決議〕、議程草案中出現已決議事項。

## 品質關卡

- 時間配置合理且加總正確。
- 每個討論案都有案由、說明與決議狀態。
- 每項決議都有執行單位與期限。
- 草稿與已確認紀錄分開。

## 交接

- 開會通知單 → `tw-edu-official-document`。
- 會議通過的計畫 → `tw-edu-school-document`。
- 課發會的課程計畫 → `tw-edu-school-curriculum-plan`。
