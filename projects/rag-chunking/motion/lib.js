// Shared drawing helpers for RAG-chunking motion graphics (1920x1080 canvas).
const C = {
  bg0: '#0b141c', bg1: '#132331', ink: '#f3efe6', dim: '#8fa3b3', faint: '#3a4d5c',
  paper: '#efe6d2', paperInk: '#2a2622', paperLine: '#b9ad95',
  cyan: '#3fd6e0', red: '#ff5a5f', amber: '#f2a64a', green: '#4cc38a', blue: '#6aa5ff', purple: '#b48cff',
};
const F = (w, s) => `${w} ${s}px "Noto Sans CJK KR", "Noto Sans CJK JP", sans-serif`;
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const easeOut = x => 1 - Math.pow(1 - clamp(x), 3);
const easeInOut = x => { x = clamp(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
const prog = (t, a, d = 0.45) => easeOut((t - a) / d);          // 0..1 starting at a
const lerp = (a, b, k) => a + (b - a) * k;

let ctx;
function setCtx(c) { ctx = c; }

function background(t) {
  const g = ctx.createRadialGradient(960, 420, 100, 960, 540, 1150);
  g.addColorStop(0, C.bg1); g.addColorStop(1, C.bg0);
  ctx.fillStyle = g; ctx.fillRect(0, 0, 1920, 1080);
  // faint grid for a 'workbench' feel
  ctx.save(); ctx.globalAlpha = 0.05; ctx.strokeStyle = '#9fd3ff'; ctx.lineWidth = 1;
  for (let x = 0; x <= 1920; x += 80) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 1080); ctx.stroke(); }
  for (let y = 0; y <= 1080; y += 80) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(1920, y); ctx.stroke(); }
  ctx.restore();
}

function alpha(a, fn) { if (a <= 0) return; ctx.save(); ctx.globalAlpha *= clamp(a); fn(); ctx.restore(); }

function rr(x, y, w, h, r) {
  r = Math.min(r, w / 2, h / 2);
  ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
}
function box(x, y, w, h, { fill = null, stroke = null, lw = 3, r = 14, glow = null, dash = null } = {}) {
  ctx.save();
  if (glow) { ctx.shadowColor = glow; ctx.shadowBlur = 28; }
  rr(x, y, w, h, r);
  if (fill) { ctx.fillStyle = fill; ctx.fill(); }
  ctx.shadowBlur = 0;
  if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = lw; if (dash) ctx.setLineDash(dash); ctx.stroke(); }
  ctx.restore();
}
function text(s, x, y, { size = 40, w = 700, color = C.ink, align = 'center', base = 'middle', maxW = null } = {}) {
  ctx.save(); ctx.font = F(w, size); ctx.fillStyle = color; ctx.textAlign = align; ctx.textBaseline = base;
  if (maxW) ctx.fillText(s, x, y, maxW); else ctx.fillText(s, x, y);
  ctx.restore();
}
function tw(s, size, w = 700) { ctx.save(); ctx.font = F(w, size); const m = ctx.measureText(s).width; ctx.restore(); return m; }
function line(x1, y1, x2, y2, { color = C.ink, lw = 4, k = 1, dash = null, cap = 'round' } = {}) {
  if (k <= 0) return;
  ctx.save(); ctx.strokeStyle = color; ctx.lineWidth = lw; ctx.lineCap = cap; if (dash) ctx.setLineDash(dash);
  ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(lerp(x1, x2, k), lerp(y1, y2, k)); ctx.stroke(); ctx.restore();
}
function arrow(x1, y1, x2, y2, { color = C.ink, lw = 5, k = 1, head = 18, dash = null } = {}) {
  if (k <= 0) return;
  const ex = lerp(x1, x2, k), ey = lerp(y1, y2, k);
  line(x1, y1, ex, ey, { color, lw, dash });
  const a = Math.atan2(y2 - y1, x2 - x1);
  ctx.save(); ctx.fillStyle = color; ctx.beginPath();
  ctx.moveTo(ex, ey); ctx.lineTo(ex - head * Math.cos(a - .45), ey - head * Math.sin(a - .45));
  ctx.lineTo(ex - head * Math.cos(a + .45), ey - head * Math.sin(a + .45)); ctx.closePath(); ctx.fill(); ctx.restore();
}
// Title at top of motion scenes
function title(s, t, t0, { sub = null, y = 96 } = {}) {
  const a = prog(t, t0, .4);
  alpha(a, () => {
    text(s, 960, y - 8 * (1 - a), { size: 54, w: 900 });
    if (sub) text(sub, 960, y + 52, { size: 28, w: 500, color: C.dim });
  });
}
// Paper card with fake text lines
function paper(x, y, w, h, { lines = 5, lineColor = C.paperLine, fill = C.paper, highlight = null, hlColor = C.paperInk, r = 8, stroke = null, seed = 1 } = {}) {
  box(x, y, w, h, { fill, r, stroke, lw: 3 });
  const pad = Math.min(22, w * .1), lh = (h - pad * 2) / Math.max(lines, 1);
  for (let i = 0; i < lines; i++) {
    const ly = y + pad + lh * (i + .5);
    if (highlight && highlight.line === i) {
      text(highlight.text, x + pad, ly, { size: highlight.size || Math.min(30, lh * .8), w: 900, color: hlColor, align: 'left', maxW: w - pad * 2 });
      continue;
    }
    const frac = 0.55 + 0.4 * Math.abs(Math.sin(seed * 12.9898 + i * 78.233));
    line(x + pad, ly, x + pad + (w - pad * 2) * (i === lines - 1 ? frac * .6 : frac), ly, { color: lineColor, lw: Math.max(3, Math.min(8, lh * .28)) });
  }
}
function tag(s, x, y, { color = C.cyan, size = 30, fg = '#0b141c', a = 1, w = 800 } = {}) {
  alpha(a, () => {
    const W = tw(s, size, w) + size * 1.1, H = size * 1.6;
    box(x - W / 2, y - H / 2, W, H, { fill: color, r: H / 2 });
    text(s, x, y + 1, { size, w, color: fg });
  });
}
function mark(ok, x, y, s = 40, color = null) {
  ctx.save(); ctx.lineWidth = s * .16; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  ctx.strokeStyle = color || (ok ? C.green : C.red); ctx.beginPath();
  if (ok) { ctx.moveTo(x - s * .5, y); ctx.lineTo(x - s * .12, y + s * .38); ctx.lineTo(x + s * .55, y - s * .42); }
  else { ctx.moveTo(x - s * .4, y - s * .4); ctx.lineTo(x + s * .4, y + s * .4); ctx.moveTo(x + s * .4, y - s * .4); ctx.lineTo(x - s * .4, y + s * .4); }
  ctx.stroke(); ctx.restore();
}
function scanBar(x1, x2, y, k, a = 1) {
  alpha(a, () => { ctx.save(); ctx.shadowColor = C.cyan; ctx.shadowBlur = 24; line(x1, y, lerp(x1, x2, k), y, { color: C.cyan, lw: 7 }); ctx.restore(); });
}
