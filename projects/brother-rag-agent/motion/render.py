import sys, subprocess, os
from playwright.sync_api import sync_playwright
import importlib; import base, scenes
FPS=24
args=sys.argv[1:]; preview='preview' in args; only=[a for a in args if a.startswith('M')]
os.makedirs('out',exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':1080})
    for k,(s,e,html) in scenes.S.items():
        if only and k not in only: continue
        pg.set_content(base.page(html)); pg.evaluate("document.fonts.ready")
        shot=lambda T: (pg.evaluate(f"R({T})"), pg.screenshot(type='jpeg',quality=92))[1]
        if preview:
            open(f'out/prev_{k}.jpg','wb').write(shot((e-1)/FPS)); continue
        tmp=f'out/{k}.tmp.mp4'
        ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate',str(FPS),'-i','-','-c:v','libx264','-crf','16','-preset','veryfast','-pix_fmt','yuv420p','-r',str(FPS),tmp],stdin=subprocess.PIPE)
        for i in range(s,e): ff.stdin.write(shot(i/FPS))
        ff.stdin.close()
        if ff.wait()==0: os.replace(tmp,f'out/{k}.mp4'); print('ok',k,e-s,flush=True)
    b.close()
