---
name: tw-edu-feedback-writer
description: 學生作品回饋。只依作品與觀察證據，指出具體優點、一個最重要的改進點與學生做得到的下一步，可依規準校準並另寫家長版語氣，不把單次表現寫成能力或人格標籤。適用於作業回饋、作文評語、報告回饋、學習回饋、批改評語。
metadata:
  version: 4.2.0
  author: 奇老師・數位敘事力社群
  category: 學生表現
---

# 學生回饋

有效的回饋讓學生知道「哪裡做得好、下一步改什麼、怎麼改」，而且學生拿到後真的會去修改。

## 定位與邊界

- **做**：依作品證據的具體優點、改進點、下一步、回饋文字、規準校準、家長版。
- **不做**：日常生活表現評語（→ `tw-edu-conduct-comments`）、全班作答統計（→ `tw-edu-learning-evidence-analyzer`）、分數換算或排名。

## 開始前

讀取 [共用工作方式](references/common/workflow.md)，檢查 `teacher-profile.md`（學段、語氣偏好）。

必要情境：作品內容或觀察紀錄、任務要求或規準、學段。學生用代碼。沒有作品或觀察時先請老師提供，不虛構學生表現、班級統計或人數。

## 思維路線

1. **看證據**：把作品中可以指出的地方列出來（第幾段、哪個步驟、哪句話）。
2. **對照目標或規準**：這份作品在哪個向度已經達到、哪個還沒有？有規準時用規準的語言。
3. **選一個最重要的改進點**：一次不給太多；選對學習目標影響最大、學生最做得到的那一個。
4. **寫下一步**：具體到學生知道要做什麼，例如「在第二段加一個例子說明你的理由」，並約定何時再看。
5. **語氣**：先肯定具體做到的部分，再說改進；描述作品而不是評價人。避免「你很粗心」「你不夠努力」。
6. **證據分級**：直接觀察（作品中看得到）與推測（可能原因）分開；推測只在需要時用「可能」表達。
7. **校準**（多位老師評同一批作品時）：比對評分與回饋，保留分歧與理由。
8. **家長版**：說明學生的進步與下一步，加上家長在家可以怎麼支持，不比較其他學生。

## 台灣情境要點

- 國中小學習評量辦法要求評量結果附具體建議並書面通知家長；回饋可作為具體建議的來源。
- 回饋不公開個別學生的成績或排名。

## 產出

依 [輸入規格](schemas/input.schema.json) 建立 JSON，[範例](examples/example.json) 只看結構。每位學生包含 `observations`、`strengths`、`next_steps`、`feedback`。

```bash
python3 "$SKILL_DIR/scripts/generate_feedback.py" --input "$TASK_DIR/input.json" --validate-only
python3 "$SKILL_DIR/scripts/generate_feedback.py" --input "$TASK_DIR/input.json" --output "$TASK_DIR/feedback.docx"
```

## 品質關卡

- 每個優點與改進點都指向作品中的具體位置。
- 下一步只有一到兩個，且學生做得到。
- 沒有人格評價或標籤。
- 家長版不洩漏其他學生資訊。

## 交接

- 規準 → `tw-edu-rubric-designer`。
- 修改歷程整理 → `tw-edu-learning-portfolio`。
- 全班共同問題 → `tw-edu-learning-evidence-analyzer` 或 `tw-edu-formative-assessment`。
