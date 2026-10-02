# 108 課綱指標查詢

本版移除未核對的手寫指標表。國語文、英語文、數學、社會、自然科學、藝術、健康與體育、綜合活動、科技的既有 PDF 抽取快照，分領域保存在 [curriculum/](curriculum/README.md)。查詢必須指定領域；同代碼跨領域的敘述不同。

```bash
python3 "$SKILL_DIR/scripts/lookup_curriculum.py" --domain 國語文 --code 5-IV-2
python3 "$SKILL_DIR/scripts/lookup_curriculum.py" --domain 英語文 --kind performance --keyword 聆聽 --limit 10
```

CLI 僅查隨包快照，沒有查到時回傳 `not_found_in_snapshot`，不臆造代碼。找到時逐字保留 `description`，教學轉化請另列為教師設計。核心素養的高中代碼依原資料保留 S，不用替換字首猜代碼。核心素養表見 [108_core_competencies.md](108_core_competencies.md)。正式使用前查 [國家教育研究院官方入口](https://www.naer.edu.tw/PageSyllabus?fid=52) 的當次公告與適用版本。
