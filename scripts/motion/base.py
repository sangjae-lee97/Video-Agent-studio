"""모션그래픽 공통 스타일·애니메이션 런타임.

장면 HTML의 요소에 절대 시각(초, 편 타임라인 기준)을 data-* 속성으로 단다. 렌더러가 프레임마다 R(T)를 호출한다.
  data-in="12.3"                    12.3초부터 0.45초 동안 떠오르며 나타남 (data-base로 기본 transform 지정 가능)
  data-grow="12.3" data-w="400"      막대 너비 0→400px (0.8초)
  data-count="12.3" data-v="466"     숫자 0→466 카운트 (data-dec 소수 자릿수, data-pre/data-suf 접두·접미)
  data-dim="12.3"                    흐려짐(강조 대상 외 항목) / data-hl="12.3" data-c="#E39A1E" 테두리 강조
  <path data-draw="12.3" data-d=".6"> SVG 선 그리기
  window.extra = T => {...}          그 밖의 장면별 동작
기본 팔레트는 밝은 오피스형(첫 편 기준). 편마다 template-spec의 팔레트로 CSS_EXTRA에서 덮어쓴다.
"""
CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden}
body{word-break:keep-all;font-family:'Noto Sans CJK KR',sans-serif;color:#1F2733;
 background:radial-gradient(1200px 800px at 8% 0%,#FFFFFF 0%,transparent 65%),linear-gradient(180deg,#EEF0F2 0%,#E4E7EA 100%)}
.abs{position:absolute}
.tag{font-size:28px;font-weight:700;color:#1A8FA3;letter-spacing:3px}
.h{font-size:58px;font-weight:900;line-height:1.2}
.card{background:#FFFFFF;border:2px solid rgba(31,39,51,.10);border-radius:22px;box-shadow:0 10px 30px rgba(31,39,51,.08)}
.chip{display:inline-flex;align-items:center;justify-content:center;border-radius:14px;font-weight:800}
.mono{font-family:'DejaVu Sans Mono',monospace}
.amber{color:#E39A1E}.cyan{color:#1FA4B8}.green{color:#2E9E57}.red{color:#D64545}.mut{color:#6B7686}
.pop,.grow,.dimx{will-change:opacity,transform}
"""
JS = r"""
const ease=x=>x<=0?0:x>=1?1:1-Math.pow(1-x,3);
const prog=(T,a,d)=>ease((T-a)/d);
function R(T){
 document.querySelectorAll('[data-in]').forEach(e=>{const p=prog(T,+e.dataset.in,.45);
   e.style.opacity=p; e.style.transform=(e.dataset.base||'')+` translateY(${(1-p)*26}px)`;});
 document.querySelectorAll('[data-grow]').forEach(e=>{const p=prog(T,+e.dataset.grow,.8);
   e.style.width=(p*+e.dataset.w)+'px';});
 document.querySelectorAll('[data-count]').forEach(e=>{const p=prog(T,+e.dataset.count,.8);
   const v=+e.dataset.v; e.textContent=(e.dataset.pre||'')+(Math.round(p*v*100)/100).toFixed(+(e.dataset.dec||0))+(e.dataset.suf||'');});
 document.querySelectorAll('[data-dim]').forEach(e=>{const p=prog(T,+e.dataset.dim,.4);
   e.style.filter=`saturate(${1-p*.85})`; e.style.opacity=1-p*.6;});
 document.querySelectorAll('[data-hl]').forEach(e=>{const p=prog(T,+e.dataset.hl,.4);
   e.style.boxShadow=`0 0 0 ${p*5}px ${e.dataset.c||'#E39A1E'}, 0 0 ${p*40}px ${e.dataset.c||'#E39A1E'}66`;});
 document.querySelectorAll('[data-draw]').forEach(e=>{const p=prog(T,+e.dataset.draw,+(e.dataset.d||.6));
   const L=e.getTotalLength(); e.style.strokeDasharray=L; e.style.strokeDashoffset=L*(1-p);});
 if(window.extra) extra(T);
}
"""
def page(body):
    return f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{body}<script>{JS}</script></body></html>"
