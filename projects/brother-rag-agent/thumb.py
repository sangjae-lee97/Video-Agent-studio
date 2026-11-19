import base64
from playwright.sync_api import sync_playwright
bg=base64.b64encode(open('thumb_bg.jpg','rb').read()).decode()
html=f"""<html><head><meta charset=utf-8><style>
*{{margin:0;padding:0}} body{{width:1280px;height:720px;overflow:hidden;font-family:'Noto Sans CJK KR';
background:url(data:image/jpeg;base64,{bg}) center/cover}}
.sh{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,17,34,.72) 0%,rgba(10,17,34,.25) 45%,rgba(10,17,34,0) 60%)}}
.t{{position:absolute;left:56px;top:40px;font-size:92px;font-weight:900;color:#fff;line-height:1.12;letter-spacing:-2px;
-webkit-text-stroke:3px #0A1122;paint-order:stroke fill;text-shadow:0 6px 18px rgba(0,0,0,.5)}}
.a{{color:#FFC33D}}
.s{{position:absolute;left:60px;top:268px;font-size:40px;font-weight:900;color:#fff;background:#1FA4B8;padding:6px 20px;border-radius:10px}}
</style></head><body><div class=sh></div>
<div class=t>숫자 <span class=a>하나</span> 차이<br>AI는 구별할까?</div>
<div class=s>Brother RAG Agent 프로젝트</div></body></html>"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':720}); pg.set_content(html); pg.evaluate("document.fonts.ready")
    pg.screenshot(path='thumb.jpg',type='jpeg',quality=92); b.close()
