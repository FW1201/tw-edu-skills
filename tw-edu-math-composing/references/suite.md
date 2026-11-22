# tw-edu-skills 整合流程

查核日期 2026-11-22。

| 需求 | 主責技能與交接 |
|---|---|
| 教案、課綱、先備與目標 | tw-edu-lesson-plan-108 使用既有 schema 和教案表格。數學技能提供正確例題、常見錯誤與驗算。 |
| 學習單與投影片 | tw-edu-worksheet-creator 與 tw-edu-slides-creator 使用各自的版面和 schema。坐標圖由數學技能輸出 SVG／PNG，可置於相應題目的後方或附在投影片。 |
| 正式命題 | tw-edu-exam-generator 主責規格、題型、配分與驗證。先用原本的 --validate-only 驗證題數、題號及總分，再以同題 ID 交接。 |
| 數學試卷 | 數學技能接收已核對的題幹、配分與答案，加上公式、圖表、題組、欄位與作答高度。保留等號、三層題號及答案隔離。 |
| 互動或資料圖 | 數學技能核對模型、資料、公式與驗收值；既有教學小程式及研究視覺化技能維持各自原有流程。 |

數學套件的共用 CLI：

```sh
python3 scripts/generate_math_composing.py --input examples/example.json --validate-only
python3 scripts/generate_math_composing.py --input examples/example.json --output /path/to/exam.docx
```

輸入採清單標準欄位 schema_version、skill、language、context、sources 及 content。content 含 title、purpose、items 和選用 layout。輸出為 exam-student.docx、exam-teacher.docx 與驗證報告。需要 PDF 或獨立 SVG 時，原始 `scripts/compose.py` 仍可讀舊版 JSON。兩種入口共用同一數學版面。
