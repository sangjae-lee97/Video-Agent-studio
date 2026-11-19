"""Render the approved pilot opening with Pillow, NumPy and FFmpeg. Run from any directory."""
import hashlib
import json
import math
import os
from functools import lru_cache
from pathlib import Path
import re
import shutil
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PLAN = json.loads((HERE / 'plan.json').read_text(encoding='utf-8'))
PROJECT = PLAN['project']
MEDIA = {row['id']: row for row in PLAN['media']}
EDITS = {row['media_id']: row for row in PLAN['edits']}
FPS, W, H = 24, 1280, 720
INK, PAPER, CORAL, GOLD = '#19191e', '#f7eee5', '#fa907f', '#ffd097'
MUTED, LINE, BLUE = '#bfb3ad', '#5e5353', '#a3cad6'
FFMPEG = os.environ.get('FFMPEG_BINARY') or shutil.which('ffmpeg') or str(next(
    (ROOT / '.venv-supertonic/Lib/site-packages/imageio_ffmpeg/binaries').glob('ffmpeg*.exe')))
FONTS = Path(os.environ.get('WINDIR','C:/Windows')) / 'Fonts'

@lru_cache(None)
def font(size, family):
    return ImageFont.truetype(str(FONTS / {'regular':'malgun.ttf','bold':'malgunbd.ttf',
                                           'latin':'bahnschrift.ttf'}[family]), size)

def label(d, xy, text, size, color=PAPER, family='bold', anchor='lm'):
    d.text(xy, text, font=font(size, family), fill=color, anchor=anchor, stroke_width=0)

def smooth(x):
    x = max(0, min(1, x))
    return x*x*(3-2*x)

def phase(t, start, duration):
    return smooth((t-start)/duration)

def rule(d, points, progress, color=CORAL, width=4):
    lengths = [math.dist(a,b) for a,b in zip(points,points[1:])]
    left = sum(lengths) * max(0,min(1,progress))
    for a,b,length in zip(points,points[1:],lengths):
        if left <= 0: break
        ratio = min(1, left/length)
        d.line([a,(a[0]+(b[0]-a[0])*ratio, a[1]+(b[1]-a[1])*ratio)], fill=color, width=width)
        left -= length

def node(d,x,y,r,color):
    d.ellipse((x-r,y-r,x+r,y+r),fill=color)

def background():
    y,x = np.mgrid[0:H,0:W]
    warm = np.exp(-((x-1010)/570)**2-((y-270)/470)**2)
    grain = np.random.default_rng(12).normal(0,.72,(H,W))
    channels = [v + g*warm + grain for v,g in [(22,28),(23,9),(28,8)]]
    return Image.fromarray(np.uint8(np.stack(channels,axis=-1)))

BASE = background()

def header(d, section):
    label(d,(65,55),'AVANT GUARD',23,GOLD,'latin')
    d.line((237,46,237,67),fill=LINE,width=2)
    label(d,(255,56),section,19,MUTED,'regular')
    d.line((65,91,1215,91),fill=LINE)

def opening(d,t):
    header(d,'첫 치료 전략')
    if t < 3.84:
        label(d,(65,203),'심방세동',73)
        label(d,(66,309),'무엇을 먼저',78)
        label(d,(66,411),'시작할까?',86,CORAL)
        # One question branches into two equal treatment choices.
        for i,(name,yy,col) in enumerate([('약물',224,BLUE),('시술',414,CORAL)]):
            points=[(653,319),(748,319),(843,yy),(914,yy)]
            rule(d,points,1,'#493e40',4)
            rule(d,points,phase(t,.14+i*.16,1.4),col,5)
            r=7+5*phase(t,.65+i*.22,.6)
            node(d,918,yy,r,col)
            label(d,(963,yy-3),name,52,col)
        node(d,653,319,10,GOLD)
    else:
        label(d,(65,181),'지속성 심방세동',55)
        label(d,(67,261),'연구 대상',24,MUTED)
        label(d,(831,208),'7',113,GOLD,'latin')
        label(d,(904,219),'일 초과',49,GOLD)
        start,end,yy=100,1155,423
        for i in range(8):
            x=start+i*128
            d.line((x,yy-12,x,yy+17),fill=LINE,width=2)
            if i in (0,1,7): label(d,(x,yy+55),f'{i}일',23,MUTED,anchor='mm')
        d.line((start,yy,end,yy),fill=LINE,width=3)
        u=phase(t,3.90,2.58)
        xx=start+(end-start)*u
        d.line((start,yy,xx,yy),fill=CORAL,width=8)
        node(d,xx,yy,9,CORAL)
        if u>.86:
            d.line((996,yy-48,996,yy+33),fill=GOLD,width=4)
            arrow=18*phase(t,6.0,.65)
            d.line([(xx-arrow,yy-arrow*.6),(xx,yy),(xx-arrow,yy+arrow*.6)],fill=CORAL,width=5)

def grade(raw):
    # The model has a warm cast even in shade. Neutral background and metallic hardware stay separate.
    a=raw.astype(np.float32)
    warmth=a[:,:,0]-a[:,:,2]
    weight=np.clip((warmth-2)/10,0,1) * np.clip((65-warmth)/25,0,1)
    target=a*np.array([1.35,.65,.63],dtype=np.float32)
    out=a+(target-a)*weight[:,:,None]
    pulse=np.clip((a[:,:,0]-a[:,:,1]-32)/70,0,1)
    out[:,:,1]+=pulse*np.maximum(0,a[:,:,0]*.69-a[:,:,1])
    return Image.fromarray(np.uint8(np.clip(out,0,255)))

def flow_panel(img,d,t,arr):
    header(d,'펄스장 절제술')
    src=EDITS['F01']['source_in']+t-EDITS['F01']['start']
    index=round((src-EDITS['F01']['source_in'])*FPS)
    img.paste(grade(arr[index]).resize((294,522),Image.Resampling.LANCZOS),(823,97))
    label(d,(65,159),'PULSED FIELD ABLATION',22,GOLD,'latin')
    label(d,(60,263),'PFA',121,PAPER,'latin')
    label(d,(67,374),'짧은 전기 펄스',54,CORAL)
    label(d,(68,458),'목표 조직에 작용',34,MUTED,'regular')
    # A sequence of short rising/falling pulses, illustrative and without measurement scales.
    coords=[(68,548)]
    for i in range(6):
        x=91+77*i
        coords.extend([(x,548),(x+8,548),(x+9,521),(x+21,521),(x+22,548),(x+48,548)])
    rule(d,coords,1,'#4a393c',3)
    rule(d,coords,phase(src,.76,3.75),CORAL,4)

def target_diagram(d,t):
    header(d,'이번 연구의 치료 부위')
    label(d,(65,164),'좌심방 뒤쪽',56)
    label(d,(69,237),'안쪽에서 본 개념도',25,MUTED,'regular')
    for i,(name,yy,col,onset) in enumerate([('폐정맥 주변',352,GOLD,12.48),('좌심방 뒤쪽 벽',439,CORAL,13.65)]):
        amt=phase(t,onset,.56)
        d.line((70,yy,70+49*amt,yy),fill=col,width=5)
        label(d,(138,yy-2),name,39,col if amt>.05 else MUTED)
    # Flattened posterior wall. Four venous openings stay lateral to the central tissue.
    d.rounded_rectangle((650,173,1160,532),radius=138,fill='#6d333a',outline='#d79084',width=4)
    d.rounded_rectangle((675,197,1135,508),radius=119,outline='#914852',width=2)
    posterior=phase(t,13.64,.92)
    if posterior:
        box=(805,246,1005,466)
        d.rounded_rectangle(box,radius=51,fill='#9b4d55',outline='#ffba9b',width=3)
        for j in range(9):
            x=828+j*18
            h=(.6+.4*math.sin((j+1)*.35))*128*posterior
            d.line((x,356-h/2,x,356+h/2), fill='#ce7d79',width=3)
    for x in [738,1072]:
        for y in [278,429]:
            d.ellipse((x-32,y-39,x+32,y+39),fill='#321c23',outline='#bf7774',width=6)
            sweep=phase(t,12.48,.78)*360
            if sweep: d.arc((x-43,y-50,x+43,y+50),-90,-90+sweep,fill=GOLD,width=5)

def allocation(d,t):
    header(d,'무작위 배정')
    label(d,(65,171),'첫 치료 전략 비교',53)
    label(d,(69,253),'항부정맥제를 본격적으로',29,MUTED,'regular')
    label(d,(69,302),'쓰기 전인 환자',29,MUTED,'regular')
    if t>=17.88:
        label(d,(63,424),'310',119,PAPER,'latin')
        label(d,(288,448),'명',40)
    # Each dot represents one participant. Mix the two eventual arms in the initial grid.
    s=phase(t,18.85,2.0)
    for i in range(310):
        original=(i*127)%310
        if original >= 310*phase(t,15.63,1.26): continue
        x0,y0=602+(original%31)*15.5,253+(original//31)*16
        left=i<207
        k=i if left else i-207
        cols=16 if left else 12
        x1,y1=(570 if left else 960)+(k%cols)*13,250+(k//cols)*13
        node(d,x0+(x1-x0)*s,y0+(y1-y0)*s,4.3,('#f39d8d' if left else BLUE) if s>.12 else '#d7c4b7')
    if t>=20.46:
        label(d,(567,474),'207',63,CORAL,'latin')
        label(d,(568,539),'PFA군',29,CORAL)
    if t>=22.22:
        label(d,(955,474),'103',63,BLUE,'latin')
        label(d,(957,539),'약물군',29,BLUE)

def read_srt():
    rows=[]
    def seconds(s):
        h,m,ss=s.replace(',','.').split(':')
        return int(h)*3600+int(m)*60+float(ss)
    for block in (ROOT/PROJECT['subtitles']).read_text(encoding='utf-8').strip().split('\n\n'):
        _,times,words=block.split('\n',2)
        a,b=times.split(' --> ')
        rows.append((seconds(a),seconds(b),words))
    return rows

def render():
    wav=ROOT/PROJECT['audio_path']
    take=ROOT/MEDIA['F01']['source_asset']
    for path,expected in [(take,MEDIA['F01']['source_sha256']),(wav,PROJECT['audio_sha256'])]:
        if hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
            raise ValueError(f'Unexpected input: {path}')
    flow=EDITS['F01']
    count=round((flow['end']-flow['start'])*FPS)
    raw=subprocess.check_output([FFMPEG,'-v','error','-ss',str(flow['source_in']),'-i',str(take),
        '-frames:v',str(count),'-an','-pix_fmt','rgb24','-f','rawvideo','-'])
    arr=np.frombuffer(raw,np.uint8).reshape((count,640,360,3))
    cues=read_srt()
    out=HERE/'renders'/'pfa-opening-24.5s.mp4'
    out.parent.mkdir(exist_ok=True)
    temp=out.with_suffix('.partial.mp4')
    duration=PROJECT['pilot_range_seconds'][1]
    cmd=[FFMPEG,'-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24',
         '-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-i',str(wav),'-map','0:v','-map','1:a',
         '-t',str(duration),'-vf','scale=out_color_matrix=bt709,format=yuv420p','-c:v','libx264',
         '-crf','17','-preset','fast','-color_primaries','bt709','-colorspace','bt709','-color_trc','bt709',
         '-af','volume=-2dB','-c:a','aac','-b:a','192k','-movflags','+faststart',str(temp)]
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for i in range(round(duration*FPS)):
            t=i/FPS
            img=BASE.copy()
            d=ImageDraw.Draw(img)
            if t<flow['start']: opening(d,t)
            elif t<flow['end']: flow_panel(img,d,t,arr)
            elif t<EDITS['M02']['start']: target_diagram(d,t)
            else: allocation(d,t)
            line=next((words for a,b,words in cues if a<=t<b),None)
            if line:
                d.rounded_rectangle((55,627,1225,698),radius=15,fill='#101115')
                label(d,(640,659),line,36,PAPER,'bold','mm')
            process.stdin.write(img.tobytes())
        process.stdin.close()
        if process.wait(): raise RuntimeError('FFmpeg encode failed')
        temp.replace(out)
    finally:
        if process.poll() is None: process.kill(); process.wait()
    print(out)

if __name__=='__main__':
    render()

