const D = JSON.parse(document.getElementById('data').textContent);
const root = document.getElementById('app');
const el = (tag, text) => { const node = document.createElement(tag); node.textContent = text; return node; };
function quiz() {
  let selected = {};
  function draw() {
    root.replaceChildren();
    const groups = [];
    D.questions.forEach(q => {
      const group = el('fieldset', ''); groups.push(group);
      group.append(el('legend', q.prompt));
      q.options.forEach(o => {
        const b = el('button', o.text); b.setAttribute('aria-pressed', 'false');
        b.onclick = () => { selected[q.id] = o.id; group.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', String(x === b))); };
        group.append(b);
      });
      group.append(el('p', `配分：${q.points}`)); root.append(group);
    });
    const result = el('p', ''); result.setAttribute('role', 'status');
    const submit = el('button', '送出評分');
    submit.onclick = () => {
      if (Object.keys(selected).length !== D.questions.length) { result.textContent = '請完成所有題目再送出。'; return; }
      let earned = 0, total = 0;
      D.questions.forEach(q => { total += q.points; if (selected[q.id] === q.answer) earned += q.points; });
      result.textContent = `得分：${earned} / ${total}`;
      D.questions.forEach(q => { const answer = q.options.find(o => o.id === q.answer); root.append(el('p', `${q.id} 答案：${answer.text}${q.explanation ? '；解析：' + q.explanation : ''}`)); });
      groups.forEach(g => g.disabled = true); submit.disabled = true;
    };
    const reset = el('button', '重新作答'); reset.onclick = () => { selected = {}; draw(); };
    root.append(submit, reset, result);
  }
  draw();
}
function flashcard() {
  D.cards.forEach(card => { let back = false; const b = el('button', card.front); b.setAttribute('aria-label', '學習卡：' + card.front); b.onclick = () => { back = !back; b.textContent = back ? card.back : card.front; b.setAttribute('aria-pressed', String(back)); }; root.append(b); });
}
function lottery() {
  const b = el('button', '抽選'), result = el('p', ''); result.setAttribute('role', 'status');
  b.onclick = () => { result.textContent = D.entries[Math.floor(Math.random() * D.entries.length)]; }; root.append(b, result);
}
function timer() {
  let remaining = D.seconds, deadline = 0, interval = null;
  const display = el('p', String(remaining)), start = el('button', '開始'), pause = el('button', '暫停'), reset = el('button', '重設');
  display.setAttribute('role', 'timer'); pause.disabled = true;
  function stop() { clearInterval(interval); interval = null; start.disabled = remaining <= 0; pause.disabled = true; }
  function tick() { remaining = Math.max(0, Math.ceil((deadline - Date.now()) / 1000)); display.textContent = String(remaining); if (!remaining) stop(); }
  start.onclick = () => { if (interval !== null || remaining <= 0) return; deadline = Date.now() + remaining * 1000; start.disabled = true; pause.disabled = false; interval = setInterval(tick, 100); };
  pause.onclick = () => { tick(); stop(); };
  reset.onclick = () => { remaining = D.seconds; stop(); display.textContent = String(remaining); };
  root.append(display, start, pause, reset);
}
({quiz, flashcard, lottery, timer})[D.mode]();
