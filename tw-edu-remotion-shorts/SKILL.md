---
name: tw-edu-remotion-shorts
description: >
  以 Remotion 製作 9:16 直式短影音學習動畫的完整流程。
  當使用者需要把教學內容轉成短影音、分鏡、字幕、旁白、動畫流程、影片風格，
  或第一次安裝與設定 Remotion、ElevenLabs、字幕、render 參數時使用。
version: 1.0.0
author: 奇老師・數位敘事力社群
allowed-tools: "Bash, Read, Write, WebSearch"
disable-model-invocation: true
---

# 直式短影音學習動畫工作流

## 核心原則

- 先分析教學內容，再設計畫面。
- 先輸出分鏡，再讓使用者確認。
- 先選視覺風格與動態流程，再開始 Remotion 生成。
- 所有動畫必須以 Remotion frame 驅動，不使用 CSS animation。
- 預設以 9:16 直式短影音為主，優先考慮可讀性、節奏與教學正確性。

## 先讀參考文件

1. [分鏡與選型](references/storyboard-and-selection.md)
2. [Remotion 設定](references/remotion-setup.md)
3. [語音與字幕](references/voiceover-captions.md)

## 工作流程

### 1. 解析教學內容

先整理出以下資訊：

- 教學主題與學習目標
- 受眾年齡與使用平台
- 必須講清楚的概念
- 容易誤解或需要強調的地方
- 是否需要旁白、字幕、示意圖、例題或 CTA
- 預期影片長度與語氣

若資訊不足，先補問最少必要問題，不要直接開始產生畫面。

### 2. 產出分鏡，先讓使用者確認

將教學內容拆成逐鏡分鏡，並用兩種視圖一起呈現：

- 表格總覽：快速檢查鏡號、畫面、文字、旁白、動作、時長、轉場
- 卡片視圖：讓使用者逐鏡選取、重排、刪減、合併

每一鏡至少包含：

- 鏡號
- 目的
- 畫面構圖
- 螢幕文字
- 旁白
- 動態重點
- 預估秒數
- 轉場/銜接方式
- 所需素材
- 風險或注意事項

在使用者確認分鏡前，不進入風格與生成設定。

### 3. 提供 5 種動態流程 + 5 種影片風格

使用「固定選單 + 推薦排序」的方式：

- 先依教學內容推薦最適合的選項
- 再讓使用者確認最終方案
- 若使用者不確定，採預設推薦值

動態流程與影片風格的完整定義請見 [分鏡與選型](references/storyboard-and-selection.md)。

### 4. 補齊 Remotion 生成資訊

開始生成前，確認下列項目：

- 直式比例與輸出尺寸
- FPS 與總時長
- `Composition`
- `defaultProps`
- `schema`
- `calculateMetadata`
- 字型與素材來源
- 字幕來源與同步方式
- 是否需要轉場、疊層、音效、透明背景
- 輸出格式與檔名規則

Remotion 的安裝與常用參數請見 [Remotion 設定](references/remotion-setup.md)。

### 5. 旁白與字幕

預設以 ElevenLabs 作為旁白 API。

- 先引導使用者建立 API key
- 使用環境變數保存 `ELEVENLABS_API_KEY`
- 若需要固定音色，再補 `ELEVENLABS_VOICE_ID`
- 若需要指定模型，再補 `ELEVENLABS_MODEL_ID`

若有旁白，就要同步檢查字幕切分、字幕行長、閱讀速度與安全邊界。
具體流程請見 [語音與字幕](references/voiceover-captions.md)。

### 6. render 前檢查

開始 render 前，至少確認：

- 教學內容是否正確
- 分鏡是否完整
- 畫面是否遮到關鍵資訊
- 字幕是否可讀
- 動態是否過強或過弱
- 旁白與鏡頭節奏是否一致
- 是否符合目標平台的觀看習慣

## 遇到第一次使用者時的處理順序

1. 先確認有沒有現成 Remotion 專案
2. 若沒有，先引導建立專案與必要套件
3. 再引導 ElevenLabs API key 與 voice 設定
4. 接著產出分鏡
5. 等使用者確認後，才進入風格、動態與 render 設定

## 輸出標準

- 分鏡要能讓人直接拿去做動畫
- 每個鏡頭都要有明確教學作用
- 字幕不能壓過內容重點
- 動態只能服務理解，不可搶走資訊
- 最終結果要能直接落到 Remotion 專案

