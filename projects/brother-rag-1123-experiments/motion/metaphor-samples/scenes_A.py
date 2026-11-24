"""메타포 A — 무향실 계측 벤치 (흑연 계측 패널 · 앰버 7세그먼트)"""
import sys; sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import FX, RANGE, W
CSS_EXTRA = r"""
body{background:#23292F;color:#E6EAEE}
.panel{background:#2E353D;border:2px solid #A9B1BA55;border-radius:6px;box-shadow:inset 0 0 0 6px #262C32, 0 18px 40px #0006}
.eng{font-size:22px;font-weight:700;letter-spacing:4px;color:#7F8B97}
.seg{font-family:'DejaVu Sans Mono',monospace;font-weight:700;color:#FFB23E;text-shadow:0 0 18px #FFB23E88;letter-spacing:6px}
.led{width:58px;height:58px;border-radius:50%;background:#3A434D;box-shadow:inset 0 3px 6px #0008}
.lamp{white-space:nowrap;padding:6px 18px;border-radius:4px;font-weight:900;font-size:26px;letter-spacing:3px}
"""
def leds(y, color_map, t0, step, tag, name, c):
    cells = ''
    for i, ok in enumerate(color_map):
        col = '#46D483' if ok else '#FF5A4E'
        cells += (f'<div class="led" style="margin-right:22px;position:relative">'
                  f'<div data-kf="{t0+i*step:.2f}:o=0;{t0+i*step+.12:.2f}:o=1" style="position:absolute;inset:0;border-radius:50%;background:{col};box-shadow:0 0 18px {col}"></div></div>')
    return (f'<div class="abs" data-in="{t0-0.9:.2f}" style="left:180px;top:{y}px;display:flex;align-items:center">'
            f'<div style="width:300px"><div class="eng">PROBE {tag}</div><div style="font-size:44px;font-weight:900;color:{c}">{name}</div></div>{cells}'
            f'<div class="seg" style="font-size:64px;margin-left:30px"><span data-roll="{t0+len(color_map)*step:.2f}" data-v="{sum(color_map)}">0</span>/10</div></div>')
HTML = (
 '<canvas class="abs fx" width="1920" height="1080" style="left:0;top:0"></canvas>'
 # 하루 진행선 (상단, 다음 장면까지 유지)
 '<div class="abs panel" style="left:120px;top:60px;width:1680px;height:120px"></div>'
 '<div class="abs eng" style="left:160px;top:78px">11 / 23 · RUN LOG</div>'
 '<svg class="abs" style="left:160px;top:110px" width="1600" height="60"><line x1="0" y1="30" x2="1600" y2="30" stroke="#7F8B97" stroke-width="2"/>'
 + ''.join(f'<line x1="{x}" y1="22" x2="{x}" y2="38" stroke="#7F8B97"/><text x="{x}" y="58" fill="#7F8B97" font-size="16" text-anchor="middle">{h}:00</text>' for x, h in [(0,9),(369,12),(738,15),(1108,18),(1477,21)])
 + '<line x1="0" y1="30" x2="1046" y2="30" stroke="#FFB23E" stroke-width="3"/><circle cx="937" cy="30" r="9" fill="#FFB23E"/>'
 f'<path data-draw="{W["저녁"]}" data-d=".6" d="M1046 30 L1314 30" stroke="#FFB23E" stroke-width="3" fill="none"/>'
 '</svg>'
 '<div class="abs" style="left:1048px;top:84px;font-size:20px;color:#FFB23E;font-weight:700">RUN 1 · 16:36 · 91.26</div>'
 f'<div class="abs" data-pop="{W["칠시"]}" style="left:1430px;top:84px;font-size:20px;color:#FFB23E;font-weight:900">RUN 2 · 19:41</div>'
 # 비교 패널
 f'<div class="abs" data-kf="89.9:o=1;{W["저녁"]-0.2}:o=1;{W["저녁"]+0.15}:o=0" style="left:0;top:0;width:1920px;height:1080px"><div class="abs panel" style="left:120px;top:230px;width:1680px;height:600px"></div>'
 f'<div class="abs" data-in="{W["직전"]}" style="left:180px;top:262px"><div class="eng">CH 16 · 제출 직전 점검</div>'
 f'<div style="font-size:52px;font-weight:900">약한 유형 <span data-marker="{W["문항"]}" data-c="#FFB23E55">10문항</span></div></div>'
 + leds(430, [1]*10, W['열개'], .07, 'B', '하이브리드', '#FFB23E')
 + leds(600, [1,1,0,1,1,0,1,1,0,0], W['여섯개'], .07, 'C', '재정렬', '#B9A3FF')
 + f'<div class="abs lamp" data-pop="{W["하이브리드로"]}" style="left:1450px;top:270px;background:#46D483;color:#1B2A22">LOCK · 2차 = B</div>'
 f'<div class="abs" data-dim="{W["그래서"]}" style="left:170px;top:590px;width:1600px;height:80px"></div></div>'
 # 판독 패널 (2차 결과)
 f'<div class="abs" data-iris="{W["저녁"]}" data-cx="50" data-cy="55" style="left:0;top:0;width:1920px;height:1080px"><div class="abs panel" style="left:420px;top:240px;width:1080px;height:560px"></div>'
 '<div class="abs eng" style="left:470px;top:270px">RUN 2 · SCORE · COMPOSITE</div>'
 f'<div class="abs seg" style="left:470px;top:330px;font-size:230px"><span data-roll="{W["백점"]-0.6}" data-v="100" data-dec="2" data-glowp="{W["백점"]+.3}">0</span></div>'
 f'<div class="abs" data-in="{W["순위표"]}" style="left:470px;top:650px;display:flex;align-items:center;gap:24px"><div class="eng">RANK</div>'
 f'<div class="seg" style="font-size:90px">1</div><div class="lamp" data-pop="{W["일위"]}" style="background:#46D483;color:#1B2A22">PEAK</div>'
 '<div style="font-size:22px;color:#7F8B97;margin-left:20px">20:02 순위표 기준</div></div></div>'
 f'<script>{FX}</script>')
S = {'A': (*RANGE, HTML)}
