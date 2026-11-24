"""Brother RAG 실험 기록 11/23 — 모션그래픽 M01~M16 (메타포: 무향실 계측 벤치, template-spec.md)

시각은 편 타임라인 절대 초(보정 WAV narration/local-short-window-v1/narration_balanced.wav 기준).
단어 시각은 narration/local-short-window-v1/asr-words.json. 렌더:
  python scripts/motion/render.py projects/brother-rag-1123-experiments/motion/scenes.py projects/brother-rag-1123-experiments/motion/out
"""
from pathlib import Path

FX = (Path(__file__).resolve().parents[3] / 'scripts/motion/effects.js').read_text(encoding='utf-8')
FPS = 24
AMB, GRN, RED, BLU, LIL, MUT, INK = '#FFB23E', '#46D483', '#FF5A4E', '#6EC6FF', '#B9A3FF', '#7F8B97', '#E6EAEE'

CSS_EXTRA = r"""
body{background:radial-gradient(1300px 900px at 50% 40%,#2A3138 0%,#20252B 70%);color:#E6EAEE}
body:before{content:'';position:absolute;inset:0;opacity:.05;
 background:repeating-linear-gradient(90deg,#fff 0 1px,transparent 1px 64px),repeating-linear-gradient(0deg,#fff 0 1px,transparent 1px 64px)}
.panel{background:#2E353D;border:2px solid #A9B1BA55;border-radius:6px;box-shadow:inset 0 0 0 6px #262C32,0 18px 40px #0006}
.eng{font-size:22px;font-weight:700;letter-spacing:4px;color:#7F8B97;white-space:nowrap}
.seg{font-family:'DejaVu Sans Mono',monospace;font-weight:700;color:#FFB23E;text-shadow:0 0 18px #FFB23E66;letter-spacing:4px;white-space:nowrap}
.led{width:46px;height:46px;border-radius:50%;background:#3A434D;box-shadow:inset 0 3px 6px #0008;position:relative;flex:none}
.lamp{white-space:nowrap;padding:6px 18px;border-radius:4px;font-weight:900;font-size:26px;letter-spacing:3px}
.chip{background:#262C32;border:2px solid #4A535D;border-radius:4px;display:flex;align-items:center;gap:14px;padding:0 18px;white-space:nowrap}
.tag{font-size:20px;font-weight:700;padding:3px 10px;border-radius:3px;white-space:nowrap}
.h1{font-size:54px;font-weight:900;white-space:nowrap}
.full{left:0;top:0;width:1920px;height:1080px}
"""


def F(t):
    return round(t * FPS)


def scene(a, b, html):
    return (F(a), F(b), f'<div class="abs full">{html}</div><script>{FX}</script>')


def panel(x, y, w, h, extra=''):
    return f'<div class="abs panel" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px" {extra}></div>'


def txt(x, y, s, t=None, cls='', style='', attr=''):
    a = f' data-in="{t}"' if t is not None else ''
    return f'<div class="abs {cls}"{a} {attr} style="left:{x}px;top:{y}px;{style}">{s}</div>'


def leds(x, y, n, on, t0, step=.06, col=GRN, off_col=None, size=46, gap=16):
    """n개 표시등. 앞 on개는 col로, 나머지는 off_col(없으면 꺼진 채)로 차례 점등."""
    out = ''
    for i in range(n):
        c = col if i < on else off_col
        inner = (f'<div data-kf="{t0+i*step:.2f}:o=0;{t0+i*step+.1:.2f}:o=1" style="position:absolute;inset:0;border-radius:50%;'
                 f'background:{c};box-shadow:0 0 14px {c}"></div>') if c else ''
        out += f'<div class="led" style="width:{size}px;height:{size}px;margin-right:{gap}px">{inner}</div>'
    return f'<div class="abs" style="left:{x}px;top:{y}px;display:flex">{out}</div>'


# 상단 하루 진행선 (M03·M07·M11에서 같은 위치·같은 눈금 유지). 09:00=0px … 22:00=1600px
def hx(h, m=0):
    return (h + m / 60 - 9) / 13 * 1600


def day(t_in, upto, markers, draw_from=None, draw_t=None):
    ticks = ''.join(f'<line x1="{hx(h):.0f}" y1="22" x2="{hx(h):.0f}" y2="38" stroke="{MUT}"/>'
                    f'<text x="{hx(h):.0f}" y="60" fill="{MUT}" font-size="16" text-anchor="middle">{h}:00</text>' for h in (9, 12, 15, 18, 21))
    prog = f'<line x1="0" y1="30" x2="{hx(*upto):.0f}" y2="30" stroke="{AMB}" stroke-width="3"/>'
    if draw_from:
        prog = (f'<line x1="0" y1="30" x2="{hx(*draw_from):.0f}" y2="30" stroke="{AMB}" stroke-width="3"/>'
                f'<path data-draw="{draw_t}" data-d=".6" d="M{hx(*draw_from):.0f} 30 L{hx(*upto):.0f} 30" stroke="{AMB}" stroke-width="3" fill="none"/>')
    mk = ''
    for (h, m), label, t in markers:
        mk += (f'<circle data-kf="{t}:o=0;{t+.2}:o=1" cx="{hx(h, m):.0f}" cy="30" r="9" fill="{AMB}"/>'
               f'<text data-kf="{t}:o=0;{t+.2}:o=1" x="{hx(h, m):.0f}" y="12" fill="{AMB}" font-size="18" font-weight="700" text-anchor="middle">{label}</text>')
    return (f'<div class="abs" data-in="{t_in}" style="left:120px;top:48px;width:1680px;height:118px">'
            + panel(0, 0, 1680, 118) + txt(1420, 14, 'RUN LOG · 11 / 23', cls='eng')
            + f'<svg class="abs" style="left:40px;top:44px;overflow:visible" width="1600" height="64">'
            f'<line x1="0" y1="30" x2="1600" y2="30" stroke="{MUT}" stroke-width="2"/>{ticks}{prog}{mk}</svg></div>')


S = {}

# M01 7.90–15.20 · 3번 줄: 대기 소음이었다 → 인쇄 49
DIAL = (f'<svg class="abs" style="left:1180px;top:300px" width="420" height="420">'
        f'<circle cx="210" cy="210" r="150" fill="#262C32" stroke="#A9B1BA88" stroke-width="4"/>'
        + ''.join(f'<text x="{210+190*__import__("math").cos(__import__("math").radians(a)):.0f}" y="{216+190*__import__("math").sin(__import__("math").radians(a)):.0f}" '
                  f'fill="{c}" font-size="30" font-weight="900" text-anchor="middle">{n}</text>'
                  for a, n, c in [(-150, '인쇄', INK), (-90, '저소음', MUT), (-30, '대기', INK)]) +
        f'<g data-kf="7.9:r=60;12.6:r=60;13.3:r=-60" style="transform-origin:210px 210px;transform-box:view-box">'
        f'<rect x="200" y="70" width="20" height="150" rx="10" fill="{AMB}"/></g>'
        f'<circle cx="210" cy="210" r="34" fill="#3A434D"/></svg>')
S['M01'] = scene(7.9, 15.2,
    panel(220, 230, 1480, 560)
    + txt(280, 262, 'SOUND LEVEL · DCP-L2640DW · 레이저 설명서 PDF 624쪽', cls='eng')
    + f'<div class="abs seg" data-kf="7.9:o=1;13.3:o=1;13.42:o=0" style="left:280px;top:330px;font-size:220px">30.0</div>'
    + f'<div class="abs seg" data-kf="7.9:o=0;13.36:o=0;13.5:o=1" data-glowp="13.5" style="left:280px;top:330px;font-size:220px">49.0</div>'
    + txt(900, 470, 'dB(A)', cls='seg', style='font-size:60px')
    + txt(280, 600, '모드', cls='eng')
    + f'<div class="abs lamp" data-kf="7.9:o=1;12.6:o=1;13.1:o=.25" data-hl="10.4" data-c="{AMB}" style="left:280px;top:640px;background:#3A434D;color:{INK}">대기 · 쉬고 있을 때</div>'
    + f'<div class="abs lamp" data-kf="7.9:o=0;13.0:o=0;13.3:o=1" style="left:640px;top:640px;background:{AMB};color:#26201A">인쇄 중</div>'
    + DIAL)

# M02 21.50–29.60 · 5번 줄: 설명서를 조각(청크)으로, 조각마다 적용 모델·PDF 쪽수
rows = [('MFC-L2805DW', 52, '연속 스캔 · ADF 최대 50매'), ('DCP-L2640DW', 624, '소음 · 인쇄 49 dB(A)'), ('DCP-T530DW', 61, '용지함 · 80gsm 150매'),
        ('MFC-T930DW', 177, '팩스 수신 모드 설정'), ('DCP-T730DW', 255, 'Wi-Fi Direct 연결')]
chips = ''
for i, (m, pg, body) in enumerate(rows):
    t = 24.0 + i * .14
    chips += (f'<div class="abs chip" data-kf="{t:.2f}:left=330,top=470,o=0;{t+.5:.2f}:left=760,top={300+i*100},o=1" style="width:960px;height:80px;font-size:28px;font-weight:700">'
              f'<span class="tag" style="background:#3A434D;color:{MUT}">CH {i+1:04d}</span>'
              f'<span style="flex:1">{body}</span>'
              f'<span class="tag" data-marker="25.66" data-c="{BLU}55" style="color:{BLU}">{m}</span>'
              f'<span class="tag" data-marker="26.32" data-c="{AMB}55" style="color:{AMB}">PDF {pg}쪽</span></div>')
S['M02'] = scene(21.5, 29.6,
    txt(200, 120, 'CH 00 · 데이터 준비 · 담당 희주님', cls='eng', t=21.6)
    + txt(200, 160, '설명서 → 검색용 조각', cls='h1', t=21.9)
    + f'<div class="abs" data-in="22.8" data-kf="22.8:o=1;24.0:o=1;24.6:o=.35" style="left:200px;top:330px;width:300px;height:360px;background:repeating-linear-gradient(0deg,#3A434D 0 6px,#2E353D 6px 12px);border:2px solid #4A535D;border-radius:4px"></div>'
    + txt(215, 700, '설명서 2권 · 1,099쪽', t=22.8, style='font-size:28px;font-weight:700;color:' + MUT)
    + chips
    + f'<div class="abs" data-in="28.5" style="left:1300px;top:820px;display:flex;align-items:baseline;gap:16px">'
      f'<span class="seg" style="font-size:96px"><span data-roll="28.0" data-v="1512" data-comma>0</span></span><span class="h1" style="font-size:40px">개 · v4.1</span></div>')

# M03 29.60–37.80 · 6번 줄: 오전, 세 가지 검색 비교
def probes(t_a, t_b, t_c, dimA=None, dimC=None, hlB=None):
    out = ''
    for i, (k, name, sub, c, t, dim) in enumerate([('A', '벡터', '의미가 비슷한 문장', BLU, t_a, dimA),
                                                     ('B', '하이브리드', '벡터 + 키워드(BM25) → 순위 결합(RRF)', AMB, t_b, None),
                                                     ('C', '재정렬', 'B 후보 20개를 생성 모델이 다시 고름', LIL, t_c, dimC)]):
        y = 300 + i * 145
        d = f' data-dim="{dim}"' if dim else ''
        h = f' data-hl="{hlB}" data-c="{AMB}"' if (k == 'B' and hlB) else ''
        out += (f'<div class="abs chip"{d}{h} data-in="{t}" style="left:760px;top:{y}px;width:960px;height:120px">'
                f'<span style="font-size:60px;font-weight:900;color:{c};width:60px">{k}</span>'
                f'<div><div style="font-size:42px;font-weight:900">{name}</div><div style="font-size:24px;color:{MUT}">{sub}</div></div></div>'
                f'<svg class="abs" style="left:520px;top:{y-30}px;overflow:visible" width="240" height="200"><path data-draw="{t}" data-d=".45" d="M0 {545-y+30} C120 {545-y+30} 120 90 240 90" stroke="{c}" stroke-width="4" fill="none"/></svg>')
    return out


Q = (f'<div class="abs chip" style="left:200px;top:495px;width:320px;height:100px;font-size:34px;font-weight:900">질문 하나</div>')
S['M03'] = scene(29.6, 37.8,
    day(29.7, (9, 30), [((9, 2), '09:02 검색 연결', 30.64)])
    + txt(200, 230, 'CH 01 · 세 가지 검색 · 같은 질문', cls='eng', t=31.0)
    + f'<div data-in="32.0">{Q}</div>'
    + probes(33.86, 35.14, 36.92))

# M04 37.80–44.30 · 7번 줄: B가 확인용 12문항 정답 페이지를 모두 상위 5개 안에
S['M04'] = scene(37.8, 44.3,
    day(37.8, (9, 30), [((9, 2), '09:02 검색 연결', 37.8)])
    + txt(200, 230, 'CH 01 · 세 가지 검색 · 같은 질문', cls='eng')
    + Q + probes(37.8, 37.8, 37.8, dimA=38.6, dimC=38.6, hlB=38.9)
    + txt(760, 760, '확인용 질문 12개 · 정답 페이지가 상위 5개 안에(Hit@5)', t=39.9, style='font-size:28px;font-weight:700;color:' + MUT)
    + leds(760, 810, 12, 12, 41.9, step=.05, size=40, gap=14)
    + txt(1440, 792, '<span data-roll="42.6" data-v="12">0</span>/12', cls='seg', style='font-size:72px', t=42.2))

# M05 52.20–56.20 · 10번 줄: 원인은 페이지가 아니라 표의 한 줄
TABLE_ROWS = [('일반 인쇄', '49'), ('저소음 인쇄', '44'), ('대기', '30')]
def table(x, y, hl_row=None, hl_t=None, w=900):
    out = f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px">'
    out += f'<div class="eng" style="padding:10px 0">소음 레벨 · 음압 LpAm</div>'
    for i, (mode, v) in enumerate(TABLE_ROWS):
        hl = f' data-hl="{hl_t}" data-c="{RED}"' if hl_row == i else ''
        out += (f'<div{hl} style="display:flex;height:84px;align-items:center;border-top:2px solid #4A535D;font-size:38px;font-weight:700;padding:0 20px">'
                f'<span style="flex:1">{mode}</span><span class="seg" style="font-size:44px">{v} dB(A)</span></div>')
    return out + '</div>'
S['M05'] = scene(52.2, 56.2,
    txt(200, 150, 'CH 02 · 원인 추적', cls='eng', t=52.3)
    + f'<div class="abs" data-kf="52.3:left=200,top=320,o=0;52.7:left=200,top=320,o=1" style="width:360px;height:460px;background:#2E353D;border:2px solid #4A535D;border-radius:4px"></div>'
    + txt(230, 350, 'PDF 624쪽', style='font-size:34px;font-weight:900')
    + f'<div class="abs lamp" data-pop="53.6" style="left:230px;top:700px;background:{GRN};color:#1B2A22">페이지 ✓</div>'
    + table(700, 300, hl_row=2, hl_t=54.9)
    + f'<div class="abs lamp" data-pop="55.1" style="left:700px;top:700px;background:{RED};color:#2A1414">표의 한 줄 ✗ · 대기 값을 읽음</div>')

# M06 56.20–68.10 · 11번 줄: v4.3 가운데 칸 소실 → v4.4 복원 → 49·44·30 각자 다른 조각
mid = (f'<div class="abs" style="left:430px;top:330px;width:260px;height:300px;border:3px dashed {AMB};border-radius:4px" '
       f'data-kf="58.3:o=0;58.6:o=1;59.6:o=1;60.1:o=.15;62.7:o=.15;63.1:o=1"></div>')
labels = ''.join(f'<div class="abs" data-kf="58.3:o=0;58.6:o=1;59.6:o=1;60.1:o=0;62.7:o=0;63.1:o=1" style="left:450px;top:{345+i*100}px;font-size:34px;font-weight:900;color:{AMB}">{m}</div>'
                 for i, m in enumerate(['인쇄', '저소음', '대기']))
vals = ''.join(f'<div class="abs seg" style="left:760px;top:{340+i*100}px;font-size:56px">{v}</div>' for i, v in enumerate(['49', '44', '30']))
rowsbox = ''.join(f'<div class="abs" style="left:200px;top:{330+i*100}px;width:860px;height:100px;border-top:2px solid #4A535D;font-size:30px;font-weight:700;padding:28px 0 0 0;color:#B8C0C8">음압 LpAm</div>' for i in range(3))
split = ''.join(f'<div class="abs chip" data-kf="{t:.2f}:left=200,top={330+i*100},w=860,h=96,o=0;{t+.05:.2f}:o=1;{t+.55:.2f}:left=1180,top={300+i*150},w=560,h=110,o=1" '
                f'style="font-size:34px;font-weight:900"><span class="tag" style="background:#3A434D;color:{MUT}">조각</span>{m}<span class="seg" style="font-size:46px;margin-left:auto">{v} dB(A)</span></div>'
                for i, (m, v, t) in enumerate([('일반 인쇄', '49', 63.32), ('저소음 인쇄', '44', 64.26), ('대기', '30', 64.92)]))
S['M06'] = scene(56.2, 68.1,
    txt(200, 150, 'CH 02 · 소음 표 · 레이저 PDF 624쪽', cls='eng', t=56.3)
    + f'<div class="abs" data-flipin="61.0" style="left:200px;top:200px"><span class="lamp" style="background:#3A434D;color:{INK}">'
      f'<span data-kf="56:o=1;61.4:o=0">청크 v4.3</span></span></div>'
    + f'<div class="abs lamp" data-pop="61.6" style="left:200px;top:200px;background:{AMB};color:#26201A">청크 v4.4 · 칸 복원</div>'
    + txt(200, 270, '항목', cls='eng') + txt(450, 270, '작동 상태', cls='eng') + txt(760, 270, '값', cls='eng')
    + f'<div data-in="56.6">{rowsbox}{vals}</div>' + mid + labels
    + f'<div class="abs" data-kf="59.6:o=0;60.0:o=1;62.6:o=1;62.9:o=0" style="left:450px;top:460px;font-size:28px;color:{RED};font-weight:900">조각에서 사라짐</div>'
    + split
    + txt(1180, 760, '각자 다른 조각', cls='h1', t=66.6, style='font-size:40px;color:' + AMB))

# M07 68.10–73.10 · 12번 줄: 1차 제출 16:36, 91.26, 당시 2위
def readout(run, t_roll, v, rank, rank_t, note, peak_t=None, glow=None):
    g = f' data-glowp="{glow}"' if glow else ''
    pk = f'<div class="lamp" data-pop="{peak_t}" style="background:{GRN};color:#1B2A22">PEAK</div>' if peak_t else ''
    return (panel(420, 250, 1080, 600)
            + txt(470, 282, f'{run} · SCORE · COMPOSITE (공식 포털)', cls='eng')
            + txt(470, 340, f'<span data-roll="{t_roll}" data-v="{v}" data-dec="2"{g}>0</span>', cls='seg', style='font-size:220px')
            + f'<div class="abs" data-in="{rank_t}" style="left:470px;top:680px;display:flex;align-items:center;gap:24px">'
              f'<div class="eng">RANK</div><div class="seg" style="font-size:90px">{rank}</div>{pk}'
              f'<div style="font-size:24px;color:{MUT};margin-left:10px;white-space:nowrap">{note}</div></div>')
S['M07'] = scene(68.1, 73.1,
    day(68.15, (16, 36), [((9, 2), '09:02', 68.1), ((16, 36), 'RUN 1 · 16:36', 68.9)], draw_from=(9, 30), draw_t=68.4)
    + readout('RUN 1 · v4.4 · B', 70.4, 91.26, 2, 72.0, '16:41 순위표 기준'))

# M08 73.10–79.10 · 13번 줄: 두 가지를 묻는 질문에서 두 번째 사실 누락
S['M08'] = scene(73.1, 79.1,
    txt(200, 150, 'CH 03 · 남은 오답', cls='eng', t=73.2)
    + f'<div class="abs chip" data-in="74.1" style="left:200px;top:330px;width:620px;height:130px;font-size:36px;font-weight:900">질문 · 두 가지를 함께 묻는다</div>'
    + f'<svg class="abs" style="left:820px;top:300px;overflow:visible" width="200" height="400"><path data-draw="75.0" d="M0 95 C100 95 100 40 200 40" stroke="{MUT}" stroke-width="4" fill="none"/>'
      f'<path data-draw="75.0" d="M0 95 C100 95 100 250 200 250" stroke="{MUT}" stroke-width="4" fill="none"/></svg>'
    + f'<div class="abs chip" data-in="75.2" style="left:1020px;top:290px;width:640px;height:100px;font-size:34px;font-weight:700">사실 1<span class="lamp" data-pop="75.5" style="margin-left:auto;background:{GRN};color:#1B2A22">답함</span></div>'
    + f'<div class="abs chip" data-in="76.3" data-hl="77.4" data-c="{RED}" style="left:1020px;top:500px;width:640px;height:100px;font-size:34px;font-weight:700;border-style:dashed">사실 2'
      f'<span class="lamp" data-pop="77.5" style="margin-left:auto;background:{RED};color:#2A1414">빠짐</span></div>')

# M09 86.10–89.90 · 15번 줄: 모델마다 대표 근거를 먼저
S['M09'] = scene(86.1, 89.9,
    txt(200, 150, 'CH 04 · 검색 보완 (B)', cls='eng', t=86.15)
    + ''.join(f'<div class="abs chip" data-in="{86.9+i*.15:.2f}" style="left:200px;top:{380+i*220}px;width:520px;height:120px;font-size:38px;font-weight:900">'
              f'<span class="tag" style="color:{BLU}">모델 {k}</span>근거 후보 20개</div>'
              f'<div class="abs chip" data-kf="{87.9+i*.12:.2f}:left=730,o=0;{88.4+i*.12:.2f}:left=900,o=1" style="top:{380+i*220}px;width:760px;height:120px;font-size:34px;font-weight:700;border-color:{AMB}">'
              f'대표 근거 1순위로 먼저 확보<span class="lamp" style="margin-left:auto;background:{GRN};color:#1B2A22">LOCK</span></div>'
              for i, k in enumerate(['①', '②'])))

# M10 89.90–99.80 · 16번 줄: 약한 유형 10문항, B 10/10 · C 6/10 → 2차도 B
S['M10'] = scene(89.9, 99.8,
    panel(120, 200, 1680, 640)
    + txt(180, 232, 'CH 05 · 제출 직전 점검 · 19:34', cls='eng', t=90.0)
    + txt(180, 270, f'약한 유형 <span data-marker="91.66" data-c="{AMB}55">10문항</span>', cls='h1', t=90.3)
    + txt(180, 420, f'<div class="eng">PROBE B</div><div style="font-size:44px;font-weight:900;color:{AMB}">하이브리드</div>', t=92.3)
    + leds(520, 430, 10, 10, 93.84, step=.06)
    + txt(1270, 412, '<span data-roll="93.9" data-v="10">0</span>/10', cls='seg', style='font-size:72px', t=93.8)
    + f'<div data-dim="97.14" class="abs full">'
    + txt(180, 600, f'<div class="eng">PROBE C</div><div style="font-size:44px;font-weight:900;color:{LIL}">재정렬</div>', t=93.9)
    + leds(520, 610, 10, 6, 95.46, step=.06, off_col='#5A4545')
    + txt(1270, 592, '<span data-roll="95.5" data-v="6">0</span>/10', cls='seg', style='font-size:72px', t=95.4)
    + '</div>'
    + f'<div class="abs lamp" data-pop="98.26" style="left:1420px;top:240px;background:{GRN};color:#1B2A22;font-size:30px">LOCK · 2차 = B</div>'
    + txt(180, 760, 'B 저장 응답 vs C 신규 응답 · 조건·인용 충족 또는 정상 거부', style='font-size:24px;color:' + MUT, t=95.0))

# M11 99.80–104.60 · 17번 줄: 19:41 2차 제출, 100.00, 순위표 1위
S['M11'] = scene(99.8, 104.6,
    day(99.85, (19, 41), [((9, 2), '09:02', 99.8), ((16, 36), 'RUN 1 · 91.26', 99.8), ((19, 41), 'RUN 2 · 19:41', 100.4)], draw_from=(16, 36), draw_t=100.1)
    + f'<div class="abs full" data-iris="99.9" data-cx="50" data-cy="52">'
    + readout('RUN 2 · v4.7 · B', 101.5, 100, 1, 102.8, '20:02 순위표 기준', peak_t=103.5, glow=102.4) + '</div>')

# M12 104.60–114.40 · 18번 줄: 같은 30문항 재호출 — 근거 30/30 같음, 문장 10/30 같음
S['M12'] = scene(104.6, 114.4,
    txt(200, 150, 'CH 06 · 재측정 · 같은 서버 · 같은 30문항', cls='eng', t=104.7)
    + txt(200, 190, '같은 질문을 한 번 더', cls='h1', t=105.6)
    + txt(200, 380, '상위 5개 근거 · 순서까지 같음', style='font-size:32px;font-weight:700', t=109.3)
    + leds(200, 440, 30, 30, 110.34, step=.02, size=30, gap=10)
    + txt(1500, 418, '<span data-roll="110.5" data-v="30">0</span>/30', cls='seg', style='font-size:64px', t=110.3)
    + txt(200, 600, '답변 문장이 똑같음', style='font-size:32px;font-weight:700', t=111.4)
    + leds(200, 660, 30, 10, 112.46, step=.02, size=30, gap=10, col=GRN, off_col='#6B5A3A')
    + txt(1500, 638, '<span data-roll="112.6" data-v="10">0</span>/30', cls='seg', style='font-size:64px', t=112.4)
    + txt(200, 780, '공식 채점 대상이 아닌 팀 내부 재실행', style='font-size:24px;color:' + MUT, t=106.3))

# M13 114.40–119.00 · 19번 줄 앞: 숫자·단위를 원문 줄과 다시 맞춰 보는 검증
steps = [('검색', 115.0, MUT), ('생성', 115.1, MUT), ('CAL · 원문 줄 대조', 117.32, AMB)]
S['M13'] = scene(114.4, 119.0,
    txt(200, 150, 'CH 07 · 교정 단계 추가 (#88)', cls='eng', t=114.5)
    + ''.join(f'<div class="abs chip" data-kf="{t:.2f}:left={x0},o=0;{t+.4:.2f}:left={x1},o=1" style="top:330px;width:{w}px;height:120px;font-size:34px;font-weight:900;border-color:{c};justify-content:center">{n}</div>'
              for (n, t, c), x0, x1, w in zip(steps, [200, 520, 840], [200, 520, 840], [280, 280, 520]))
    + f'<div class="abs" data-kf="115.2:left=860,o=0;115.6:left=860,o=1;117.2:left=860,o=1;117.6:left=1400,o=1" style="top:330px;width:280px;height:120px;border:2px solid {MUT};border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:34px;font-weight:900">답변</div>'
    + f'<div class="abs chip" data-in="115.5" style="left:200px;top:560px;width:520px;height:110px;font-size:34px;font-weight:700">초안 숫자<span class="seg" style="margin-left:auto;font-size:44px">49 dB</span></div>'
    + f'<div class="abs chip" data-in="116.0" style="left:840px;top:560px;width:880px;height:110px;font-size:30px;font-weight:700">원문 줄 · 인쇄 · LpAm = 49 dB (A)'
      f'<span class="lamp" data-pop="117.8" style="margin-left:auto;background:{GRN};color:#1B2A22">일치</span></div>')

# M14 119.00–124.60 · 19번 줄 뒤: P95 4.75초 → 9.66초
import math
def gauge_angle(v):  # 0~12초 → -210°~30°
    return -210 + v / 12 * 240
ticks = ''.join(f'<line x1="{360+230*math.cos(math.radians(gauge_angle(v))):.0f}" y1="{360+230*math.sin(math.radians(gauge_angle(v))):.0f}" '
                f'x2="{360+260*math.cos(math.radians(gauge_angle(v))):.0f}" y2="{360+260*math.sin(math.radians(gauge_angle(v))):.0f}" stroke="{MUT}" stroke-width="3"/>'
                f'<text x="{360+300*math.cos(math.radians(gauge_angle(v))):.0f}" y="{368+300*math.sin(math.radians(gauge_angle(v))):.0f}" fill="{MUT}" font-size="26" text-anchor="middle">{v}</text>'
                for v in range(0, 13, 2))
S['M14'] = scene(119.0, 124.6,
    txt(200, 150, 'CH 07 · 비용 · 서버 P95 (로컬 44문항)', cls='eng', t=119.1)
    + f'<svg class="abs" data-in="119.2" style="left:180px;top:200px" width="720" height="720"><path d="M{360+245*math.cos(math.radians(-210)):.0f} {360+245*math.sin(math.radians(-210)):.0f} A245 245 0 1 1 {360+245*math.cos(math.radians(30)):.0f} {360+245*math.sin(math.radians(30)):.0f}" stroke="#4A535D" stroke-width="6" fill="none"/>{ticks}'
      f'<g data-kf="119.3:r={gauge_angle(4.75)+90:.1f};121.9:r={gauge_angle(4.75)+90:.1f};122.6:r={gauge_angle(9.66)+90:.1f}" style="transform-origin:360px 360px;transform-box:view-box">'
      f'<rect x="352" y="140" width="16" height="230" rx="8" fill="{AMB}"/></g><circle cx="360" cy="360" r="30" fill="#3A434D"/></svg>'
    + txt(1000, 330, '검증 전', cls='eng', t=119.8)
    + txt(1000, 370, '4.75<span style="font-size:60px">초</span>', cls='seg', style='font-size:130px', t=120.4)
    + txt(1000, 560, '검증 후', cls='eng', t=122.0)
    + txt(1000, 600, '<span data-roll="122.2" data-v="9.66" data-dec="2">0</span><span style="font-size:60px">초</span>', cls='seg', style='font-size:130px;color:' + RED, t=122.0)
    + txt(1000, 800, '이 버전의 공식 점수는 없음', style='font-size:24px;color:' + MUT, t=123.0))

# M15 132.50–134.40 · 20번 줄 끝: 무엇이 몇 점을 올렸는지 나눌 수 없다
S['M15'] = scene(132.5, 134.4,
    panel(420, 300, 1080, 480)
    + txt(470, 332, '기여도 · 91.26 → 100.00', cls='eng')
    + ''.join(f'<div class="abs chip" style="left:{470+i*330}px;top:420px;width:300px;height:110px;font-size:36px;font-weight:900;justify-content:center">{n}</div>' for i, n in enumerate(['청크', '검색', '생성']))
    + ''.join(f'<div class="abs seg" style="left:{580+i*330}px;top:560px;font-size:80px;color:{MUT}">?</div>' for i in range(3))
    + f'<div class="abs lamp" data-pop="133.1" style="left:470px;top:690px;background:#3A434D;color:{INK}">함께 바뀜 · 분리 불가</div>')

# M16 141.10–145.43 · 22번 줄: 검증은 꼭 필요할 때만 부를 수 있을까
S['M16'] = scene(141.1, 145.431,
    txt(200, 150, 'NEXT RUN', cls='eng', t=141.2)
    + txt(200, 190, '다음 실험의 질문', cls='h1', t=141.7)
    + f'<div class="abs" data-in="142.9" style="left:760px;top:380px;width:400px;height:400px;border-radius:50%;background:#2E353D;border:6px solid {AMB};display:flex;align-items:center;justify-content:center;flex-direction:column">'
      f'<div class="seg" style="font-size:96px">CAL</div><div class="eng" style="color:{AMB}">원문 줄 대조</div></div>'
    + f'<div class="abs" style="left:200px;top:820px;width:1520px;text-align:center;font-size:44px;font-weight:900;white-space:nowrap" data-type="143.5" data-cps="16">꼭 필요할 때만 부를 수 있을까?</div>')
