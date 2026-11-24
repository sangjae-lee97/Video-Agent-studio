"""메타포 C — 기록 재생 관제실 (레이더 스윕·타임코드·이벤트 로그)"""
import sys; sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import FX, RANGE, W
CSS_EXTRA = r"""
body{background:radial-gradient(1400px 900px at 50% 45%,#0F1A15 0%,#070B09 70%);color:#CFF7DD}
.mono{font-family:'DejaVu Sans Mono',monospace}
.ph{color:#39FF88;text-shadow:0 0 12px #39FF8888}
.am{color:#FFB547;text-shadow:0 0 12px #FFB54788}
.scan:after{content:'';position:absolute;inset:0;background:repeating-linear-gradient(0deg,#0000 0 3px,#00000040 3px 4px);pointer-events:none}
"""
RADAR = r"""<script>window.extra=T=>{const c=document.getElementById('rad');if(!c)return;const x=c.getContext('2d');x.clearRect(0,0,700,700);
x.strokeStyle='#39FF8833';x.lineWidth=2;for(let r=80;r<=320;r+=80){x.beginPath();x.arc(350,350,r,0,6.283);x.stroke();}
x.beginPath();x.moveTo(30,350);x.lineTo(670,350);x.moveTo(350,30);x.lineTo(350,670);x.stroke();
const a=(T*1.4)%6.283;for(let k=0;k<40;k++){x.strokeStyle=`rgba(57,255,136,${0.5*(1-k/40)})`;x.beginPath();x.moveTo(350,350);x.lineTo(350+320*Math.cos(a-k*.02),350+320*Math.sin(a-k*.02));x.stroke();}
const blips=[[93.84,250,-60,'B'],[95.46,-170,120,'C'],[102.06,40,-210,'#2']];blips.forEach(([t,bx,by,l])=>{if(T<t)return;const p=Math.min(1,(T-t)/.4);const col=l==='C'?'255,90,78':'57,255,136';
x.fillStyle=`rgba(${col},${0.9})`;x.beginPath();x.arc(350+bx,350+by,8,0,6.283);x.fill();x.strokeStyle=`rgba(${col},${1-p})`;x.beginPath();x.arc(350+bx,350+by,8+40*p,0,6.283);x.stroke();
x.fillStyle=`rgb(${col})`;x.font='bold 22px DejaVu Sans Mono';x.fillText(l,350+bx+14,350+by+6);});};</script>"""
def tc(T):
    return ''
LOG = [(W['직전'], '19:34  PRECHECK  약한 유형 10문항 대조', 'ph'),
       (W['열개'], '      PROBE B 하이브리드 ......... 10/10  PASS', 'ph'),
       (W['여섯개'], '      PROBE C 재정렬 ............  6/10  FAIL', 'am'),
       (W['하이브리드로'], '      DECISION  2차 제출 구성 = B', 'ph'),
       (W['칠시'], '19:41  SUBMIT #2  v4.7 · B · 49d3e58', 'ph'),
       (W['백점'], '      SCORE  COMPOSITE 100.00', 'ph'),
       (W['일위'], '20:02  RANK  1', 'ph')]
HTML = (
 '<div class="abs scan" style="left:0;top:0;width:1920px;height:1080px">'
 '<div class="abs mono ph" style="left:110px;top:60px;font-size:24px;letter-spacing:4px">REPLAY · 2026-11-23 · RUN LOG</div>'
 '<div class="abs mono am" style="left:1350px;top:52px;font-size:40px;font-weight:700">TC <span data-kf="89.9:o=1">▶</span> '
 f'<span data-type="{W["저녁"]}" data-cps="20">19:41:00:00</span></div>'
 '<canvas id="rad" class="abs" width="700" height="700" style="left:1120px;top:180px"></canvas>'
 + RADAR +
 '<div class="abs mono" style="left:110px;top:170px;width:960px;font-size:28px;line-height:1.9">'
 + ''.join(f'<div class="{c}" data-type="{t:.2f}" data-cps="38" style="white-space:pre">{s}</div>' for t, s, c in LOG) +
 '</div>'
 f'<div class="abs mono ph" data-blurin="{W["백점"]}" style="left:110px;top:720px;font-size:170px;font-weight:700">100.00</div>'
 f'<div class="abs mono" data-in="{W["순위표"]}" style="left:780px;top:800px;font-size:30px;color:#7FA88F">RUN 1 · 16:36 · 91.26</div>'
 '</div>'
 f'<script>{FX}</script>')
S = {'C': (*RANGE, HTML)}
