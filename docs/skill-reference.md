# 技能參考

由 skills-manifest.json 與各技能 schema 產生。共 21 個獨立 Skills。

| Skill | 用途 | 輸入內容 | 輸出 |
|---|---|---|---|
| [tw-edu-lesson-plan-108](../tw-edu-lesson-plan-108/SKILL.md) | 依課程目標安排活動、時間與評量 | title, total_minutes, objectives, activities, assessments | docx |
| [tw-edu-curriculum-mapper](../tw-edu-curriculum-mapper/SKILL.md) | 跨單元安排學期目標、進度與課綱對應 | title, units | xlsx |
| [tw-edu-differentiated](../tw-edu-differentiated/SKILL.md) | 依學習證據調整任務與支持 | title, shared_goal, learner_groups, activities | docx |
| [tw-edu-interdisciplinary](../tw-edu-interdisciplinary/SKILL.md) | 整合不同學科的概念與探究任務 | title, disciplines, driving_question, discipline_contributions, activities, product | docx |
| [tw-edu-exam-generator](../tw-edu-exam-generator/SKILL.md) | 製作有答案、解析與配分的評量 | title, expected_question_count, total_points, questions | docx |
| [tw-edu-rubric-designer](../tw-edu-rubric-designer/SKILL.md) | 建立任務專屬的表現描述與評分方式 | title, type, total_points, levels | docx |
| [tw-edu-formative-assessment](../tw-edu-formative-assessment/SKILL.md) | 收集課中證據並決定教學調整 | title, learning_target, checks, response_rules | docx |
| [tw-edu-worksheet-creator](../tw-edu-worksheet-creator/SKILL.md) | 編排學生可完成的練習與思考任務 | title, instructions, prompts, reflection | docx |
| [tw-edu-slides-creator](../tw-edu-slides-creator/SKILL.md) | 製作可編輯投影片與教師講稿 | title, slides | pptx |
| [tw-edu-feedback-writer](../tw-edu-feedback-writer/SKILL.md) | 根據作品證據撰寫具體可行的回饋 | title, students | docx |
| [tw-edu-learning-portfolio](../tw-edu-learning-portfolio/SKILL.md) | 協助整理學習證據、反思與成果 | title, records | docx |
| [tw-edu-parent-communication](../tw-edu-parent-communication/SKILL.md) | 撰寫清楚、有同理心的親師草稿 | title, recipients, purpose, message, requested_action, contact_channel | docx |
| [tw-edu-classroom-culture](../tw-edu-classroom-culture/SKILL.md) | 設計共同規範、班級活動與支持策略 | title, agreements, routines, response_plan | docx |
| [tw-edu-school-document](../tw-edu-school-document/SKILL.md) | 整理計畫、會議與行政文稿 | title, document_type, basis, purpose, implementation, responsible_people, expected_results | docx |
| [tw-edu-meeting-facilitator](../tw-edu-meeting-facilitator/SKILL.md) | 建立議程、紀錄與可追蹤行動事項 | title, participants, agenda, decisions, actions | docx |
| [tw-edu-pbl-designer](../tw-edu-pbl-designer/SKILL.md) | 設計驅動問題、探究歷程與真實成果 | title, driving_question, authentic_context, milestones, final_product, assessment_criteria | docx |
| [tw-edu-mini-app](../tw-edu-mini-app/SKILL.md) | 產出可本機開啟的互動教學網頁 | title, mode | html |
| [tw-edu-research-viz](../tw-edu-research-viz/SKILL.md) | 以真實數據製作研究圖表 | title, type | png |
| [tw-edu-citation-checker](../tw-edu-citation-checker/SKILL.md) | 核實文獻存在性與引用資訊 | 由 Agent 讀取來源／偏好，產出 Markdown | markdown |
| [tw-edu-anti-ai-assessment](../tw-edu-anti-ai-assessment/SKILL.md) | 檢視評量證據與改善任務設計 | title, items | docx |
| [tw-edu-synchronizer](../tw-edu-synchronizer/SKILL.md) | 建立與更新可供技能讀取的教師偏好 | 由 Agent 讀取來源／偏好，產出 Markdown | markdown |

## 共同輸入

schema_version=1.0、skill、language=zh-TW、context（subject、grade、topic）、sources、content。各技能 schema 與 example.json 是具體欄位定義。

CLI：--input JSON、--output PATH、--validate-only、--example。正式模式驗證失敗即停止，不產生成品。

驗收核對輸入與成品，學生卷不含答案；圖片簡報非文字可編輯，預設 editable。尚待來源查證、Office 視覺及宿主實測項目見 ACCEPTANCE-v4.md。
