# 教學簡報設計鐵則（doctrine）v3.0

> v3.0：輸出改為原生 .pptx（PptxGenJS）。版面契約由 `assets/slides-kit/` 強制，本檔是 Claude 規劃內容
> 與 subagent 審圖時的判斷依據。內容類型→版型對應表見 `pptx-layout-templates.md`。

---

## 一、四條核心信條

1. **結構優於裝飾**：層級靠排版、留白、網格對齊建立，不靠陰影/漸層/浮卡。
2. **圖片是第一公民**：每張都要有視覺元素（圖、圖表、形狀、icon、數據），**禁純文字（標題＋條列）投影片**。
3. **克制優於炫技**：一個視覺母題（左上色塊）跨頁重複；不堆元素。
4. **dominance over equality**：主色佔 60–70% 視覺權重，1–2 輔色＋1 銳利 accent，禁止平均分配。

---

## 二、AI 投影片破綻（務必避免）

- ⚠️ **標題下方裝飾底線/accent line** —— 最明顯的 AI 痕跡。改用留白或背景色塊區隔。
- 連續同版型 >3 張（validate 報 P1）→ 用 `section` 分段或換版型。
- 內文置中（只有標題置中，內文一律左對齊）。
- 低對比文字/圖示（已由 token 預先過 AA；勿在 schema 自帶 hex 破壞）。
- 間距忽大忽小（套件用 8pt scale，勿手動微調）。

---

## 三、年級適配

| 年級 | 重點 | 版型偏好 |
|------|------|----------|
| 國小低 | 字大、條目少（≤3）、多圖、注音 | vocab, activity, hero, image-hero |
| 國小中高 | 具象、步驟化 | process-flow, timeline, three-column |
| 國中 | 對比、分析 | two-column, pros-cons, data, matrix |
| 高中/大學 | 抽象、論證 | concept-web, matrix, quote, data |

字級由 `meta.grade` 自動套（見 `layout-grid.md`），不需手動指定。

---

## 四、Bloom 分層 → 版型

- **記憶/理解**：`bullets`、`vocab`、`summary`、`data`
- **應用/分析**：`two-column`、`pros-cons`、`matrix`、`process-flow`、`timeline`
- **評鑑/創造**：`discussion`、`activity`、`concept-web`、`checklist`

一份簡報應跨越多個 Bloom 層級，避免全部停留在「記憶/理解」。

---

## 五、dark/light sandwich 節奏

- 深底：`cover`（開場）→ … → `closing`（收尾）；中途 `section`/`quote`/`hero` 作為深底錨點。
- 淺底：所有內容頁。
- 預設已自動套用；要覆寫用 slide 的 `tone: "dark" | "light"`。

---

## 六、QA 心態（吸收原生 pptx skill）

> 「假設一定有錯，你的工作是找出來。」第一次 render 幾乎不會對；QA 是抓蟲不是確認。
> 若第一輪零問題，是你看得不夠仔細。修一個常引發另一個 → 至少跑一輪 fix-and-verify。

審圖清單見 `SKILL.md`「Subagent 審圖清單」。
