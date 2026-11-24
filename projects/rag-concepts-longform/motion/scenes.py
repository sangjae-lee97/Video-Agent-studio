# rag-concepts-longform 모션그래픽 — 템플릿: 물류 센터 출고 라인 (template-spec.md)
# 시각은 보정 음성 sentence-boundaries.json 기준 절대 초. 프레임 = 초 x 24.
# 하단 약 150px(자막 영역)에는 핵심 요소를 두지 않는다.

NAVY, YEL, TEAL, ORG, GRN, RED = '#23395B', '#F2B400', '#138A8A', '#E2701E', '#2E8B57', '#C8372D'
F = 24

CSS_EXTRA = r"""
body{background:#EFE6D6;color:#23395B;font-family:'Noto Sans CJK KR',sans-serif;
 background-image:repeating-linear-gradient(90deg,rgba(150,110,60,.035) 0 2px,transparent 2px 7px),repeating-linear-gradient(0deg,rgba(150,110,60,.03) 0 1px,transparent 1px 9px)}
.st{display:inline-block;border:4px solid #23395B;padding:6px 18px;font-size:26px;font-weight:900;letter-spacing:4px;color:#23395B;background:#EFE6D6}
.h{font-size:56px;font-weight:900;line-height:1.22;color:#23395B}
.lbl{background:#FFFFFF;border:2.5px solid #23395B;border-radius:4px;box-shadow:0 8px 0 rgba(35,57,91,.10)}
.lbl .hd{background:#23395B;color:#fff;font-weight:900;padding:10px 20px;font-size:28px;letter-spacing:1px}
.row{display:flex;align-items:center;border-top:1.5px solid rgba(35,57,91,.25);padding:10px 20px;font-size:28px}
.row .k{width:300px;color:#6A7A90;font-family:'DejaVu Sans Mono',monospace;font-size:24px}
.row .v{font-weight:800}
.box{background:linear-gradient(180deg,#D7B07A 0%,#C79C63 100%);border:3px solid #A57A45;border-radius:6px;box-shadow:0 10px 0 rgba(120,85,40,.18)}
.stamp{border:7px solid;border-radius:10px;font-weight:900;padding:6px 26px;background:rgba(255,255,255,.85);letter-spacing:2px}
.tape{background-image:linear-gradient(rgba(242,180,0,.55),rgba(242,180,0,.55));background-repeat:no-repeat;background-size:0% 100%;padding:0 6px}
.mono{font-family:'DejaVu Sans Mono',monospace}
.mut{color:#6A7A90}.teal{color:#138A8A}.org{color:#E2701E}.grn{color:#2E8B57}.red{color:#C8372D}.yel{color:#C98F00}
.chip{display:inline-flex;align-items:center;justify-content:center;border-radius:6px;font-weight:800;border:2.5px solid #23395B;background:#fff;padding:6px 16px}
.lane{position:absolute;height:0;border-top:6px dashed #F2B400}
"""

XJS = r"""<script>
window.extra=T=>{
 const pg=(a,d)=>{const x=(T-a)/d;return x<=0?0:x>=1?1:1-Math.pow(1-x,3)};
 document.querySelectorAll('[data-stamp]').forEach(e=>{const a=+e.dataset.stamp;const p=Math.min(1,Math.max(0,(T-a)/.12));
   e.style.opacity=T<a?0:1;e.style.transform=(e.dataset.base||'')+` scale(${1.6-.6*p})`;});
 document.querySelectorAll('[data-tape]').forEach(e=>{e.style.backgroundSize=(pg(+e.dataset.tape,.4)*100)+'% 100%';});
 document.querySelectorAll('[data-out]').forEach(e=>{const o=e.style.opacity===''?1:+e.style.opacity;e.style.opacity=o*(1-pg(+e.dataset.out,.35));});
 document.querySelectorAll('[data-mv]').forEach(e=>{const p=pg(+e.dataset.mv,+(e.dataset.d||.7));
   e.style.transform=`translate(${p*+(e.dataset.dx||0)}px,${p*+(e.dataset.dy||0)}px)`;});
 document.querySelectorAll('[data-lit]').forEach(e=>{const on=T>=+e.dataset.lit;e.style.background=on?e.dataset.on:(e.dataset.off||'');
   if(e.dataset.fc)e.style.color=on?e.dataset.fc:'';});
 document.querySelectorAll('[data-strike]').forEach(e=>{e.style.textDecoration=T>=+e.dataset.strike?'line-through 6px #C8372D':'none';});
};
</script>"""

S = {}


def scene(k, a, b, html):
    S[k] = (round(a * F), round(b * F), html + XJS)


def hdr(no, name, title, t, y=70, out=None):
    o = f' data-out="{out}"' if out else ''
    return (f'<div class="abs st" data-in="{t}"{o} style="left:120px;top:{y}px">STATION {no:02d} · {name}</div>'
            f'<div class="abs h" data-in="{t + .1:.2f}"{o} style="left:120px;top:{y + 66}px">{title}</div>')


def lbl(x, y, w, head, rows, t, step=.25, hc=NAVY, extra=''):
    r = ''.join(f'<div class="row" data-in="{t + .2 + i * step:.2f}"><div class="k">{k}</div><div class="v" {a}>{v}</div></div>'
                for i, (k, v, a) in enumerate(rows))
    return (f'<div class="abs lbl" data-in="{t}" style="left:{x}px;top:{y}px;width:{w}px;{extra}">'
            f'<div class="hd" style="background:{hc}">{head}</div>{r}</div>')


def box(x, y, w, h, t, inner='', extra=''):
    return f'<div class="abs box" data-in="{t}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{extra}">{inner}</div>'


def stamp(x, y, text, c, t, rot=-6, size=52):
    return (f'<div class="abs stamp" data-stamp="{t}" data-base="rotate({rot}deg)" '
            f'style="left:{x}px;top:{y}px;border-color:{c};color:{c};font-size:{size}px;opacity:0">{text}</div>')


def txt(x, y, s, t, size=34, w=None, extra='', cls=''):
    ww = f'width:{w}px;' if w else ''
    return f'<div class="abs {cls}" data-in="{t}" style="left:{x}px;top:{y}px;font-size:{size}px;{ww}{extra}">{s}</div>'


def arrow(x1, y1, x2, y2, t, c=NAVY, w=6, d=.5, dash=False):
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    hx1, hy1 = x2 - 26 * math.cos(ang - .45), y2 - 26 * math.sin(ang - .45)
    hx2, hy2 = x2 - 26 * math.cos(ang + .45), y2 - 26 * math.sin(ang + .45)
    da = 'stroke-dasharray="14 10"' if dash else ''
    return (f'<svg class="abs" style="left:0;top:0;pointer-events:none" width="1920" height="1080">'
            f'<path data-draw="{t}" data-d="{d}" d="M{x1} {y1} L{x2} {y2}" stroke="{c}" stroke-width="{w}" fill="none" {da}/>'
            f'<path data-draw="{t + d:.2f}" data-d=".2" d="M{hx1:.0f} {hy1:.0f} L{x2} {y2} L{hx2:.0f} {hy2:.0f}" stroke="{c}" stroke-width="{w}" fill="none"/></svg>')


def plate(x, y, code, digit_i, c, t, size=46):
    s = ''.join(f'<span style="color:{c}">{ch}</span>' if i == digit_i else ch for i, ch in enumerate(code))
    return f'<div class="abs lbl mono" data-in="{t}" style="left:{x}px;top:{y}px;padding:14px 26px;font-size:{size}px;font-weight:900">{s}</div>'


# ───────────── 0장 · 오프닝 ─────────────
# M01 15.833–25.5  (2 끝) ~ 3: 세 덩어리
st = [('01', '자료 준비', '파싱 · 청킹 · 메타데이터', 18.6, NAVY), ('02', '찾고 답하기', '검색 · 생성 · 검증', 20.9, TEAL), ('03', '평가', '정확도 · 속도 · 비용', 23.2, ORG)]
html = (txt(120, 80, '<span class="st">OUTBOUND LINE</span>', 15.9) + txt(120, 150, '질문 하나가 답이 되기까지', 16.0, 58, extra='font-weight:900')
        + '<div class="abs lane" data-in="16.3" style="left:120px;top:560px;width:1680px"></div>')
for i, (no, n, sub, t, c) in enumerate(st):
    x = 140 + i * 580
    html += (f'<div class="abs lbl" data-in="{t}" style="left:{x}px;top:330px;width:480px">'
             f'<div class="hd" style="background:{c}">STATION {no}</div>'
             f'<div style="padding:26px 24px"><div style="font-size:52px;font-weight:900">{n}</div>'
             f'<div class="mut" style="font-size:28px;margin-top:10px">{sub}</div></div></div>')
html += box(70, 600, 150, 110, 16.4, '<div class="mono" style="text-align:center;margin-top:36px;font-size:26px;font-weight:900">질문</div>', '') \
    + f'<div class="abs" data-mv="18.4" data-d="6.4" data-dx="1560" style="left:0;top:0"><div class="abs lbl mono" data-in="16.5" style="left:70px;top:740px;padding:8px 18px;font-size:30px;font-weight:900;border-top:10px solid {YEL}">L2805</div></div>'
scene('M01', 15.833, 25.5, html)

# ───────────── 1장 · 래그 ─────────────
# M02 25.5–43.5  4~6: R·A·G, 왜 필요한가
rag = [('R', 'Retrieval', '검색', '문서에서 찾고', 28.6, TEAL), ('A', 'Augmented', '증강', 'AI에게 함께 건네고', 31.2, YEL), ('G', 'Generation', '생성', '근거로 답한다', 33.6, GRN)]
html = hdr(0, '개념', '래그 = 검색 증강 생성', 25.6)
for i, (L, en, ko, d, t, c) in enumerate(rag):
    x = 140 + i * 580
    html += (f'<div class="abs lbl" data-in="{t}" data-out="35.4" style="left:{x}px;top:330px;width:480px;height:330px;padding:26px 30px">'
             f'<div style="display:flex;align-items:baseline;gap:18px"><div style="font-size:120px;font-weight:900;color:{c};line-height:1">{L}</div>'
             f'<div><div class="mono" style="font-size:30px;font-weight:700">{en}</div><div style="font-size:40px;font-weight:900">{ko}</div></div></div>'
             f'<div style="font-size:36px;margin-top:40px;font-weight:700">{d}</div></div>')
# 왜 필요할까요 (35.68~43.16)
html += (txt(140, 300, '기억만으로 답하면', 35.9, 40, extra='font-weight:900;opacity:0')
         + f'<div class="abs lbl" data-in="36.6" style="left:140px;top:380px;width:760px;padding:28px 32px">'
           f'<div class="mut" style="font-size:28px">질문 · MFC-L2805DW</div><div style="font-size:40px;font-weight:900;margin-top:12px">“<span class="mono" data-tape="38.4">L2885</span> 기준으로는…”</div>'
           f'<div style="font-size:40px;font-weight:900;margin-top:12px">“최대 <span data-tape="40.6">○○매</span>입니다.”</div>'
           f'<div class="mut" style="font-size:26px;margin-top:16px">출처 없음</div></div>'
         + stamp(620, 400, '코드 혼동', RED, 39.0, -5, 40) + stamp(520, 640, '근거 없는 숫자', RED, 41.2, 4, 40)
         + txt(1000, 300, '근거로 답하면', 36.2, 40, extra='font-weight:900')
         + f'<div class="abs lbl" data-in="36.9" style="left:1000px;top:380px;width:780px;padding:28px 32px;border-color:{GRN}">'
           f'<div class="mut" style="font-size:28px">질문 · MFC-L2805DW</div><div style="font-size:40px;font-weight:900;margin-top:12px">“해당 모델 근거에 따르면…”</div>'
           f'<div class="mono" style="font-size:30px;margin-top:16px;color:{GRN};font-weight:800">[R1] 매뉴얼 · 페이지 · 적용 모델</div></div>')
scene('M02', 25.5, 43.5, html)

# M03 43.5–50.2  7: 환각이 저절로 사라지지 않음 → 검증·평가가 붙는다
html = (hdr(0, '주의', '래그를 써도 환각은 저절로 사라지지 않는다', 43.6)
        + '<div class="abs lane" data-in="44.0" style="left:120px;top:560px;width:1680px"></div>'
        + ''.join(f'<div class="abs lbl" data-in="{t}" style="left:{x}px;top:420px;width:300px;text-align:center;padding:30px 0;font-size:40px;font-weight:900;{s}">{n}</div>'
                  for x, n, t, s in [(140, '검색', 44.2, ''), (500, '생성', 44.5, ''), (980, '검증', 46.9, f'border:4px solid {GRN};color:{GRN}'), (1340, '평가', 47.6, f'border:4px solid {ORG};color:{ORG}')])
        + arrow(450, 480, 495, 480, 44.6) + arrow(810, 480, 975, 480, 46.5, GRN) + arrow(1290, 480, 1335, 480, 47.4, ORG)
        + txt(980, 640, '← 뒤에 붙는 두 정거장', 48.0, 34, extra='font-weight:800'))
scene('M03', 43.5, 50.2, html)

# ───────────── 2장 · 자료 준비 ─────────────
# M04 50.2–68.6  8~10: 파싱, 표 깨짐
table = (f'<div class="abs lbl" data-in="51.2" style="left:140px;top:330px;width:760px">'
         f'<div class="hd">PDF · 사양표 (보이는 모습)</div>'
         f'<div style="display:grid;grid-template-columns:260px 250px 250px;font-size:30px">'
         + ''.join(f'<div style="padding:16px 20px;border-top:1.5px solid #23395B44;border-right:1.5px solid #23395B44;font-weight:{w}" {a}>{c}</div>'
                   for c, w, a in [('기능', 900, ''), ('<span class="mono">L2805</span>', 900, ''), ('<span class="mono">L2885</span>', 900, ''),
                                   ('ADF 용량', 700, ''), ('예시값 A', 700, f'data-hl="58.4" data-c="{TEAL}"'), ('예시값 B', 700, f'data-hl="58.4" data-c="{ORG}"'),
                                   ('조건*', 700, ''), ('표준 용지', 700, ''), ('표준 용지', 700, '')])
         + '</div><div class="mut" style="font-size:24px;padding:12px 20px">* 각주: 일부 모델에만 적용</div></div>')
html = (hdr(2, '자료 준비', '파싱 — PDF에서 제대로 꺼내기', 50.3) + table
        + arrow(920, 520, 1040, 520, 52.6)
        + f'<div class="abs lbl" data-in="53.0" style="left:1060px;top:330px;width:720px">'
          f'<div class="hd">추출 결과</div><div style="padding:22px 24px;font-size:30px;line-height:1.7">'
          f'<div data-in="53.4"><b>글자</b> · <b>표</b> · <b>각주</b> · <b>페이지</b></div>'
          f'<div data-in="58.0" class="mono" style="margin-top:10px;color:#6A7A90">기능 ADF L2805 예시값 조건* L2885 표준 예시값 용지 …</div>'
          f'<div data-in="64.0" style="margin-top:14px;font-weight:900">어느 숫자가 <span data-tape="65.4">어느 모델</span> 것?</div></div></div>'
        + stamp(1240, 700, '행·열 뒤섞임', RED, 59.6, -4, 44)
        + txt(140, 760, 'PDF는 “어디에 무엇이 보이는지”를 기록한 파일', 57.3, 30, cls='mut', extra='font-weight:700'))
scene('M04', 50.2, 68.6, html)

# M05 68.6–80.3  11: 도구 비교 → 원문 대조
html = (hdr(2, '자료 준비', '도구보다 원문 대조', 68.7)
        + lbl(140, 330, 560, 'pdfplumber', [('다루는 것', '글자 · 좌표 · 표', ''), ('강점', '위치 확인이 쉽다', '')], 70.2, hc=TEAL)
        + lbl(760, 330, 560, 'Docling', [('다루는 것', '문서 구조 인식', ''), ('강점', '복잡한 구조', '')], 72.6, hc=ORG)
        + txt(1380, 360, '어느 쪽이<br>더 낫다?', 74.3, 44, extra='font-weight:900')
        + stamp(1400, 500, '단정 금지', RED, 75.0, -6, 44)
        + f'<div class="abs lbl" data-in="76.4" style="left:140px;top:640px;width:1180px;padding:22px 28px;font-size:34px;font-weight:800;border:4px solid {GRN}">'
          f'대표 페이지를 <span data-tape="77.6">원문과 직접 대조</span>해서 고른다</div>'
        + stamp(1380, 640, '원문 대조', GRN, 78.4, -4, 44))
scene('M05', 68.6, 80.3, html)

# M06 88.217–103.0  13~14: 함께 담기 원칙, 예시 분리
items = [('모델명', NAVY), ('수치', TEAL), ('예외 조건', ORG), ('각주', YEL), ('페이지', GRN)]
html = hdr(2, '청킹', '가장 중요한 원칙', 88.3)
html += box(140, 320, 760, 430, 88.7, '<div class="abs mono" style="left:24px;top:16px;font-size:26px;font-weight:900;color:#5A3C14">CHUNK · 한 상자</div>')
for i, (n, c) in enumerate(items):
    html += f'<div class="abs chip" data-in="{89.6 + i * .55:.2f}" style="left:{180 + (i % 3) * 235}px;top:{400 + (i // 3) * 120}px;width:210px;height:84px;font-size:32px;border-color:{c};color:{c}">{n}</div>'
html += txt(160, 680, '서로 떼어 놓지 않는다', 92.6, 36, extra='font-weight:900;color:#3B2A12')
html += (txt(1000, 300, '예를 들어 <span class="mut" style="font-size:26px">(설명용 예시)</span>', 95.2, 34, extra='font-weight:900')
         + box(1000, 370, 360, 170, 95.6, '<div style="text-align:center;margin-top:44px;font-size:40px;font-weight:900">최대 50매</div>')
         + box(1420, 370, 360, 170, 96.4, '<div style="text-align:center;margin-top:44px;font-size:36px;font-weight:900">표준 용지 기준</div>')
         + f'<div class="abs" data-in="97.6" style="left:1375px;top:350px;width:6px;height:220px;background:{RED}"></div>'
         + f'<div class="abs lbl" data-in="99.6" style="left:1000px;top:600px;width:780px;padding:22px 28px;font-size:34px;font-weight:800">'
           f'검색된 상자 하나: “최대 50매” <span class="mut" style="font-size:28px">— 조건 없음</span></div>'
         + stamp(1300, 700, '절반짜리 답', RED, 101.0, -5, 46))
scene('M06', 88.217, 103.0, html)

# M07 103.0–123.1  15~17: 송장 라벨 필드 → 모델 필터
rows = [('document_id', '문서 아이디', ''), ('chunk_id', '조각 아이디', ''), ('page', '페이지', ''), ('source_url', '출처 주소', ''),
        ('version', '문서 버전', ''), ('applicable_models', '<span class="mono">MFC-L2805DW</span>', 'data-tape="114.6"')]
html = (hdr(2, '메타데이터', '조각마다 송장 라벨을 붙인다', 103.1)
        + txt(120, 230, '데이터 자체가 아니라, 어디서 왔고 무엇에 해당하는지', 105.0, 30, cls='mut', extra='font-weight:700')
        + lbl(120, 300, 800, 'SHIPPING LABEL · 메타데이터', rows, 110.4, step=.8)
        + txt(1020, 300, '질문 · <span class="mono">L2805</span>', 116.0, 34, extra='font-weight:900')
        + '<div class="abs lane" data-in="116.3" style="left:1020px;top:380px;width:760px"></div>'
        + ''.join(f'<div class="abs" data-in="{116.8 + i * .2:.2f}" style="left:{1030 + i * 150}px;top:410px">'
                  f'<div class="box" style="width:130px;height:96px;{"" if ok else "opacity:.35"}"><div class="mono" style="text-align:center;margin-top:30px;font-size:22px;font-weight:900">{c}</div></div></div>'
                  for i, (c, ok) in enumerate([('2805', 1), ('2885', 0), ('2805', 1), ('2885', 0), ('2805', 1)]))
        + txt(1020, 540, '적용 모델 칸으로 걸러 검색', 118.2, 32, extra=f'font-weight:900;color:{GRN}')
        + arrow(1300, 720, 1300, 620, 120.2, TEAL)
        + txt(1020, 730, '답 → 라벨 → 원문 페이지까지 역추적', 120.6, 32, extra='font-weight:800'))
scene('M07', 103.0, 123.1, html)

# M08 123.1–129.5  18: 다중 적용 모델
html = (hdr(2, '메타데이터', '한 조각에 적용 모델이 여럿일 수 있다', 123.2)
        + box(140, 330, 620, 380, 123.6, '<div class="abs" style="left:30px;top:30px;font-size:32px;font-weight:900;color:#3B2A12">공통 내용 · 한 조각</div>')
        + lbl(820, 330, 960, 'applicable_models (예시)', [], 124.4)
        + ''.join(f'<div class="abs chip mono" data-in="{125.0 + i * .35:.2f}" style="left:{850 + (i % 2) * 460}px;top:{420 + (i // 2) * 90}px;width:420px;height:70px;font-size:30px;border-color:{YEL}">{m}</div>'
                  for i, m in enumerate(['MFC-L2805DW', 'MFC-L2885DW', 'DCP-L2605DW', 'DCP-L2640DW']))
        + txt(820, 640, '공통 내용이 빠지지 않게', 127.2, 34, extra=f'font-weight:900;color:{GRN}'))
scene('M08', 123.1, 129.5, html)

# ───────────── 3장 · 검색 ─────────────
# M09 129.5–147.4  19~21: 임베딩
pts = [(1180, 470, '여러 장 연속 스캔', TEAL), (1300, 430, '자동 문서 공급 장치', TEAL), (1240, 560, 'ADF 다중 페이지', TEAL),
       (1560, 700, '토너 교체', NAVY), (1640, 640, '드럼 수명', NAVY), (1020, 760, '무선 네트워크', NAVY)]
html = (hdr(3, '검색', '임베딩 — 문장을 숫자 벡터로', 129.6)
        + f'<div class="abs lbl" data-in="134.3" style="left:120px;top:330px;width:740px;padding:26px 30px">'
          f'<div style="font-size:36px;font-weight:900">“여러 장 연속 스캔”</div>'
          f'<div class="mono" data-in="135.4" style="font-size:32px;margin-top:22px;color:{TEAL};font-weight:700">[0.82, -0.15, 0.63, … ]</div>'
          f'<div class="mut" data-in="135.8" style="font-size:24px;margin-top:8px">설명용 숫자 · 실제로는 수백~수천 차원</div></div>'
        + arrow(870, 450, 990, 500, 136.4, TEAL)
        + f'<div class="abs lbl" data-in="136.2" style="left:980px;top:330px;width:800px;height:520px"><div class="hd">의미 지도 (2차원으로 그린 예시)</div></div>')
for i, (x, y, n, c) in enumerate(pts):
    html += (f'<div class="abs" data-in="{137.0 + i * .35:.2f}" style="left:{x - 12}px;top:{y - 12}px;width:24px;height:24px;border-radius:50%;background:{c}"></div>'
             f'<div class="abs" data-in="{137.0 + i * .35:.2f}" style="left:{x + 20}px;top:{y - 20}px;font-size:24px;font-weight:800;color:{c}">{n}</div>')
html += (f'<svg class="abs" style="left:0;top:0" width="1920" height="1080"><ellipse data-draw="139.0" data-d=".8" cx="1260" cy="490" rx="210" ry="110" stroke="{TEAL}" stroke-width="5" fill="none" stroke-dasharray="12 8"/></svg>'
         + txt(120, 640, '비슷한 의미 → 가까운 자리', 139.4, 34, extra='font-weight:900')
         + f'<div class="abs lbl" data-in="142.2" style="left:120px;top:720px;width:740px;padding:18px 26px;font-size:30px;font-weight:800;border:4px solid {RED}">'
           f'숫자 하나하나에 <span data-tape="144.2">정해진 단어 뜻은 없다</span></div>')
scene('M09', 129.5, 147.4, html)

# M10 155.317–171.1  23끝~25: 장점·약점·필터 / 코사인 오해
html = (hdr(3, '벡터 검색', '가까운 것을 찾는다 — 그래서 헷갈리는 것도', 155.4)
        + lbl(120, 320, 820, '장점', [('질문', '“서류 여러 장 연속 스캔”', ''), ('찾음', '자동 문서 공급 장치 · ADF', f'style="color:{TEAL}"')], 155.6, hc=TEAL)
        + lbl(1000, 320, 800, '약점', [('질문', '<span class="mono">L2805</span>', ''), ('가까움', '<span class="mono">L2885</span> 페이지', f'style="color:{RED}"')], 159.4, hc=RED)
        + f'<div class="abs lbl" data-in="163.3" style="left:1000px;top:560px;width:800px;padding:18px 26px;font-size:32px;font-weight:900;border:4px solid {GRN}">'
          f'→ 모델 필터를 <span data-tape="164.4">따로</span> 둔다</div>'
        + f'<div class="abs lbl" data-in="166.2" style="left:120px;top:560px;width:820px;padding:24px 28px">'
          f'<div class="mono" style="font-size:44px;font-weight:900">cosine = 0.9</div>'
          f'<div style="font-size:36px;font-weight:900;margin-top:14px" data-strike="168.4">정답일 확률 90%</div>'
          f'<div data-in="169.0" style="font-size:30px;margin-top:12px;color:{TEAL};font-weight:800">벡터 방향이 얼마나 비슷한가</div></div>')
scene('M10', 155.317, 171.1, html)

# M11 177.9–192.4  27~28: BM25 세 요소 / 강점·약점
cards = [('① 몇 번 나왔나 (TF)', '많을수록 ↑, 하지만 끝없이 오르지 않음', 178.4), ('② 얼마나 드문가 (IDF)', '흔한 말보다 드문 말이 중요', 180.6), ('③ 문서 길이 보정', '길어서 우연히 많이 나온 건 아닌지', 182.9)]
html = hdr(3, 'BM25', '바코드 스캐너 — 세 가지를 본다', 177.95)
for i, (a, b, t) in enumerate(cards):
    html += (f'<div class="abs lbl" data-in="{t}" style="left:{120 + i * 570}px;top:310px;width:540px;padding:22px 26px;border-top:12px solid {ORG}">'
             f'<div style="font-size:34px;font-weight:900">{a}</div><div class="mut" style="font-size:27px;margin-top:12px;font-weight:700">{b}</div></div>')
html += (f'<svg class="abs" data-in="178.8" style="left:150px;top:470px" width="480" height="200"><path data-draw="179.0" data-d=".9" d="M10 190 C 120 60, 240 30, 470 22" stroke="{ORG}" stroke-width="6" fill="none"/>'
         f'<path d="M10 190 L470 190" stroke="#23395B55" stroke-width="3"/></svg>'
         + txt(120, 690, '<span class="grn">강함</span> · 제품 코드, 오류 코드처럼 정확한 단어', 186.4, 34, extra='font-weight:900')
         + txt(120, 760, '<span class="red">약함</span> · 뜻이 같은 다른 표현', 189.6, 34, extra='font-weight:900'))
scene('M11', 177.9, 192.4, html)

# M12 192.4–207.2  29~30: Kiwi 토큰화 → BM25 점수
html = (hdr(3, '한국어', '키위가 토큰을 만들고, 점수는 BM25가', 192.5)
        + ''.join(f'<div class="abs lbl" data-in="{t}" style="left:120px;top:{y}px;width:460px;padding:20px 26px;font-size:40px;font-weight:900">{w}</div>'
                  for w, y, t in [('스캔하는', 330, 193.2), ('스캔할', 460, 193.6)])
        + arrow(600, 430, 720, 430, 195.6, NAVY)
        + f'<div class="abs lbl" data-in="195.8" style="left:740px;top:300px;width:300px;padding:20px 0;text-align:center"><div class="mut" style="font-size:26px">형태소 분석</div><div style="font-size:44px;font-weight:900">Kiwi</div></div>'
        + arrow(1060, 430, 1180, 430, 197.4, NAVY)
        + f'<div class="abs chip" data-in="197.6" style="left:1200px;top:380px;width:220px;height:100px;font-size:46px;border-color:{YEL};background:#FFF6D6">스캔</div>'
        + txt(1200, 500, '공통 토큰', 198.0, 28, cls='mut', extra='font-weight:800')
        + '<div class="abs lane" data-in="200.6" style="left:120px;top:640px;width:1680px"></div>'
        + f'<div class="abs lbl" data-in="200.9" style="left:120px;top:680px;width:780px;padding:18px 26px;font-size:32px;font-weight:900">Kiwi → <span class="mut">검색용 토큰</span></div>'
        + f'<div class="abs lbl" data-in="202.6" style="left:980px;top:680px;width:800px;padding:18px 26px;font-size:32px;font-weight:900;border-top:10px solid {ORG}">BM25 → <span class="mut">점수 계산</span></div>'
        + stamp(1480, 560, '역할이 다르다', NAVY, 205.0, -4, 40))
scene('M12', 192.4, 207.2, html)

# M13 207.2–221.3  31~33: 하이브리드, 단위 다른 점수 → RRF
def plist(x, head, c, rows, t, unit):
    r = ''.join(f'<div class="row" data-in="{t + .3 + i * .25:.2f}"><div class="k" style="width:90px">{i + 1}위</div><div class="v mono" style="width:240px">{n}</div><div class="mono" style="color:{c};font-weight:900">{s}</div></div>' for i, (n, s) in enumerate(rows))
    return f'<div class="abs lbl" data-in="{t}" style="left:{x}px;top:300px;width:560px"><div class="hd" style="background:{c}">{head} · {unit}</div>{r}</div>'
html = (hdr(3, '하이브리드', '두 피킹 목록을 함께 쓴다', 207.3)
        + plist(120, '벡터', TEAL, [('chunk A', '0.83'), ('chunk B', '0.81'), ('chunk C', '0.77')], 208.0, '유사도')
        + plist(760, 'BM25', ORG, [('chunk B', '12.4'), ('chunk D', '9.8'), ('chunk A', '7.1')], 209.3, '점수')
        + txt(1380, 330, '0.83 + 12.4 ?', 213.2, 50, extra='font-weight:900').replace('class="abs "', 'class="abs mono"')
        + stamp(1400, 420, '단위가 다르다', RED, 214.4, -5, 40)
        + f'<div class="abs lbl" data-in="217.0" style="left:1380px;top:560px;width:400px;padding:22px 26px;border:4px solid {GRN}">'
          f'<div class="mono" style="font-size:44px;font-weight:900;color:{GRN}">RRF</div><div style="font-size:32px;font-weight:900;margin-top:8px">점수 대신 <span data-tape="219.4">순위</span>를 합친다</div></div>')
scene('M13', 207.2, 221.3, html)

# M14 221.3–242.3  34~36: RRF 영수증
rc = (f'<div class="abs lbl mono" data-in="221.8" style="left:120px;top:300px;width:820px;padding:26px 32px;border-style:dashed">'
      f'<div style="font-size:30px;font-weight:900;text-align:center">RRF RECEIPT</div>'
      f'<div style="font-size:40px;font-weight:900;text-align:center;margin:22px 0">Σ 1 / (k + 순위)</div>'
      f'<div class="mut" style="font-size:24px;text-align:center" data-in="223.6">검색기마다 순위 → 역수 → 모두 더함</div></div>')
def rec(x, name, rows, total, t, win):
    r = ''.join(f'<div data-in="{t + .5 + i * .6:.2f}" style="display:flex;justify-content:space-between;font-size:30px;margin:10px 0"><span>{a}</span><span>{b}</span></div>' for i, (a, b) in enumerate(rows))
    c = GRN if win else NAVY
    return (f'<div class="abs lbl mono" data-in="{t}" style="left:{x}px;top:{560}px;width:400px;padding:20px 26px;border-style:dashed">'
            f'<div style="font-size:32px;font-weight:900">{name}</div>{r}'
            f'<div data-in="{t + 2.0:.2f}" style="border-top:3px dashed #23395B;margin-top:10px;padding-top:10px;display:flex;justify-content:space-between;font-size:34px;font-weight:900;color:{c}"><span>합계</span><span>{total}</span></div></div>')
html = (hdr(3, 'RRF', '순위로 합치는 영수증', 221.4) + rc
        + txt(1000, 320, 'k = 60일 때', 227.4, 36, extra='font-weight:900')
        + rec(120, 'chunk A', [('벡터 1위', '1/61'), ('BM25 3위', '1/63')], '≈0.03227', 228.0, False)
        + rec(560, 'chunk B', [('벡터 2위', '1/62'), ('BM25 1위', '1/61')], '≈0.03252', 230.6, True)
        + stamp(1020, 620, '근소하게 B', GRN, 234.4, -4, 46)
        + f'<div class="abs lbl" data-in="236.8" style="left:1000px;top:400px;width:780px;padding:22px 28px;font-size:32px;font-weight:900;border:4px solid {RED}">'
          f'RRF는 <span data-tape="238.4">순위 결합</span>이지<br>내용 검증이 아니다</div>')
scene('M14', 221.3, 242.3, html)

# M15 242.3–260.6  37~39: 리랭킹 검수대
html = hdr(3, '리랭킹', '검수대에서 다시 줄 세우기', 242.4)
order0 = [('연속 스캔 방법', NAVY), ('ADF 최대 용량', GRN), ('용지 걸림 해결', NAVY)]
for i, (n, c) in enumerate(order0):
    y0 = 330 + i * 120
    dy = {0: 120, 1: -120, 2: 0}[i]
    html += (f'<div class="abs" data-mv="250.4" data-d=".8" data-dy="{dy}" style="left:0;top:0"><div class="abs lbl" data-in="{243.0 + i * .3:.2f}" style="left:120px;top:{y0}px;width:760px;padding:20px 26px;font-size:34px;font-weight:900;{"border:4px solid " + GRN if c == GRN else ""}">{n}</div></div>')
html += (''.join(f'<div class="abs" data-in="243.0" style="left:60px;top:{345 + i * 120}px;font-size:36px;font-weight:900" class="mut">{i + 1}</div>' for i in range(3))
         + f'<div class="abs lbl" data-in="248.9" style="left:980px;top:330px;width:800px;padding:22px 28px;font-size:34px;font-weight:900">질문 · “<span data-tape="249.6">최대 몇 장?</span>”</div>'
         + txt(980, 440, '→ 최대 용량이 적힌 조각을 위로', 251.4, 32, extra=f'font-weight:900;color:{GRN}')
         + f'<div class="abs lbl" data-in="255.2" style="left:980px;top:560px;width:800px;padding:22px 28px;font-size:30px;font-weight:800;border:4px solid {RED}">'
           f'처음 후보에 없던 정답은 <span data-tape="256.6">새로 찾지 못한다</span><div class="mut" style="font-size:26px;margin-top:10px">+ 시간 · 연산 증가</div></div>')
scene('M15', 242.3, 260.6, html)

# M16 260.6–274.8  40~41: A/B/C 세 레인
lanes = [('A', '벡터 검색만', '기준선', TEAL, 262.6), ('B', '벡터 + BM25 + RRF', '하이브리드', ORG, 264.6), ('C', 'B + 리랭킹', '하이브리드 + 재정렬', GRN, 267.4)]
html = hdr(3, '비교', '세 구성을 같은 조건에서', 260.7)
for i, (L, a, b, c, t) in enumerate(lanes):
    y = 300 + i * 150
    html += (f'<div class="abs" data-in="{t}" style="left:120px;top:{y}px;width:1660px;height:120px;border:3px solid {c};border-radius:6px;background:#fff;display:flex;align-items:center">'
             f'<div style="width:120px;height:100%;background:{c};color:#fff;font-size:64px;font-weight:900;display:flex;align-items:center;justify-content:center">{L}</div>'
             f'<div style="padding-left:30px;font-size:38px;font-weight:900;width:700px">{a}</div><div class="mut" style="font-size:30px;font-weight:700">{b}</div>'
             f'<div data-in="271.4" style="margin-left:auto;margin-right:40px;font-size:60px;font-weight:900;color:{c}">?</div></div>')
html += txt(120, 770, '같은 질문 · 같은 생성 모델 · 같은 프롬프트 — 승자는 재 봐야 안다', 271.6, 32, extra='font-weight:900')
scene('M16', 260.6, 274.8, html)

# ───────────── 4장 · Supabase ─────────────
# M17 282.717–296.6  43~44: 테이블과 pgvector
cols = ['chunk_id', '본문', 'applicable_models', 'page', 'embedding']
rws = [['c-0412', '“ADF에 원본을…”', 'L2805, L2885', '52*', '[0.82, …]'], ['c-0413', '“표준 용지 기준…”', 'L2805', '52*', '[0.11, …]'], ['c-0977', '“토너 교체는…”', 'L2885', '310*', '[-0.4, …]']]
def tbl(t):
    w = [190, 380, 380, 140, 260]
    def hattr(c):
        if c == 'applicable_models':
            return f'data-lit="{t + 2.6}" data-on="{YEL}"'
        if c == 'embedding':
            return f'data-lit="{t + 7.0}" data-on="{TEAL}" data-fc="#fff"'
        return ''
    head = ''.join(f'<div style="width:{w[i]}px;padding:14px 16px;font-weight:900;font-size:24px" class="mono" {hattr(c)}>{c}</div>' for i, c in enumerate(cols))
    body = ''.join('<div style="display:flex;border-top:1.5px solid #23395B33" data-in="' + f'{t + .4 + j * .3:.2f}' + '">' + ''.join(f'<div class="{"mono" if i != 1 else ""}" style="width:{w[i]}px;padding:14px 16px;font-size:24px;font-weight:700">{v}</div>' for i, v in enumerate(r)) + '</div>' for j, r in enumerate(rws))
    return f'<div class="abs lbl" data-in="{t}" style="left:120px;top:300px;width:1360px"><div style="display:flex;background:#F4EEE2">{head}</div>{body}</div>'
html = (hdr(4, 'Supabase', '랙의 칸 = 테이블의 행과 열', 282.8) + tbl(283.4)
        + txt(120, 560, '* 페이지 번호는 설명용', 284.0, 22, cls='mut')
        + f'<div class="abs lbl" data-in="285.6" style="left:120px;top:620px;width:820px;padding:20px 26px;font-size:32px;font-weight:900">모델 필터 = <span class="mono" data-tape="286.6">applicable_models</span> 칸 조건</div>'
        + f'<div class="abs lbl" data-in="291.2" style="left:1000px;top:620px;width:780px;padding:20px 26px;font-size:32px;font-weight:900;border:4px solid {TEAL}">'
          f'<span class="mono teal">pgvector</span> 확장 → 벡터 저장 + 유사도 검색</div>')
scene('M17', 282.717, 296.6, html)

# M18 296.6–310.0  45~46: ts_rank ≠ BM25
html = (hdr(4, '헷갈리는 점', 'PostgreSQL 전문 검색 ≠ BM25', 296.7)
        + f'<div class="abs lbl" data-in="297.4" style="left:120px;top:320px;width:760px;padding:26px 30px"><div class="mut" style="font-size:26px">PostgreSQL 기본</div>'
          f'<div style="font-size:38px;font-weight:900;margin-top:10px">단어 전문 검색</div><div class="mono" style="font-size:40px;font-weight:900;margin-top:16px">ts_rank()</div></div>'
        + f'<div class="abs" data-in="302.4" style="left:930px;top:400px;font-size:110px;font-weight:900;color:{RED}">≠</div>'
        + f'<div class="abs lbl" data-in="302.8" style="left:1080px;top:320px;width:700px;padding:26px 30px;border-top:12px solid {ORG}"><div class="mut" style="font-size:26px">알고리즘</div>'
          f'<div class="mono" style="font-size:52px;font-weight:900;margin-top:10px;color:{ORG}">BM25</div></div>'
        + f'<div class="abs lbl" data-in="306.6" style="left:120px;top:640px;width:1660px;padding:22px 28px;font-size:34px;font-weight:900">'
          f'기본 기능만으로 <span data-tape="307.6">Kiwi와 BM25가 자동 연결되지 않는다</span></div>')
scene('M18', 296.6, 310.0, html)

# M19 310.0–335.6  47~49: 방법 A 역할 분담, 미리 만든 검색용 자료
html = (hdr(4, '방법 A', 'Supabase + Python BM25', 310.1)
        + f'<div class="abs lbl" data-in="310.6" style="left:120px;top:300px;width:800px"><div class="hd">Supabase · 랙</div>'
          f'<div style="padding:22px 26px;font-size:32px;line-height:1.8;font-weight:800">'
          f'<div data-in="311.6">· 조각 · 메타데이터 · 벡터 저장</div><div data-in="314.2">· 모델 필터</div><div data-in="315.4">· 벡터 검색 <span class="mono teal" style="font-size:26px">(pgvector)</span></div></div></div>'
        + f'<div class="abs lbl" data-in="317.7" style="left:980px;top:300px;width:800px"><div class="hd" style="background:{ORG}">Python · 작업대</div>'
          f'<div style="padding:22px 26px;font-size:32px;line-height:1.8;font-weight:800">'
          f'<div data-in="320.0">· Kiwi 토큰화 <span class="mut" style="font-size:24px">(질문 · 조각 같은 방식)</span></div><div data-in="322.6">· <span class="mono">rank_bm25</span> 점수</div></div></div>'
        + stamp(140, 600, '구현이 비교적 간단', GRN, 327.0, -3, 40)
        + f'<div class="abs lbl" data-in="329.6" style="left:980px;top:600px;width:800px;padding:20px 26px;font-size:30px;font-weight:800;border:4px solid {YEL}">'
          f'요청마다 전체 재토큰화 <span class="red">✗</span><br>검색용 자료를 <span data-tape="332.6">미리 만들어 재사용</span> <span class="grn">✓</span></div>')
scene('M19', 310.0, 335.6, html)

# M20 335.6–348.3  50~51: RRF도 파이썬 / 저장 위치 vs 계산 위치
html = (hdr(4, '방법 A', 'RRF도 작업대에서', 335.7)
        + lbl(120, 300, 560, 'Supabase 벡터 결과', [('1위', '<span class="mono">c-0412</span>', ''), ('2위', '<span class="mono">c-0413</span>', '')], 336.2, hc=TEAL)
        + lbl(120, 560, 560, 'Python BM25 결과', [('1위', '<span class="mono">c-0413</span>', ''), ('2위', '<span class="mono">c-0977</span>', '')], 336.8, hc=ORG)
        + arrow(700, 420, 840, 520, 338.2) + arrow(700, 680, 840, 580, 338.4)
        + f'<div class="abs lbl" data-in="338.6" style="left:860px;top:460px;width:360px;padding:24px;text-align:center;font-size:40px;font-weight:900;color:{GRN}">RRF<div class="mut" style="font-size:24px">조각 아이디 + 순위</div></div>'
        + f'<div class="abs lbl" data-in="341.8" style="left:1280px;top:300px;width:500px;padding:26px 28px;font-size:34px;font-weight:900;line-height:1.6">'
          f'<div>저장 위치</div><div class="mut" style="font-size:28px">Supabase</div><div style="margin-top:20px">계산 위치</div><div class="mut" style="font-size:28px">Supabase + Python</div></div>'
        + stamp(1300, 680, '따로 생각하기', NAVY, 345.0, -4, 40))
scene('M20', 335.6, 348.3, html)

# ───────────── 5장 · 생성·검증·보류 ─────────────
# M21 348.3–379.2  52~56: 입력 3요소, 오독, 인용 vs 검증
ins = [('지시', '제공된 근거만 · 출처 표시', NAVY, 352.6), ('질문', 'MFC-L2805DW 연속 스캔 몇 장?', TEAL, 355.0), ('근거', '찾은 조각 원문 + 근거 번호 [R1]', GRN, 356.6)]
html = hdr(5, '생성', '찾은 근거를 직접 넣어 준다', 348.4)
for i, (a, b, c, t) in enumerate(ins):
    html += (f'<div class="abs lbl" data-in="{t}" data-out="371.9" style="left:120px;top:{300 + i * 130}px;width:820px;padding:18px 24px;border-left:14px solid {c}">'
             f'<div style="font-size:34px;font-weight:900">{a}</div><div class="mut" style="font-size:26px;font-weight:700">{b}</div></div>')
html += (arrow(960, 470, 1080, 470, 357.6, NAVY, d=.4).replace('<svg ', '<svg data-out="371.9" ') + '<div class="abs" data-out="371.9" style="left:0;top:0">' + box(1100, 330, 300, 280, 357.8, '<div style="text-align:center;margin-top:100px;font-size:52px;font-weight:900">LLM</div>') + '</div>'
         + txt(1100, 640, '검색 시스템을 알아서 읽지 않는다', 361.0, 28, cls='mut', extra='font-weight:800').replace('data-in="361.0"', 'data-in="361.0" data-out="371.9"')
         + stamp(1450, 400, '근거 오독', RED, 368.6, -5, 44).replace('data-stamp', 'data-out="371.9" data-stamp')
         # 인용 vs 검증
         + f'<div class="abs lbl" data-in="372.5" style="left:120px;top:330px;width:800px;padding:26px 30px"><div class="mono" style="font-size:30px;color:{TEAL};font-weight:900">CITATION · 인용</div>'
           f'<div style="font-size:40px;font-weight:900;margin-top:12px">어디서 가져왔나?</div></div>'
         + f'<div class="abs lbl" data-in="375.0" style="left:980px;top:330px;width:800px;padding:26px 30px;border:4px solid {GRN}"><div class="mono" style="font-size:30px;color:{GRN};font-weight:900">VERIFICATION · 검증</div>'
           f'<div style="font-size:40px;font-weight:900;margin-top:12px">정말 이 말을 뒷받침하나?</div></div>')
scene('M21', 348.3, 379.2, html)

# M22 387.117–394.1  58: 교차 모델 인용
html = (hdr(5, '검증', '숫자가 같아도, 모델이 다르면 실패', 387.2)
        + lbl(120, 320, 760, '질문', [('모델', '<span class="mono">MFC-L2805DW</span>', '')], 387.5, hc=TEAL)
        + lbl(980, 320, 800, '인용한 근거 [R2]', [('적용 모델', '<span class="mono">MFC-L2885DW</span>', 'data-tape="389.4"'), ('수치', '우연히 같음', '')], 388.0, hc=NAVY)
        + stamp(1200, 600, '근거 실패', RED, 391.4, -5, 56))
scene('M22', 387.117, 394.1, html)

# M23 402.017–428.4  61~64: 부당 거부, 원인 4갈래, 좋은 래그, 6장 예고
causes = [('자료에 답이 없다', GRN, '보류가 정답'), ('검색이 놓쳤다', ORG, '검색 점검'), ('찾고도 생성에서 틀렸다', ORG, '프롬프트·생성 점검'), ('시스템 오류 · 시간 초과', RED, '보류가 아님')]
html = (hdr(5, '보류', '무조건 거부가 좋은 건 아니다', 402.1, out=424.6)
        + f'<div class="abs lbl" data-in="402.8" data-out="409.2" style="left:120px;top:320px;width:1660px;padding:24px 28px;font-size:34px;font-weight:900">'
          f'매뉴얼에 답이 있는데 검색을 못 해서 “모르겠다” → <span class="red" data-tape="407.2">부당한 거부</span></div>')
for i, (a, c, b) in enumerate(causes):
    html += (f'<div class="abs lbl" data-in="{410.6 + i * 1.7:.2f}" data-out="418.5" style="left:{120 + (i % 2) * 840}px;top:{450 + (i // 2) * 150}px;width:820px;padding:18px 24px;border-left:14px solid {c}">'
             f'<div style="font-size:32px;font-weight:900">{a}</div><div class="mut" style="font-size:24px;font-weight:700">{b}</div></div>')
html += (f'<div class="abs lbl" data-in="418.9" data-out="424.6" style="left:120px;top:360px;width:1660px;padding:30px 34px;font-size:44px;font-weight:900;line-height:1.5;border:4px solid {GRN}">'
         f'답할 수 있을 때 답하고,<br><span data-tape="421.8">없을 때만 정직하게 멈춘다</span></div>'
         + txt(120, 70, '<span class="st">STATION 06 · 최적화</span>', 424.9, 26)
         + txt(120, 136, '더 빠르게, 더 잘 찾게', 425.2, 56, extra='font-weight:900')
         + f'<div class="abs chip" data-in="426.2" style="left:120px;top:330px;width:300px;height:90px;font-size:38px">캐싱</div>'
         + f'<div class="abs chip" data-in="426.6" style="left:460px;top:330px;width:360px;height:90px;font-size:38px">쿼리 리라이트</div>')
scene('M23', 402.017, 428.4, html)

# ───────────── 6장 · 최적화 ─────────────
# M24 435.9–450.3  66~67: 캐시 키
html = (hdr(6, '캐싱', '위험: 엉뚱한 답의 재사용', 436.0)
        + lbl(120, 310, 760, '저장된 답', [('키', '<span class="mono">L2805 + 질문</span>', '')], 436.6, hc=GRN)
        + lbl(980, 310, 800, '새 질문', [('키', '<span class="mono">L2885 + 질문</span>', 'data-tape="438.6"')], 437.4, hc=NAVY)
        + stamp(1150, 470, '재사용 금지', RED, 439.6, -4, 44)
        + f'<div class="abs lbl" data-in="441.8" style="left:120px;top:590px;width:1000px;padding:20px 26px;font-size:32px;font-weight:900;border:4px solid {GRN}">'
          f'처음엔 <span data-tape="443.0">모델명 + 질문이 정확히 같을 때만</span> 재사용</div>'
        + f'<div class="abs lbl" data-in="446.2" style="left:1180px;top:590px;width:600px;padding:20px 26px;font-size:30px;font-weight:800">문서 버전 · 설정 변경 →<br><span class="red">저장한 답 무효</span></div>')
scene('M24', 435.9, 450.3, html)

# M25 450.3–477.1  68~71: 리라이트 표, 보존 항목, 전체 경로 예고
pairs = [('“종이가 씹혀요”', '용지 걸림', 456.6), ('“와이파이가 안 돼요”', '무선 네트워크 연결', 458.6)]
html = hdr(6, '쿼리 리라이트', '뜻은 그대로, 매뉴얼의 말로', 450.4, out=472.9)
for i, (a, b, t) in enumerate(pairs):
    y = 310 + i * 120
    html += (f'<div class="abs lbl" data-in="{t}" data-out="472.9" style="left:120px;top:{y}px;width:640px;padding:20px 26px;font-size:34px;font-weight:900">{a}</div>'
             + arrow(780, y + 44, 900, y + 44, t + .4, NAVY, d=.3).replace('<svg ', '<svg data-out="472.9" ')
             + f'<div class="abs lbl" data-in="{t + .6:.2f}" data-out="472.9" style="left:920px;top:{y}px;width:640px;padding:20px 26px;font-size:34px;font-weight:900;border:4px solid {TEAL}">{b}</div>')
html += (f'<div class="abs lbl" data-in="462.8" data-out="472.9" style="left:120px;top:580px;width:1000px;padding:20px 26px;font-size:30px;font-weight:900">'
         f'절대 바꾸지 않기 · <span class="mono">모델 코드 · 오류 코드 · 수치 · 조건</span></div>'
         + f'<div class="abs lbl" data-in="467.4" data-out="472.9" style="left:1180px;top:580px;width:600px;padding:20px 26px;font-size:28px;font-weight:800">원래 질문 ↔ 바꾼 질문<br>나란히 기록해 개선 확인</div>'
         + txt(120, 70, '<span class="st">STATION 07 · 전체 경로</span>', 473.3, 26)
         + txt(120, 136, '질문 하나가 지나가는 길', 473.5, 56, extra='font-weight:900')
         + '<div class="abs lane" data-in="474.2" style="left:120px;top:420px;width:1680px"></div>')
scene('M25', 450.3, 477.1, html)

# ───────────── 7장 · 전체 경로 ─────────────
# M26 485.017–515.2  73끝~77: 경로 지도 점등, 로그
stops = [('모델 코드', 485.2), ('캐시', 486.6), ('리라이트', 489.6), ('모델 필터', 491.6), ('벡터', 494.4), ('BM25', 496.4), ('RRF', 498.2), ('리랭킹', 500.0),
         ('생성', 502.2), ('검증', 504.2), ('보류', 506.2)]
html = (txt(120, 70, '<span class="st">STATION 07 · 전체 경로</span>', 485.1, 26)
        + txt(120, 140, '<span class="mono">L2805</span> · 연속 스캔 몇 장?', 485.1, 50, extra='font-weight:900')
        + '<div class="abs lane" data-in="485.1" style="left:140px;top:420px;width:1640px"></div>')
for i, (n, t) in enumerate(stops):
    x = 140 + i * 150
    html += (f'<div class="abs" style="left:{x}px;top:395px;width:50px;height:50px;border-radius:50%;border:5px solid {NAVY}" data-lit="{t}" data-on="{YEL}" data-off="#EFE6D6"></div>'
             f'<div class="abs" style="left:{x - 40}px;top:{465 if i % 2 == 0 else 310}px;width:130px;text-align:center;font-size:26px;font-weight:900">{n}</div>')
html += (f'<div class="abs lbl mono" data-in="508.4" style="left:120px;top:570px;width:1660px;padding:20px 26px;font-size:24px;line-height:1.7;border-style:dashed">'
         f'<div style="font-weight:900;font-size:28px">LOG</div>'
         f'<div data-in="509.0">candidates · ranks · scores · rerank · answer · citations · hold_reason</div>'
         f'<div data-in="510.0">latency_ms · tokens_in · tokens_out · cost · retries</div></div>'
         + txt(1180, 760, '틀렸을 때, 어디서 틀렸는지', 512.4, 32, extra='font-weight:900'))
scene('M26', 485.017, 515.2, html)

# ───────────── 8장 · 평가 ─────────────
checks = ['찾았나', '답이 맞나', '근거가 맞나', '거부 판단이 맞나', '느리고 비싼가', '정상 동작했나']
def sheet(t, active, x=1240):
    r = ''.join(f'<div style="display:flex;align-items:center;gap:14px;padding:10px 0;font-size:28px;font-weight:{900 if i == active else 700};{"" if i == active else "opacity:.45"}">'
                f'<div style="width:30px;height:30px;border:3px solid {NAVY};{"background:" + YEL if i == active else ""}"></div>{c}</div>' for i, c in enumerate(checks))
    return f'<div class="abs lbl" data-in="{t}" style="left:{x}px;top:300px;width:540px;padding:20px 26px"><div style="font-weight:900;font-size:26px" class="mono">QC SHEET</div>{r}</div>'

# M27 523.117–547.2  78끝~80: Hit@5, 답변 정확도
html = (hdr(8, '평가', '히트 앳 파이브 · 답변 정확도', 523.2) + sheet(523.4, 0).replace('opacity:.45', 'opacity:.45').replace('data-in="523.4"', 'data-in="523.4" data-out="536.2"') + sheet(536.4, 1)
        + ''.join(f'<div class="abs lbl" data-in="{526.6 + i * .2:.2f}" data-out="536.2" style="left:{120 + i * 210}px;top:330px;width:190px;height:120px;padding:14px;text-align:center;{"border:4px solid " + GRN if i == 3 else ""}">'
                  f'<div class="mut" style="font-size:24px">{i + 1}위</div><div class="mono" style="font-size:24px;font-weight:900;margin-top:10px">{"정답 근거" if i == 3 else "chunk"}</div></div>' for i in range(5))
        + f'<div class="abs" data-in="527.4" data-out="536.2" style="left:110px;top:310px;width:1060px;height:160px;border:5px dashed {NAVY}"></div>'
        + txt(120, 500, '상위 5개 안에 있으면 <b class="grn">1</b>, 아니면 <b class="red">0</b>', 529.6, 36, extra='font-weight:800').replace('data-in="529.6"', 'data-in="529.6" data-out="536.2"')
        + txt(120, 580, '분모 = <span data-tape="533.0">답이 있는 질문만</span>', 532.4, 36, extra='font-weight:900').replace('data-in="532.4"', 'data-in="532.4" data-out="536.2"')
        + stamp(140, 360, '찾음 ≠ 맞음', RED, 536.8, -4, 44)
        + f'<div class="abs lbl" data-in="540.0" style="left:120px;top:480px;width:1060px;padding:22px 28px;font-size:32px;font-weight:900">'
          f'최종 답이 채운 핵심 사실<div style="display:flex;gap:16px;margin-top:16px">'
          + ''.join(f'<div class="chip" data-in="{542.6 + i * .5:.2f}" style="font-size:30px">{c}</div>' for i, c in enumerate(['모델', '수치', '조건', '절차'])) + '</div></div>')
scene('M27', 523.117, 547.2, html)

# M28 547.2–568.5  81~83: 근거 정확도, 인용 0건, 거부 정확도
html = (hdr(8, '평가', '근거 정확도 · 거부 정확도', 547.3) + sheet(547.4, 2).replace('data-in="547.4"', 'data-in="547.4" data-out="562.5"') + sheet(562.6, 3)
        + lbl(120, 310, 1060, '근거 정확도', [('확인', '인용한 근거가 주장 · 모델 · 조건을 뒷받침?', ''), ('주의', '답이 우연히 맞아도 인용이 틀리면 실패', f'style="color:{RED}"')], 547.8, step=2.4)
        + f'<div class="abs lbl mono" data-in="557.6" style="left:120px;top:560px;width:1060px;padding:20px 26px;font-size:30px;font-weight:900">인용 0건 → 근거 정확도 <span data-strike="559.6">100%</span></div>'
        + stamp(820, 600, '계산 실수', RED, 560.0, -4, 38)
        + f'<div class="abs lbl" data-in="562.9" style="left:120px;top:680px;width:1060px;padding:18px 26px;font-size:28px;font-weight:900">'
          f'거부 정확도 · 답 있으면 <span class="grn">답하고</span>, 근거 없으면 <span class="red">거부</span>했나</div>')
scene('M28', 547.2, 568.5, html)

# M29 568.5–590.0  84~86: P50/P95, 토큰·비용
bars = [3, 5, 8, 10, 9, 7, 5, 4, 3, 2, 2, 1, 1, 1]
bh = ''.join(f'<div class="abs" data-in="{569.4 + i * .05:.2f}" style="left:{140 + i * 64}px;top:{620 - b * 26}px;width:52px;height:{b * 26}px;background:{TEAL}"></div>' for i, b in enumerate(bars))
html = (hdr(8, '평가', '속도와 비용', 568.6) + sheet(568.7, 4) + bh
        + f'<div class="abs" style="left:130px;top:620px;width:920px;height:3px;background:{NAVY}"></div>'
        + txt(140, 640, '응답 시간 →', 569.6, 26, cls='mut', extra='font-weight:800')
        + f'<div class="abs" data-in="574.8" style="left:{140 + 4 * 64 + 26}px;top:330px;width:5px;height:300px;background:{GRN}"></div>'
        + txt(140 + 4 * 64 - 20, 290, 'P50 · 중앙값', 574.8, 28, extra=f'font-weight:900;color:{GRN}')
        + f'<div class="abs" data-in="576.0" style="left:{140 + 10 * 64 + 26}px;top:330px;width:5px;height:300px;background:{ORG}"></div>'
        + txt(140 + 10 * 64 - 140, 290, 'P95 · 약 95%가 이 안에', 576.0, 28, extra=f'font-weight:900;color:{ORG}')
        + txt(140 + 12 * 64, 380, '최댓값 아님 →', 579.2, 24, extra=f'font-weight:900;color:{RED}')
        + f'<div class="abs lbl mono" data-in="581.6" style="left:120px;top:700px;width:1060px;padding:16px 24px;font-size:26px;font-weight:800;border-style:dashed">'
          f'tokens_in · tokens_out <span class="mut">(단가 따로)</span> → 질문당 비용 = <span data-tape="586.2">재시도 포함 전체 비용 ÷ 시도 질문 수</span></div>')
scene('M29', 568.5, 590.0, html)

# M30 590.0–612.4  87~89: 성공률 vs 정확도, 공정 비교
html = (hdr(8, '평가', '정상 동작 · 공정한 비교', 590.1) + sheet(590.2, 5).replace('data-in="590.2"', 'data-in="590.2" data-out="600.9"')
        + f'<div class="abs lbl" data-in="592.6" data-out="600.9" style="left:120px;top:320px;width:1060px;padding:22px 28px">'
          f'<div style="font-size:30px;font-weight:900">틀린 답이 정상적으로 돌아옴</div>'
          f'<div style="display:flex;gap:30px;margin-top:16px;font-size:30px;font-weight:900"><div class="grn">성공률 ✓</div><div class="red">정확도 ✗</div></div></div>'
        + f'<div class="abs lbl" data-in="597.6" data-out="600.9" style="left:120px;top:520px;width:1060px;padding:18px 26px;font-size:28px;font-weight:900">오류 · 시간 초과는 <span data-tape="598.6">기록에서 지우지 않는다</span></div>')
fix = [('검색 구성 비교', ['생성 모델', '프롬프트'], 'A · B · C', 601.4), ('생성 모델 비교', ['검색 결과', '프롬프트'], '모델 1 · 모델 2', 605.0)]
for i, (a, locked, var, t) in enumerate(fix):
    y = 320 + i * 220
    html += (f'<div class="abs lbl" data-in="{t}" style="left:120px;top:{y}px;width:1660px;padding:22px 28px;display:flex;align-items:center;gap:26px">'
             f'<div style="font-size:34px;font-weight:900;width:300px">{a}</div>'
             + ''.join(f'<div class="chip" style="font-size:28px;background:#E7EDF4">🔒 {l}</div>' for l in locked)
             + f'<div style="margin-left:auto;font-size:30px;font-weight:900;color:{ORG}">바꾸는 것 · {var}</div></div>')
html += txt(120, 780, '그래야 무엇이 결과를 바꿨는지 안다', 609.2, 34, extra='font-weight:900')
scene('M30', 590.0, 612.4, html)

# ───────────── 9장 · 마무리 ─────────────
# M31 620.317–626.8  91: 과정 전체
fin = ['꺼내기', '맞는 조각 찾기', '근거로 답하기', '근거 확인', '실패 기록']
html = ('<div class="abs lane" data-in="620.4" style="left:120px;top:520px;width:1680px"></div>'
        + txt(120, 160, '구별하는 건 모델 하나가 아니라', 620.4, 40, cls='mut', extra='font-weight:800')
        + txt(120, 230, '과정 전체', 620.6, 80, extra='font-weight:900'))
for i, n in enumerate(fin):
    html += (f'<div class="abs lbl" data-in="{620.8 + i * .55:.2f}" style="left:{120 + i * 340}px;top:440px;width:310px;padding:22px 0;text-align:center;font-size:32px;font-weight:900">'
             f'<div class="mono mut" style="font-size:22px">STATION {i + 1:02d}</div>{n}</div>')
html += stamp(1440, 650, '출고 완료', GRN, 624.4, -5, 52)
scene('M31', 620.317, 626.8, html)
