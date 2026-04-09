# 研究計畫書 .docx 輸出格式規格
# DOCX Output Specification for Research Proposal

本指引說明如何將 Phase 4 生成的 Markdown 草稿，
輸出為符合台灣學術規範的 Word (.docx) 文件。

---

## 格式規格

### 頁面設定（A4）

```javascript
properties: {
  page: {
    size: {
      width: 11906,   // A4 寬度（DXA）
      height: 16838   // A4 高度（DXA）
    },
    margin: {
      top: 1701,    // 3cm ≈ 1701 DXA
      bottom: 1134, // 2cm ≈ 1134 DXA
      left: 1701,   // 3cm
      right: 1701   // 3cm
    }
  }
}
```

### 字型規格

| 元素 | 中文字型 | 英文字型 | 大小 |
|------|---------|---------|------|
| 正文 | 標楷體 (DFKai-SB) 或 新細明體 | Times New Roman | 12pt (24 half-points) |
| 標題1 | 標楷體 Bold | Times New Roman Bold | 16pt (32 half-points) |
| 標題2 | 標楷體 Bold | Times New Roman Bold | 14pt (28 half-points) |
| 標題3 | 標楷體 | Times New Roman | 12pt Bold |
| 封面標題 | 標楷體 Bold | Times New Roman Bold | 18pt (36 half-points) |

**注意**：Claude 環境中可用字型為 Arial（英文），中文若無標楷體可用 Arial 替代，
並在文件中加入注釋說明使用者需自行更換中文字型。

### 行距

```javascript
spacing: {
  line: 360,      // 1.5倍行距（240 = single, 480 = double）
  lineRule: "auto"
}
```

### 頁碼設定

```javascript
// 頁碼置於頁面下方正中央
footers: {
  default: new Footer({
    children: [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun("- "),
          new TextRun({ children: [PageNumber.CURRENT] }),
          new TextRun(" -")
        ]
      })
    ]
  })
}
```

---

## 文件結構程式骨架

```javascript
const { Document, Packer, Paragraph, TextRun, HeadingLevel,
        AlignmentType, PageBreak, Footer, PageNumber,
        LevelFormat, BorderStyle, WidthType, Table, TableRow,
        TableCell, ShadingType } = require('docx');
const fs = require('fs');

// 台灣學術格式樣式設定
const academicStyles = {
  default: {
    document: {
      run: {
        font: "Arial",  // 替代中文字型，提示使用者手動更換
        size: 24,       // 12pt
        color: "000000"
      },
      paragraph: {
        spacing: { line: 360, lineRule: "auto" },
        alignment: AlignmentType.JUSTIFIED
      }
    }
  },
  paragraphStyles: [
    {
      id: "Heading1",
      name: "Heading 1",
      basedOn: "Normal",
      quickFormat: true,
      run: { size: 32, bold: true, font: "Arial" },
      paragraph: {
        spacing: { before: 360, after: 240 },
        outlineLevel: 0,
        alignment: AlignmentType.LEFT
      }
    },
    {
      id: "Heading2",
      name: "Heading 2",
      basedOn: "Normal",
      quickFormat: true,
      run: { size: 28, bold: true, font: "Arial" },
      paragraph: {
        spacing: { before: 240, after: 180 },
        outlineLevel: 1
      }
    },
    {
      id: "Heading3",
      name: "Heading 3",
      basedOn: "Normal",
      quickFormat: true,
      run: { size: 24, bold: true, font: "Arial" },
      paragraph: {
        spacing: { before: 180, after: 120 },
        outlineLevel: 2
      }
    }
  ]
};

// 封面頁生成函數
function createCoverPage(metadata) {
  return [
    new Paragraph({ spacing: { before: 2880 }, children: [] }), // 頂部空白
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: metadata.institution, size: 28, bold: true })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: metadata.department, size: 24 })]
    }),
    new Paragraph({ spacing: { before: 1440 }, children: [] }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: "研究計畫書", size: 36, bold: true })]
    }),
    new Paragraph({ spacing: { before: 1440 }, children: [] }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: `計畫題目：${metadata.titleChinese}`, size: 28, bold: true })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: metadata.titleEnglish, size: 24 })]
    }),
    new Paragraph({ spacing: { before: 1440 }, children: [] }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: `申請人：${metadata.applicant}`, size: 24 })]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: `${new Date().getFullYear()} 年 ${new Date().getMonth()+1} 月`, size: 24 })]
    }),
    new Paragraph({
      children: [new PageBreak()]
    })
  ];
}
```

---

## 快速生成流程

Phase 4 完成後，執行以下步驟：

### Step 1：安裝依賴

```bash
npm install -g docx
```

### Step 2：建立 Node.js 腳本

將 Markdown 草稿轉換為 docx-js 物件結構，
主要對應關係：

| Markdown | docx-js |
|----------|---------|
| `# 標題` | `HeadingLevel.HEADING_1` |
| `## 標題` | `HeadingLevel.HEADING_2` |
| `### 標題` | `HeadingLevel.HEADING_3` |
| 一般段落 | `new Paragraph({ children: [new TextRun(text)] })` |
| `- 清單` | `numbering: { reference: "bullets", level: 0 }` |
| `1. 編號` | `numbering: { reference: "numbers", level: 0 }` |
| `表格` | `new Table(...)` |
| 空行 | `new Paragraph({ children: [] })` |

### Step 3：驗證並輸出

```bash
python /mnt/skills/public/docx/scripts/office/validate.py research_proposal.docx
```

### Step 4：複製到輸出目錄

```bash
cp /home/claude/research_proposal.docx /mnt/user-data/outputs/research_proposal.docx
```

---

## 文件完成後提示語

```
✅ 您的研究計畫書已生成！

📄 檔案名稱：research_proposal.docx

⚠️ 使用前請注意：
1. 請在 Word 中將字型更換為「標楷體」（中文）
2. 請確認 APA 格式引用是否符合所屬學校規範
3. 請依指導教授或審查委員意見進行修改
4. 若需要 IRB 倫理審查，請提早申請

祝您研究順利！🎓
```
