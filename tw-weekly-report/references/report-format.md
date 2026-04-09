# 週報視覺化格式規範

## 使用 visualize:show_widget 輸出週報

週報必須透過 `visualize:show_widget` 生成 HTML 介面，**不得純文字輸出**。

---

## HTML 結構規範

### 整體佈局
```
┌─────────────────────────────┐
│  週報標題列（日期 + 統計摘要）  │
├─────────────────────────────┤
│  角色工作量分布（橫條圖）       │
├──────────────┬──────────────┤
│ 已完成任務清單 │ 需跟進清單   │
├─────────────────────────────┤
│  跨角色機會提示（最多3項）     │
├─────────────────────────────┤
│  下週優先任務（3-5項排序）     │
└─────────────────────────────┘
```

---

## 各區塊設計細節

### 1. 週報標題列
- 週報標題：「📊 本週工作盤點」
- 副標：「YYYY/MM/DD – YYYY/MM/DD（共 N 則對話）」
- 右側小字：生成時間

### 2. 角色工作量分布（橫條圖）
使用 HTML + CSS 製作簡單橫條圖，不用 canvas 或外部庫：

```html
<div class="bar-row">
  <span class="role-label">🟣 主編</span>
  <div class="bar" style="width: XX%">N 個任務</div>
</div>
```

- 橫條寬度 = 該角色任務數 / 最多角色任務數 × 100%
- 顏色：主編紫色 #EEEDFE/#3C3489、研究者藍色 #E6F1FB/#0C447C、
  教師青綠 #E1F5EE/#085041、開發者綠色 #EAF3DE/#27500A
- 支援 Dark Mode（使用 CSS 變數或 @media query）

### 3. 任務清單（左右分欄）
左欄：**已完成** ✅
- 每項：`[角色標記] 任務摘要（點擊可查看原始對話鏈接）`
- 最多顯示 6 項，超過折疊

右欄：**需跟進** ⚠️
- 每項：`[角色標記] 待處理任務 + 估計難度`
- 若無需跟進，顯示「本週無待跟進事項 🎉」

### 4. 跨角色機會
每項格式：
```
✨ [來源角色] → [目標角色]
   [具體機會描述]
   → 建議行動：[具體 Skill 或工具]
```

若本週無機會，顯示「本週各角色任務相互獨立，暫無跨角色轉化機會」

### 5. 下週優先任務
排序規則（按重要性降序）：
1. 🔴 高（有截止日 / 碩論進度）
2. 🟡 中（期刊週期 / 教學日程）
3. 🟢 低（開發維護 / 機會性任務）

每項格式：
```
[優先序號]. [任務名稱] [角色標記]
    難易：⬜⬜⬜ | 預估時間：Xh
    建議工具：/[角色指令] + [Skill 名稱]
```

---

## 色彩 CSS 設計（Dark Mode 相容）

```css
/* 角色色系（同 V2 操作手冊） */
.role-ed { background:#EEEDFE; color:#3C3489; }
.role-re { background:#E6F1FB; color:#0C447C; }
.role-te { background:#E1F5EE; color:#085041; }
.role-de { background:#EAF3DE; color:#27500A; }

/* Dark mode */
@media(prefers-color-scheme:dark){
  .role-ed { background:#3C3489; color:#CECBF6; }
  .role-re { background:#0C447C; color:#B5D4F4; }
  .role-te { background:#085041; color:#9FE1CB; }
  .role-de { background:#27500A; color:#C0DD97; }
}

/* 狀態標記 */
.status-done    { color: #3B6D11; }
.status-prog    { color: #854F0B; }
.status-follow  { color: #A32D2D; }
```

---

## loading_messages 建議

```python
loading_messages=[
  "掃描對話紀錄中...",
  "按角色分類任務...",
  "偵測跨角色機會...",
  "生成本週工作盤點..."
]
```

---

## 報告底部固定元素

1. **一鍵觸發下週計畫**：`sendPrompt('請依照週報優先清單，幫我規劃下週一到週五的工作安排')`
2. **執行時間戳記**：「本報告於 YYYY/MM/DD HH:MM 生成」
3. **更新記憶提示**：「確認無誤後，輸入「確認」更新 Claude Memory」
