---
name: tw-edu-classroom-culture
description: 班級規範與文化。把班級規範分成安全底線、共同協議、可選擇事項三層，設計可預期的儀式、日常程序、關係經營、班級活動、學生參與方式與修復路徑，依正向管教原則回應違反規範。適用於班規、班級公約、班級經營、班級氣氛、開學班級共識、班會。
metadata:
  version: 5.0.0
  author: 奇老師・數位敘事力社群
  category: 班級經營
---

# 班級規範與文化

班級文化是學生每天感受到的「在這裡怎麼一起生活」。規範讓大家安全，儀式讓大家安心，關係讓大家願意，修復路徑讓犯錯的人有路回來。

## 定位與邊界

- **做**：三層規範、儀式、日常程序、關係經營、班級活動、學生參與（班會、輪值決策）、修復路徑、事件回應原則。
- **不做**：導師行政事務如出缺勤與幹部輪替（→ `tw-edu-homeroom-operations`）、個別學生行為計畫（→ `tw-edu-behavior-support`）、事件通報（→ `tw-edu-incident-response`）。

## 開始前

讀取 [共用工作方式](references/common/workflow.md)，檢查 `teacher-profile.md`（學段、班級人數、導師或科任）。

必要情境：學段、班級特性（新生、重組班、已相處一年）、學校既有規定、老師想改善的具體狀況。

## 思維路線

1. **分三層規範**：
   - 安全底線：涉及人身安全、霸凌、法律義務的規則。不交付表決，老師直接說明理由。
   - 共同協議：怎麼上課、怎麼討論、怎麼借東西。和學生一起討論、一起寫，定期檢視。
   - 可選擇事項：學生可以自己決定的範圍，讓學生練習自主。
2. **規範寫成可觀察的行為**：「發言前舉手」而不是「要有禮貌」。每條規範說明為什麼。
3. **可預期的儀式**：一天的開始、活動轉換、結束、重要時刻（考試前、節日、離別）各有固定做法，降低焦慮與混亂。
4. **日常程序**：分組、收作業、討論、轉換教室等的步驟；前兩週要教、要練習。
5. **關係經營**：叫每位學生的名字、具體的肯定、短暫的個別聊天。關係不取代界線；教師不以分享私事換取學生親近。
6. **學生參與**：班會、輪流負責、提案修改協議的管道。
7. **修復路徑**：違反協議後怎麼彌補：冷靜 → 說出發生的事與影響 → 討論怎麼彌補 → 追蹤。事先公布，不臨時加碼處罰。
8. **事件回應**：違反安全底線時立即制止並確保安全，課後個別談；涉及紅旗時改走通報流程。回應不得體罰、羞辱、連坐或侵害財產。

## 台灣情境要點

- 管教原則依學校經校務會議通過的教師輔導與管教學生辦法，以及教育部注意事項（113.02.05 修正）：不得體罰、不得連坐、不得以罰錢等侵害財產權的方式管教、處罰前視情況給予陳述意見並說明理由。
- 涉及霸凌、性平、安全的事項不放入班級投票。

## 產出

依 [輸入規格](schemas/input.schema.json) 建立 JSON，[範例](examples/example.json) 只看結構。v5 結構：`norms`（safety_floor、shared_agreements、choices）、`rituals`、`routines`、`repair_paths`、`response_plan`，選填 `relationship_practices`、`class_activities`、`student_voice`。

```bash
python3 "$SKILL_DIR/scripts/generate_classroom.py" --input "$TASK_DIR/input.json" --validate-only
python3 "$SKILL_DIR/scripts/generate_classroom.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/classroom-culture.docx"
```

語意閘門：規範、修復路徑與事件回應中出現體罰、羞辱、連坐、罰錢等措施會被擋下（「不得體罰」之類的否定句不受影響）。

## 品質關卡

- 安全底線與共同協議分開，安全底線不交付表決。
- 每條協議都是可觀察的行為，並說明理由。
- 至少有開始與結束兩個儀式。
- 修復路徑事先公布，不是事後臨時決定。
- 沒有公開排名、羞辱或集體處罰。

## 交接

- 導師例行事務 → `tw-edu-homeroom-operations`。
- 個別學生 → `tw-edu-behavior-support` 或 `tw-edu-student-guidance-advice`。
- 事件 → `tw-edu-incident-response`。
- 班會紀錄 → `tw-edu-meeting-facilitator`。
