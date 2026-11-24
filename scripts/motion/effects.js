/* 모션그래픽 효과 모음 (모든 편 공통, 선택 사용) — docs/MOTION_EFFECTS_LIBRARY.md 참고.

규칙: 모든 효과는 "시각 T(초)만으로 화면이 정해지는" 순수 함수다. 렌더러는 프레임을 순서 없이(미리보기는 마지막
프레임만) 그리므로 이전 프레임 상태·Math.random()·requestAnimationFrame을 쓰지 않는다. 난수는 seed로 고정한다.

사용(편의 motion/scenes.py):
  from pathlib import Path
  FX = (Path(__file__).resolve().parents[3] / 'scripts/motion/effects.js').read_text(encoding='utf-8')
  html = '<canvas class="abs fx" width="1920" height="1080" style="left:0;top:0"></canvas>' + ... + FX를 script 태그로 감싸 html 맨 끝에 붙인다
  (이 파일 안에는 닫는 script 태그 문자열을 절대 쓰지 않는다 — 브라우저가 거기서 스크립트를 끊는다)
  그리고 아래 data-fx 속성을 단 요소를 배치한다. 장면 자체의 window.extra가 있으면 FX가 감싸서 함께 호출한다.

캔버스 효과 (<i class="fxp" data-fx="종류" data-t="시작초" ...> — 화면에 보이지 않는 마커 요소. 첫 .fx 캔버스에 그린다)
  dust      떠다니는 먼지(배경 깊이감)       data-n=60 data-c="#fff" data-a=.25(최대 불투명) data-dur=끝까지
  burst     한 점에서 터지는 불꽃(확정·통과)  data-x data-y data-n=28 data-c data-r=180(도달 반경) data-dur=.9
  converge  흩어진 점이 목표로 모임(형성)     data-x data-y data-w data-h(목표 사각형) data-n=80 data-c data-dur=1.1
  comet     경로를 따라가는 빛+꼬리(흐름)     data-path="x1,y1 x2,y2 ..." data-c data-dur=1.0 data-tail=.18(경로 비율)
  flow      흐르는 입자장(데이터 흐름 배경)   data-n=220 data-c data-a=.5 data-speed=60 data-dur
  ripple    동심원 파문(신호·탐지)           data-x data-y data-c data-n=3(겹) data-r=220 data-dur=1.2
  grain     필름 그레인(질감)               data-a=.06  (매 프레임 seed가 바뀌는 노이즈, 결정적)
DOM 효과 (일반 요소에 속성)
  data-sheen="t"        표면을 가로지르는 빛 반사 1회(0.7초). 요소에 position 필요(.abs 등)
  data-shake="t"        임팩트 흔들림 0.35초(data-amp=10)
  data-pop="t"          스프링 등장(오버슈트 후 정착, 0.6초) — data-in 대신 사용
  data-type="t"         타자 치듯 글자 등장(data-cps=18 초당 글자)
  data-roll="t" data-v  자릿수 롤링 숫자(오도미터) data-from(시작값, 기본 0) data-dec data-suf data-comma(천 단위 쉼표), 0.9초
  data-glowp="t"        발광 맥박 2회(data-c), 강조 후 잦아듦
  data-wipe="t"         왼→오 드러내기(clip-path), data-d=.5
  data-blurin="t"       초점이 맞으며 등장(blur 14px→0), 0.5초
카메라·공간 (장면을 감싼 무대 요소에)
  data-cam="t:s,x,y; t:s,x,y ..."  키프레임 카메라. s=배율, x,y=화면 중심에 올 무대 좌표(px). 구간마다 easeInOut
  data-pan="t0,t1,dx,dy"           t0→t1 동안 dx,dy만큼 이동(층마다 다른 값 = 2.5D 패럴랙스)
  data-follow="t" data-path="x,y x,y ..." data-d=1  요소 중심이 경로를 따라 이동
가리기·드러내기
  data-iris="t" data-cx=50 data-cy=50 data-d=.6   원형 마스크로 열림(% 좌표)
  data-marker="t" data-c="#FFE27A" data-d=.45     형광펜이 글자 뒤를 왼→오로 칠함
  data-strike="t" data-c="#FF5A4E" data-d=.35     취소선이 그어짐(정정·폐기)
  data-flipin="t"                                 카드가 세로축으로 돌며 등장(0.6초)
상태 보간 (PowerPoint 모프·Keynote 매직 무브와 같은 개념: 같은 요소의 A 상태 → B 상태)
  data-kf="t:left=200,top=300,w=400,h=120,bg=#2E353D,o=1,r=0,s=1; t:left=900,...,bg=#46D483"
     키: left top w h(px), o(불투명도), r(회전°), s(배율), bg/c(색, #RRGGBB), fs(글자 px). 구간마다 easeInOut
타이포
  data-split="t" data-stagger=.06                  단어마다 차례로 떠오름(공백 기준)
도형
  <path data-morph="t" data-to="목표 d" data-d=.8>   두 경로의 숫자를 보간(명령 구성·개수가 같아야 함)
*/
(function () {
  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  const eo = x => 1 - Math.pow(1 - clamp(x), 3);              // easeOutCubic
  const eio = x => { x = clamp(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
  const spring = x => { x = clamp(x); return 1 - Math.exp(-6 * x) * Math.cos(10 * x); }; // 오버슈트 후 정착
  function rng(seed) { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  const num = (e, k, d) => (e.dataset[k] !== undefined ? +e.dataset[k] : d);
  const hex = (c, a) => { const h = c.replace('#', ''); const v = parseInt(h.length === 3 ? h.split('').map(x => x + x).join('') : h, 16); return `rgba(${v >> 16 & 255},${v >> 8 & 255},${v & 255},${a})`; };

  function dot(ctx, x, y, r, c, a) { if (a <= 0) return; ctx.fillStyle = hex(c, a); ctx.beginPath(); ctx.arc(x, y, r, 0, 6.2832); ctx.fill(); }

  const CANVAS = {
    dust(ctx, e, T, t0, i) {
      const n = num(e, 'n', 60), c = e.dataset.c || '#ffffff', A = num(e, 'a', .25), R = rng(1000 + i);
      const fade = eo((T - t0) / .8);
      for (let k = 0; k < n; k++) {
        const x0 = R() * 1920, y0 = R() * 1080, sp = 6 + R() * 18, ph = R() * 6.28, r = .8 + R() * 2.2, depth = R();
        const x = (x0 + Math.sin(T * .3 + ph) * 30 + T * sp * (depth - .3) + 1920) % 1920;
        const y = (y0 - T * sp * .5 * depth + 2160) % 1080;
        dot(ctx, x, y, r, c, A * fade * (.35 + .65 * depth) * (.6 + .4 * Math.sin(T * 1.7 + ph)));
      }
    },
    burst(ctx, e, T, t0, i) {
      const p = (T - t0) / num(e, 'dur', .9); if (p < 0 || p > 1) return;
      const n = num(e, 'n', 28), x = num(e, 'x', 960), y = num(e, 'y', 540), c = e.dataset.c || '#FFB23E', Rmax = num(e, 'r', 180), R = rng(2000 + i);
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      for (let k = 0; k < n; k++) {
        const ang = (k / n) * 6.2832 + R() * .4, d = Rmax * (.55 + R() * .45) * eo(p), g = 40 * p * p;
        const px = x + Math.cos(ang) * d, py = y + Math.sin(ang) * d + g;
        const tail = Math.max(0, d - 26 * (1 - p));
        ctx.strokeStyle = hex(c, (1 - p) * .9); ctx.lineWidth = 2.5 * (1 - p) + .5;
        ctx.beginPath(); ctx.moveTo(x + Math.cos(ang) * tail, y + Math.sin(ang) * tail + g); ctx.lineTo(px, py); ctx.stroke();
        dot(ctx, px, py, 2.6 * (1 - p) + .6, c, 1 - p);
      }
      ctx.restore();
    },
    converge(ctx, e, T, t0, i) {
      const p = (T - t0) / num(e, 'dur', 1.1); if (p < 0) return;
      const n = num(e, 'n', 80), tx = num(e, 'x', 960), ty = num(e, 'y', 540), w = num(e, 'w', 300), h = num(e, 'h', 120), c = e.dataset.c || '#FFB23E', R = rng(3000 + i);
      const fadeOut = p > 1 ? 1 - clamp((p - 1) / .4) : 1; if (fadeOut <= 0) return;
      for (let k = 0; k < n; k++) {
        const sx = R() * 1920, sy = R() * 1080, ex = tx + R() * w, ey = ty + R() * h, delay = R() * .35;
        const q = eio((clamp(p, 0, 1) - delay) / (1 - delay));
        const bend = Math.sin(q * 3.1416) * (R() - .5) * 160;
        dot(ctx, sx + (ex - sx) * q + bend, sy + (ey - sy) * q - bend * .5, 2.2, c, (.25 + .75 * q) * fadeOut);
      }
    },
    comet(ctx, e, T, t0, i) {
      const pts = (e.dataset.path || '0,540 1920,540').trim().split(/\s+/).map(s => s.split(',').map(Number));
      const dur = num(e, 'dur', 1.0), tail = num(e, 'tail', .18), c = e.dataset.c || '#FFB23E';
      const p = (T - t0) / dur; if (p < 0 || p > 1 + tail) return;
      const seg = []; let L = 0; for (let k = 1; k < pts.length; k++) { const d = Math.hypot(pts[k][0] - pts[k - 1][0], pts[k][1] - pts[k - 1][1]); seg.push(d); L += d; }
      const at = s => { s = clamp(s) * L; for (let k = 0; k < seg.length; k++) { if (s <= seg[k] || k === seg.length - 1) { const f = seg[k] ? s / seg[k] : 0; return [pts[k][0] + (pts[k + 1][0] - pts[k][0]) * f, pts[k][1] + (pts[k + 1][1] - pts[k][1]) * f]; } s -= seg[k]; } };
      const head = eio(Math.min(p, 1));
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      const steps = 40; for (let k = 0; k < steps; k++) {
        const s = head - tail * (k / steps); if (s < 0) break; const [x, y] = at(s);
        dot(ctx, x, y, 6 * (1 - k / steps) + 1, c, .5 * (1 - k / steps) * (p > 1 ? 1 - (p - 1) / tail : 1));
      }
      const [hx, hy] = at(head); ctx.shadowColor = c; ctx.shadowBlur = 24; dot(ctx, hx, hy, 7, c, p > 1 ? 1 - (p - 1) / tail : 1);
      ctx.restore();
    },
    flow(ctx, e, T, t0, i) {
      const n = num(e, 'n', 220), c = e.dataset.c || '#7F8B97', A = num(e, 'a', .5), sp = num(e, 'speed', 60), R = rng(4000 + i);
      const fade = eo((T - t0) / .8); const dt = T - t0; if (dt < 0) return;
      const field = (x, y) => Math.sin(x * .0023 + y * .0011) * 1.2 + Math.cos(y * .0031 - x * .0007) * .8; // 결정적 각도장
      for (let k = 0; k < n; k++) {
        let x = R() * 1920, y = R() * 1080; const life = 2 + R() * 3, ph = R() * life;
        const age = (dt + ph) % life; // 수명 순환
        const steps = Math.floor(age * 12); for (let s = 0; s < steps; s++) { const a = field(x, y); x += Math.cos(a) * sp / 12; y += Math.sin(a) * sp / 12; }
        const lf = age / life, la = lf < .15 ? lf / .15 : lf > .8 ? (1 - lf) / .2 : 1;
        const a = field(x, y); ctx.strokeStyle = hex(c, A * fade * la); ctx.lineWidth = 1.6;
        ctx.beginPath(); ctx.moveTo(x - Math.cos(a) * 14, y - Math.sin(a) * 14); ctx.lineTo(x, y); ctx.stroke();
      }
    },
    ripple(ctx, e, T, t0, i) {
      const dur = num(e, 'dur', 1.2), n = num(e, 'n', 3), x = num(e, 'x', 960), y = num(e, 'y', 540), Rm = num(e, 'r', 220), c = e.dataset.c || '#FFB23E';
      for (let k = 0; k < n; k++) { const p = (T - t0 - k * .22) / dur; if (p < 0 || p > 1) continue;
        ctx.strokeStyle = hex(c, (1 - p) * .8); ctx.lineWidth = 3 * (1 - p) + .5; ctx.beginPath(); ctx.arc(x, y, Rm * eo(p), 0, 6.2832); ctx.stroke(); }
    },
    grain(ctx, e, T) {
      const A = num(e, 'a', .06), R = rng(Math.floor(T * 24) + 7);
      for (let k = 0; k < 2600; k++) { const v = R() > .5 ? 255 : 0; ctx.fillStyle = `rgba(${v},${v},${v},${A * R()})`; ctx.fillRect(R() * 1920, R() * 1080, 2, 2); }
    },
  };

  function domFX(T) {
    const q = (s, f) => document.querySelectorAll(s).forEach(f);
    q('[data-sheen]', e => { const p = (T - +e.dataset.sheen) / .7; let s = e.querySelector(':scope>.fx-sheen');
      if (!s) { s = document.createElement('i'); s.className = 'fx-sheen'; s.style.cssText = 'position:absolute;inset:0;pointer-events:none;border-radius:inherit;mix-blend-mode:screen'; e.style.overflow = 'hidden'; e.appendChild(s); }
      const x = -40 + 180 * eio(p); s.style.opacity = p > 0 && p < 1 ? 1 : 0;
      s.style.background = `linear-gradient(105deg,transparent ${x - 18}%,rgba(255,255,255,.55) ${x}%,transparent ${x + 18}%)`; });
    q('[data-shake]', e => { const p = (T - +e.dataset.shake) / .35, amp = num(e, 'amp', 10);
      const d = p > 0 && p < 1 ? amp * (1 - p) * Math.sin(p * 40) : 0; e.style.translate = `${d}px ${d * .4}px`; });
    q('[data-pop]', e => { const p = (T - +e.dataset.pop) / .6; const s = p <= 0 ? 0 : spring(p);
      e.style.opacity = clamp(p * 3); e.style.transform = (e.dataset.base || '') + ` scale(${s})`; });
    q('[data-type]', e => { if (e.dataset.full === undefined) e.dataset.full = e.textContent; const full = e.dataset.full;
      const k = Math.max(0, Math.floor((T - +e.dataset.type) * num(e, 'cps', 18))); e.textContent = full.slice(0, k); });
    q('[data-roll]', e => { const p = eo((T - +e.dataset.roll) / .9), v = +e.dataset.v, dec = num(e, 'dec', 0);
      const fmt = x => e.dataset.comma !== undefined ? x.toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec }) : x.toFixed(dec);
      const f = num(e, 'from', 0); const s = fmt(f + (v - f) * p); const target = fmt(v);
      // 자릿수 고정폭: 목표값 자릿수에 맞춰 앞을 0으로 채우지 않고, 끝까지 굴러간 뒤 정확히 목표값
      e.textContent = (p >= 1 ? target : s) + (e.dataset.suf || ''); e.style.fontVariantNumeric = 'tabular-nums'; });
    q('[data-glowp]', e => { const p = (T - +e.dataset.glowp) / 1.4, c = e.dataset.c || '#FFB23E';
      const g = p > 0 && p < 1 ? Math.abs(Math.sin(p * 6.2832)) * (1 - p) : 0;
      e.style.filter = `drop-shadow(0 0 ${g * 26}px ${c})`; });
    q('[data-wipe]', e => { const p = eio((T - +e.dataset.wipe) / num(e, 'd', .5)); e.style.clipPath = `inset(0 ${100 - p * 100}% 0 0)`; });
    q('[data-blurin]', e => { const p = eo((T - +e.dataset.blurin) / .5); e.style.opacity = p; e.style.filter = `blur(${(1 - p) * 14}px)`; });
  }


  function kf(spec) { return spec.split(';').map(x => x.trim()).filter(Boolean).map(x => { const [t, v] = x.split(':'); return [+t, v.split(',').map(Number)]; }).sort((a, b) => a[0] - b[0]); }
  function kfAt(K, T) { if (T <= K[0][0]) return K[0][1]; for (let i = 1; i < K.length; i++) if (T <= K[i][0]) { const [a, va] = K[i - 1], [b, vb] = K[i]; const p = eio((T - a) / (b - a)); return va.map((v, j) => v + (vb[j] - v) * p); } return K[K.length - 1][1]; }
  function pathPts(s) { return s.trim().split(/\s+/).map(q => q.split(',').map(Number)); }
  function along(P, u) { const seg = []; let L = 0; for (let k = 1; k < P.length; k++) { const d = Math.hypot(P[k][0] - P[k - 1][0], P[k][1] - P[k - 1][1]); seg.push(d); L += d; } let s = clamp(u) * L; for (let k = 0; k < seg.length; k++) { if (s <= seg[k] || k === seg.length - 1) { const f = seg[k] ? Math.min(1, s / seg[k]) : 0; return [P[k][0] + (P[k + 1][0] - P[k][0]) * f, P[k][1] + (P[k + 1][1] - P[k][1]) * f]; } s -= seg[k]; } return P[0]; }

  function spaceFX(T) {
    const q = (s, f) => document.querySelectorAll(s).forEach(f);
    q('[data-cam]', e => { const K = e._k || (e._k = kf(e.dataset.cam)); const [sc, x, y] = kfAt(K, T);
      e.style.transformOrigin = '0 0'; e.style.transform = `translate(${960 - x * sc}px,${540 - y * sc}px) scale(${sc})`; });
    q('[data-pan]', e => { const [a, b, dx, dy] = e.dataset.pan.split(',').map(Number); const p = eio((T - a) / (b - a)); e.style.translate = `${dx * p}px ${dy * p}px`; });
    q('[data-follow]', e => { const P = e._p || (e._p = pathPts(e.dataset.path)); const [x, y] = along(P, eio((T - +e.dataset.follow) / num(e, 'd', 1)));
      e.style.left = (x - e.offsetWidth / 2) + 'px'; e.style.top = (y - e.offsetHeight / 2) + 'px'; });
    q('[data-iris]', e => { const p = eio((T - +e.dataset.iris) / num(e, 'd', .6)); e.style.clipPath = `circle(${p * 150}% at ${num(e, 'cx', 50)}% ${num(e, 'cy', 50)}%)`; });
    q('[data-marker]', e => { const p = eo((T - +e.dataset.marker) / num(e, 'd', .45)), c = e.dataset.c || '#FFE27A';
      e.style.backgroundImage = `linear-gradient(${c},${c})`; e.style.backgroundRepeat = 'no-repeat'; e.style.backgroundPosition = '0 70%'; e.style.backgroundSize = `${p * 100}% 45%`; });
    q('[data-strike]', e => { let l = e.querySelector(':scope>.fx-strike'); if (!l) { l = document.createElement('i'); l.className = 'fx-strike'; l.style.cssText = 'position:absolute;left:-2%;top:52%;height:.09em;border-radius:.05em;pointer-events:none'; if (getComputedStyle(e).position === 'static') e.style.position = 'relative'; e.appendChild(l); }
      const p = eo((T - +e.dataset.strike) / num(e, 'd', .35)); l.style.background = e.dataset.c || '#FF5A4E'; l.style.width = (p * 104) + '%'; });
    q('[data-flipin]', e => { const p = eo((T - +e.dataset.flipin) / .6); e.style.opacity = p > 0 ? 1 : 0; e.style.transform = (e.dataset.base || '') + ` perspective(1200px) rotateY(${(1 - p) * 90}deg)`; });
    q('[data-split]', e => { if (!e._w) { const words = e.textContent.split(/(\s+)/); e.textContent = ''; e._w = words.map(w => { const sp = document.createElement('span'); sp.textContent = w; sp.style.display = 'inline-block'; sp.style.whiteSpace = 'pre'; e.appendChild(sp); return sp; }).filter(sp => sp.textContent.trim()); }
      const t0 = +e.dataset.split, st = num(e, 'stagger', .06); e._w.forEach((sp, i) => { const p = eo((T - t0 - i * st) / .4); sp.style.opacity = p; sp.style.transform = `translateY(${(1 - p) * .45}em)`; }); });
    q('path[data-morph]', e => { if (!e._a) { const re = /-?\d*\.?\d+(?:e-?\d+)?/g; e._from = e.getAttribute('d'); e._a = (e._from.match(re) || []).map(Number); e._b = (e.dataset.to.match(re) || []).map(Number); e._ok = e._a.length === e._b.length; }
      if (!e._ok) return; const p = eio((T - +e.dataset.morph) / num(e, 'd', .8)); let i = 0;
      e.setAttribute('d', e._from.replace(/-?\d*\.?\d+(?:e-?\d+)?/g, () => { const v = e._a[i] + (e._b[i] - e._a[i]) * p; i++; return v.toFixed(2); })); });
  }


  const toRGB = h => { h = h.replace('#', ''); const v = parseInt(h, 16); return [v >> 16 & 255, v >> 8 & 255, v & 255]; };
  function kfState(spec) { return spec.split(';').map(x => x.trim()).filter(Boolean).map(x => { const i = x.indexOf(':'); const t = +x.slice(0, i); const o = {};
      x.slice(i + 1).split(',').forEach(kv => { const [k, v] = kv.split('=').map(z => z.trim()); o[k] = v.startsWith('#') ? toRGB(v) : +v; }); return [t, o]; }).sort((a, b) => a[0] - b[0]); }
  function stateAt(K, T) { let a = K[0], b = K[0], p = 0; if (T >= K[K.length - 1][0]) { a = b = K[K.length - 1]; } else if (T > K[0][0]) { for (let i = 1; i < K.length; i++) if (T <= K[i][0]) { a = K[i - 1]; b = K[i]; p = eio((T - a[0]) / (b[0] - a[0])); break; } }
    const o = {}; for (const k in a[1]) { const va = a[1][k], vb = b[1][k] !== undefined ? b[1][k] : va; o[k] = Array.isArray(va) ? va.map((v, j) => Math.round(v + (vb[j] - v) * p)) : va + (vb - va) * p; } return o; }
  function kfFX(T) {
    document.querySelectorAll('[data-kf]').forEach(e => { const K = e._kf || (e._kf = kfState(e.dataset.kf)); const o = stateAt(K, T), st = e.style;
      if (o.left !== undefined) st.left = o.left + 'px'; if (o.top !== undefined) st.top = o.top + 'px';
      if (o.w !== undefined) st.width = o.w + 'px'; if (o.h !== undefined) st.height = o.h + 'px';
      if (o.o !== undefined) st.opacity = o.o; if (o.fs !== undefined) st.fontSize = o.fs + 'px';
      if (o.bg) st.background = `rgb(${o.bg})`; if (o.c) st.color = `rgb(${o.c})`;
      if (o.r !== undefined || o.s !== undefined) st.transform = (e.dataset.base || '') + ` rotate(${o.r || 0}deg) scale(${o.s === undefined ? 1 : o.s})`; });
  }

  function canvasFX(T) {
    const cv = document.querySelector('canvas.fx'); if (!cv) return;
    const ctx = cv.getContext('2d'); ctx.clearRect(0, 0, cv.width, cv.height);
    document.querySelectorAll('.fxp[data-fx]').forEach((e, i) => { const f = CANVAS[e.dataset.fx]; const t0 = num(e, 't', 0);
      const end = e.dataset.until !== undefined ? +e.dataset.until : Infinity;
      if (f && T >= t0 && T <= end) { ctx.save(); f(ctx, e, T, t0, i); ctx.restore(); } });
  }

  const prev = window.extra && window.extra._fx ? window.extra._base : window.extra; // FX가 두 번 실려도 한 번만 실행
  const run = T => { if (prev) prev(T); kfFX(T); spaceFX(T); domFX(T); canvasFX(T); };
  run._fx = true; run._base = prev; window.extra = run;
  window.FX = { rng, eo, eio, spring, CANVAS, kf, kfAt, along };
})();
