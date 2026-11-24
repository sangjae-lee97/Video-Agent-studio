"""효과 미리보기: python scripts/motion/render.py scripts/motion/effects_demo_scenes.py outputs/fx-demo --preview
장면 A(0~3초): dust·burst·ripple·comet + pop·sheen·roll·type. 장면 B(3~6초): flow·converge·grain + blurin·glowp·wipe·shake.
장면 C(6~10초): cam·pan(패럴랙스)·follow·iris·marker·strike·flipin·split·morph.
장면 D(10~13초): kf(PPT 모프식 상태 보간) — 같은 카드 3개가 자리·크기·색을 바꾸며 순위 변경.
문서: docs/MOTION_EFFECTS_LIBRARY.md"""
from pathlib import Path
FX = (Path(__file__).resolve().parent / 'effects.js').read_text(encoding='utf-8')
CSS_EXTRA = 'body{background:#23292F;color:#E6EAEE}'
cv = '<canvas class="abs fx" width="1920" height="1080" style="left:0;top:0"></canvas>'
S = {}
S['A'] = (0, 72, cv +
 '<i class="fxp" data-fx="dust" data-t="0"></i>'
 '<i class="fxp" data-fx="burst" data-t="1.0" data-x="480" data-y="400"></i>'
 '<i class="fxp" data-fx="ripple" data-t="0.8" data-x="1440" data-y="400"></i>'
 '<i class="fxp" data-fx="comet" data-t="0.5" data-path="100,900 900,700 1800,880" data-dur="1.4"></i>'
 '<div class="abs card" data-sheen="1.2" data-pop="0.2" style="left:300px;top:560px;width:600px;height:200px;background:#2E353D;color:#fff;font-size:90px;font-weight:900;display:flex;align-items:center;justify-content:center"><span data-roll="0.4" data-v="91.26" data-dec="2">0</span></div>'
 '<div class="abs" data-type="0.3" style="left:1100px;top:600px;font-size:60px;font-weight:900">버전 4.4</div>'
 f'<script>{FX}</script>')
S['B'] = (72, 144, cv +
 '<i class="fxp" data-fx="flow" data-t="3" data-c="#6EC6FF"></i>'
 '<i class="fxp" data-fx="converge" data-t="3.2" data-x="760" data-y="420" data-w="400" data-h="160"></i>'
 '<i class="fxp" data-fx="grain" data-t="3"></i>'
 '<div class="abs" data-blurin="4.0" data-glowp="4.3" style="left:760px;top:420px;font-size:140px;font-weight:900;color:#FFB23E">100.00</div>'
 '<div class="abs" data-wipe="3.5" data-shake="4.6" style="left:600px;top:700px;font-size:60px;font-weight:900">1,512 → 1,528</div>'
 f'<script>{FX}</script>')

S['C'] = (144, 240,
 '<div class="abs" data-cam="6:1,960,540; 7.6:1.6,700,420; 9.2:1,960,540" style="left:0;top:0;width:1920px;height:1080px">'
 '<div class="abs" data-pan="6,10,-160,0" style="left:0;top:820px;width:2400px;height:40px;background:repeating-linear-gradient(90deg,#3A434D 0 60px,transparent 60px 120px)"></div>'
 '<div class="abs" data-pan="6,10,-60,0" style="left:120px;top:140px;font-size:34px;color:#7F8B97">배경층(느리게)</div>'
 '<div class="abs" data-flipin="6.3" style="left:200px;top:300px;width:460px;height:240px;background:#2E353D;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:56px;font-weight:900">v4.3 → v4.4</div>'
 '<div class="abs" style="left:760px;top:320px;font-size:64px;font-weight:900"><span data-marker="6.8" data-c="#FFB23E66">인쇄</span> 49 dB · <span data-strike="7.4">대기 30 dB</span></div>'
 '<div class="abs" data-split="7.9" style="left:760px;top:440px;font-size:52px;font-weight:700">페이지가 아니라 표의 한 줄</div>'
 '<div class="abs" data-follow="6.5" data-d="1.6" data-path="200,700 900,620 1700,720" style="width:34px;height:34px;border-radius:50%;background:#FFB23E"></div>'
 '<svg class="abs" style="left:1450px;top:560px" width="300" height="220"><path data-morph="8.2" data-to="M20 110 L150 20 L280 110 L150 200 Z" d="M20 20 L280 20 L280 200 L20 200 Z" fill="#6EC6FF"/></svg>'
 '</div>'
 '<div class="abs" data-iris="8.8" data-cx="50" data-cy="50" style="left:0;top:0;width:1920px;height:1080px;background:#46D483;display:flex;align-items:center;justify-content:center;font-size:120px;font-weight:900;color:#23292F">100.00</div>'
 f'<script>{FX}</script>')

S['D'] = (240, 312,
 ''.join(f'<div class="abs" data-kf="10.3:left=200,top={250+i*170},w={w},h=120,bg=#2E353D; 11.3:left=200,top={250+j*170},w={w2},h=120,bg={c}; 12.6:left=200,top={250+j*170},w={w2},h=120,bg={c}" '
         f'style="border-radius:6px;display:flex;align-items:center;padding-left:30px;font-size:48px;font-weight:900">{n}</div>'
         for i,(n,w,j,w2,c) in enumerate([('A 벡터',900,2,700,'#3A434D'),('B 하이브리드',1100,0,1500,'#B07A1E'),('C 재정렬',1000,1,1200,'#3A434D')]))
 + f'<script>{FX}</script>')
