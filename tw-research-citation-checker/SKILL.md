---
name: tw-research-citation-checker
description: >
  嚴格查核學術文獻的準確性與引用格式，透過 WebSearch、Consensus MCP 進行
  多源交叉驗證，逐一確認作者/年份/標題/期刊/頁碼，並驗證目標引用格式
  (APA 7th / MLA 9th / 臺灣學位論文 / Chicago) 是否正確。
  查核不到的文獻直接標示「查無」，格式錯誤直接指出哪裡錯。
  當使用者提及「查文獻」「驗證引用」「確認參考資料」「文獻格式對嗎」
  「APA格式」「MLA格式」「引用正確嗎」「幫我查一下這個文獻」
  「格式查驗」「文獻清單」「參考書目」「bibliography」「references」時觸發。
version: 1.0.0
author: 奇老師・數位敘事力社群
allowed-tools: "Bash, Read, Write, WebSearch"
disable-model-invocation: true
---

# 學術文獻嚴格查核與格式驗證系統 v1.0

## 核心原則
「**寧可說查無，也不給假答案。**
查不到的文獻直接標示 ❌ 查無；格式錯誤直接標出錯誤位置，不美化。」

---

## Step 0：讀取必要文件

1. `references/citation_formats.md` — 各格式完整規範（APA 7th / MLA / 臺灣格式）
2. `references/verification_protocol.md` — 文獻查核流程與標準
3. `../../tw_edu_guided_collection.md` — 引導式收集框架

MCP 查核工具（依優先順序）：
1. **Consensus MCP**（學術論文搜尋）
2. **WebSearch**（Google Scholar / CrossRef / DOI resolver）

---


**概念對齊協議（必要前置步驟）：**
`../../tw_edu_concept_alignment.md`
→ 在執行任何工作前，先完成概念對齊確認卡。


## Step 1：引導式資訊收集

### 第一輪（必填）
```
Q1: 「請貼上要查核的文獻清單（可以是原始引用格式，或混亂的草稿）」

Q2: 「目標引用格式是什麼？
    A. APA 7th Edition（美國心理學會）
    B. MLA 9th Edition
    C. 臺灣學位論文格式（國科會/教育部）
    D. Chicago 17th
    E. Vancouver（醫學/理工）
    F. 只查真假，不管格式」
```

### 第二輪（選填）
```
Q3: 「文獻類型有哪些？（幫我更準確地查核）
    □ 期刊文章（journal article）
    □ 學位論文（thesis/dissertation）
    □ 書籍（book）
    □ 書章（book chapter）
    □ 研討會論文（conference paper）
    □ 政府/機構報告
    □ 網頁/新聞」

Q4: 「有 DOI 或 URL 嗎？（有的話查核最精確）」
```

### 確認摘要
```
✅ 文獻數量：{N} 筆
📋 目標格式：{格式名稱}
🔍 查核工具：Consensus MCP + WebSearch + DOI Resolver
⚠️ 原則：查不到 = 直接標示「查無」，不猜測
```

---

## Step 2：查核流程（每筆文獻執行）

### 查核五步驟（每筆文獻都要走完）

```
Step A：解析文獻資訊
  從輸入文獻中提取：
  ・作者（姓名拼寫、排列順序）
  ・年份
  ・標題（大小寫、標點符號）
  ・來源（期刊名 / 書名 / 出版社）
  ・頁碼 / 卷期號 / DOI
```

```
Step B：Consensus MCP 學術搜尋（若可用）
  呼叫：
  Consensus:search(query: "{作者} {標題關鍵詞} {年份}")
  
  解析返回結果：
  ・比對標題（允許細微差異）
  ・比對作者（注意東亞姓名順序）
  ・比對年份
  ・比對期刊名
  ・記錄 Consensus 搜尋結果
```

```
Step C：WebSearch 交叉驗證
  搜尋策略（依序執行，找到即停）：
  
  搜尋 1：DOI 解析（最精確）
    https://doi.org/{doi} 或 搜尋 "DOI:{doi}"
  
  搜尋 2：Google Scholar 風格
    "{作者姓} {標題前7字}" {年份} filetype:pdf
  
  搜尋 3：期刊官網
    site:{期刊縮寫}.com OR site:{期刊縮寫}.org "{標題}"
  
  搜尋 4：CrossRef API
    api.crossref.org/works?query={標題關鍵詞}&filter=from-pub-date:{年份}
  
  搜尋 5：最廣泛搜尋
    "{作者姓} {年份} {標題前5字}" academic
```

```
Step D：判定結果（嚴格標準）
  
  ✅ 確認存在：多個來源均可確認基本資訊一致
     → 進行格式驗證
  
  ⚠️ 部分確認：僅找到部分資訊，有疑點
     → 標示哪裡不確定，建議使用者自行確認
  
  ❌ 查無：
     a. 多方搜尋均找不到
     b. 找到的資訊與輸入不符（作者/年份/標題 不一致）
     c. 懷疑為 AI 幻覺（hallucinated reference）
     → 直接標示「查無 / 資訊不符」，不猜測、不補足
```

```
Step E：格式驗證（若文獻存在）
  逐字比對目標格式規範：
  ・作者格式是否正確（姓名縮寫、&/and 使用）
  ・年份位置
  ・標題大小寫規則
  ・期刊名斜體/縮寫
  ・卷號/期號/頁碼格式
  ・DOI 格式（https://doi.org/...）
  ・標點符號（逗號/句號/冒號位置）
```

---

## Step 3：各格式嚴格規範

### APA 7th Edition
```
期刊文章：
Author, A. A., & Author, B. B. (Year). Title of article with only first word capitalized and proper nouns. Journal Name in Italics, Volume(Issue), StartPage–EndPage. https://doi.org/xxxxx

常見錯誤檢查點：
□ 作者：姓在前，名縮寫（A. A.），多作者用 & 連接最後兩位
□ 年份：緊接在作者後，用括號 ()
□ 文章標題：只有第一個字、副標題第一個字、專有名詞大寫
□ 期刊名：斜體、每個主要詞都大寫（Title Case）
□ 卷號：斜體；期號：括號內，不斜體
□ 頁碼：用 en dash（–）不是連字號（-）
□ DOI：必須用 https://doi.org/ 開頭（新格式）
□ 超過 20 位作者：列前 19 位 + ... + 最後一位
```

```
書籍：
Author, A. A. (Year). Title of book: Subtitle in italics. Publisher. https://doi.org/xxxxx

書章：
Author, A. A. (Year). Title of chapter. In E. Editor (Ed.), Title of Book (pp. XX–XX). Publisher.

學位論文（臺灣）：
Author, A. A. (Year). Title of dissertation [Unpublished doctoral dissertation / master's thesis]. University Name.
注意：臺灣學位論文加上 http://handle.ncl.edu.tw/11296/xxxxxx

網頁：
Author, A. A. (Year, Month Day). Title of webpage. Website Name. URL
（注意：若無作者，用組織名稱；若無日期，用 n.d.）
```

### MLA 9th Edition
```
期刊文章：
Author Last, First, and Author First Last. "Title of Article." Journal Name, vol. X, no. X, Year, pp. X–X. DOI or URL.

常見錯誤：
□ 作者：第一位姓在前，後面作者名在前
□ 文章標題用引號，期刊名斜體
□ 用逗號分隔各元素（不是句號）
□ 頁碼用 pp.（多頁）或 p.（單頁）
```

### 臺灣學位論文格式（APA 中文版）
```
中文期刊：
作者（年份）。文章標題。期刊名稱，卷（期），頁碼–頁碼。https://doi.org/xxxxx

中文書籍：
作者（年份）。書名。出版社。

英文文獻：
同 APA 7th，但需注意：
・中文作者的英文拼音（需確認作者自己使用的拼法）
・臺灣出版社要加國別（Taipei, Taiwan: 出版社）

常見錯誤：
□ 中英文標點混用（應全部用英文標點，或全部用中文標點）
□ 年份沒加（）
□ 卷期號格式不一致
```

---

## Step 4：AI 幻覺文獻識別指引

**已知 LLM 容易「幻覺」出的文獻特徵：**

```
高風險特徵（須加強查核）：
1. 作者名字看似真實但無法在 Scholar 找到
2. 標題聽起來完全符合你的研究主題（太合適）
3. 年份是近期（2020-2024）但 DOI 無法解析
4. 期刊名有細微拼寫錯誤（如 Journal of Educational Technology vs Journal of Educational Technologies）
5. 頁碼異常（如 pp. 1-200 或 pp. 1000-1050）
6. 卷期號不合理（如 Vol. 99, No. 99）

查核策略：
→ 先用 Consensus MCP 搜尋作者的其他已知論文，確認此作者真實存在
→ 用 DOI 直接驗證（doi.org/{doi}）
→ 搜尋期刊官網的 TOC（Table of Contents）確認該期有無此文
→ 若以上都找不到：直接標示 ❌ 疑為 AI 幻覺文獻，強烈建議移除
```

---

## Step 5：查核報告格式

### 每筆文獻的報告格式
```
══════════════════════════════════════════════════
文獻 #X
══════════════════════════════════════════════════

【原始輸入】
{使用者提供的原始文字}

【查核狀態】{在此選一}
  ✅ 確認存在 | ⚠️ 部分確認 | ❌ 查無 | ❌ 疑為 AI 幻覺

【查核過程】
  Consensus 搜尋：{找到/未找到，說明}
  WebSearch：{搜尋策略和結果摘要}
  DOI 驗證：{有效/無效/未提供}

【正確資訊】（若找到）
  作者：{正確拼寫}
  年份：{確認年份}
  標題：{確認標題}
  來源：{期刊/出版社}
  DOI：{確認 DOI}

【格式驗證】（若為存在的文獻）
  目標格式：{APA 7th / MLA / 臺灣}
  使用者輸入：{原始格式}
  正確格式：{應該是什麼}
  
  格式錯誤清單：
  ❌ [錯誤位置]：{描述錯誤} → 應改為：{正確寫法}
  ❌ [錯誤位置]：...
  
  若無錯誤：✅ 格式正確

【建議行動】
  {替換為正確資訊 / 移除此文獻 / 使用者自行確認 / 無需修改}
══════════════════════════════════════════════════
```

### 全批次摘要報告
```
════ 查核完成摘要 ════════════════════════════════
總計文獻數：{N} 筆
✅ 確認存在：{n} 筆
⚠️ 部分確認：{n} 筆（需使用者自行確認）
❌ 查無：{n} 筆
❌ 疑為 AI 幻覺：{n} 筆

格式問題：{N} 個錯誤（共 {n} 筆有格式問題）

最常見錯誤類型：
1. {錯誤類型1}（{n} 筆）
2. {錯誤類型2}（{n} 筆）

建議：{整體改進方向}
═════════════════════════════════════════════════
```

---

## Step 6：Consensus MCP 調用規範

```
Consensus 是學術論文專用搜尋 MCP，返回真實學術論文資訊。

呼叫語法：
Consensus:search(query: "{搜尋詞}")

搜尋策略（由精確到廣泛）：
策略1：完整標題搜尋
  query: ""{完整標題}""

策略2：作者 + 年份 + 關鍵詞
  query: "{第一作者姓} {年份} {標題前5個詞}"

策略3：主題搜尋確認作者
  query: "{作者名} {研究領域} {年份前後3年}"

解析返回結果：
  ・比對 paper_title（允許大小寫差異）
  ・比對 authors（注意順序和拼寫）
  ・比對 year（年份必須一致）
  ・記錄 doi（用於進一步驗證）
  
注意事項：
  ・Consensus 主要覆蓋英語學術文獻
  ・中文文獻查核需同時用 WebSearch 搜尋 CNKI / HyRead / 臺灣期刊論文索引
  ・Consensus 返回不代表 100% 正確，仍需 DOI 驗證
```

---

## Step 7：各平台 MCP 差異

| 功能 | Claude Code | Claude.ai | Codex/gemini-cli |
|------|------------|-----------|-----------------|
| Consensus 搜尋 | ✅ MCP | ✅ MCP（若連接） | ❌ → 僅 WebSearch |
| WebSearch | ✅ | ✅ | ✅ |
| DOI 解析 | ✅（WebSearch） | ✅ | ✅ |
| CrossRef API | ✅ | ✅ | ✅ |
| 中文資料庫（CNKI/HyRead） | ✅ WebSearch | ✅ WebSearch | ✅ |

### 無 Consensus MCP 時的降級方案
改用以下 WebSearch 組合進行多源驗證：
1. Google Scholar（直接搜尋）
2. doi.org（DOI 驗證）
3. Crossref REST API（api.crossref.org）
4. Semantic Scholar（semanticscholar.org）
5. PubMed（生醫類）
6. JSTOR（人文社科類）
7. 臺灣博碩士論文系統（ndltd.ncl.edu.tw）

---

## Step 8：品質確認清單

- [ ] 每筆文獻至少通過 2 個獨立來源驗證
- [ ] DOI 格式已驗證（https://doi.org/...）
- [ ] 未找到的文獻直接標示「查無」，未猜測補全
- [ ] 中文文獻已搜尋中文資料庫（非只用英文資料庫）
- [ ] AI 幻覺特徵已逐一審查
- [ ] 格式錯誤已逐條列出（不只說「有錯誤」）
- [ ] 摘要報告清楚呈現通過/疑問/失敗的數量
