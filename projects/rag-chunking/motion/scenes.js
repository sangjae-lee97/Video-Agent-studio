// Scene drawings. All times are absolute seconds on the 160.780 s narration timeline.
const TOPICS = [
  { name: '과제 제출', color: C.amber }, { name: '수업 환경', color: C.green },
  { name: '질문·문의', color: C.blue }, { name: '평가·근거', color: C.purple },
];

// ---------- M01 7.917–20.000 : RAG flow → mixed document → chunks ----------
function M01(t) {
  background(t);
  // phase A: RAG pipeline (8.0–9.4), then shrinks to top strip
  const shrink = easeInOut((t - 9.4) / .8);
  const nodes = ['질문', '검색', '근거', '답'];
  const yA = lerp(380, 170, shrink), sc = lerp(1, .62, shrink);
  const gap = 330 * sc, x0 = 960 - gap * 1.5;
  nodes.forEach((n, i) => {
    const a = prog(t, 7.95 + i * .28, .3);
    alpha(a, () => {
      const x = x0 + gap * i, w = 210 * sc, h = 96 * sc;
      box(x - w / 2, yA - h / 2, w, h, { fill: i === 1 ? C.cyan : '#1d3242', stroke: i === 1 ? null : C.dim, lw: 2, r: 18 * sc });
      text(n, x, yA, { size: 44 * sc, w: 900, color: i === 1 ? '#0b141c' : C.ink });
      if (i > 0) arrow(x - gap + w / 2 + 12 * sc, yA, x - w / 2 - 12 * sc, yA, { color: C.dim, lw: 4 * sc, head: 14 * sc, k: prog(t, 7.95 + i * .28 - .1, .3) });
    });
  });
  alpha(prog(t, 8.1) * (1 - shrink), () => text('RAG — 문서를 검색해, 찾은 근거로 답하기', 960, 560, { size: 40, w: 700, color: C.dim }));

  // phase B: one long document with mixed topics (9.52–15.1)
  const docA = prog(t, 9.6, .5);
  const split = easeInOut((t - 16.0) / 1.1);           // document splits into 4 cards
  const blocks = [];
  // block order: interleaved topics to show mixing
  const order = [0, 1, 0, 2, 3, 1, 2, 3, 0, 2];
  const mix = prog(t, 11.5, .9);                       // colors become visible = mixed
  const docX = 760, docY = 270, docW = 400, docH = 560;
  if (split <= 0) {
    alpha(docA, () => {
      box(docX, docY, docW, docH, { fill: C.paper, r: 10 });
      order.forEach((tp, i) => {
        const by = docY + 24 + i * 52;
        alpha(.25 + .75 * mix, () => box(docX + 18, by, 10, 38, { fill: TOPICS[tp].color, r: 4 }));
        paper(docX + 34, by, docW - 52, 40, { lines: 2, fill: 'rgba(0,0,0,0)', seed: i + 3 });
      });
      text('긴 문서 한 덩어리', docX + docW / 2, docY - 30, { size: 32, w: 700, color: C.dim });
    });
    // confused search: scan bar sweeps without settling + '?' (12.9–14.6)
    const sk = (t - 12.6) / 1.6;
    if (sk > 0 && sk < 1.4) scanBar(docX - 40, docX + docW + 40, docY + 60 + 440 * (0.5 + 0.5 * Math.sin(sk * 6)), 1, Math.min(1, 1.4 - sk));
    alpha(prog(t, 13.3), () => { text('?', docX + docW + 120, docY + 240, { size: 140, w: 900, color: C.cyan });
      text('필요한 부분을 가려내기 어렵다', docX + docW / 2, docY + docH + 50, { size: 34, w: 700, color: C.ink }); });
    // legend of topics
    alpha(mix, () => TOPICS.forEach((tp, i) => { box(330, 360 + i * 70, 26, 26, { fill: tp.color, r: 6 }); text(tp.name, 372, 373 + i * 70, { size: 30, w: 500, align: 'left' }); }));
    // red cut lines preview (15.6–16.0)
    const cutK = prog(t, 15.4, .5);
    [2, 5, 7].forEach(ci => line(docX - 30, docY + 24 + ci * 52 + 46, docX + docW + 30, docY + 24 + ci * 52 + 46, { color: C.red, lw: 5, k: cutK, dash: [16, 10] }));
  } else {
    // 4 chunk cards spread horizontally, each one topic-ish (by cut groups)
    const groups = [[0, 1], [2, 3, 4], [5, 6], [7, 8, 9]];
    const cw = 330, gapX = 40, totalW = cw * 4 + gapX * 3, sx = 960 - totalW / 2;
    groups.forEach((g, gi) => {
      const fromY = docY + 24 + g[0] * 52, fromX = docX;
      const tx = sx + gi * (cw + gapX), ty = 330;
      const x = lerp(fromX, tx, split), y = lerp(fromY, ty, split), w = lerp(docW, cw, split);
      const h = g.length * 52 + 30;
      box(x, y, w, h, { fill: C.paper, r: 10 });
      g.forEach((bi, k) => { box(x + 16, y + 16 + k * 52, 10, 38, { fill: TOPICS[order[bi]].color, r: 4 }); paper(x + 32, y + 16 + k * 52, w - 48, 40, { lines: 2, fill: 'rgba(0,0,0,0)', seed: bi + 3 }); });
      tag('청크 ' + (gi + 1), x + w / 2, y - 34, { color: C.cyan, size: 28, a: prog(t, 17.1 + gi * .12, .35) });
    });
    alpha(prog(t, 18.5, .5), () => {
      text('청킹 Chunking', 960, 720, { size: 76, w: 900 });
      text('긴 문서를 검색할 수 있는 조각(청크)으로 나누기 · 청크 = 검색 단위', 960, 800, { size: 32, w: 500, color: C.dim });
    });
  }
}

// ---------- M02 20.000–26.380 : chunk → embedding vector ; cutting ≠ embedding ----------
function M02(t) {
  background(t);
  title('자른 다음에는 임베딩', t, 20.0);
  const cw = 300, gapX = 60, sx = 960 - (cw * 4 + gapX * 3) / 2;
  const vecs = [[.12, -.40, .33, .71, -.18, .05], [-.27, .58, .10, -.44, .36, .22], [.48, .09, -.31, .15, .62, -.12], [-.05, -.22, .54, .30, -.47, .41]];
  const toBoxes = easeInOut((t - 23.0) / .7);
  for (let i = 0; i < 4; i++) {
    const x = sx + i * (cw + gapX);
    alpha(1 - toBoxes, () => {
      paper(x, 200, cw, 140, { lines: 4, seed: i + 7 });
      text('청크 ' + (i + 1), x + cw / 2, 182, { size: 24, w: 700, color: C.cyan });
      const ak = prog(t, 20.4 + i * .25, .5);
      arrow(x + cw / 2, 352, x + cw / 2, 452, { color: C.cyan, lw: 5, k: ak });
      if (i === 0) alpha(ak, () => text('임베딩', x + cw / 2 + 64, 400, { size: 26, w: 700, color: C.cyan, align: 'left' }));
      const vk = prog(t, 21.0 + i * .25, .5);
      alpha(vk, () => {
        // vector as bar glyphs
        vecs[i].forEach((v, j) => {
          const bx = x + 26 + j * 44, base = 560;
          box(bx, v > 0 ? base - v * 90 : base, 28, Math.abs(v) * 90, { fill: v > 0 ? C.cyan : '#2b7f88', r: 4 });
        });
        line(x + 16, 560, x + cw - 16, 560, { color: C.faint, lw: 2 });
        text('[' + vecs[i].slice(0, 3).map(v => v.toFixed(2)).join(', ') + ', …]', x + cw / 2, 680, { size: 24, w: 500, color: C.ink });
      });
    });
  }
  alpha(prog(t, 21.2) * (1 - toBoxes), () => text('숫자는 설명용 예시 값', 960, 760, { size: 24, w: 400, color: C.dim }));
  // two task boxes
  alpha(toBoxes, () => {
    box(330, 330, 520, 300, { fill: '#1d3242', stroke: C.red, lw: 4, r: 24 });
    text('자르기', 590, 420, { size: 64, w: 900 });
    text('청킹 · 문서를 조각으로', 590, 510, { size: 32, w: 500, color: C.dim });
    line(470, 570, 710, 570, { color: C.red, lw: 6, dash: [18, 12] });
    box(1070, 330, 520, 300, { fill: '#1d3242', stroke: C.cyan, lw: 4, r: 24 });
    text('숫자로 바꾸기', 1330, 420, { size: 64, w: 900 });
    text('임베딩 · 조각을 벡터로', 1330, 510, { size: 32, w: 500, color: C.dim });
    [.12, -.4, .33, .71, -.18].forEach((v, j) => box(1250 + j * 34, v > 0 ? 585 - v * 40 : 585, 22, Math.abs(v) * 40, { fill: C.cyan, r: 3 }));
  });
  alpha(prog(t, 24.86, .35), () => text('≠', 960, 480, { size: 140, w: 900, color: C.amber }));
}

// shared example document for M03 (paragraph blocks with blank gaps)
const PARAS = [3, 2, 4, 2, 3];   // lines per paragraph; answer sentence in paragraph 1 line 1
function exampleDoc(x, y, w, lh, { answerColor = C.paperInk } = {}) {
  let cy = y; const out = [];
  PARAS.forEach((n, pi) => {
    for (let i = 0; i < n; i++) {
      const ly = cy + i * lh;
      if (pi === 1 && i === 0) text('과제 제출 기한은 금요일 오후 6시', x + 14, ly + lh / 2, { size: lh * .82, w: 900, color: answerColor, align: 'left', maxW: w - 28 });
      else { const f = .6 + .35 * Math.abs(Math.sin(pi * 7.1 + i * 3.3)); line(x + 14, ly + lh / 2, x + 14 + (w - 28) * (i === n - 1 ? f * .6 : f), ly + lh / 2, { color: C.paperLine, lw: lh * .28 }); }
    }
    out.push({ top: cy, bottom: cy + n * lh });
    cy += n * lh + lh;  // blank line gap
  });
  return out;
}

// ---------- M03 34.297–44.000 : fixed-size vs paragraph ----------
function M03(t) {
  background(t);
  title('두 가지 기본 자르기', t, 34.3);
  const lh = 30, w = 560, y0 = 230;
  const docH = PARAS.reduce((a, n) => a + n, 0) * lh + (PARAS.length - 1) * lh;
  // left: fixed
  const L = 220, R = 1140;
  [L, R].forEach(x => box(x - 10, y0 - 14, w + 20, docH + 28, { fill: C.paper, r: 10 }));
  const leftHit = prog(t, 38.08, .3);
  exampleDoc(L, y0, w, lh, { answerColor: leftHit > 0 ? C.red : C.paperInk });
  const paras = exampleDoc(R, y0, w, lh);
  text('고정 크기', L + w / 2, y0 - 60, { size: 44, w: 900 });
  text('문단', R + w / 2, y0 - 60, { size: 44, w: 900 });
  // fixed cuts: every 4 lines (=120px)
  const fk = prog(t, 34.6, .6);
  for (let c = 1; c * 4 * lh < docH; c++) {
    const cy = y0 + c * 4 * lh + (c === 1 ? lh * 0.5 : 0);   // second cut lands mid answer line
    line(L - 30, cy, L + w + 30, cy, { color: C.red, lw: 5, k: fk });
  }
  alpha(prog(t, 35.9), () => {
    for (let c = 0; c < 5; c++) box(L + w + 46, y0 + c * 120 + 8, 14, 104, { fill: C.dim, r: 4 });
    text('모두 같은 크기', L + w + 54, y0 + docH + 34, { size: 22, w: 500, color: C.dim });
  });
  tag('✓ 예측 쉬움', L + w / 2, y0 + docH + 80, { color: C.green, size: 30, a: prog(t, 36.7) });
  alpha(leftHit, () => { box(L - 6, y0 + 4 * lh + lh * .5 - 24, w + 12, 48, { stroke: C.red, lw: 4, r: 8 }); });
  tag('✕ 문장 중간 절단', L + w / 2, y0 + docH + 150, { color: C.red, size: 30, fg: '#fff', a: prog(t, 38.5) });
  // paragraph cuts at blank gaps
  const pk = prog(t, 39.4, .6);
  paras.slice(0, -1).forEach((p, i) => { const gy = p.bottom + lh / 2; line(R - 30, gy, R + w + 30, gy, { color: C.red, lw: 5, k: pk }); });
  alpha(prog(t, 41.6), () => paras.forEach(p => box(R - 46, p.top + 4, 14, p.bottom - p.top - 8, { fill: C.amber, r: 4 })));
  tag('✓ 경계 보존', R + w / 2, y0 + docH + 80, { color: C.green, size: 30, a: prog(t, 40.62) });
  tag('△ 길이 들쭉날쭉', R + w / 2, y0 + docH + 150, { color: C.amber, size: 30, a: prog(t, 41.94) });
}

// ---------- M04 51.917–64.500 : top-10 zero → overlap → 160/30 arithmetic ----------
function M04(t) {
  background(t);
  const outA = easeInOut((t - 52.95) / .4);
  if (outA < 1) alpha(1 - outA, () => {
    title('60자씩 자르면', t, 51.92, { sub: 'Lesson 08 예시 · fixed 60, overlap 0' });
    for (let i = 0; i < 10; i++) {
      const x = 360 + (i % 5) * 250, y = 330 + Math.floor(i / 5) * 170;
      const a = prog(t, 51.95 + i * .05, .2);
      alpha(a, () => { box(x, y, 210, 120, { fill: '#1d3242', stroke: C.faint, lw: 2, r: 12 }); text((i + 1) + '위', x + 50, y + 60, { size: 30, w: 700 }); mark(false, x + 150, y + 60, 46); });
    }
    alpha(prog(t, 52.3, .3), () => text('상위 10개 안에 ‘금요일 오후 6시’ 온전히 포함: 0', 960, 720, { size: 40, w: 900, color: C.red }));
  });
  if (t < 53.2) return;
  title('오버랩 Overlap', t, 53.26, { sub: '앞 조각의 끝부분을 다음 조각 첫머리에 겹친다' });
  const k2 = easeInOut((t - 59.2) / .5);       // move overlap demo up/out for number line
  alpha(1 - k2, () => {
    const ay = 360;
    paper(380, ay, 640, 150, { lines: 4, seed: 2 });
    text('조각 A', 700, ay - 30, { size: 30, w: 700, color: C.dim });
    const bx = lerp(1300, 880, prog(t, 56.6, .7));
    alpha(prog(t, 56.3, .3), () => { paper(bx, ay + 190, 640, 150, { lines: 4, seed: 5 }); text('조각 B', bx + 320, ay + 370, { size: 30, w: 700, color: C.dim }); });
    const hk = prog(t, 55.98, .4);
    alpha(hk, () => { box(880, ay - 6, 140, 162, { stroke: C.amber, lw: 5, r: 8 }); ctx.save(); ctx.globalAlpha *= .28; box(880, ay - 6, 140, 162, { fill: C.amber, r: 8 }); ctx.restore(); });
    const ok = prog(t, 57.6, .4);
    alpha(ok, () => { ctx.save(); ctx.globalAlpha *= .35; box(880, ay + 190, 140, 150, { fill: C.amber, r: 8 }); ctx.restore(); text('겹침', 950, ay + 172, { size: 30, w: 900, color: C.amber }); });
  });
  if (t < 59.2) return;
  alpha(k2, () => {
    const X = v => 300 + v * 3.1, base = 700;   // 0..420 chars → 300..1602 px
    line(X(0), base, X(420), base, { color: C.dim, lw: 3 });
    [0, 130, 160, 260, 290, 420].forEach(v => { line(X(v), base - 10, X(v), base + 10, { color: C.dim, lw: 3 }); text(String(v), X(v), base + 38, { size: 26, w: 500, color: C.dim }); });
    text('문자 위치', X(420) + 40, base, { size: 24, w: 500, color: C.dim, align: 'left' });
    const bars = [[0, 160, 59.42, '청크 1  [0:160]'], [130, 290, 60.56, '청크 2  [130:290]'], [260, 420, 61.6, '청크 3  [260:420]']];
    bars.forEach(([a, b, t0, lab], i) => {
      const k = prog(t, t0, .5), y = 300 + i * 110;
      alpha(k, () => { box(X(a), y, (X(b) - X(a)) * k, 70, { fill: C.paper, r: 8 }); text(lab, X(a) + 18, y + 35, { size: 28, w: 700, color: C.paperInk, align: 'left' }); });
    });
    const ok = prog(t, 61.18, .4);
    alpha(ok, () => {
      [[130, 160, 410], [260, 290, 520]].forEach(([a, b, y]) => { ctx.save(); ctx.globalAlpha *= .55; box(X(a), y - 110, X(b) - X(a), 180, { fill: C.amber, r: 6 }); ctx.restore(); });
      text('30자 겹침', X(145), 262, { size: 28, w: 900, color: C.amber });
    });
    const sk = prog(t, 63.0, .5);
    alpha(sk, () => {
      arrow(X(0), 640, X(130), 640, { color: C.cyan, lw: 5, k: sk });
      text('다음 시작 = +130자', X(65), 612, { size: 28, w: 900, color: C.cyan });
    });
    alpha(prog(t, 63.4), () => text('160 − 30 = 130', 1500, 800, { size: 48, w: 900, color: C.ink }));
  });
}

// ---------- M05 64.500–72.920 : recursive splitter, overlap slider question ----------
function M05(t) {
  background(t);
  const q = easeInOut((t - 69.8) / .5);
  alpha(1 - q, () => {
    title('재귀 분할기', t, 64.5, { sub: 'LangChain RecursiveCharacterTextSplitter · 큰 구분자부터 차례로' });
    const steps = [['① 빈 줄', 66.2], ['② 줄바꿈', 67.02], ['③ 공백', 67.74], ['④ 필요하면 글자', 68.36]];
    steps.forEach(([s, t0], i) => {
      const a = prog(t, t0, .35), act = t >= t0 && (i === 3 || t < steps[i + 1][1]);
      alpha(.25 + .75 * a, () => {
        box(260, 260 + i * 120, 420, 90, { fill: act ? C.cyan : '#1d3242', stroke: act ? null : C.faint, lw: 2, r: 16 });
        text(s, 470, 305 + i * 120, { size: 38, w: 900, color: act ? '#0b141c' : (i === 3 ? C.dim : C.ink) });
      });
      if (i < 3) arrow(470, 352 + i * 120, 470, 378 + i * 120, { color: C.faint, lw: 3, head: 10 });
    });
    // document on the right being split stage-wise
    const dx = 860, dw = 800, lh = 34;
    const y0 = 250;
    let y = y0;
    const paraN = [3, 6, 2];
    const k1 = prog(t, 66.2, .4), k2 = prog(t, 67.02, .4), k3 = prog(t, 67.74, .4);
    paraN.forEach((n, pi) => {
      const sep = 24 * k1 * pi;
      const top = y + sep;
      box(dx, top, dw, n * lh + 20, { fill: C.paper, r: 8 });
      for (let i = 0; i < n; i++) { const f = .6 + .35 * Math.abs(Math.sin(pi * 5 + i * 2.1)); line(dx + 20, top + 10 + lh * (i + .5), dx + 20 + (dw - 40) * f, top + 10 + lh * (i + .5), { color: C.paperLine, lw: 9 }); }
      if (pi === 1) {
        // too-big paragraph: split at a line break (after line 3)
        line(dx - 20, top + 10 + 3 * lh, dx + dw + 20, top + 10 + 3 * lh, { color: C.amber, lw: 5, k: k2 });
        // still too big piece: split at a space inside line 5
        const sx = dx + 20 + (dw - 40) * .45, sy = top + 10 + 4.5 * lh;
        alpha(k3, () => { line(sx, sy - 22, sx, sy + 22, { color: C.amber, lw: 5 }); text('공백', sx + 14, sy - 30, { size: 22, w: 700, color: C.amber, align: 'left' }); });
      }
      y += n * lh + 20 + 30;
    });
    alpha(k1, () => text('빈 줄에서 먼저 나눔', dx + dw / 2, 222, { size: 26, w: 700, color: C.cyan }));
    alpha(prog(t, 68.6), () => text('의미를 이해하는 게 아니라, 구분자 우선순위로 자를 자리를 찾는다', 960, 860, { size: 30, w: 500, color: C.dim }));
  });
  if (t < 69.8) return;
  alpha(q, () => {
    text('겹침', 560, 420, { size: 44, w: 900, color: C.amber });
    const v = lerp(30, 60, easeInOut((t - 71.0) / .7));
    const X = 700, W = 700;
    line(X, 420, X + W, 420, { color: C.faint, lw: 10 });
    line(X, 420, X + W * v / 90, 420, { color: C.amber, lw: 10 });
    ctx.save(); ctx.fillStyle = C.ink; ctx.beginPath(); ctx.arc(X + W * v / 90, 420, 22, 0, 7); ctx.fill(); ctx.restore();
    text(Math.round(v) + '자', X + W * v / 90, 370, { size: 40, w: 900, color: C.amber });
    alpha(prog(t, 71.2), () => text('많이 겹칠수록 좋을까?', 960, 620, { size: 72, w: 900 }));
  });
}

// ---------- M06 80.837–93.820 : rank table, fixture caveat ----------
function M06(t) {
  background(t);
  title('정답 조각의 순위', t, 80.85, { sub: 'Lesson 07 강의 검증 실행 · 질문 ‘과제 마감일’ · 교육용 Fixture' });
  const cx = [700, 1010, 1320], cw = 270;
  ['1위', '2위', '3위'].forEach((h, i) => text(h, cx[i] + cw / 2, 250, { size: 34, w: 900, color: C.dim }));
  const rows = [
    { lab: '겹침 30자', y: 300, cells: [['문의 안내', C.blue], ['정답 조각', C.green], ['다른 조각', C.faint]], t0: 80.9 },
    { lab: '겹침 60자', y: 450, cells: [['문의 안내', C.blue], ['문의 안내', C.blue], ['정답 조각', C.green]], t0: 81.5 },
  ];
  rows.forEach(r => {
    alpha(prog(t, r.t0, .35), () => {
      text(r.lab, 600, r.y + 50, { size: 36, w: 900, align: 'right' });
      r.cells.forEach(([s, col], i) => {
        box(cx[i], r.y, cw, 100, { fill: col === C.faint ? '#1d3242' : col, r: 14 });
        text(s, cx[i] + cw / 2, r.y + 50, { size: 32, w: 900, color: col === C.faint ? C.dim : '#0b141c' });
      });
    });
  });
  // duplicate highlight
  alpha(prog(t, 82.2, .3), () => { box(cx[0] - 8, 442, cw * 2 + 48, 116, { stroke: C.amber, lw: 5, r: 18, dash: [14, 8] }); text('같은 내용 중복', cx[0] + cw + 20, 590, { size: 28, w: 700, color: C.amber }); });
  const ak = prog(t, 82.9, .5);
  arrow(cx[1] + cw / 2, 405, cx[2] + cw / 2 - 30, 450, { color: C.red, lw: 6, k: ak });
  alpha(ak, () => text('2위 → 3위', cx[2] + cw / 2 + 120, 400, { size: 36, w: 900, color: C.red }));
  // caveat
  const ck = prog(t, 84.6, .4);
  alpha(ck, () => {
    box(360, 640, 1200, 110, { fill: '#1d3242', stroke: C.faint, lw: 2, r: 18 });
    text('교육용 Fixture 벡터 = [과제, 마감, 제출] 단어 개수', 960, 678, { size: 32, w: 700 });
    alpha(prog(t, 86.8), () => text('실제 의미 임베딩 아님 · 일반 법칙 아님', 960, 722, { size: 28, w: 700, color: C.amber }));
  });
  alpha(prog(t, 89.6, .4), () => { tag('→ 자른 방식은 검색 결과로 확인', 960, 820, { color: C.cyan, size: 34 }); });
}

// three rank slots helper
function slots(x, y, filled, t0, t, { w = 360 } = {}) {
  for (let i = 0; i < 3; i++) {
    const yy = y + i * 110;
    box(x, yy, w, 90, { fill: '#1d3242', stroke: C.faint, lw: 2, r: 12 });
    text((i + 1) + '위', x + 44, yy + 45, { size: 28, w: 700, color: C.dim });
    if (filled === i) alpha(prog(t, t0, .35), () => { box(x + 90, yy + 12, w - 104, 66, { fill: C.paper, r: 8 }); text('금요일 오후 6시', x + 90 + (w - 104) / 2, yy + 46, { size: 28, w: 900, color: C.paperInk }); });
    else alpha(prog(t, t0, .35), () => { box(x + 90, yy + 12, w - 104, 66, { fill: '#2a3c4a', r: 8 }); line(x + 110, yy + 45, x + w - 40, yy + 45, { color: '#466070', lw: 8 }); });
  }
}

// ---------- M07 93.820–99.780 : Hit@3 ----------
function M07(t) {
  background(t);
  title('첫 번째 잣대 · Hit@3', t, 93.85, { sub: '상위 3개 안에 정답 근거가 있으면 1, 없으면 0' });
  slots(380, 300, 1, 95.8, t);
  slots(1180, 300, -1, 95.8, t);
  alpha(prog(t, 97.5, .3), () => { text('1', 560, 720, { size: 110, w: 900, color: C.green }); text('Hit@3', 560, 800, { size: 30, w: 700, color: C.dim }); });
  alpha(prog(t, 98.1, .3), () => { text('0', 1360, 720, { size: 110, w: 900, color: C.red }); text('Hit@3', 1360, 800, { size: 30, w: 700, color: C.dim }); });
}

// ---------- M08 99.780–108.560 : reciprocal rank ----------
function M08(t) {
  background(t);
  title('두 번째 잣대 · MRR', t, 99.8, { sub: 'Mean Reciprocal Rank — 정답이 처음 나온 순위의 역수 평균' });
  const cols = [[300, 0, 102.42, '1', '1위'], [820, 1, 103.62, '1/2', '2위'], [1340, 2, 104.92, '1/3', '3위']];
  cols.forEach(([x, r, t0, rr, lab]) => {
    slots(x, 270, r, t0, t, { w: 300 });
    alpha(prog(t, t0 + .4, .3), () => { text('RR = ' + rr, x + 150, 650, { size: 50, w: 900, color: C.cyan }); });
  });
  alpha(prog(t, 106.3, .4), () => text('질문들의 RR 평균 = MRR', 960, 760, { size: 44, w: 900 }));
}

// ---------- M09 108.560–121.940 : same Hit@3, different MRR ; not accuracy ----------
function M09(t) {
  background(t);
  title('같은 Hit@3, 다른 MRR', t, 108.6, { sub: '강의의 가상 계산 예시 (실측 아님)' });
  const head = ['질문', '정답 순위', 'Hit@3', 'RR'], hx = [480, 790, 1100, 1410];
  const fade = 1 - .8 * prog(t, 116.0, .5);
  alpha(fade, () => {
    head.forEach((h, i) => text(h, hx[i], 250, { size: 32, w: 900, color: C.dim }));
    const rows = [['A', '1위', '1', '1.000', 111.84], ['B', '2위', '1', '0.500', 112.36], ['C', '3위', '1', '0.333', 112.66]];
    rows.forEach(([q, rk, h, r, tr], i) => {
      const y = 330 + i * 90;
      alpha(prog(t, 108.9 + i * .15, .3), () => { line(380, y + 40, 1520, y + 40, { color: C.faint, lw: 1 }); text(q, hx[0], y, { size: 40, w: 900 }); });
      alpha(prog(t, 109.6 + i * .15, .3), () => text(h, hx[2], y, { size: 40, w: 900, color: C.green }));
      alpha(prog(t, tr - .3, .3), () => text(rk, hx[1], y, { size: 40, w: 700 }));
      alpha(prog(t, tr, .3), () => text(r, hx[3], y, { size: 40, w: 900, color: C.cyan }));
    });
    alpha(prog(t, 113.3, .4), () => text('MRR = (1 + 0.5 + 0.333) ÷ 3', 960, 650, { size: 44, w: 700 }));
    alpha(prog(t, 114.5, .4), () => text('≈ 0.611', 960, 735, { size: 72, w: 900, color: C.cyan }));
  });
  // not accuracy
  const nk = prog(t, 116.4, .4);
  alpha(nk, () => {
    box(560, 560, 800, 280, { fill: '#0f1b25', stroke: C.faint, lw: 2, r: 24 });
    text('정답률 61%', 960, 640, { size: 64, w: 900, color: C.ink });
    line(760, 640, lerp(760, 1160, prog(t, 117.4, .35)), 640, { color: C.red, lw: 9 });
    alpha(prog(t, 118.2, .4), () => text('정답을 얼마나 앞에서 찾았나', 960, 760, { size: 48, w: 900, color: C.cyan }));
  });
}

// ---------- M10 129.857–142.260 : Document & HOLD ----------
function M10(t) {
  background(t);
  const toHold = easeInOut((t - 137.2) / .5);
  alpha(1 - toHold, () => {
    title('근거는 원문 그대로, 출처와 함께', t, 129.9);
    // retrieved excerpt
    alpha(prog(t, 130.6), () => {
      box(220, 260, 640, 200, { fill: C.paper, r: 12 });
      text('원문 발췌', 260, 300, { size: 26, w: 700, color: '#7a6f5d', align: 'left' });
      text('과제 제출 기한은', 260, 360, { size: 36, w: 700, color: C.paperInk, align: 'left' });
      text('금요일 오후 6시입니다.', 260, 410, { size: 36, w: 900, color: C.paperInk, align: 'left' });
    });
    alpha(prog(t, 131.96), () => tag('출처: 수업 공지문 · p.1', 540, 500, { color: C.cyan, size: 28 }));
    // Document object
    const dk = prog(t, 133.98, .5);
    alpha(dk, () => {
      arrow(880, 380, 1000, 380, { color: C.dim, lw: 5 });
      box(1020, 220, 700, 420, { fill: '#1d3242', stroke: C.cyan, lw: 3, r: 20 });
      text('Document', 1060, 268, { size: 40, w: 900, color: C.cyan, align: 'left' });
      text('LangChain', 1680, 268, { size: 24, w: 500, color: C.dim, align: 'right' });
      alpha(prog(t, 134.82), () => {
        text('page_content  본문', 1060, 340, { size: 28, w: 700, color: C.amber, align: 'left' });
        box(1060, 362, 620, 70, { fill: C.paper, r: 8 });
        text('과제 제출 기한은 금요일 오후 6시입니다.', 1076, 397, { size: 27, w: 700, color: C.paperInk, align: 'left' });
      });
      alpha(prog(t, 135.36), () => {
        text('metadata  출처', 1060, 470, { size: 28, w: 700, color: C.amber, align: 'left' });
        box(1060, 492, 620, 110, { fill: '#0f1b25', r: 8 });
        text('source: "수업 공지문"', 1080, 525, { size: 27, w: 500, align: 'left' });
        text('page: 1', 1080, 568, { size: 27, w: 500, align: 'left' });
      });
    });
    alpha(prog(t, 136.0), () => text('본문과 출처를 한 객체에 함께 담는다', 960, 730, { size: 34, w: 700, color: C.dim }));
  });
  if (t < 137.2) return;
  alpha(toHold, () => {
    title('근거를 확인하지 못하면?', t, 137.3);
    // decision node
    box(760, 240, 400, 110, { fill: '#1d3242', stroke: C.ink, lw: 3, r: 55 });
    text('근거 문구 확인?', 960, 295, { size: 38, w: 900 });
    arrow(860, 352, 560, 450, { color: C.green, lw: 5, k: prog(t, 137.6, .4) });
    text('예', 680, 380, { size: 30, w: 900, color: C.green });
    alpha(prog(t, 137.9), () => { box(330, 460, 460, 120, { fill: '#1d3242', stroke: C.green, lw: 3, r: 16 }); text('원문 발췌 + 출처', 560, 520, { size: 36, w: 900 }); });
    arrow(1060, 352, 1360, 450, { color: C.red, lw: 5, k: prog(t, 138.24, .4) });
    text('아니요', 1250, 380, { size: 30, w: 900, color: C.red });
    // generation arrow broken
    alpha(prog(t, 138.64), () => {
      box(1130, 460, 460, 120, { fill: '#1d3242', stroke: C.faint, lw: 2, r: 16, dash: [10, 8] });
      text('답 생성', 1360, 520, { size: 36, w: 900, color: C.dim });
      mark(false, 1560, 470, 40);
    });
    const hk = prog(t, 139.9, .3);
    alpha(hk, () => {
      ctx.save(); ctx.translate(1360, 680); ctx.rotate(-.08); ctx.scale(lerp(1.4, 1, hk), lerp(1.4, 1, hk));
      box(-200, -70, 400, 140, { stroke: C.red, lw: 8, r: 16 });
      text('HOLD', 0, -8, { size: 76, w: 900, color: C.red });
      ctx.restore();
    });
    alpha(prog(t, 140.8), () => text('답을 지어내지 않고 보류', 1360, 800, { size: 32, w: 700, color: C.ink }));
  });
}

// ---------- M11 142.260–152.080 : HOLD limit, temperature ----------
function M11(t) {
  background(t);
  const toT = easeInOut((t - 146.7) / .5);
  alpha(1 - toT, () => {
    title('HOLD ≠ 답이 없다는 증명', t, 142.3);
    ctx.save(); ctx.translate(560, 330); ctx.rotate(-.08);
    box(-180, -64, 360, 128, { stroke: C.red, lw: 7, r: 14 }); text('HOLD', 0, -4, { size: 66, w: 900, color: C.red }); ctx.restore();
    alpha(prog(t, 143.2), () => text('문서에 답이 없다는 뜻은 아님', 560, 470, { size: 32, w: 700, color: C.ink }));
    // two split strips (redrawn, not the Flow footage)
    const sk = prog(t, 144.72, .5);
    alpha(sk, () => {
      const gap = lerp(0, 46, sk);
      box(980, 280, 360, 110, { fill: C.paper, r: 6 }); text('금요일 오', 1320 - 10, 335, { size: 46, w: 900, color: C.paperInk, align: 'right' });
      box(1340 + gap, 280, 300, 110, { fill: C.paper, r: 6 }); text('후 6시', 1360 + gap, 335, { size: 46, w: 900, color: C.paperInk, align: 'left' });
      line(1340 + gap / 2, 260, 1340 + gap / 2, 410, { color: C.red, lw: 5, dash: [12, 8] });
    });
    alpha(prog(t, 145.3), () => text('자른 자리 때문에 놓쳤을 수도', 1320, 470, { size: 32, w: 700, color: C.amber }));
  });
  if (t < 146.7) return;
  alpha(toT, () => {
    title('temperature를 낮추면', t, 147.18, { sub: '답의 무작위성에 영향을 주는 설정' });
    // slider
    const v = lerp(.9, .1, easeInOut((t - 147.7) / .8));
    const X = 260, W = 520, Y = 330;
    text('temperature', X, Y - 50, { size: 30, w: 700, color: C.dim, align: 'left' });
    line(X, Y, X + W, Y, { color: C.faint, lw: 10 });
    line(X, Y, X + W * v, Y, { color: C.cyan, lw: 10 });
    ctx.save(); ctx.fillStyle = C.ink; ctx.beginPath(); ctx.arc(X + W * v, Y, 20, 0, 7); ctx.fill(); ctx.restore();
    text('낮음', X, Y + 46, { size: 24, w: 500, color: C.dim, align: 'left' }); text('높음', X + W, Y + 46, { size: 24, w: 500, color: C.dim, align: 'right' });
    // three identical answer cards stacking
    const ck = prog(t, 148.44, .5);
    for (let i = 2; i >= 0; i--) {
      const off = lerp(i * 120, i * 14, ck);
      alpha(prog(t, 148.1, .3), () => {
        box(1000 + off, 250 + off, 560, 300, { fill: C.paper, r: 12, stroke: '#cfc4ad', lw: 2 });
        line(1040 + off, 310 + off, 1440 + off, 310 + off, { color: C.paperLine, lw: 12 });
        line(1040 + off, 370 + off, 1500 + off, 370 + off, { color: prog(t, 149.18, .3) > 0 ? C.red : C.paperLine, lw: 12 });
        line(1040 + off, 430 + off, 1380 + off, 430 + off, { color: C.paperLine, lw: 12 });
      });
    }
    alpha(ck, () => text('답이 일관돼진다', 1280, 640, { size: 34, w: 700, color: C.cyan }));
    alpha(prog(t, 149.4), () => text('틀린 근거는 그대로 틀림', 1280, 700, { size: 34, w: 700, color: C.red }));
    alpha(prog(t, 150.4, .4), () => tag('일관 ≠ 정확', 520, 560, { color: C.amber, size: 48 }));
  });
}

// ---------- M12 159.997–160.780 : end title over F06 final frame ----------
let F06LAST = null;
function M12(t) {
  if (F06LAST) ctx.drawImage(F06LAST, 0, 0, 1920, 1080); else background(t);
  const a = prog(t, 160.0, .5);
  alpha(a, () => {
    ctx.save(); const g = ctx.createLinearGradient(0, 0, 0, 400); g.addColorStop(0, 'rgba(8,14,20,.85)'); g.addColorStop(1, 'rgba(8,14,20,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, 1920, 400); ctx.restore();
    text('근거를 끊지 않는 칼질', 960, 150, { size: 84, w: 900 });
  });
}

const SCENES = { M01, M02, M03, M04, M05, M06, M07, M08, M09, M10, M11, M12 };
