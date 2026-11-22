# 排版輸出與教材資料

輸出以繁中 A4 為預設。維持題幹、公式、圖與必要表格在同一作答脈絡。教師版加答案與提示，學生版採白名單組裝。學生交付時只傳學生檔及必要圖文來源。

教材來源為 UTF-8 JSON。上層有 `version: 1`、`title`、`stage`、`purpose`、`sources`、`items`。每題有唯一 `id`、`prompt`，可含 `formula`、`figure`、`table`、`answer_lines` 及教師專用 `answer`。公式輸入含 `latex` 與 `parts`，可用字串、`frac`、`sup`、`matrix`、`system` 組成。樣例展示各圖形類型和參數。學生來源會移除教師專用欄位。檔案只在指定輸出目錄內產生。

```bash
python3 -m pip install python-docx Pillow
python3 scripts/compose.py examples/elementary.json --validate-only
python3 scripts/compose.py examples/elementary.json --output /path/to/artifacts
```

內附工具用 Python 3.10+、python-docx、Pillow 和 soffice。可用 `--no-pdf` 僅輸出 DOCX，或用 `--figures-only` 只輸出 SVG。需要完整圖文時驗證所有工具可用，再生成。公式是 Word 原生 OMML，表格與文字是 Word 物件，數學圖可從 SVG 與參數重製。超出內建圖形種類時，可用其他本機工具產生 SVG，再依相同題號、來源與學生版規則交付。

逐份開啟後看 A4 黑白、題圖距離、表格欄底、可寫空間、公式上下標與字型。PDF 應與 DOCX 內容一致。聲稱可編輯前，在 Word 選取公式並更改一項，再重新開啟確認結構仍在。任何未執行的檢驗需標出。

## 字型與考卷分欄

在來源 JSON 的 `layout` 記錄字型與版面。舊資料沒有這一欄時，以 Noto Serif TC、單欄輸出，備用字型為 Noto Sans TC。

```json
{
  "layout": {
    "font_family": "Noto Serif TC",
    "fallback_font_family": "Noto Sans TC",
    "mode": "mixed",
    "zones": [
      {"start_item": "A1", "columns": 2, "title": "第一部分｜短題"},
      {"start_item": "B1", "columns": 1, "title": "第二部分｜圖表與推理"}
    ]
  }
}
```

- **單欄 `single`**：全部題目全寬，適合題幹較長、寬表格、大圖或手寫推導。
- **雙欄 `double`**：全部題目雙欄，封面標題和學生欄位保留全寬。題目依左欄往下、再右欄往下的順序流動。適合較短的題目。
- **分區混排 `mixed`**：每區從指定的 `start_item` 開始，直到下一區，標題可省略。第一區從首題開始，各區起始題號依原題序且不重複，須包含單欄和雙欄。題組標題全寬，同一題的 `page_break: true` 可讓該區或題目另起一頁。

使用 Word 原生分節分欄，學生版及教師版各自流動，同一份題目的頁碼可能因此不同。圖形、表格及作答線依欄寬縮放，避免窄欄溢出。遇到寬公式、密集表頭或需要手寫的長題，移到單欄區並重新檢查 PDF。可由 [示範輸入](../examples/exam-layout.json) 重製混排，或改成 `single`、`double` 並移除 `zones`。

指定字型用於正文、標題與圖表標籤，公式沿用 Word 的數學字型。產生器若能用 `fc-match` 確認字型已安裝，會採用指定字型，找不到時試用設定的備用字型。無法確認時會在終端與 `render-report.json` 提示。若有 `pdffonts`，報告也列出 PDF 實際使用及內嵌的字型。逐頁查看輸出，仍是檢查缺字及排版的依據。

### 左右欄指定題區

需要像校內考卷一樣，左欄固定排填答與計算、右欄固定從應用題開始時，採 `layout.mode: "double"`，並視需要使用以下設定：

| 欄位 | 行為 |
|---|---|
| `layout.exam_header: true` | 考卷學生版額外顯示學校欄。全套版式均採置中卷首；學生卷有年班、座號及姓名欄，獨立圖文頁僅顯示卷別。 |
| `layout.column_rule: true` | 雙欄區顯示中央直線，單欄區維持全寬。 |
| 題目的 `group_heading` | 在該題前加上欄內題區標題，例如題型和配分。 |
| 題目的 `column_break: true` | 在該題及題區標題之前跳到下一欄。放在右欄首題；可用於已有內容的雙欄區，不與換頁或分區起始題同時使用。 |
| 題目的 `workspace_mm` | 學生卷保留無線的作答空間，接受 5–90 毫米的整數，與舊欄位 `answer_lines` 二選一。舊欄位的每一行換成 6 mm 純空白。教師卷同一題放指定解析。 |

換欄前確認左欄內容能放進當頁。Word 會按實際版面流動，若左欄內容已溢到右欄，換欄會接到次頁。以教師版和學生版 PDF 分開確認右欄首題、圖形完整性、分數上下緣及作答空間。考卷範例見 [左右題區示例](../examples/exam-fixed-columns.json)。

考卷、講義及學習單統一使用 15 pt 卷首、10.5 pt 正文、12 pt 大題、11 pt 題目及 10.5 pt 子題。表頭以淺灰底辨識，教師版以「解析」引出答案。

### 算式填答

獨立算式若要求學生計算結果，於 `formula` 設定 `"answer_blank": true`。在 Word 原生公式後顯示「＝」後留白，原始 `latex` 和 `parts` 只填等號前的運算。分數、根式化簡、三角值等直接計算題皆可使用。有既定等號、提供條件的聯立方程式、圖示指定值及用文字問的應用題，保留原有數學關係。教師版保留原題供比對，答案和解析仍放在下方。

### 題目間距

`layout.question_gap_pt` 設定同欄相鄰題目的題號或題區標題上方間距，接受 0–30 pt 的整數。預設 10 pt。新頁、換欄與分區首題沿用其版面起點。`workspace_mm` 仍單獨控制手寫作答空間。


### 三層題號

每個 `group_heading` 或混排區的 `zone.title` 開始新的大題，依序編為「一、二、三、」。未設大題的文件會補「一、練習題」或「一、圖示」。各大題內題目重新由「1、」起算。大題與題目的編號由程式依順序產生，題目 `id` 仍作為資料與資產對應鍵。

同一題有多個子題時，在第一個子題同時設 `"parent_heading": "分數乘法"` 與 `"subquestion": true`，後續子題只設 `"subquestion": true`，顯示為縮排的「（1）（2）（3）」。新父題、新大題與一般題目會結束前一組子題。Word 採三層標題樣式，可在導航窗格查看；產出的題號是依輸入順序生成，調整題序後重新輸出即可更新。

優先使用 `workspace_mm` 指定純空白作答高度。只有姓名、座號及題意需要的圖表線保留線條。
