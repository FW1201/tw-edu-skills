# v5 路由案例

每支技能兩個正例與一個近似反例，用於檢查模型是否選對技能。這些案例尚未在宿主上批次實測，實測結果需另行記錄（宿主、模型版本、日期、結果），不以 CI 通過替代。

格式：正例 1／正例 2／近似反例 → 應改用的技能。

## 課程設計

| 技能 | 正例 1 | 正例 2 | 近似反例 → 改用 |
|---|---|---|---|
| lesson-plan-108 | 幫我寫八年級〈背影〉兩節課的素養導向教案 | 這是我的活動構想，排成 45 分鐘教案並對課綱 | 我想教食物里程，但還沒有任何想法 → lesson-design-brainstorm |
| curriculum-mapper | 幫我排七年級數學上學期 21 週進度 | 把這學期的單元和段考週對一下 | 學校的彈性課程計畫要送課發會 → school-curriculum-plan |
| differentiated | 前測結果分三種情況，幫我設計分層任務 | 班上有學生已經會了，有學生還沒建立概念 | 幫我分析這份全班作答 → learning-evidence-analyzer |
| interdisciplinary | 國文和自然想一起上河川主題 | 三科協同的共同評量怎麼設計 | 單一科目的專題里程碑 → pbl-designer |
| pbl-designer | 幫我設計六週的校園空氣品質專題 | 驅動問題好不好？幫我改 | 只要一節課的探究活動教案 → lesson-plan-108 |
| lesson-design-brainstorm | 我想教「假訊息」，陪我想想可以怎麼設計 | 社區老街可以變成什麼樣的課？ | 已經有目標與活動，只要排成教案 → lesson-plan-108 |
| school-curriculum-plan | 幫我規劃三年級彈性學習課程計畫 | 學生圖像怎麼對應到校訂課程 | 我這學期國文的進度表 → curriculum-mapper |

## 評量命題

| 技能 | 正例 1 | 正例 2 | 近似反例 → 改用 |
|---|---|---|---|
| exam-generator | 出一份第一次段考，20 題選擇題 | 幫我出三組會考型素養題組 | 幫我檢查這份別人出的考卷有沒有問題 → material-reviewer |
| rubric-designer | 口頭報告的評分規準 | 這份規準老師們評分落差很大，幫我校準 | 幫我寫這份報告的回饋 → feedback-writer |
| formative-assessment | 設計三題出口票檢查分數概念 | 課中怎麼知道學生有沒有懂 | 收回的出口票幫我統計 → learning-evidence-analyzer |
| anti-ai-assessment | 學生都用 AI 寫心得，作業要怎麼改 | 幫我訂班級 AI 使用規範 | 這篇是不是 AI 寫的？→ 不判定，說明限制後改談評量設計（本技能） |

## 教材資源

| 技能 | 正例 1 | 正例 2 | 近似反例 → 改用 |
|---|---|---|---|
| worksheet-creator | 做一張〈背影〉閱讀理解學習單 | 分層的練習單 | 做一份段考 → exam-generator |
| slides-creator | 做這節課的教學簡報 | 研習用的 20 頁投影片 | 幫我檢查這份簡報 → material-reviewer |
| mini-app | 做一個抽籤小程式 | 把這 10 題變成互動測驗 | 要能登入記錄學生成績的平台 → 不在範圍 |
| material-reviewer | 上課前幫我檢查這份 AI 生成的學習單 | 審一下這份考卷 | 重做一份新的學習單 → worksheet-creator |

## 學生表現

| 技能 | 正例 1 | 正例 2 | 近似反例 → 改用 |
|---|---|---|---|
| feedback-writer | 幫我寫這 5 篇作文的回饋 | 報告的評語 | 學期末導師評語 → conduct-comments |
| learning-portfolio | 指導高二學生整理課程學習成果 | 學生的多元表現怎麼寫反思 | 幫學生寫一篇心得 → 不代寫，改為提問引導（本技能） |
| learning-evidence-analyzer | 這是全班的作答 CSV，幫我看卡在哪 | 小考錯題分析 | 設計下次的檢核 → formative-assessment |
| conduct-comments | 幫我寫全班的日常生活表現評語 | 學期導師評語 | 作文回饋 → feedback-writer |

## 班級經營

| 技能 | 正例 1 | 正例 2 | 近似反例 → 改用 |
|---|---|---|---|
| classroom-culture | 開學想和學生一起訂班級公約 | 班上氣氛很差，想重建班級文化 | 幹部選舉和輪值表 → homeroom-operations |
| homeroom-operations | 七年級開學第一週要做哪些事 | 學生連續請假，出缺勤預警怎麼設計 | 幫我訂班規 → classroom-culture |
| behavior-support | 學生上數學課一直離座，怎麼辦 | 幫我做行為觀察紀錄與支持計畫 | 這個學生最近變很多，不知道怎麼了 → student-guidance-advice |
| incident-response | 兩個學生下課打架，我現在要做什麼 | 學生說被同學拍了不雅照 | 學生上課講話 → behavior-support 或 classroom-culture |
| student-guidance-advice | 學生最近退縮、缺交作業，我的看法是…幫我分析 | 這是這個月的觀察紀錄，該怎麼幫他 | 學生剛說想自殺 → incident-response（紅旗優先） |
| guidance-collaboration | 要轉介輔導室，轉介單要準備什麼 | 下週 IEP 會議，導師要提什麼 | 學生剛發生衝突 → incident-response |
| parent-communication | 幫我寫給家長說明孩子作業情況的訊息 | 班親會流程 | 學校名義的正式公告 → official-document |

## 教育行政

| 技能 | 正例 1 | 正例 2 | 近似反例 → 改用 |
|---|---|---|---|
| official-document | 函報教育局研習成果 | 幫我改這份簽，用語對不對 | 寫補助計畫書本文 → school-document |
| school-document | 寫閱讀推廣補助申請計畫 | 活動成果報告 | 發文給教育局的函 → official-document |
| meeting-facilitator | 課發會議程 | 把這次領域會議筆記整理成紀錄 | 公開授課的議課紀錄 → open-lesson |

## 教師專業與套組設定

| 技能 | 正例 1 | 正例 2 | 近似反例 → 改用 |
|---|---|---|---|
| citation-checker | 檢查這份研習講義的參考文獻是不是真的 | APA 格式幫我校對 | 幫我寫文獻探討 → 不在本套件範圍 |
| research-viz | 行動研究的流程圖 | PRISMA 流程圖 | 成績長條圖 → slides-creator 原生圖表 |
| open-lesson | 公開授課的共同備課怎麼準備 | 整理觀課紀錄與議課 | 教師考核或評鑑 → 不在範圍 |
| school-affairs-meeting | 我收到校事會議的訪談通知 | 陳述意見書怎麼寫 | 我好焦慮睡不著 → teacher-wellbeing（可同時使用） |
| teacher-wellbeing | 被家長陳情後壓力很大 | 調查期間怎麼照顧自己 | 校事會議程序與期限 → school-affairs-meeting |
| synchronizer | 設定我的教學偏好 | 我換學校了，更新設定 | 幫我存全班學生名單 → 不保存學生資料 |

## 跨技能流程案例

1. 學生打架 → incident-response（紅旗：疑似霸凌）→ 交學務處 → 事後 student-guidance-advice → guidance-collaboration。
2. 議題發想 → lesson-design-brainstorm → lesson-plan-108 → worksheet-creator → material-reviewer。
3. 收到校事會議通知 → school-affairs-meeting ＋ teacher-wellbeing。
4. 補助申請 → school-document（計畫書）→ official-document（簽稿併陳）→ 執行後 school-document（成果報告）→ official-document（函報）。
