"""예시 장면 2개. 렌더: python scripts/motion/render.py scripts/motion/example_scenes.py outputs/motion-example
타임라인 24fps 기준. M01은 0~3초(0~72프레임), M02는 3~6초(72~144프레임)."""
S = {}
S['M01'] = (0, 72,
 '<div class="abs tag" data-in="0.0" style="left:140px;top:90px">EXAMPLE</div>'
 '<div class="abs h" data-in="0.1" style="left:140px;top:134px">숫자 등장과 강조</div>'
 '<div class="abs card" data-in="0.4" style="left:140px;top:320px;width:700px;height:360px;display:flex;align-items:center;justify-content:center">'
 '<div data-count="0.6" data-v="466" style="font-size:180px;font-weight:900" class="cyan">0</div>'
 '<div style="font-size:60px;font-weight:800;margin-left:10px">쪽</div></div>'
 '<div class="abs card" data-in="1.2" data-hl="2.0" style="left:940px;top:320px;width:700px;height:360px;display:flex;align-items:center;justify-content:center;font-size:56px;font-weight:900">발화에 맞춰 강조</div>')
S['M02'] = (72, 144,
 '<div class="abs h" data-in="3.0" style="left:140px;top:134px">막대 비교</div>'
 + ''.join(f'<div class="abs" data-in="{3.2+i*0.3:.1f}" style="left:140px;top:{320+i*110}px;display:flex;align-items:center">'
           f'<div style="width:300px;font-size:38px;font-weight:800">{n}</div>'
           f'<div data-grow="{3.3+i*0.3:.1f}" data-w="{v*20}" style="height:64px;border-radius:12px;background:{c}"></div>'
           f'<div style="font-size:44px;font-weight:900;margin-left:20px">{v}</div></div>'
           for i, (n, v, c) in enumerate([('항목 A', 45, '#1FA4B8'), ('항목 B', 20, '#4A6FA5'), ('항목 C', 10, '#E39A1E')])))
