// usage: node render.js preview M01 8.5 12 ...   |  node render.js video M01 7.917 20.0 out.mp4
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
(async () => {
  const [mode, id, ...rest] = process.argv.slice(2);
  const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.resolve('index.html'));
  await page.evaluate(async () => { for (const w of [400, 500, 700, 900]) await document.fonts.load(`${w} 40px "Noto Sans CJK KR"`, '가A'); await loadF06(); });
  const errs = []; page.on('pageerror', e => errs.push(String(e)));
  const canvas = await page.$('#c');
  if (mode === 'preview') {
    for (const t of rest) { await page.evaluate(([i, tt]) => draw(i, tt), [id, +t]); await canvas.screenshot({ path: `prev/${id}_${t}.png` }); }
  } else {
    const [a, b, out] = rest; const fps = 24; const n = Math.round((+b - +a) * fps);
    const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', '24', '-c:v', 'png', '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '16', '-preset', 'medium', '-r', '24', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = 0; i < n; i++) {
      const t = +a + (i + 0.5) / fps;   // sample mid-frame
      await page.evaluate(([id_, tt]) => draw(id_, tt), [id, t]);
      const buf = await canvas.screenshot({ type: 'png' });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
    console.log(id, 'frames', n);
  }
  if (errs.length) console.log('ERR', errs);
  await browser.close();
})();
