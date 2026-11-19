# (id, start_frame, end_frame, html)  times in data-* are absolute timeline seconds
S = {}
def hdr(tag, title, t, y=90):
    return f'<div class="abs tag" data-in="{t}" style="left:140px;top:{y}px">{tag}</div><div class="abs h" data-in="{t+0.08}" style="left:140px;top:{y+44}px">{title}</div>'

# M01 13.0–16.0  3~4명 · 5일 · 40시간
S['M01']=(312,384, hdr('PROJECT','Brother 10개 모델 · 기술지원 RAG Agent',13.0)+''.join(
 f'<div class="abs card" data-in="{t}" style="left:{x}px;top:380px;width:500px;height:300px;display:flex;flex-direction:column;align-items:center;justify-content:center">'
 f'<div style="font-size:120px;font-weight:900" class="{c}">{big}</div><div style="font-size:38px;font-weight:700;margin-top:6px" class="mut">{small}</div></div>'
 for x,t,big,small,c in [(140,13.2,'3~4명','한 팀','cyan'),(710,14.15,'5일','닷새',''),(1280,14.75,'40시간','개발 시간','amber')]))

# M02 16.0–24.29  두 권의 PDF
ink=['DCP-T530DW','DCP-T730DW','DCP-T830DW','DCP-T835DW','MFC-T930DW']
las=['HL-L2464DW','DCP-L2605DW','DCP-L2640DW','MFC-L2805DW','MFC-L2885DW']
def book(x,title,col,models,tm,tp,pages):
    chips=''.join(f'<div data-in="{tm+i*0.12:.2f}" class="mono" style="display:flex;align-items:center;justify-content:center;border-radius:14px;font-weight:800;width:320px;height:60px;margin:12px 0;font-size:28px;background:#F3F5F8;border:2px solid {col}55;color:#1F2733">{m}</div>' for i,m in enumerate(models))
    return (f'<div class="abs card" data-in="16.9" style="left:{x}px;top:250px;width:760px;height:600px;border-color:{col}88">'
     f'<div style="position:absolute;left:44px;top:34px;font-size:44px;font-weight:900;color:{col}">{title}</div>'
     f'<div style="position:absolute;left:44px;top:96px;font-size:28px" class="mut">한국어 공식 PDF</div>'
     f'<div style="position:absolute;left:44px;top:160px">{chips}</div>'
     f'<div style="position:absolute;right:50px;top:200px;text-align:right"><div data-count="{tp}" data-v="{pages}" style="font-size:150px;font-weight:900;line-height:1;color:{col}">0</div>'
     f'<div data-in="{tp}" style="font-size:44px;font-weight:800">쪽</div></div></div>')
S['M02']=(384,583, hdr('SOURCES','자료는 공식 PDF 두 권',16.0)+book(140,'잉크젯','#1FA4B8',ink,19.0,20.2,466)+book(1020,'흑백 레이저','#E39A1E',las,21.2,22.8,633))

# M03 30.875–36.208  일부 모델에만 → 다른 모델 절차 = 그럴듯한 오답
cols=['A','B','C','D','E']
cells=''.join(f'<div style="width:120px;height:70px;display:flex;align-items:center;justify-content:center;font-size:40px;font-weight:900;border-left:2px solid #E3E7EC" '
   + (f'data-hl="31.2" data-c="#E39A1E" class="amber">✓</div>' if c in 'AB' else f'data-dim="31.3" class="mut">—</div>') for c in cols)
heads=''.join(f'<div style="width:120px;height:60px;display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:900;background:#34506B;color:#fff">모델 {c}</div>' for c in cols)
S['M03']=(741,869,
 f'<div class="abs" data-in="30.9" style="left:140px;top:90px"><div class="tag">TRAP</div><div class="h" style="margin-top:8px">한 행이 <span class="amber">일부 모델에만</span> 해당</div></div>'
 f'<div class="abs card" data-in="30.95" style="left:140px;top:300px;padding:20px 26px"><div style="display:flex;margin-left:160px">{heads}</div>'
 f'<div style="display:flex;align-items:center"><div style="width:160px;font-size:28px;font-weight:700" class="mut">표의 한 행*</div>{cells}</div>'
 f'<div style="font-size:24px;margin-top:10px" class="mut">* 각주: 일부 모델에만 적용</div></div>'
 f'<div class="abs card" data-in="32.75" style="left:140px;top:600px;width:600px;height:220px;padding:26px 34px;border-color:#1FA4B8aa"><div style="font-size:26px" class="cyan">검색된 근거</div><div style="font-size:40px;font-weight:900;margin-top:8px">모델 A의 절차</div><div style="font-size:26px;margin-top:8px" class="mut">1. … 2. … 3. …</div></div>'
 f'<svg class="abs" style="left:740px;top:620px" width="300" height="180"><path data-draw="33.7" d="M20 90 L270 90" stroke="#1FA4B8" stroke-width="8" fill="none"/><path data-draw="34.2" data-d=".3" d="M240 60 L275 90 L240 120" stroke="#1FA4B8" stroke-width="8" fill="none"/></svg>'
 f'<div class="abs card" data-in="34.0" style="left:1060px;top:600px;width:720px;height:220px;padding:26px 34px"><div style="font-size:26px" class="mut">질문 · 모델 C</div><div style="font-size:40px;font-weight:900;margin-top:8px">답변: 1. … 2. … 3. …</div>'
 f'<div style="font-size:26px;margin-top:8px" class="mut">문장은 자연스럽다</div></div>'
 f'<div class="abs" data-in="34.9" data-base="rotate(-6deg)" style="left:1330px;top:520px;padding:10px 26px;border:6px solid #D64545;border-radius:14px;color:#D64545;font-size:54px;font-weight:900;background:#FFFFFFee">그럴듯한 오답</div>')

# M04 36.208–45.0  메타데이터 역추적
tags=[('document_id',37.6,'#6B7686'),('page / section',38.5,'#6B7686'),('applicable_models',39.9,'#E39A1E')]
tg=''.join(f'<div data-in="{t}" class="chip mono" style="height:54px;padding:0 22px;margin:8px 10px 0 0;font-size:28px;border:2px solid {c};color:{c}">{n}</div>' for n,t,c in tags)
S['M04']=(869,1085, hdr('METADATA','조각마다 출처와 적용 모델을 붙인다',36.25)+
 f'<div class="abs card" data-in="36.6" style="left:140px;top:300px;width:560px;height:520px;padding:30px 34px"><div class="tag" style="font-size:24px">원문 PDF</div>'
 f'<div style="font-size:34px;font-weight:900;margin-top:10px">잉크젯 공통 PDF</div><div style="margin-top:20px">'+''.join(f'<div style="height:16px;width:{w}px;background:#D9DEE5;border-radius:8px;margin:14px 0"></div>' for w in [440,380,460,300,420,360])+
 f'</div><div data-hl="42.8" data-c="#1FA4B8" style="margin-top:12px;padding:10px 16px;border-radius:10px;font-size:28px;font-weight:800">p. ○○ · 표 한 행</div></div>'
 f'<div class="abs card" data-in="37.0" style="left:800px;top:300px;width:980px;height:250px;padding:28px 34px;border-color:#1FA4B8aa"><div style="font-size:24px" class="cyan">청크 chunk_id</div>'
 f'<div style="font-size:32px;font-weight:700;margin-top:6px">“… 해당 기능의 설정 절차 …”</div><div style="display:flex;flex-wrap:wrap">{tg}</div></div>'
 f'<div class="abs card" data-in="41.6" style="left:800px;top:620px;width:980px;height:200px;padding:28px 34px"><div style="font-size:24px" class="mut">답변 속 주장</div><div style="font-size:34px;font-weight:800;margin-top:8px">“이 모델에서는 … 를 확인하세요”</div></div>'
 f'<svg class="abs" style="left:0;top:0" width="1920" height="1080"><path data-draw="42.4" data-d=".7" d="M800 720 C 740 720, 740 690, 700 690" stroke="#1FA4B8" stroke-width="6" fill="none"/>'
 f'<path data-draw="43.3" data-d=".7" d="M1600 620 L1600 540" stroke="#E39A1E" stroke-width="6" fill="none"/></svg>'
 f'<div class="abs" data-in="43.4" style="left:1620px;top:560px;font-size:28px;font-weight:800" class="amber"><span class="amber">모델까지 역추적</span></div>')

# M05 45.0–54.42  검색 3종
def col(x,L,name,sub,t,c,order):
    rows=''.join(f'<div data-in="{t+0.3+i*0.12:.2f}" style="display:flex;align-items:center;margin:12px 0"><div style="width:44px;font-size:28px;font-weight:900" class="mut">{i+1}</div>'
       f'<div class="mono" style="flex:1;height:56px;border-radius:12px;background:#F3F5F8;display:flex;align-items:center;padding-left:18px;font-size:26px;{"border:2px solid "+c if k=="c07" else ""}">chunk {k}</div></div>' for i,k in enumerate(order))
    return (f'<div class="abs card" data-in="{t}" style="left:{x}px;top:330px;width:500px;height:500px;padding:26px 30px;border-color:{c}aa">'
      f'<div style="display:flex;align-items:baseline;gap:16px"><div style="font-size:70px;font-weight:900;color:{c}">{L}</div><div style="font-size:34px;font-weight:900">{name}</div></div>'
      f'<div style="font-size:24px;margin-top:4px" class="mut">{sub}</div><div style="margin-top:14px">{rows}</div></div>')
S['M05']=(1085,1306,
 f'<div class="abs tag" data-in="45.05" style="left:140px;top:90px">RETRIEVAL</div><div class="abs h" data-in="45.1" style="left:140px;top:134px">같은 질문 · 같은 조건 · 세 가지 검색기</div>'
 +col(140,'A','Vector','의미(임베딩)로 찾기',48.2,'#1FA4B8',['c12','c07','c31'])
 +col(710,'B','Hybrid','BM25 키워드 + Vector 결합',49.6,'#4A6FA5',['c07','c12','c44'])
 +col(1280,'C','Re-ranking','후보를 다시 채점',52.3,'#E39A1E',['c07','c44','c12'])
 +'<div class="abs" data-in="53.4" style="left:140px;top:860px;font-size:28px" class="mut"><span class="mut">후보 · 순위 · 점수 · chunk_id를 단계별로 기록 (순위는 예시)</span></div>')

# M06 54.42–59.0 인용
S['M06']=(1306,1416, hdr('ANSWER','찾아낸 문서를 그대로 인용',54.45)+
 '<div class="abs card" data-in="54.7" style="left:140px;top:300px;width:1640px;height:470px;padding:40px 50px">'
 '<div style="font-size:28px" class="mut">질문 · DCP-T830DW</div><div style="font-size:40px;font-weight:800;margin-top:16px;line-height:1.6">답변: 공식 문서에 따르면 … 순서로 확인합니다.</div>'
 '<div style="display:flex;gap:20px;margin-top:50px">'
 '<div data-in="56.6" class="chip" style="height:70px;padding:0 28px;font-size:30px;background:#E3F4F7;border:2px solid #1FA4B8;color:#1A8FA3">문서 제목 · 잉크젯 공통 PDF</div>'
 '<div data-in="57.5" class="chip" style="height:70px;padding:0 28px;font-size:30px;background:#E3F4F7;border:2px solid #1FA4B8;color:#1A8FA3">페이지 · 절</div>'
 '<div data-in="57.9" class="chip" style="height:70px;padding:0 28px;font-size:30px;background:#FBEFD9;border:2px solid #E39A1E;color:#E39A1E">적용 모델 ✓</div></div></div>')

# M07 66.2–74.0 거부 규칙 + 상태 3종
def row(y,t,q,act,res,c,mark):
    return (f'<div class="abs card" data-in="{t}" style="left:140px;top:{y}px;width:1640px;height:150px;display:flex;align-items:center;padding:0 40px;gap:30px">'
      f'<div style="width:520px;font-size:36px;font-weight:800">{q}</div><div style="font-size:44px" class="mut">→</div>'
      f'<div style="width:300px;font-size:36px;font-weight:800">{act}</div><div style="font-size:44px" class="mut">→</div>'
      f'<div style="font-size:48px;font-weight:900;color:{c}">{mark} {res}</div></div>')
st=''.join(f'<div data-in="{t}" class="chip" style="height:74px;padding:0 34px;font-size:34px;border:3px solid {c};color:{c};margin-right:24px">{n}</div>' for n,t,c in [('근거 부족',70.4,'#E39A1E'),('검색 오류',71.0,'#1FA4B8'),('생성 오류',71.8,'#D64545')])
S['M07']=(1589,1776, hdr('ABSTENTION','거부도 맞아야 점수',66.25)+
 row(300,66.3,'근거 없는 질문','거부','정답 (1점)','#2E9E57','✓')+row(480,67.4,'답이 있는 질문','거부','오답','#D64545','✗')+
 f'<div class="abs" style="left:140px;top:700px"><div class="tag" data-in="70.3" style="font-size:24px;margin-bottom:14px">상태를 따로 표시</div><div style="display:flex">{st}</div></div>')

# M08 74.0–81.92 최적화 + 모델 비교
S['M08']=(1776,1966, hdr('EFFICIENCY','속도와 비용도 챙긴다',74.05)+
 '<div class="abs card" data-in="76.1" style="left:140px;top:300px;width:700px;height:520px;padding:34px 40px"><div class="tag" style="font-size:24px">최적화 · 1개 이상</div>'
 '<div data-in="76.3" class="chip" style="width:600px;height:110px;margin-top:30px;font-size:44px;border:3px solid #1FA4B8;color:#1A8FA3">캐싱</div>'
 '<div data-in="76.6" style="text-align:center;font-size:34px;margin:14px 0" class="mut">또는</div>'
 '<div data-in="77.0" class="chip" style="width:600px;height:110px;font-size:44px;border:3px solid #4A6FA5;color:#5E7FB0">쿼리 리라이트</div></div>'
 '<div class="abs card" data-in="79.2" style="left:940px;top:300px;width:840px;height:150px;display:flex;align-items:center;justify-content:center;font-size:38px;font-weight:800">같은 검색 결과 + 같은 프롬프트</div>'
 '<svg class="abs" style="left:940px;top:450px" width="840" height="110"><path data-draw="80.0" d="M420 0 L200 100 M420 0 L640 100" stroke="#6B7686" stroke-width="5" fill="none"/></svg>'
 + ''.join(f'<div class="abs card" data-in="{t}" style="left:{x}px;top:570px;width:400px;height:250px;padding:28px 32px"><div style="font-size:40px;font-weight:900;color:{c}">생성 모델 {n}</div>'
   f'<div style="font-size:28px;margin-top:16px;line-height:1.7" class="mut">정확도<br>시간 · 비용</div></div>' for x,t,n,c in [(940,80.3,'A','#1FA4B8'),(1380,80.5,'B','#E39A1E')]))

# M09 81.92–88.08 공개 10 → 비공개 100
d10=''.join(f'<div style="width:46px;height:46px;border-radius:50%;background:#1FA4B8;margin:8px"></div>' for i in range(10))
d100=''.join(f'<div data-in="{85.4+i*0.016:.3f}" style="width:30px;height:30px;border-radius:50%;background:#E39A1E;margin:4px"></div>' for i in range(100))
S['M09']=(1966,2114, hdr('EVALUATION','공개 10문항으로 개발, 비공개 100문항으로 평가',81.95)+
 f'<div class="abs card" data-in="82.9" style="left:140px;top:300px;width:520px;height:520px;padding:34px"><div style="font-size:36px;font-weight:900" class="cyan">공개 개발 질문</div>'
 f'<div style="display:flex;flex-wrap:wrap;width:330px;margin-top:40px">{d10}</div><div style="font-size:90px;font-weight:900;margin-top:30px">10</div></div>'
 f'<div class="abs" data-in="84.5" style="left:690px;top:520px;font-size:70px" class="mut"><span class="mut">→</span></div>'
 f'<div class="abs card" data-in="85.3" style="left:800px;top:300px;width:980px;height:520px;padding:34px"><div style="font-size:36px;font-weight:900" class="amber">비공개 평가 · 교수자 관리</div>'
 f'<div style="display:flex;flex-wrap:wrap;width:390px;margin-top:24px">{d100}</div>'
 f'<div style="position:absolute;right:50px;bottom:40px;text-align:right"><div data-count="85.5" data-v="100" style="font-size:150px;font-weight:900;line-height:1" class="amber">0</div><div style="font-size:36px;font-weight:800">문항</div></div></div>')

# M10 88.08–96.6 유형별
qt=[('기본 기능·사양',25,88.5,'#1FA4B8'),('사용 방법·설정·오류 해결',25,89.8,'#1FA4B8'),('유사 제품 간 기능 구분',20,91.8,'#4A6FA5'),('복합 조건·예외 처리',20,93.0,'#4A6FA5'),('근거 없는 질문',10,94.9,'#E39A1E')]
S['M10']=(2114,2318, hdr('100 QUESTIONS','다섯 가지 유형',88.1)+''.join(
 f'<div class="abs" data-in="{t}" style="left:140px;top:{300+i*110}px;display:flex;align-items:center"><div style="width:560px;font-size:38px;font-weight:800">{n}</div>'
 f'<div data-grow="{t+0.1}" data-w="{v*40}" style="height:64px;border-radius:12px;background:{c}"></div><div style="font-size:48px;font-weight:900;margin-left:24px">{v}</div></div>' for i,(n,v,t,c) in enumerate(qt))
 +'<div class="abs" data-in="95.8" style="left:1500px;top:820px;font-size:34px;font-weight:800"><span class="mut">합계</span> 100</div>')

# shared score bar (M11/M12)
SC=[('답변 정확도·근거 신뢰성',45,'#1FA4B8'),('RAG 기술 구현',20,'#4A6FA5'),('효율성',15,'#1A8FA3'),('데이터',10,'#8A9BB5'),('모델 비교',5,'#5E7FB0'),('협업·재현',5,'#5E7FB0')]
def scorebar(top, dim_t=None, hl=None, eff_drain=None, t_in=96.65):
    segs=''
    for n,v,c in SC:
        attr=''
        if dim_t and n!=hl: attr=f'data-dim="{dim_t}"'
        inner=f'<div id="eff" style="position:absolute;left:0;top:0;bottom:0;width:100%;background:{c}"></div>' if (eff_drain and n=='효율성') else ''
        bg='transparent' if inner else c
        segs+=(f'<div {attr} style="position:relative;width:{v*16}px;height:110px;background:{bg};border:2px solid #FFFFFF;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:{40 if v>=10 else 30}px;font-weight:900;color:#FFFFFF;overflow:hidden">{inner}<span style="position:relative">{v}</span></div>')
    return f'<div class="abs" data-in="{t_in}" style="left:160px;top:{top}px;display:flex">{segs}</div>'
labels=''.join(f'<div style="width:{v*16}px;font-size:22px;font-weight:700;text-align:center;line-height:1.3" class="mut">{n if v>=10 else n.replace("·","<br>")}</div>' for n,v,c in SC)
S['M11']=(2318,2429, hdr('SCORING','100점 중 45점',96.65)+scorebar(380,dim_t=98.2,hl='답변 정확도·근거 신뢰성')+
 f'<div class="abs" data-in="96.8" style="left:160px;top:500px;display:flex">{labels}</div>'
 '<div class="abs" data-in="99.9" style="left:160px;top:640px;font-size:54px;font-weight:900"><span class="cyan">답변 정확도 25 · 근거 적합성 15 · 근거 없음 대응 5</span></div>')
S['M12']=(2429,2558, hdr('GATE','Answer Accuracy &lt; 0.40 이면',101.25)+
 '<div class="abs card" data-in="101.3" style="left:160px;top:300px;width:1600px;height:170px;padding:26px 40px">'
 '<div style="position:relative;height:60px;margin-top:20px;border-radius:30px;background:linear-gradient(90deg,#F8DCDC 0 40%,#E3ECF3 40% 100%)">'
 '<div style="position:absolute;left:40%;top:-20px;bottom:-20px;width:6px;background:#E39A1E"></div>'
 '<div data-in="102.4" style="position:absolute;left:calc(40% - 60px);top:-62px;font-size:34px;font-weight:900" class="amber">0.40</div>'
 '<div data-in="103.0" style="position:absolute;left:14%;top:10px;font-size:30px;font-weight:900" class="red">미만</div>'
 '<div style="position:absolute;left:0;top:70px;font-size:24px" class="mut">0</div><div style="position:absolute;right:0;top:70px;font-size:24px" class="mut">1.0</div></div></div>'
 +scorebar(600,eff_drain=True,t_in=101.3)+
 '<div class="abs" data-in="105.2" style="left:880px;top:740px;font-size:54px;font-weight:900"><span class="red">효율성 15 → 0점</span></div>'
 '<script>window.extra=T=>{const p=Math.max(0,Math.min(1,(T-105.3)/0.9));const e=document.getElementById("eff");if(e){e.style.height=((1-p)*100)+"%";e.style.top="auto";e.style.bottom="0";e.style.background=p>0?"#D64545":"#1A8FA3";}}</script>')

# M13 119.0–125.125 결말
def plate(x,txt,dig,t):
    a,b=txt.split(dig,1) if False else (txt[:8],txt[9:])
    return (f'<div class="abs card" data-in="{t}" style="left:{x}px;top:280px;width:700px;height:150px;display:flex;align-items:center;justify-content:center;font-size:66px;font-weight:900">'
      f'{txt[:7]}<span class="amber">{txt[7]}</span>{txt[8:]}</div>')
S['M13']=(2856,3003,
 plate(160,'DCP-T830DW','0',119.05)+plate(1060,'DCP-T835DW','5',119.2)+
 '<div class="abs" data-in="121.4" style="left:160px;top:500px;width:1600px;display:flex;gap:40px">'
 '<div class="card" style="flex:1;height:200px;padding:30px 36px;border-color:#2E9E57"><div style="font-size:30px" class="green">근거가 있으면</div><div style="font-size:46px;font-weight:900;margin-top:10px">맞는 모델의 근거로 답한다</div></div>'
 '<div class="card" data-in="123.4" style="flex:1;height:200px;padding:30px 36px;border-color:#E39A1E"><div style="font-size:30px" class="amber">근거가 없으면</div><div style="font-size:46px;font-weight:900;margin-top:10px">모른다고 말한다</div></div></div>')

import base64 as _b
_bg=_b.b64encode(open('/home/claude/bra/motion/m00_bg.jpg','rb').read()).decode()
def _plate(y,pre,d,post,t):
    return (f'<div class="abs" data-in="{t}" style="left:0;right:0;top:{y}px;display:flex;justify-content:center">'
      f'<div style="background:#FFFFFF;border-radius:26px;box-shadow:0 18px 50px rgba(31,39,51,.18);padding:34px 70px;font-size:150px;font-weight:900;letter-spacing:4px;color:#1F2733;line-height:1">'
      f'{pre}<span class="dig" style="display:inline-block;border-radius:18px;padding:0 10px">{d}</span>{post}</div></div>')
S['M00']=(0,72,
 f'<div class="abs" style="inset:0;background:url(data:image/jpeg;base64,{_bg}) center/cover"></div>'
 '<div class="abs" style="inset:0;background:rgba(238,240,242,.35)"></div>'
 +_plate(170,'DCP-T83','0','DW',0.0)+_plate(450,'DCP-T83','5','DW',0.15)+
 '<div class="abs" data-in="1.35" style="left:0;right:0;top:740px;display:flex;justify-content:center"><div style="background:#E39A1E;color:#fff;font-size:60px;font-weight:900;padding:12px 40px;border-radius:999px">숫자 하나 차이</div></div>'
 '<script>window.extra=T=>{const p=Math.max(0,Math.min(1,(T-0.95)/0.35));document.querySelectorAll(".dig").forEach(e=>{e.style.background=`rgba(227,154,30,${p})`;e.style.color=p>.5?"#FFFFFF":"#1F2733";e.style.transform=`scale(${1+0.12*Math.sin(Math.min(p,1)*Math.PI)})`;});}</script>')
