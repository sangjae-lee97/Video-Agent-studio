"""Render the approved 92.610 s edit, then apply the shared SRT caption program."""
import hashlib
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from render_opening import FFMPEG, HERE, ROOT, font, phase


FPS, W, H = 24, 1920, 1080
PAPER, SUB, CORAL, BLUE, GOLD = '#f8f2e6', '#b7c1c2', '#ffab96', '#a8d6e9', '#f1cf93'
LINE, TRACK = '#566369', '#323c41'
PLAN = json.loads((HERE/'production-plan.json').read_text('utf-8'))
MEDIA = {m['id']:m for m in PLAN['media']}
OUT = ROOT / PLAN['project'].get('render_target', 'projects/pfa-pilot/renders/AVANT-GUARD-final-1080p.mp4')
y,x = np.ogrid[:H,:W]
glow = np.exp(-((x-650)/1360)**2-((y-220)/840)**2)
BASE = Image.fromarray((np.array([20,24,28])+glow[...,None]*[17,19,20]).astype('uint8'))


def text(d,x,y,words,size,fill=PAPER,anchor='lm',family='bold'):
    d.text((x,y),words,font=font(size,family),fill=fill,anchor=anchor)


def top(d,section,title):
    text(d,110,73,'AVANT GUARD',32,GOLD,family='latin')
    d.line((337,52,337,91),fill=LINE,width=2)
    text(d,373,70,section,31,SUB)
    d.line((110,125,1810,125), fill=LINE,width=2)
    text(d,106,217,title,80)


def dot(d,x,y,r,col):
    d.ellipse((x-r,y-r,x+r,y+r),fill=col)


def stroke(d,a,b,amt,col,width=6):
    if amt>0:
        end = (a[0]+(b[0]-a[0])*amt,a[1]+(b[1]-a[1])*amt)
        d.line((a,end),fill=col,width=width)
        return end
    return a


def callout(d,x,y,words,amt,color=GOLD):
    if amt>0:
        end = stroke(d,(x,y),(x+74,y),amt,color,5)
        text(d,end[0]+21,y,words,36,color)


def result_bars(d,t):
    x0,x1,base,amp = 210,1230,818,448
    for pct in [0,25,50,75,100]:
        yy=base-amp*pct/100
        text(d,x0-21,yy,f'{pct}%',29,SUB,'rm','latin')
        d.line((x0,yy,x1,yy),fill=LINE if pct==0 else TRACK,width=2)
    for cx,pct,begin,col,name,num in [(540,56,29.62,CORAL,'PFA 시술','56%'),
                                        (965,30,32.48,BLUE,'약물 치료','약 30%')]:
        f=phase(t,begin,1.12)
        text(d,cx,872,name,40,col,'mm')
        if f:
            yy=base-amp*pct*f/100
            d.rounded_rectangle((cx-102,yy,cx+102,base),radius=5,fill=col)
            if f>=.999:
                text(d,cx,yy-53,num,64,col,'mm')


def effect_chart(d,t):
    top(d,'치료 효과','1년 치료 성공 추정치')
    result_bars(d,t)
    base,amp=818,448
    a=phase(t,34.60,.78)
    if a:
        y1,y2=base-.56*amp,base-.30*amp
        stroke(d,(644,y1),(1247,y1),a,GOLD,3)
        stroke(d,(1069,y2),(1247,y2),a,GOLD,3)
        stroke(d,(1246,y1),(1246,y2),a,GOLD,4)
        text(d,1310,(y1+y2)/2-54,'두 군의 차이',35,SUB)
        text(d,1305,(y1+y2)/2+14,'약 26%p',80,GOLD)
    if t>36.25:
        callout(d,1299,780,'12개월 추정치',phase(t,36.25,.65),SUB)


def interpretation(d,t):
    top(d,'평가 기준','연구에서 말하는 ‘성공’')
    result_bars(d,t)
    text(d,1300,464,'치료 성공',60)
    mark=phase(t,40.50,.48)
    if mark:
        for yy in (562,583):
            stroke(d,(1310,yy),(1375,yy),mark,GOLD,7)
        stroke(d,(1317,602),(1369,542),mark,GOLD,6)
        text(d,1410,569,'완치',72,GOLD)
    callout(d,1300,736,'연구의 평가 기준',phase(t,41.02,.9),SUB)


def criteria(d,t):
    top(d,'평가 기준','세 가지를 함께 평가')
    left,right=185,1710
    yline=531
    d.line((left,yline,right,yline),fill=TRACK,width=10)
    x90=left+(right-left)*90/365
    a=phase(t,42.41,1.6)
    stroke(d,(left,yline),(x90,yline),a,CORAL,8)
    dot(d,left,yline,13,CORAL)
    text(d,left,440,'초기 치료 성공',49,CORAL)
    text(d,left,598,'치료 시작',32,SUB)
    after=phase(t,44.43,2.4)
    if after:
        end=stroke(d,(x90,yline),(right,yline),after,BLUE,8)
        dot(d,*end,11,BLUE)
        d.line((x90,yline-25,x90,yline+25),fill=PAPER,width=4)
        text(d,x90,598,'90일',34,PAPER,'mm')
        text(d,1090,430,'기준에 해당하는 부정맥 재발',49,BLUE,'mm')
        text(d,right,598,'12개월',34,SUB,'rm')
    cond=phase(t,48.90,.9)
    if cond:
        stroke(d,(left,702),(right,702),cond,GOLD,3)
        text(d,left,790,'추가 시술과 약물 사용 조건',52,GOLD)
        if t>50.62:
            text(d,right,790,'군별 약물 기준 적용',36,SUB,'rm')


def safety_question(d,t):
    top(d,'첫 치료 전략','모두 시술부터 하면 될까?')
    text(d,460,545,'치료 효과',77,CORAL,'mm')
    text(d,460,665,'1년 성공 추정치',39,SUB,'mm')
    d.line((966,408,966,754),fill=LINE,width=2)
    progress=phase(t,53.0,2.9)
    stroke(d,(605,550),(896,550),progress,LINE,4)
    stroke(d,(1035,550),(1260,550),phase(t,55.65,.7),GOLD,5)
    if t>=55.9:
        text(d,1480,550,'안전성',77,GOLD,'mm')
        text(d,1480,665,'기기·시술 관련 사건',39,SUB,'mm')


def study_timeline(d,t):
    """Same pause, baseline and endpoints on both sides of the safety-scene cut."""
    if t < 67.83:
        return
    y=380
    d.line((140,y,1770,y),fill=TRACK,width=5)
    stop=phase(t,67.83,.65)
    stroke(d,(140,y),(435,y),stop,GOLD,5)
    if stop>=.99:
        for x in (429,442):
            d.line((x,y-12,x,y+12),fill=GOLD,width=5)
        text(d,435,319,'연구 일시 중단',34,GOLD,'mm')
    if t>=76.48:
        end=stroke(d,(447,y),(1530,y),phase(t,76.48,.85),BLUE,5)
        dot(d,*end,8,BLUE)
        text(d,1530,319,'연구 재개',34,BLUE,'mm')


def safety_counts(d,t):
    top(d,'안전성','PFA 안전성 분석 대상')
    # Each dot is one participant. The six stroke cases remain inside the set of thirteen.
    reveal=phase(t,57.81,1.35)
    cases=phase(t,60.57,1.08)
    strokes=phase(t,66.00,.7)
    for i in range(round(257*reveal)):
        row,col=divmod(i,20)
        color=GOLD if i<round(6*strokes) else CORAL if i<round(13*cases) else '#65757c'
        dot(d,134+col*39,519+row*24,8,color)
    text(d,125,450,'점 하나 = 한 명',34,SUB)
    x0=1050
    text(d,x0,479,'전체 257명',56,PAPER if not cases else SUB)
    if cases:
        text(d,x0,573,'기기·시술 관련 중대한 이상사건',38,SUB)
        text(d,x0,668,'13명',86,CORAL)
        text(d,x0+229,678,'5.1%',51,CORAL)
    if strokes:
        callout(d,x0,792,'그중 뇌졸중 6명',strokes,GOLD)
    study_timeline(d,t)


def safeguards(d,t):
    top(d,'안전성','연구 재개 전 보완한 절차')
    study_timeline(d,t)
    steps=[('환자 선정 기준 강화',70.75,72.77),('시술 전 검사 강화',72.77,74.9),
           ('항응고 관리 강화',74.9,76.48)]
    for i,(label,start,end) in enumerate(steps):
        if t<start: continue
        yy=480+i*102
        active=t<end
        if active:
            d.rounded_rectangle((196,yy-40,1620,yy+40),radius=9,fill='#303e42')
            stroke(d,(196,yy-36),(196,yy+36),phase(t,start,.28),BLUE,6)
        dot(d,246,yy,7,BLUE if active else SUB)
        text(d,292,yy,label,46,BLUE if active else SUB)
    if t>=78.36:
        callout(d,196,834,'보완 후에도 위험 해소 여부는 단정할 수 없음',phase(t,78.48,.8),GOLD)


def conclusion(d,t):
    top(d,'첫 치료 전략','1년 효과에서 앞선 PFA')
    for x,label,amount,col in [(478,'PFA 시술',56,CORAL),(1402,'약물 치료',30,BLUE)]:
        text(d,x,421,label,53,col,'mm')
        xy=(x-253,633,x+253,633)
        d.line(xy,fill=TRACK,width=14)
        stroke(d,xy[:2],(xy[0]+506*amount/100,633),phase(t,82.62,.9),col,14)
        text(d,x,547,('약 ' if amount==30 else '')+str(amount)+'%',85,col,'mm')
    callout(d,594,798,'첫 치료로 고려할 근거',phase(t,85.73,1.0))


def decision(d,t):
    top(d,'첫 치료 전략','누구에게 먼저 시행할까?')
    for x,label,col in [(420,'효과',CORAL),(1500,'위험',BLUE)]:
        text(d,x,528,label,82,col,'mm')
        end=(x+185 if x<960 else x-185,528)
        stroke(d,end,(960,738),phase(t,89.0,1.55),col,5)
    if t>=90.36:
        dot(d,960,738,11,GOLD)
        text(d,960,829,'환자별로 함께 판단',55,PAPER,'mm')


def graphic(t):
    im=BASE.copy()
    d=ImageDraw.Draw(im)
    for end,draw in [(38.375,effect_chart),(42.375,interpretation),(52.75,criteria),
                     (57.8125,safety_question),(70.4375,safety_counts),
                     (82.5625,safeguards),(88,conclusion),(93,decision)]:
        if t<end:
            draw(d,t)
            return im
    raise ValueError(t)


def render():
    subprocess.run([sys.executable,str(ROOT/'scripts/export_plan.py'),
                    str(HERE/'production-plan.json')],check=True,stdout=subprocess.DEVNULL)
    project=PLAN['project']
    for edit in PLAN['edits']:
        media = MEDIA[edit['media_id']]
        if media['kind'] == 'flow' and not media.get('source_asset'):
            raise FileNotFoundError(f"{media['id']}: accepted Flow source required before rendering")
    wav=ROOT/project['audio_path']
    paths={ROOT/m['source_asset']:m['source_sha256'] for m in MEDIA.values() if m.get('source_asset')}
    paths[wav]=project['audio_sha256']
    for source,expected in paths.items():
        if hashlib.sha256(source.read_bytes()).hexdigest()!=expected:
            raise ValueError(f'Source hash mismatch: {source}')
    exe=[FFMPEG,'-hide_banner','-loglevel','error','-y']
    framebytes=W*H*3
    duration=project['duration_seconds']
    total=math.ceil(duration*FPS)
    closing_heart=None
    def boundary(t):
        return math.ceil(round(t*FPS,7))
    with tempfile.TemporaryDirectory(dir=OUT.parent) as folder:
        folder=Path(folder)
        master=folder/'edit.mp4'
        cmd=exe+['-f','rawvideo','-pixel_format','rgb24','-video_size','1920x1080',
                 '-framerate','24','-i','pipe:0','-i',str(wav),'-map','0:v','-map','1:a',
                 '-c:v','libx264','-threads','6','-preset','veryfast','-crf','12',
                 '-vf','scale=out_color_matrix=bt709,format=yuv420p','-colorspace','bt709',
                 '-color_trc','bt709','-color_primaries','bt709','-c:a','aac','-ar','48000',
                 '-af','volume=-2dB','-b:a','256k',str(master)]
        with subprocess.Popen(cmd,stdin=subprocess.PIPE) as writer:
            with writer.stdin:
                for edit in PLAN['edits']:
                    media=MEDIA[edit['media_id']]
                    lo,hi=boundary(edit['start']),boundary(edit['end'])
                    if asset:=media.get('source_asset'):
                        decode=exe+['-ss',str(edit['source_in']),'-i',str(ROOT/asset),'-an',
                                    '-frames:v',str(hi-lo),'-pix_fmt','rgb24','-f','rawvideo','-']
                        with subprocess.Popen(decode,stdout=subprocess.PIPE) as reader:
                            for index in range(hi-lo):
                                raw=reader.stdout.read(framebytes)
                                if len(raw)!=framebytes:
                                    raise ValueError(f'Short decode: {asset}')
                                writer.stdin.write(raw)
                                if edit['id']=='E14b' and index==hi-lo-1:
                                    closing_heart=Image.frombytes('RGB',(W,H),raw)
                            if reader.wait():
                                raise RuntimeError(asset)
                    else:
                        for frame in range(lo,hi):
                            t=frame/FPS
                            image=graphic(t)
                            if edit['id']=='E14c':
                                k=phase(t,88.625,1.05)
                                # Carry the same heart from the opening motif into the decision diagram.
                                box=(round(520*k),round(45*k),W-round(525*k),H-round(125*k))
                                scale=1-.70*k
                                plate=closing_heart.resize((round((box[2]-box[0])*scale),
                                                           round((box[3]-box[1])*scale)),
                                                          Image.Resampling.LANCZOS,box=box)
                                image.paste(plate,((W-plate.width)//2,round(328*k)))
                            writer.stdin.write(image.tobytes())
            if writer.wait():
                raise RuntimeError('Master encode failed')
        subbed=folder/'captioned.mp4'
        subprocess.run([sys.executable,str(ROOT/'scripts/apply_captions.py'),str(master),
                        str(ROOT/project['subtitles']),str(subbed)],check=True)
        final=folder/OUT.name
        # Trim the last displayed frame to the exact audio end on the 24 kHz MP4 clock.
        tail_ticks=round(duration*24000)-(total-1)*1000
        timing=f"setts=duration='if(eq(N,{total-1}),{tail_ticks},DURATION)'"
        subprocess.run(exe+['-i',str(subbed),'-map','0:v','-map','0:a','-c','copy',
                            '-bsf:v',timing,'-video_track_timescale','24000','-movflags','+faststart',
                            str(final)],check=True)
        final.replace(OUT)


if __name__=='__main__':
    render()
