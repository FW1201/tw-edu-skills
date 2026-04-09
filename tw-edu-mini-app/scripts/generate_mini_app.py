#!/usr/bin/env python3
"""教學小程式 HTML 生成腳本"""
import argparse, json, sys
from pathlib import Path

GRADE_SPECS = {
    'elementary': {'title': '2.8rem', 'body': '1.6rem', 'btn': '1.4rem', 'padding': '20px'},
    'junior':     {'title': '2.2rem', 'body': '1.2rem', 'btn': '1.1rem', 'padding': '16px'},
    'senior':     {'title': '1.8rem', 'body': '1rem',   'btn': '0.95rem','padding': '14px'},
}

def get_stage(grade):
    if any(x in grade for x in ['國小','低年級','一年','二年','三年','四年','五年','六年']): return 'elementary'
    if any(x in grade for x in ['國中','七','八','九']): return 'junior'
    return 'senior'

# ──────── 互動測驗（Quiz）────────
QUIZ_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  :root {{
    --blue: #1A5276; --mid: #2471A3; --light: #EBF5FB;
    --green: #1E8449; --orange: #CA6F1E; --gold: #D4AC0D;
    --text: #1C2A35; --bg: #F8F9FA;
    --title: {title_size}; --body: {body_size}; --btn: {btn_size}; --pad: {padding};
  }}
  body {{ font-family: 'Microsoft JhengHei', 'Noto Sans TC', sans-serif;
          background: var(--bg); color: var(--text); min-height: 100vh;
          display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }}
  .quiz-card {{ background: white; border-radius: 16px; padding: 32px;
                max-width: 700px; width: 100%; box-shadow: 0 4px 24px rgba(26,82,118,0.12); }}
  .quiz-header {{ background: var(--blue); color: white; padding: 16px 20px;
                  border-radius: 10px; margin-bottom: 24px; text-align: center; }}
  .quiz-header h1 {{ font-size: var(--title); font-weight: 700; }}
  .quiz-header p {{ font-size: calc(var(--body) - 0.1rem); opacity: 0.85; margin-top: 4px; }}
  .progress-bar {{ background: var(--light); border-radius: 8px; height: 10px; margin-bottom: 20px; }}
  .progress-fill {{ background: linear-gradient(90deg, var(--mid), var(--gold));
                    height: 100%; border-radius: 8px; transition: width 0.4s; }}
  .progress-text {{ text-align: right; font-size: 0.85rem; color: #666; margin-bottom: 16px; }}
  .question {{ font-size: var(--body); font-weight: 600; color: var(--blue);
               line-height: 1.6; margin-bottom: 24px; padding: 16px;
               background: var(--light); border-radius: 10px; border-left: 4px solid var(--mid); }}
  .options {{ display: grid; gap: 12px; }}
  .option-btn {{ background: white; border: 2px solid #D0DCE8; border-radius: 10px;
                 padding: var(--pad); font-size: var(--btn); cursor: pointer;
                 text-align: left; transition: all 0.2s; color: var(--text); font-family: inherit; }}
  .option-btn:hover:not(:disabled) {{ border-color: var(--mid); background: var(--light); transform: translateX(4px); }}
  .option-btn.correct {{ background: #EAFAF1; border-color: var(--green); color: var(--green); font-weight: 600; }}
  .option-btn.wrong  {{ background: #FDEDEC; border-color: #E74C3C; color: #C0392B; }}
  .feedback {{ padding: 16px; border-radius: 10px; margin-top: 16px; font-size: var(--body);
               display: none; line-height: 1.5; }}
  .feedback.correct {{ background: #EAFAF1; color: #1E8449; border: 1px solid #A9DFBF; }}
  .feedback.wrong   {{ background: #FDEDEC; color: #C0392B; border: 1px solid #F5B7B1; }}
  .next-btn {{ margin-top: 20px; background: var(--blue); color: white; border: none;
               padding: 14px 32px; border-radius: 10px; font-size: var(--btn); cursor: pointer;
               font-family: inherit; font-weight: 600; width: 100%; display: none;
               transition: background 0.2s; }}
  .next-btn:hover {{ background: var(--mid); }}
  .result-card {{ text-align: center; display: none; }}
  .result-card .score {{ font-size: 3.5rem; font-weight: 700; color: var(--blue); }}
  .result-card .score-label {{ font-size: 1.1rem; color: #666; margin-bottom: 20px; }}
  .result-card .stars {{ font-size: 2.5rem; margin: 16px 0; }}
  .result-card .comment {{ font-size: var(--body); color: var(--text); padding: 16px;
                           background: var(--light); border-radius: 10px; margin-bottom: 24px; }}
  .retry-btn {{ background: var(--gold); color: white; border: none; padding: 14px 32px;
                border-radius: 10px; font-size: var(--btn); cursor: pointer;
                font-family: inherit; font-weight: 600; margin: 8px; transition: background 0.2s; }}
  .retry-btn:hover {{ opacity: 0.85; }}
  .difficulty {{ display: inline-block; font-size: 0.75rem; padding: 2px 8px;
                 border-radius: 12px; margin-bottom: 12px; background: var(--light); color: var(--mid); }}
</style>
</head>
<body>
<div class="quiz-card">
  <div class="quiz-header">
    <h1>{title}</h1>
    <p>{subject}｜{grade}</p>
  </div>
  
  <div id="quiz-area">
    <div class="progress-bar"><div class="progress-fill" id="progress" style="width:0%"></div></div>
    <div class="progress-text" id="progress-text">第 1 題 / 共 {total} 題</div>
    <div class="difficulty" id="difficulty">★☆☆ 基礎</div>
    <div class="question" id="question-text">載入題目中...</div>
    <div class="options" id="options"></div>
    <div class="feedback" id="feedback"></div>
    <button class="next-btn" id="next-btn" onclick="nextQuestion()">下一題 →</button>
  </div>
  
  <div class="result-card" id="result-card">
    <div class="stars" id="stars"></div>
    <div class="score" id="final-score">0</div>
    <div class="score-label">分（共 {total_pts} 分）</div>
    <div class="comment" id="comment"></div>
    <button class="retry-btn" onclick="restart()">🔄 重新作答</button>
    <button class="retry-btn" style="background:var(--mid)" onclick="window.print()">🖨 列印結果</button>
  </div>
</div>

<script>
const questions = {questions_json};
const POINTS_PER_Q = {points_each};
let current = 0, score = 0, answered = false;

const stars = s => s >= 90 ? '⭐⭐⭐' : s >= 70 ? '⭐⭐' : s >= 50 ? '⭐' : '💪';
const comments = {{
  90: ['太厲害了！全部答對！繼續保持！', '滿分！你真的很認真準備！', '非常優秀！'],
  70: ['答得很好！再複習一下錯的地方就完美了！', '不錯！繼續加油！'],
  50: ['有一半以上答對，繼續努力！', '不要灰心，再複習一次！'],
  0:  ['沒關係，先複習課本再試一次！', '繼續學習，你一定可以的！'],
}};

const diffLabels = ['★☆☆ 基礎', '★★☆ 中等', '★★★ 進階'];

function renderQuestion() {{
  const q = questions[current];
  const pct = (current / questions.length) * 100;
  document.getElementById('progress').style.width = pct + '%';
  document.getElementById('progress-text').textContent = `第 ${{current+1}} 題 / 共 ${{questions.length}} 題`;
  document.getElementById('difficulty').textContent = diffLabels[q.difficulty - 1] || diffLabels[0];
  document.getElementById('question-text').textContent = q.question;
  const optDiv = document.getElementById('options');
  optDiv.innerHTML = q.options.map((opt, i) =>
    `<button class="option-btn" onclick="selectAnswer(${{i}})">${{String.fromCharCode(65+i)}}. ${{opt}}</button>`
  ).join('');
  document.getElementById('feedback').style.display = 'none';
  document.getElementById('next-btn').style.display = 'none';
  answered = false;
}}

function selectAnswer(idx) {{
  if (answered) return;
  answered = true;
  const q = questions[current];
  const btns = document.querySelectorAll('.option-btn');
  btns[q.answer].classList.add('correct');
  if (idx !== q.answer) {{ btns[idx].classList.add('wrong'); }}
  else {{ score += POINTS_PER_Q; }}
  btns.forEach(b => b.disabled = true);
  const fb = document.getElementById('feedback');
  fb.style.display = 'block';
  fb.className = 'feedback ' + (idx === q.answer ? 'correct' : 'wrong');
  fb.innerHTML = idx === q.answer
    ? `✅ 正確！${{q.explanation || ''}}`
    : `❌ 正確答案是 ${{String.fromCharCode(65+q.answer)}}。${{q.explanation || ''}}`;
  document.getElementById('next-btn').style.display = 'block';
  document.getElementById('next-btn').textContent = current < questions.length-1 ? '下一題 →' : '查看成績 🏆';
}}

function nextQuestion() {{
  current++;
  if (current < questions.length) {{ renderQuestion(); }}
  else {{ showResult(); }}
}}

function showResult() {{
  document.getElementById('quiz-area').style.display = 'none';
  const rc = document.getElementById('result-card');
  rc.style.display = 'block';
  const pct = Math.round((score / (questions.length * POINTS_PER_Q)) * 100);
  document.getElementById('final-score').textContent = score;
  document.getElementById('stars').textContent = stars(pct);
  const lvl = pct >= 90 ? 90 : pct >= 70 ? 70 : pct >= 50 ? 50 : 0;
  const cmts = comments[lvl];
  document.getElementById('comment').textContent = cmts[Math.floor(Math.random() * cmts.length)];
}}

function restart() {{
  current = 0; score = 0;
  document.getElementById('quiz-area').style.display = 'block';
  document.getElementById('result-card').style.display = 'none';
  renderQuestion();
}}

renderQuestion();
</script>
</body>
</html>'''

# ──────── 隨機分組器 ────────
LOTTERY_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-TW">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>隨機分組器</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ font-family: 'Microsoft JhengHei','Noto Sans TC',sans-serif;
          background: #EBF5FB; min-height: 100vh; padding: 20px; }}
  .container {{ max-width: 600px; margin: 0 auto; }}
  h1 {{ text-align: center; color: #1A5276; font-size: {title_size}; margin-bottom: 20px; }}
  .card {{ background: white; border-radius: 14px; padding: 24px; margin-bottom: 16px;
           box-shadow: 0 2px 12px rgba(26,82,118,0.1); }}
  label {{ display: block; color: #1A5276; font-weight: 600; margin-bottom: 8px; font-size: {body_size}; }}
  textarea {{ width: 100%; height: 120px; padding: 10px; border: 2px solid #D0DCE8;
              border-radius: 8px; font-size: {body_size}; font-family: inherit; resize: vertical; }}
  input[type=number] {{ padding: 10px; border: 2px solid #D0DCE8; border-radius: 8px;
                        font-size: {body_size}; width: 100px; font-family: inherit; }}
  .btn {{ background: #1A5276; color: white; border: none; padding: 14px 28px;
          border-radius: 10px; font-size: {btn_size}; cursor: pointer; font-family: inherit;
          font-weight: 600; width: 100%; margin-top: 12px; transition: background 0.2s; }}
  .btn:hover {{ background: #2471A3; }}
  .btn-secondary {{ background: #D4AC0D; margin-top: 8px; }}
  .result-group {{ background: #EBF5FB; border-radius: 10px; padding: 16px; margin-bottom: 12px;
                   border-left: 4px solid #1A5276; }}
  .result-group h3 {{ color: #1A5276; font-size: {body_size}; margin-bottom: 8px; }}
  .member-chip {{ display: inline-block; background: white; border: 1px solid #2471A3;
                  border-radius: 20px; padding: 4px 12px; margin: 4px; font-size: {body_size};
                  color: #1A5276; }}
  #results {{ display: none; }}
  .copy-btn {{ background: #1E8449; color: white; border: none; padding: 8px 16px;
               border-radius: 6px; cursor: pointer; font-size: 0.85rem; margin-top: 12px; font-family: inherit; }}
</style>
</head>
<body>
<div class="container">
  <h1>🎲 隨機分組器</h1>
  <div class="card">
    <label>學生名單（每行一個名字）</label>
    <textarea id="names" placeholder="王小明&#10;李小花&#10;張大偉&#10;..."></textarea>
    <label style="margin-top:16px">分成幾組？</label>
    <input type="number" id="group-count" value="4" min="2" max="20">
    <button class="btn" onclick="shuffle()">🎲 隨機分組！</button>
  </div>
  <div id="results">
    <div id="group-results"></div>
    <button class="btn btn-secondary" onclick="shuffle()">🔄 重新分組</button>
    <button class="copy-btn" onclick="copyResults()">📋 複製結果</button>
  </div>
</div>
<script>
function shuffle() {{
  const raw = document.getElementById('names').value.trim();
  if (!raw) {{ alert('請先輸入學生名單！'); return; }}
  const students = raw.split('\\n').map(s => s.trim()).filter(Boolean);
  const n = parseInt(document.getElementById('group-count').value) || 4;
  if (students.length < n) {{ alert(`學生人數（${{students.length}}）少於分組數（${{n}}）！`); return; }}
  // Fisher-Yates shuffle
  for (let i = students.length - 1; i > 0; i--) {{
    const j = Math.floor(Math.random() * (i + 1));
    [students[i], students[j]] = [students[j], students[i]];
  }}
  const groups = Array.from({{length: n}}, () => []);
  students.forEach((s, i) => groups[i % n].push(s));
  const div = document.getElementById('group-results');
  const labels = ['第一組','第二組','第三組','第四組','第五組','第六組','第七組','第八組'];
  div.innerHTML = groups.map((g, i) => `
    <div class="result-group">
      <h3>🏷 ${{labels[i] || '第'+(i+1)+'組'}} （${{g.length}} 人）</h3>
      ${{g.map(m => `<span class="member-chip">${{m}}</span>`).join('')}}
    </div>`).join('');
  document.getElementById('results').style.display = 'block';
}}
function copyResults() {{
  const groups = document.querySelectorAll('.result-group');
  const text = Array.from(groups).map((g, i) => {{
    const title = g.querySelector('h3').textContent;
    const members = Array.from(g.querySelectorAll('.member-chip')).map(c => c.textContent).join('、');
    return `${{title}}：${{members}}`;
  }}).join('\\n');
  navigator.clipboard.writeText(text).then(() => alert('已複製！可貼到 Line 或其他地方'));
}}
</script>
</body></html>'''

# ──────── 課堂計時器 ────────
TIMER_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-TW">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>課堂計時器</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ font-family: 'Microsoft JhengHei','Noto Sans TC',sans-serif;
          background: #1A1A2E; color: white; min-height: 100vh;
          display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }}
  .timer-display {{ text-align: center; }}
  .label {{ font-size: 1.6rem; color: #AEC6D8; margin-bottom: 12px; letter-spacing: 2px; }}
  .time {{ font-size: 7rem; font-weight: 700; color: #EBF5FB; line-height: 1;
           transition: color 0.5s; font-variant-numeric: tabular-nums; }}
  .time.warning {{ color: #E8593C; animation: pulse 0.5s infinite; }}
  @keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.6; }} }}
  .presets {{ display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; margin: 24px 0; }}
  .preset-btn {{ padding: 10px 18px; border-radius: 20px; border: none; cursor: pointer;
                 font-size: 0.95rem; font-family: inherit; font-weight: 600;
                 transition: transform 0.1s; }}
  .preset-btn:active {{ transform: scale(0.95); }}
  .preset-btn.p1 {{ background: #2471A3; color: white; }}
  .preset-btn.p2 {{ background: #1E8449; color: white; }}
  .preset-btn.p3 {{ background: #D4AC0D; color: white; }}
  .preset-btn.p4 {{ background: #6C358E; color: white; }}
  .controls {{ display: flex; gap: 16px; margin-top: 20px; }}
  .ctrl-btn {{ padding: 16px 32px; font-size: 1.2rem; border-radius: 12px; border: none;
               cursor: pointer; font-family: inherit; font-weight: 600; transition: opacity 0.2s; }}
  .ctrl-btn:hover {{ opacity: 0.85; }}
  .start {{ background: #1E8449; color: white; }}
  .pause {{ background: #D4AC0D; color: white; }}
  .reset {{ background: #566573; color: white; }}
  .custom {{ display: flex; gap: 8px; align-items: center; margin: 16px 0; }}
  .custom input {{ background: rgba(255,255,255,0.1); border: 1px solid #4A6B7C;
                   color: white; padding: 8px; border-radius: 6px; width: 70px;
                   text-align: center; font-size: 1rem; font-family: inherit; }}
  .custom label {{ font-size: 0.9rem; color: #AEC6D8; }}
</style>
</head>
<body>
<div class="timer-display">
  <div class="label" id="timer-label">課堂計時器</div>
  <div class="time" id="display">05:00</div>
  <div class="presets">
    <button class="preset-btn p1" onclick="setTimer(60)">⏱ 1分 思考</button>
    <button class="preset-btn p2" onclick="setTimer(180)">💬 3分 討論</button>
    <button class="preset-btn p3" onclick="setTimer(300)">📝 5分 寫作</button>
    <button class="preset-btn p4" onclick="setTimer(600)">🎤 10分 發表</button>
  </div>
  <div class="custom">
    <label>自訂：</label>
    <input type="number" id="custom-min" value="5" min="1" max="60"> 分
    <button onclick="setCustom()" style="background:#2471A3;color:white;border:none;padding:8px 14px;border-radius:6px;cursor:pointer;font-family:inherit;">設定</button>
  </div>
  <div class="controls">
    <button class="ctrl-btn start" id="start-btn" onclick="toggleTimer()">▶ 開始</button>
    <button class="ctrl-btn reset" onclick="resetTimer()">↺ 重置</button>
  </div>
</div>
<script>
let total = 300, remaining = 300, interval = null, running = false;
const audio = new AudioContext();

function beep(freq, dur, vol) {{
  const osc = audio.createOscillator();
  const gain = audio.createGain();
  osc.connect(gain); gain.connect(audio.destination);
  osc.frequency.value = freq; gain.gain.value = vol;
  osc.start(); osc.stop(audio.currentTime + dur);
}}

function fmt(s) {{
  const m = Math.floor(s / 60), sec = s % 60;
  return `${{String(m).padStart(2,'0')}}:${{String(sec).padStart(2,'0')}}`;
}}

function updateDisplay() {{
  const el = document.getElementById('display');
  el.textContent = fmt(remaining);
  el.className = 'time' + (remaining <= 10 && remaining > 0 ? ' warning' : '');
}}

function setTimer(secs, label) {{
  resetTimer();
  total = remaining = secs;
  if (label) document.getElementById('timer-label').textContent = label;
  updateDisplay();
}}

function setCustom() {{
  const m = parseInt(document.getElementById('custom-min').value) || 5;
  setTimer(m * 60);
}}

function toggleTimer() {{
  if (running) {{
    clearInterval(interval); running = false;
    document.getElementById('start-btn').textContent = '▶ 繼續';
  }} else {{
    if (remaining <= 0) return;
    running = true;
    document.getElementById('start-btn').textContent = '⏸ 暫停';
    interval = setInterval(() => {{
      remaining--;
      updateDisplay();
      if (remaining <= 10 && remaining > 0) beep(880, 0.1, 0.3);
      if (remaining <= 0) {{
        clearInterval(interval); running = false;
        document.getElementById('start-btn').textContent = '▶ 開始';
        beep(440, 0.5, 0.5); setTimeout(() => beep(660, 0.5, 0.5), 600);
        document.getElementById('timer-label').textContent = '⏰ 時間到！';
      }}
    }}, 1000);
  }}
}}

function resetTimer() {{
  clearInterval(interval); running = false;
  remaining = total; updateDisplay();
  document.getElementById('start-btn').textContent = '▶ 開始';
  document.getElementById('timer-label').textContent = '課堂計時器';
}}
updateDisplay();
</script>
</body></html>'''


def build_quiz_html(title, subject, grade, questions, stage):
    spec = GRADE_SPECS[stage]
    pts = 10 if len(questions) <= 10 else round(100/len(questions))
    total_pts = pts * len(questions)
    return QUIZ_TEMPLATE.format(
        title=title, subject=subject, grade=grade,
        title_size=spec['title'], body_size=spec['body'],
        btn_size=spec['btn'], padding=spec['padding'],
        questions_json=json.dumps(questions, ensure_ascii=False, indent=2),
        total=len(questions), total_pts=total_pts, points_each=pts
    )

def build_lottery_html(grade, stage):
    spec = GRADE_SPECS[stage]
    return LOTTERY_TEMPLATE.format(
        title_size=spec['title'], body_size=spec['body'], btn_size=spec['btn']
    )

def build_timer_html():
    return TIMER_TEMPLATE

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type',    default='quiz',
                        choices=['quiz','lottery','timer','flashcard'])
    parser.add_argument('--title',   default='互動測驗')
    parser.add_argument('--subject', default='國語文')
    parser.add_argument('--grade',   default='國中八年級')
    parser.add_argument('--content', default='')
    parser.add_argument('--output',  default='教學小程式.html')
    args = parser.parse_args()

    stage = get_stage(args.grade)

    if args.type == 'quiz':
        if args.content:
            try: questions = json.loads(args.content)
            except: questions = None
        else: questions = None

        if not questions:
            questions = [
                {"question": f"關於{args.title}，下列敘述何者正確？",
                 "options": ["選項A（正確答案）","選項B","選項C","選項D"],
                 "answer": 0, "explanation": "請教師替換為實際題目", "difficulty": 1},
                {"question": "這是第二題範例，請依課程內容修改。",
                 "options": ["選項A","選項B（正確）","選項C","選項D"],
                 "answer": 1, "explanation": "請教師替換為解析", "difficulty": 2},
                {"question": "這是進階思考題，請依課程修改。",
                 "options": ["選項A","選項B","選項C（正確）","選項D"],
                 "answer": 2, "explanation": "請教師替換為解析", "difficulty": 3},
            ]
        html = build_quiz_html(args.title, args.subject, args.grade, questions, stage)

    elif args.type == 'lottery':
        html = build_lottery_html(args.grade, stage)
    elif args.type == 'timer':
        html = build_timer_html()
    else:
        html = build_lottery_html(args.grade, stage)

    Path(args.output).write_text(html, encoding='utf-8')
    print(f'✓ 教學小程式已生成：{args.output}')
    print(f'  ➤ 直接在瀏覽器開啟，或上傳到 Vercel / GitHub Pages')

if __name__ == '__main__':
    main()
