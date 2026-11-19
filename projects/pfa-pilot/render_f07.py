"""Compose F07 from the unused trial-model take at native pixel density."""
import subprocess

import numpy as np
from PIL import Image, ImageDraw
from render_film import BASE, CORAL, GOLD, SUB, FPS, HERE, FFMPEG, phase, stroke, text, top

SOURCE=HERE/'media/flow/F07-0f8e1484-1080p.mp4'
OUT=HERE/'renders/F07-treatment-choice-1080p.mp4'
FIRST,COUNT=70,72

def render():
    cmd=[FFMPEG,'-v','error','-y']
    width,height=932,596
    y,x=np.ogrid[:height,:width]
    # The take pans past a source label at the upper-left edge of the insert.
    opacity=Image.fromarray(np.uint8(255*np.clip((x+y-254)/115,0,1)))
    crop=f'crop={width}:{height}:496:428'
    decode=cmd+['-ss',str(FIRST/FPS),'-i',str(SOURCE),'-an','-frames:v',str(COUNT),
                '-vf',crop,'-pix_fmt','rgb24','-f','rawvideo','-']
    encode=cmd+['-f','rawvideo','-s','1920x1080','-pix_fmt','rgb24','-r','24','-i','-',
                '-an','-vf','scale=out_color_matrix=bt709,format=yuv420p','-colorspace','bt709',
                '-color_primaries','bt709','-color_trc','bt709','-c:v','libx264','-crf','13',
                '-preset','veryfast','-threads','5','-movflags','+faststart',str(OUT.with_suffix('.part.mp4'))]
    with subprocess.Popen(decode,stdout=subprocess.PIPE) as reader, subprocess.Popen(encode,stdin=subprocess.PIPE) as writer:
        with writer.stdin:
            for i in range(COUNT):
                raw=reader.stdout.read(width*height*3)
                tile=Image.frombytes('RGB',(width,height),raw)
                frame=BASE.copy()
                d=ImageDraw.Draw(frame)
                top(d,'첫 치료 전략','연구 결과에서 첫 치료 선택으로')
                frame.paste(tile,(871,288),opacity)
                text(d,122,426,'연구에서 본 1년 효과',40,SUB)
                text(d,119,521,'PFA 우세',77,CORAL)
                stroke(d,(128,619),(128,702),phase(i/FPS,.25,.70),GOLD,4)
                if i>=20:
                    text(d,121,782,'환자별 첫 치료는?',55)
                writer.stdin.write(frame.tobytes())
        if reader.wait() or writer.wait():
            raise RuntimeError('F07 render failed')
    OUT.with_suffix('.part.mp4').replace(OUT)

if __name__=='__main__':
    render()
