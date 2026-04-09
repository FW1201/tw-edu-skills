---
name: tw-social-infocard
description: >
  製作社群媒體資訊圖卡（FB、Threads、Instagram），支援單張與輪播多張，
  產出可直接預覽並下載 PNG 的互動式 HTML Artifact。
  內建對話式風格引導（平台尺寸、配色、字型），支援品牌底圖上傳，
  並自動偵測文字是否超出方框給予字數建議。
  當使用者提及「資訊圖卡」「社群圖卡」「IG 圖卡」「FB 圖文」「Threads 卡片」
  「做圖」「圖卡設計」「幫我做貼文圖片」「社群媒體視覺設計」「品牌圖卡」
  「輪播圖」「carousel 圖」「做一張可以貼到社群的圖」時，必須觸發此 Skill。
  即使使用者只說「幫我把這段文字做成圖」「這篇文章做成 IG 卡片」也要觸發。
---

# 社群媒體資訊圖卡製作 Skill

## 總覽

本 Skill 引導 Claude 完成從原始內容→風格對齊→Artifact 輸出→PNG 下載的完整圖卡製作流程。  
**核心原則**：先對齊，再生成。不要一開始就輸出圖卡，要先跑完 Phase 1–2 的引導流程。

---

## 流程總覽（必須依序執行）

```
Phase 1：內容處理   → 讀取輸入，提出文案簡化建議，等使用者確認
Phase 2：設計引導   → 平台/尺寸 → 底圖/配色 → 字型 → 版型
Phase 3：Artifact 輸出 → 生成互動預覽 + 下載功能
```

---

## Phase 1：內容處理

### 1-1 接收輸入

使用者可能提供以下任一形式：
- **純文字段落**：直接使用
- **上傳的 PDF 或 Word 檔**：先讀取檔案內容再處理
- **結構化資料**（已有標題+要點）：確認結構後使用

### 1-2 文案簡化建議（必做）

分析原始內容後，**主動提出簡化版本**，格式如下：

```
📋 原始內容（共 XXX 字）
[顯示原文摘要]

✏️ 建議簡化版本（適合圖卡，XXX 字以內）
標題：[建議標題，15 字以內]
主體：[建議內文，依版型建議字數]
標籤/備註：[可選，例如品牌名、日期]

→ 請問要用建議版、原始版，還是您自己調整？
```

**字數指引（避免文字超出方框）**：
| 區塊 | 建議上限 |
|------|---------|
| 主標題 | 15 字 |
| 副標題 | 20 字 |
| 內文（每段）| 50–80 字 |
| 條列項目 | 每點 15 字以內，最多 5 點 |
| 輪播每張 | 各自視為獨立圖卡，同上限 |

---

## Phase 2：設計引導對話

依序問以下問題（可合併成一則訊息），**等使用者回覆後再進入 Phase 3**。

### 2-1 平台與尺寸

```
📐 請選擇圖卡尺寸（或輸入自訂寬 x 高）：
1. Instagram 正方形 1080×1080（最通用）
2. Instagram/Threads 豎版 1080×1350
3. FB/Threads 橫幅 1200×630
4. IG Story / Reels 封面 1080×1920
5. 自訂尺寸（請輸入 寬×高，例如 900×900）
```

### 2-2 底圖選項

```
🖼️ 底圖來源：
A. 我會上傳品牌底圖（Artifact 裡有上傳按鈕）
B. 純色背景（請告訴我顏色，或提供 hex code）
C. 漸層背景（請描述方向和兩個顏色）
D. 讓 Claude 依主題自動選配
```

### 2-3 主色調 / 配色

若選 B/C/D，詢問：
```
🎨 主題色系偏向？（可說顏色名、情境或直接給 hex）
例如：海軍藍、珊瑚橘、#2D4A8A、科技感藍綠、溫暖大地色
```

若選 A（自己上傳底圖），跳過配色，直接問字型。

### 2-4 字型風格

```
✍️ 字型偏好？
1. 現代無襯線（思源黑體 / Noto Sans TC）—— 清爽、科技感
2. 人文明朝（Noto Serif TC）—— 典雅、學術感
3. 圓體（Cubic11 / M PLUS Rounded）—— 活潑、親切
4. 粗標題 + 細內文混排（衝突感、設計感強）
5. 讓 Claude 依主題決定
```

### 2-5 版型（Layout）

```
📌 版型風格？
1. 置中對齊（適合短句、宣言型）
2. 左對齊條列（適合知識分享、步驟型）
3. 大標題佔版上半、內文下半（視覺衝擊型）
4. 上圖下文（底圖佔上方，資訊集中下半）
5. Claude 依內容自動判斷
```

---

## Phase 3：Artifact 輸出規格

確認所有設計選項後，生成 **HTML Artifact**。

### 技術規格

**必須使用的函式庫（CDN）**：
```html
<!-- 字型 -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;700;900&family=Noto+Serif+TC:wght@400;700&display=swap" rel="stylesheet">

<!-- PNG 下載 -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
```

### Artifact 必備功能區塊

#### A. 控制列（Control Bar）
在圖卡預覽上方或側欄，包含：
- 底圖上傳按鈕（`<input type="file" accept="image/*">`）→ 設為圖卡背景
- 下載 PNG 按鈕（呼叫 html2canvas）
- 若是輪播：上一張 / 下一張 導覽按鈕 + 目前第幾張/共幾張

#### B. 圖卡預覽區（Card Preview）
- 以 CSS 依使用者選擇的尺寸等比例縮放到畫面適合大小（`transform: scale()`）
- 外層 wrapper 維持真實像素比例
- 所有文字區塊加上 `overflow: hidden` 和 `word-break: break-word`
- 字體大小以 `clamp()` 或固定 px 值確保不超框

#### C. 下載邏輯（關鍵）
```javascript
async function downloadCard(cardElement, filename) {
  const canvas = await html2canvas(cardElement, {
    scale: 2,           // 2x 高解析度輸出
    useCORS: true,
    allowTaint: false,
    backgroundColor: null,
    width: CARD_WIDTH,
    height: CARD_HEIGHT
  });
  const link = document.createElement('a');
  link.download = filename || 'infocard.png';
  link.href = canvas.toDataURL('image/png');
  link.click();
}
```

#### D. 輪播邏輯（若多張）
- 每張卡片為獨立的 `div.card`，用 CSS 控制顯示/隱藏
- 下載按鈕下載「目前顯示的那張」
- 提供「全部下載（打包）」按鈕，依序 download 每張

### 防止文字超框的 CSS 原則

```css
.card-title {
  font-size: clamp(24px, 4vw, 56px);
  line-height: 1.3;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.card-body {
  font-size: clamp(14px, 2vw, 22px);
  line-height: 1.6;
  overflow: hidden;
  word-break: break-word;
  flex: 1;
}
```

---

## 輸出品質檢查清單

Claude 生成 Artifact 前，自我確認：

- [ ] 是否跑完 Phase 1–2，獲得使用者確認的文案和設計選項？
- [ ] 圖卡尺寸正確（像素值對應使用者選擇）？
- [ ] 是否有底圖上傳按鈕？
- [ ] 是否有 html2canvas 下載按鈕？
- [ ] 標題字數 ≤ 15 字？內文每段 ≤ 80 字？
- [ ] 所有文字區塊是否都有 overflow 保護？
- [ ] 若輪播，是否有導覽按鈕和個別下載？
- [ ] Google Fonts CJK 字型是否正確載入？

---

## 常見版型模板提示

### 知識分享型（條列）
```
[大標題]
━━━━━━━━━━━
① 要點一
② 要點二
③ 要點三
─────────
[品牌名 / 來源]
```

### 金句宣言型（置中）
```
     [小標 / 引言]
  
  ❝ 主要金句文字 ❞
  
  ── 作者或出處 ──
```

### 步驟教學型（輪播）
```
封面卡：主題 + 共 N 張
第 1 張：步驟一
第 2 張：步驟二
...
結尾卡：CTA 或品牌資訊
```

---

## 特別注意事項

1. **底圖上傳後的文字可讀性**：若使用者上傳底圖，自動在文字區塊加半透明遮罩（`rgba(0,0,0,0.4)` 或白色）確保對比度
2. **繁體中文字型**：優先使用 `Noto Sans TC`，確保 Google Fonts 正常載入
3. **下載解析度**：html2canvas scale 固定為 2，確保輸出為 FullHD 以上品質
4. **不要一開始就輸出圖卡**：必須先完成 Phase 1 文案確認 + Phase 2 設計引導
