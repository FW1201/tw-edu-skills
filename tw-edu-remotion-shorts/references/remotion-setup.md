# Remotion 設定

## 建議基準

- 直式短影音預設：`1080 x 1920`
- 預設 FPS：`30`
- 預設編碼：先以常見 web-friendly MP4 流程為主
- 所有時長計算都以 frames 為準

## 第一次使用時的安裝順序

先確認專案是否已經是 Remotion 專案。
若還沒有，先建立專案，再補齊必要套件。

常用套件如下：

- `@remotion/media`：圖片、影片、音訊
- `@remotion/transitions`：轉場
- `@remotion/captions`：字幕資料與 TikTok-style captions
- `@remotion/google-fonts`：Google Fonts
- `@remotion/fonts`：本機字型
- `@remotion/install-whisper-cpp`：音訊轉字幕
- `@remotion/zod-types`：schema 與 color picker

使用時只安裝真的需要的套件，不要一次加過多依賴。

## 常用命令

```bash
npx remotion studio
npx remotion still [composition-id] --frame=30
npx remotion render [composition-id] out/video.mp4
```

## Composition 設定

一個學習動畫至少要固定：

- `id`
- `component`
- `durationInFrames`
- `fps`
- `width`
- `height`

若影片長度會依內容變動，使用 `calculateMetadata` 動態調整。

## 重要參數

### `defaultProps`

用來提供初始內容，方便第一次在 Studio 檢查版面。

### `schema`

用 Zod 管理可調參數，讓使用者可以在 Remotion sidebar 直接改。

### `calculateMetadata`

用來動態取得長度、尺寸或 props。
若有旁白、外部影片或長度依資料而變，優先使用它。

### `Sequence` 與 `TransitionSeries`

- `Sequence` 用來切鏡
- `TransitionSeries` 用來做轉場或疊層效果
- 若使用轉場，總長度要扣掉 overlap

### `staticFile()`

所有本機素材都放在 `public/`，並用 `staticFile()` 取用。

### `useCurrentFrame()` + `interpolate()`

所有動畫都用 frame 驅動，不要用 CSS animation。
需要動態時，先算 frame，再做 easing。

## 排版與字型

- 字型要先確認是否可用，避免 render 時變成 fallback
- 直式短影音不要讓字幕壓到主題字
- 文字區保留安全邊界
- 單行過長就拆成兩行，但不要拆得太碎

## 出圖前檢查

- 內容在 9:16 畫面中是否仍可讀
- 標題與字幕有沒有互相遮擋
- 是否有超出畫面安全區
- 轉場是否影響理解
- 動態是否過多，導致學生看不到重點

