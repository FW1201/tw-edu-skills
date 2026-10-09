# v5 遷移指南

v5.0.0 新增面向分類、12 支技能，並重新設計 6 支既有技能的輸入規格。其餘技能的輸入 JSON 與 CLI 不變。

## 技能名稱

既有 23 支名稱不變。新增：

| 面向 | 新技能 |
|---|---|
| 課程設計 | tw-edu-lesson-design-brainstorm、tw-edu-school-curriculum-plan |
| 學生表現 | tw-edu-conduct-comments |
| 班級經營 | tw-edu-homeroom-operations、tw-edu-behavior-support、tw-edu-incident-response、tw-edu-student-guidance-advice、tw-edu-guidance-collaboration |
| 教育行政 | tw-edu-official-document |
| 教師專業 | tw-edu-open-lesson、tw-edu-school-affairs-meeting、tw-edu-teacher-wellbeing |

## 輸入規格變更（不相容）

| 技能 | v4 | v5 |
|---|---|---|
| tw-edu-classroom-culture | `agreements`、`routines`、`response_plan` | `norms`（safety_floor、shared_agreements、choices）、`rituals`、`routines`、`repair_paths`、`response_plan`；選填 `relationship_practices`、`class_activities`、`student_voice` |
| tw-edu-parent-communication | `recipients`、`purpose`、`message`、`requested_action`、`contact_channel` | 新增必填 `audience`、`channel`、`sensitivity`、`facts`、`send_status`；選填 `concerns`、`pending`、`meeting_plan` |
| tw-edu-school-document | `document_type`：plan、memo、report、application、curriculum | `document_type`：活動計畫、補助申請計畫、成果報告、校內辦法草案、實施計畫、其他；新增必填 `approval_status`；選填 `schedule`、`budget`、`total_budget`、`funding_source`、`results`、`pending` |
| tw-edu-meeting-facilitator | `participants`、`agenda`（topic、minutes、owner）、`decisions`、`actions` | 新增必填 `meeting_type`、`date`、`duration_minutes`、`record_status`；agenda 加 `kind`；`decisions` 改為 `reports` 與 `discussions`（含 status） |

v4 的 `document_type: memo` 若是公文，改用 `tw-edu-official-document`。v4 meeting-facilitator 的觀課模式改用 `tw-edu-open-lesson`。

## 相容擴充（舊輸入仍可用）

| 技能 | 新增選填欄位 |
|---|---|
| tw-edu-lesson-plan-108 | `mode`、`learning_focus`、`issues`、`differentiation` |
| tw-edu-curriculum-mapper | `school_events`（輸出第二張工作表「校行事對照」） |

lesson-plan-108 與 curriculum-mapper 因思維路線大幅改寫升為 5.0.0，輸入仍向下相容。

## 執行行為

- 所有生成器的 `.validation.json` 新增 `advisories` 欄位，記錄非阻擋性提醒。
- 新增語意閘門：學生代碼不得像姓名；回應措施不得含體罰、羞辱、連坐、罰錢；分析與評語不得含診斷或標籤用語；紅旗事件必須有通報項目且不得標為已結案；公文主旨不得分項、「鈞」只用於上行。
- 課綱快照移至 `shared/curriculum/`，同步到 lesson-plan-108、curriculum-mapper、interdisciplinary、lesson-design-brainstorm、school-curriculum-plan；各技能的 `scripts/lookup_curriculum.py` 用法不變。
- 所有技能新增 `references/common/safety-red-flags.md`。

## 開發端

- `shared/runtime/build_runtime_assets.py` 已移除；schema 與 example 直接在技能目錄維護。
- `validate_skills.py` 不再限定 23 支，改為 manifest 與目錄一致；並檢查 category、bundles、v5 七段式與 description。
- 測試的生成器清單改由 manifest 推導。
