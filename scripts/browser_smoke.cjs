// Run after generating output/acceptance/mini-{mode}.html.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
(async () => {
  const browser = await chromium.launch({channel: 'chrome', headless: true});
  try {
    const page = await browser.newPage(); const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    const open = mode => page.goto(pathToFileURL(path.resolve('output/acceptance/mini-' + mode + '.html')).href);
    await open('quiz');
    await page.getByRole('button', {name:'送出評分'}).click();
    await page.getByRole('status').filter({hasText:'請完成所有題目'}).waitFor();
    await page.getByRole('button', {name:'鳥鳴', exact:true}).click();
    await page.getByRole('button', {name:'送出評分'}).click();
    await page.getByRole('status').filter({hasText:'得分：1 / 1'}).waitFor();
    await page.getByRole('button', {name:'重新作答'}).click();
    assert.equal(await page.locator('[aria-pressed=true]').count(), 0);
    await open('flashcard');
    await page.getByRole('button').click();
    assert.equal(await page.getByRole('button').textContent(), '後面');
    assert.equal(await page.locator('img').count(), 0);
    await open('lottery'); await page.getByRole('button', {name:'抽選'}).click();
    assert.ok(['甲','乙'].includes(await page.getByRole('status').textContent()));
    await open('timer');
    await page.getByRole('button', {name:'開始'}).click();
    await page.waitForTimeout(1150);
    await page.getByRole('button', {name:'暫停'}).click();
    const paused = await page.getByRole('timer').textContent();
    await page.waitForTimeout(1100);
    assert.equal(await page.getByRole('timer').textContent(), paused);
    await page.getByRole('button', {name:'重設'}).click();
    assert.equal(await page.getByRole('timer').textContent(), '3');
    await page.getByRole('button', {name:'開始'}).click();
    await page.getByRole('timer').filter({hasText:/^0$/}).waitFor();
    assert.equal(await page.getByRole('button', {name:'開始'}).isDisabled(), true);
    assert.deepEqual(errors, []);
    await page.screenshot({path:'output/acceptance/mini-timer.png'});
    console.log('PASS: Chromium quiz, flashcard injection, lottery, timer pause/reset/end; no page errors');
  } finally { await browser.close(); }
})().catch(e => {console.error(e); process.exitCode=1;});
