# ICS 行事曆檔案格式（無 Calendar MCP 時的降級方案）

## 標準 .ics 格式
```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//tw-edu-skills//meeting-facilitator//TW
BEGIN:VEVENT
UID:{uuid}@tw-edu-skills
DTSTAMP:{YYYYMMDDTHHMMSSZ}
DTSTART;TZID=Asia/Taipei:{YYYYMMDDTHHMMSS}
DTEND;TZID=Asia/Taipei:{YYYYMMDDTHHMMSS}
SUMMARY:{會議類型} — {主題}
LOCATION:{地點}
DESCRIPTION:{議程摘要}
BEGIN:VALARM
TRIGGER:-PT15M
ACTION:DISPLAY
DESCRIPTION:會議即將開始
END:VALARM
BEGIN:VALARM
TRIGGER:-P1D
ACTION:EMAIL
DESCRIPTION:明天有 {會議類型}
END:VALARM
END:VEVENT
END:VCALENDAR
```

## 生成方式
```python
import uuid
from datetime import datetime

uid = str(uuid.uuid4())
stamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
# 輸出為 meeting_[date].ics 供使用者匯入
```
