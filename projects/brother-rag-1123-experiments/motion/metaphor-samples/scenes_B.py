"""메타포 B — 레이스 텔레메트리 (피트 월·타이밍 타워·랩타임)"""
import sys; sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import FX, RANGE, W
CSS_EXTRA = r"""
body{background:linear-gradient(135deg,#121416 0%,#1B1E21 100%);color:#F2F2F2}
body:before{content:'';position:absolute;inset:0;background:repeating-linear-gradient(45deg,#ffffff06 0 2px,transparent 2px 6px)}
.tw{font-family:'DejaVu Sans Mono',monospace;font-weight:700}
.row{height:84px;display:flex;align-items:center;background:#22262A;border-left:10px solid #555;font-size:40px;font-weight:900}
.sec{width:96px;height:30px;margin-right:8px;transform:skewX(-18deg)}
.flag{font-weight:900;font-size:30px;padding:8px 22px;transform:skewX(-14deg);display:inline-block}
"""
def sectors(y, oks, t0, name, c):
    cells = ''.join(f'<div class="sec" style="background:#33383D;position:relative"><div data-kf="{t0+i*.07:.2f}:o=0;{t0+i*.07+.08:.2f}:o=1" style="position:absolute;inset:0;background:{"#2BD46A" if ok else "#FF3B30"}"></div></div>' for i, ok in enumerate(oks))
    return (f'<div class="abs" data-in="{t0-0.9:.2f}" style="left:140px;top:{y}px">'
            f'<div style="font-size:30px;font-weight:900;color:{c};margin-bottom:12px">{name}</div><div style="display:flex">{cells}'
            f'<div class="tw" style="font-size:54px;margin-left:30px;margin-top:-14px"><span data-roll="{t0+.8:.2f}" data-v="{sum(oks)}">0</span>/10</div></div></div>')
HTML = (
 '<div class="abs" style="left:0;top:0;width:1920px;height:70px;background:#FFD400;color:#111;display:flex;align-items:center;padding-left:140px;font-weight:900;font-size:30px;letter-spacing:3px">'
 'KANT · BROTHER RAG GP · 11/23</div>'
 f'<div class="abs" data-kf="89.9:o=1;{W["저녁"]-0.2}:o=1;{W["저녁"]+0.15}:o=0" style="left:0;top:0;width:1920px;height:1080px">'
 f'<div class="abs" data-in="{W["직전"]}" style="left:140px;top:120px;font-size:26px;letter-spacing:4px;color:#FFD400;font-weight:900">PRE-RACE TEST · 약한 구간 10개</div>'
 f'<div class="abs" data-in="{W["유형"]}" style="left:140px;top:160px;font-size:58px;font-weight:900">어느 세팅으로 나갈까</div>'
 + sectors(300, [1]*10, W['열개'], 'B · 하이브리드 세팅', '#FFD400')
 + sectors(480, [1,1,0,1,1,0,1,1,0,0], W['여섯개'], 'C · 재정렬 세팅', '#9AA0A6')
 + f'<div class="abs flag" data-pop="{W["하이브리드로"]}" style="left:1380px;top:250px;background:#FFD400;white-space:nowrap;color:#111">PIT CALL: SETUP B</div>'
 + f'<div class="abs" data-dim="{W["그래서"]}" style="left:130px;top:470px;width:1500px;height:120px"></div>'
 '</div>'
 # 타이밍 타워
 f'<div class="abs" data-wipe="{W["저녁"]}" data-d=".4" style="left:0;top:70px;width:1920px;height:1010px">'
 f'<div class="abs" style="left:140px;top:60px;font-size:26px;letter-spacing:4px;color:#FFD400;font-weight:900">SESSION 2 · <span data-type="{W["칠시"]}" data-cps="12">19:41</span></div>'
 '<div class="abs" style="left:140px;top:110px;width:900px;height:480px">'
 '<div class="abs tw" style="left:-4px;top:22px;font-size:40px;color:#FFD400">P1</div><div class="abs tw" style="left:-4px;top:122px;font-size:40px;color:#9AA0A6">P2</div>'
 + ''.join(f'<div class="abs row" data-kf="{W["백점"]+.2}:top={y0};{W["순위표"]+.3}:top={y1}" style="left:90px;width:810px;border-left-color:{c}">'
           f'<div style="flex:1;padding-left:30px">{n}</div><div class="tw" style="padding-right:28px">{sc}</div></div>'
           for n, y0, y1, c, p, sc in [('다른 팀', 0, 100, '#555', '', ''), ('KANT', 100, 0, '#FFD400', '', '100.00')]) +
 '</div>'
 f'<div class="abs tw" style="left:1140px;top:150px;font-size:24px;color:#9AA0A6">COMPOSITE</div>'
 f'<div class="abs tw" style="left:1140px;top:180px;font-size:180px;color:#FFD400"><span data-roll="{W["백점"]-0.6}" data-v="100" data-dec="2">0</span></div>'
 f'<div class="abs tw" data-in="{W["백점"]}" style="left:1140px;top:400px;font-size:34px;color:#9AA0A6">RUN 1  91.26  <span style="color:#2BD46A">+8.74</span></div>'
 f'<div class="abs flag" data-pop="{W["일위"]}" style="left:1140px;top:480px;background:#2BD46A;color:#111;font-size:44px">P1 · 20:02 기준</div>'
 '</div>'
 f'<script>{FX}</script>')
S = {'B': (*RANGE, HTML)}
