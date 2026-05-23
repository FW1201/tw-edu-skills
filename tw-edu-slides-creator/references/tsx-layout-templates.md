# TSX Layout Templates（open-slide v2.0）

畫布尺寸：1920×1080px（固定，open-slide 自動縮放）
基準主題：Edu Warm ｜ 基準年級：國中
字型基準：標題 72px ｜ 副標 52px ｜ 內文 40px ｜ 說明 32px

其他年級字型對照見 `tailwind-themes.md`。

---

## 01. cover（封面）

```tsx
// slides/01-cover/index.tsx
import type { Page } from '@open-slide/core';

const Cover: Page = () => (
  <div className="relative flex h-full w-full flex-col items-center justify-center bg-[#fffbf5]">
    <div className="absolute inset-x-0 bottom-0 h-3 bg-[#d97757]" />
    <span className="mb-4 text-[32px] font-medium tracking-widest text-[#987b63] uppercase">
      七年級國文
    </span>
    <h1 className="text-center text-[72px] font-bold leading-tight text-[#2d1a0e] max-w-[1400px]">
      課程標題
    </h1>
    <p className="mt-8 text-[40px] text-[#987b63]">吳老師 ｜ 2026/05/23</p>
  </div>
);

export default [Cover];
export const meta = { title: '01 封面' };
```

---

## 02. objectives（學習目標）

```tsx
// slides/02-objectives/index.tsx
import type { Page } from '@open-slide/core';

const Objectives: Page = () => (
  <div className="flex h-full w-full flex-col bg-[#fffbf5] px-24 py-16">
    <h2 className="mb-12 border-b-4 border-[#d97757] pb-4 text-[52px] font-bold text-[#2d1a0e]">
      學習目標
    </h2>
    <div className="grid grid-cols-3 gap-8">
      {[
        { tag: '認知', content: '了解...' },
        { tag: '情意', content: '體會...' },
        { tag: '技能', content: '能夠...' },
      ].map(({ tag, content }, i) => (
        <div key={i} className="rounded-2xl bg-[#f5ede0] p-10 border border-[#e8d5bf]">
          <span className="mb-4 inline-block rounded-full bg-[#d97757] px-6 py-2 text-[28px] font-bold text-white">
            {tag}
          </span>
          <p className="mt-4 text-[36px] leading-relaxed text-[#2d1a0e]">{content}</p>
        </div>
      ))}
    </div>
  </div>
);

export default [Objectives];
export const meta = { title: '02 學習目標' };
```

---

## 03. section（章節分隔）

```tsx
// slides/03-section/index.tsx
import type { Page } from '@open-slide/core';

const Section: Page = () => (
  <div className="relative flex h-full w-full flex-col items-center justify-center bg-[#d97757]">
    <span className="absolute text-[320px] font-black text-white opacity-10 select-none leading-none">
      1
    </span>
    <span className="mb-6 text-[40px] font-medium uppercase tracking-widest text-white opacity-80">
      Chapter 01
    </span>
    <h2 className="text-[80px] font-bold text-white">章節名稱</h2>
  </div>
);

export default [Section];
export const meta = { title: '03 章節' };
```

---

## 04. bullets（條列重點）

```tsx
// slides/04-bullets/index.tsx
import type { Page } from '@open-slide/core';

const Bullets: Page = () => (
  <div className="flex h-full w-full flex-col bg-[#fffbf5] px-24 py-20">
    <h2 className="mb-12 border-b-4 border-[#d97757] pb-4 text-[52px] font-bold text-[#2d1a0e]">
      核心重點
    </h2>
    <ul className="flex flex-col gap-8">
      {['重點一：...', '重點二：...', '重點三：...', '重點四：...', '重點五：...'].map((item, i) => (
        <li key={i} className="flex items-start gap-6 text-[40px] text-[#2d1a0e]">
          <span className="mt-3 h-5 w-5 shrink-0 rounded-full bg-[#d97757]" />
          <span>{item}</span>
        </li>
      ))}
    </ul>
  </div>
);

export default [Bullets];
export const meta = { title: '04 條列重點' };
```

---

## 05. two-column（雙欄對比）

```tsx
// slides/05-two-column/index.tsx
import type { Page } from '@open-slide/core';

const TwoColumn: Page = () => (
  <div className="flex h-full w-full flex-col bg-[#fffbf5] px-24 py-16">
    <h2 className="mb-10 text-[52px] font-bold text-[#2d1a0e]">對比分析</h2>
    <div className="grid flex-1 grid-cols-2 gap-12">
      {[
        { title: '左欄標題', items: ['項目 A', '項目 B', '項目 C'] },
        { title: '右欄標題', items: ['項目 X', '項目 Y', '項目 Z'] },
      ].map(({ title, items }, i) => (
        <div key={i} className="rounded-2xl bg-[#f5ede0] p-10">
          <h3 className="mb-6 text-[40px] font-bold uppercase tracking-wide text-[#d97757]">
            {title}
          </h3>
          <ul className="flex flex-col gap-4">
            {items.map((item, j) => (
              <li key={j} className="text-[36px] text-[#2d1a0e]">▸ {item}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  </div>
);

export default [TwoColumn];
export const meta = { title: '05 雙欄對比' };
```

---

## 06. vocab（詞彙卡）

```tsx
// slides/06-vocab/index.tsx
import type { Page } from '@open-slide/core';

const Vocab: Page = () => (
  <div className="flex h-full w-full flex-col bg-[#fffbf5] px-24 py-16">
    <h2 className="mb-10 text-[52px] font-bold text-[#2d1a0e]">詞彙學習</h2>
    <div className="grid flex-1 grid-cols-3 gap-8">
      {[
        { word: '詞彙一', zhuyin: 'ㄘˊˊ', example: '造句範例...' },
        { word: '詞彙二', zhuyin: 'ㄘˊˊ', example: '造句範例...' },
        { word: '詞彙三', zhuyin: 'ㄘˊˊ', example: '造句範例...' },
        { word: '詞彙四', zhuyin: 'ㄘˊˊ', example: '造句範例...' },
        { word: '詞彙五', zhuyin: 'ㄘˊˊ', example: '造句範例...' },
        { word: '詞彙六', zhuyin: 'ㄘˊˊ', example: '造句範例...' },
      ].map(({ word, zhuyin, example }, i) => (
        <div key={i} className="rounded-2xl border border-[#e8d5bf] bg-[#f5ede0] p-8">
          <div className="mb-2 text-[48px] font-bold text-[#2d1a0e]">{word}</div>
          <div className="mb-4 text-[32px] text-[#987b63]">{zhuyin}</div>
          <p className="text-[28px] leading-relaxed text-[#987b63]">{example}</p>
        </div>
      ))}
    </div>
  </div>
);

export default [Vocab];
export const meta = { title: '06 詞彙學習' };
```

---

## 07. activity（課堂活動）

```tsx
// slides/07-activity/index.tsx
import type { Page } from '@open-slide/core';

const Activity: Page = () => (
  <div className="flex h-full w-full flex-col bg-[#fffbf5] px-24 py-16">
    <div className="mb-10 flex items-center gap-6">
      <h2 className="text-[52px] font-bold text-[#2d1a0e]">課堂活動</h2>
      <span className="rounded-full bg-[#6a9bcc] px-6 py-2 text-[28px] text-white">⏱ 10 分鐘</span>
      <span className="rounded-full border border-[#e8d5bf] bg-[#f5ede0] px-6 py-2 text-[28px] text-[#987b63]">
        👥 小組
      </span>
    </div>
    <ol className="flex flex-col gap-7">
      {['步驟一：...', '步驟二：...', '步驟三：...', '步驟四：...'].map((step, i) => (
        <li key={i} className="flex items-start gap-8">
          <span className="flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-[#d97757] text-[32px] font-bold text-white">
            {i + 1}
          </span>
          <span className="pt-1 text-[40px] text-[#2d1a0e]">{step}</span>
        </li>
      ))}
    </ol>
  </div>
);

export default [Activity];
export const meta = { title: '07 課堂活動' };
```

---

## 08. discussion（討論提示）

```tsx
// slides/08-discussion/index.tsx
import type { Page } from '@open-slide/core';

const Discussion: Page = () => (
  <div className="flex h-full w-full flex-col items-center justify-center bg-[#fffbf5] px-24">
    <span className="mb-8 rounded-full border-2 border-[#d97757] px-8 py-3 text-[32px] font-medium text-[#d97757]">
      ⏱ 3 分鐘思考
    </span>
    <h2 className="mb-10 text-center text-[64px] font-bold leading-tight text-[#2d1a0e] max-w-[1400px]">
      討論主題或問題
    </h2>
    <p className="text-center text-[40px] leading-relaxed text-[#987b63] max-w-[1200px]">
      提示：可以從...角度思考
    </p>
  </div>
);

export default [Discussion];
export const meta = { title: '08 討論提示' };
```

---

## 09. hero（大字強調）

```tsx
// slides/09-hero/index.tsx
import type { Page } from '@open-slide/core';

const Hero: Page = () => (
  <div className="flex h-full w-full flex-col items-center justify-center bg-[#d97757] px-24">
    <div className="mb-6 h-2 w-24 bg-white opacity-60" />
    <h1 className="text-center text-[96px] font-black leading-tight text-white max-w-[1600px]">
      核心訊息
    </h1>
    <p className="mt-10 text-center text-[44px] text-white opacity-80">補充說明文字</p>
    <div className="mt-6 h-2 w-24 bg-white opacity-60" />
  </div>
);

export default [Hero];
export const meta = { title: '09 核心訊息' };
```

---

## 10. data（數據展示）

```tsx
// slides/10-data/index.tsx
import type { Page } from '@open-slide/core';

const Data: Page = () => (
  <div className="flex h-full w-full flex-col bg-[#fffbf5] px-24 py-16">
    <h2 className="mb-12 text-[52px] font-bold text-[#2d1a0e]">數據一覽</h2>
    <div className="grid flex-1 grid-cols-4 gap-8">
      {[
        { value: '87%', label: '指標一', desc: '說明文字' },
        { value: '1,234', label: '指標二', desc: '說明文字' },
        { value: '3.8x', label: '指標三', desc: '說明文字' },
        { value: 'Top 5', label: '指標四', desc: '說明文字' },
      ].map(({ value, label, desc }, i) => (
        <div
          key={i}
          className="flex flex-col items-center justify-center rounded-2xl border border-[#e8d5bf] bg-[#f5ede0] p-10 text-center"
        >
          <div className="text-[72px] font-black text-[#d97757]">{value}</div>
          <div className="mt-3 text-[36px] font-bold text-[#2d1a0e]">{label}</div>
          <div className="mt-2 text-[28px] text-[#987b63]">{desc}</div>
        </div>
      ))}
    </div>
  </div>
);

export default [Data];
export const meta = { title: '10 數據展示' };
```

---

## 11. summary（重點摘要）

```tsx
// slides/11-summary/index.tsx
import type { Page } from '@open-slide/core';

const Summary: Page = () => (
  <div className="flex h-full w-full flex-col bg-[#fffbf5] px-24 py-16">
    <h2 className="mb-10 text-[52px] font-bold text-[#2d1a0e]">重點回顧</h2>
    <div className="flex flex-col gap-6">
      {[
        { key: '重點一', value: '...' },
        { key: '重點二', value: '...' },
        { key: '重點三', value: '...' },
        { key: '重點四', value: '...' },
      ].map(({ key, value }, i) => (
        <div
          key={i}
          className={`flex items-start gap-8 rounded-xl p-6 ${
            i % 2 === 0 ? 'bg-[#f5ede0]' : 'border border-[#e8d5bf] bg-white'
          }`}
        >
          <span className="w-48 shrink-0 text-[36px] font-bold text-[#d97757]">{key}</span>
          <span className="text-[36px] text-[#2d1a0e]">{value}</span>
        </div>
      ))}
    </div>
  </div>
);

export default [Summary];
export const meta = { title: '11 重點回顧' };
```

---

## 12. timeline（時間軸）

```tsx
// slides/12-timeline/index.tsx
import type { Page } from '@open-slide/core';

const Timeline: Page = () => (
  <div className="flex h-full w-full flex-col bg-[#fffbf5] px-24 py-16">
    <h2 className="mb-12 text-[52px] font-bold text-[#2d1a0e]">時間軸</h2>
    <div className="relative flex flex-1 flex-col justify-around pl-20">
      <div className="absolute left-6 top-0 bottom-0 w-1 bg-[#e8d5bf]" />
      {[
        { year: '1895', event: '事件一說明' },
        { year: '1945', event: '事件二說明' },
        { year: '1949', event: '事件三說明' },
        { year: '1987', event: '事件四說明' },
      ].map(({ year, event }, i) => (
        <div key={i} className="relative flex items-center gap-8">
          <div className="absolute -left-[58px] h-7 w-7 rounded-full border-4 border-[#fffbf5] bg-[#d97757]" />
          <span className="w-36 text-[36px] font-bold text-[#d97757]">{year}</span>
          <span className="text-[40px] text-[#2d1a0e]">{event}</span>
        </div>
      ))}
    </div>
  </div>
);

export default [Timeline];
export const meta = { title: '12 時間軸' };
```

---

## 13. quote（名言引用）

```tsx
// slides/13-quote/index.tsx
import type { Page } from '@open-slide/core';

const Quote: Page = () => (
  <div className="flex h-full w-full flex-col items-center justify-center bg-[#fffbf5] px-32">
    <span className="mb-4 text-[160px] font-black leading-none text-[#d97757] opacity-20 select-none">
      "
    </span>
    <blockquote className="-mt-16 text-center text-[56px] font-medium leading-relaxed text-[#2d1a0e] max-w-[1400px]">
      名言或精華語句放在這裡
    </blockquote>
    <cite className="mt-10 text-[36px] not-italic text-[#987b63]">
      — 作者名，《出處》
    </cite>
  </div>
);

export default [Quote];
export const meta = { title: '13 名言引用' };
```

---

## 14. three-column（三欄卡片）

```tsx
// slides/14-three-column/index.tsx
import type { Page } from '@open-slide/core';

const ThreeColumn: Page = () => (
  <div className="flex h-full w-full flex-col bg-[#fffbf5] px-24 py-16">
    <h2 className="mb-10 text-[52px] font-bold text-[#2d1a0e]">三欄比較</h2>
    <div className="grid flex-1 grid-cols-3 gap-8">
      {[
        { icon: '🔵', title: '欄位一', body: '說明文字...' },
        { icon: '🟠', title: '欄位二', body: '說明文字...' },
        { icon: '🟢', title: '欄位三', body: '說明文字...' },
      ].map(({ icon, title, body }, i) => (
        <div
          key={i}
          className="flex flex-col rounded-2xl border-t-8 border-[#d97757] bg-[#f5ede0] p-10"
        >
          <span className="mb-4 text-[60px]">{icon}</span>
          <h3 className="mb-4 text-[44px] font-bold text-[#2d1a0e]">{title}</h3>
          <p className="text-[36px] leading-relaxed text-[#987b63]">{body}</p>
        </div>
      ))}
    </div>
  </div>
);

export default [ThreeColumn];
export const meta = { title: '14 三欄卡片' };
```

---

## 15. image-hero（圖文分割）

```tsx
// slides/15-image-hero/index.tsx
import type { Page } from '@open-slide/core';

const ImageHero: Page = () => (
  <div className="flex h-full w-full bg-[#fffbf5]">
    {/* 圖片區（65%）*/}
    <div className="flex w-[65%] items-center justify-center border-r-4 border-[#e8d5bf] bg-[#f5ede0]">
      <div className="flex h-[600px] w-[1000px] items-center justify-center rounded-2xl border-4 border-dashed border-[#d97757]">
        <div className="text-center">
          <p className="text-[56px] text-[#d97757]">📷</p>
          <p className="mt-2 text-[36px] text-[#987b63]">在此插入圖片</p>
          <p className="mt-1 text-[28px] text-[#987b63]">建議尺寸 1000×600px</p>
        </div>
      </div>
    </div>
    {/* 說明區（35%）*/}
    <div className="flex w-[35%] flex-col justify-center px-16">
      <h2 className="mb-8 text-[52px] font-bold text-[#2d1a0e]">圖片標題</h2>
      <p className="text-[36px] leading-relaxed text-[#987b63]">
        圖片說明或補充資訊，可以寫 2-3 句話。
      </p>
      <div className="mt-8 h-1 w-16 bg-[#d97757]" />
      <p className="mt-4 text-[28px] text-[#987b63]">資料來源：...</p>
    </div>
  </div>
);

export default [ImageHero];
export const meta = { title: '15 圖文分割' };
```

---

## 16. pros-cons（優缺點分析）

```tsx
// slides/16-pros-cons/index.tsx
import type { Page } from '@open-slide/core';

const ProsCons: Page = () => (
  <div className="flex h-full w-full flex-col bg-[#fffbf5] px-24 py-16">
    <h2 className="mb-10 text-[52px] font-bold text-[#2d1a0e]">優缺點分析</h2>
    <div className="grid flex-1 grid-cols-[1fr_4px_1fr]">
      {/* 優點 */}
      <div className="pr-12">
        <h3 className="mb-8 text-[44px] font-bold text-[#4caf50]">◆ 優點</h3>
        <ul className="flex flex-col gap-6">
          {['優點一：...', '優點二：...', '優點三：...'].map((item, i) => (
            <li key={i} className="flex items-start gap-4 text-[36px] text-[#2d1a0e]">
              <span className="mt-1 shrink-0 text-[#4caf50]">+</span>
              <span>{item}</span>
            </li>
          ))}
        </ul>
      </div>
      {/* 分隔線 */}
      <div className="bg-[#e8d5bf]" />
      {/* 缺點 */}
      <div className="pl-12">
        <h3 className="mb-8 text-[44px] font-bold text-[#e53935]">▼ 缺點</h3>
        <ul className="flex flex-col gap-6">
          {['缺點一：...', '缺點二：...', '缺點三：...'].map((item, i) => (
            <li key={i} className="flex items-start gap-4 text-[36px] text-[#2d1a0e]">
              <span className="mt-1 shrink-0 text-[#e53935]">−</span>
              <span>{item}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  </div>
);

export default [ProsCons];
export const meta = { title: '16 優缺點分析' };
```

---

## 17. checklist（學習自評）

```tsx
// slides/17-checklist/index.tsx
import type { Page } from '@open-slide/core';

const Checklist: Page = () => (
  <div className="flex h-full w-full flex-col bg-[#fffbf5] px-24 py-16">
    <h2 className="mb-10 text-[52px] font-bold text-[#2d1a0e]">學習自評</h2>
    <ul className="flex flex-col gap-7">
      {[
        '我能說明...',
        '我能舉例...',
        '我能應用...',
        '我能分析...',
        '我能評估...',
      ].map((item, i) => (
        <li key={i} className="flex items-center gap-8 rounded-xl p-4">
          <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-md border-[3px] border-[#d97757]" />
          <span className="text-[40px] text-[#2d1a0e]">{item}</span>
        </li>
      ))}
    </ul>
    <p className="mt-8 text-[32px] text-[#987b63]">
      📝 完成自評後與同學分享一項最有收穫的地方
    </p>
  </div>
);

export default [Checklist];
export const meta = { title: '17 學習自評' };
```
