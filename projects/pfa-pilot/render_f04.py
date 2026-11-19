"""Render the narrated 15.625–24.500 s patient-assignment graphic."""
import hashlib
import json
import math
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from render_opening import FFMPEG, HERE, ROOT, font, phase


W, H, FPS, FRAMES = 1920, 1080, 24, 213
OUTPUT = HERE / 'renders/F04-assignment-1080p.mp4'
OPENING = HERE / 'renders/F03-44a227c2-flow1080-relabel-frame191.png'
IVORY, CORAL, BLUE = '#faf3e8', '#ffac96', '#a6d3ea'


def route(u, side):
    """One continuous centreline, with a tangent shared by both branches."""
    if u < .31:
        return (960, 405 + 118 * u / .31)
    v = (u - .31) / .69
    return (960 + side * 470 * v*v*(3-2*v), 523 + 195*v)


def path(draw, side, end, width, color, start=0):
    if end > start:
        points = [route(v, side) for v in np.linspace(start, end, 100)]
        draw.line(points, fill=color, width=width, joint='curve')


def pill_image():
    img = Image.new('RGBA', (180, 82))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((4, 4, 176, 78), 36, fill='#c2e1ee')
    mask = Image.new('L', img.size)
    ImageDraw.Draw(mask).rounded_rectangle((4, 4, 176, 78), 36, fill=255)
    paint = Image.new('RGBA', img.size)
    ImageDraw.Draw(paint).rectangle((91, 0, 180, 82), fill='#6594ae')
    img.alpha_composite(Image.composite(paint, Image.new('RGBA', img.size), mask))
    d.line((90, 8, 90, 73), fill='#395568', width=4)
    d.line((46, 15, 68, 15), fill='#eff9fb', width=4)
    return img.rotate(26, Image.Resampling.BICUBIC, expand=True).resize((80, 59), Image.Resampling.LANCZOS)


def render():
    project = json.loads((HERE / 'production-plan.json').read_text('utf-8'))['project']
    wav = ROOT / project['audio_path']
    assert hashlib.sha256(wav.read_bytes()).hexdigest() == project['audio_sha256']
    source = Image.open(OPENING).convert('RGB')
    assert source.size == (W, H) and FRAMES/FPS == 8.875
    y, x = np.ogrid[:H, :W]
    light = np.exp(-((x-780)/1170)**2 - ((y-195)/870)**2)
    background = Image.fromarray((np.array([21, 25, 29]) + light[..., None]*[17, 19, 20]).astype('uint8'))
    pill = pill_image()
    portrait_mask = Image.new('L', (240, 208))
    ImageDraw.Draw(portrait_mask).rounded_rectangle((13,12,227,196), radius=40, fill=255)
    portrait_mask = portrait_mask.filter(ImageFilter.GaussianBlur(7))
    header = '약보다 시술을 먼저 하면?'
    size = font(63, 'bold')
    # Both treatment names and counts stay fixed, even as the narration changes focus.
    with tempfile.TemporaryDirectory(dir=OUTPUT.parent) as tmp:
        out = Path(tmp) / OUTPUT.name
        cmd = [FFMPEG, '-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo',
               '-pix_fmt', 'rgb24', '-s', '1920x1080', '-r', '24', '-i', 'pipe:0',
               '-ss', '15.625', '-i', str(wav), '-map', '0:v', '-map', '1:a',
               '-t', '8.875', '-af', 'atrim=duration=8.875,asetpts=PTS-STARTPTS',
               '-c:v', 'libx264', '-preset', 'fast', '-crf', '16', '-threads', '5',
               '-vf', 'scale=out_color_matrix=bt709', '-colorspace', 'bt709',
               '-color_primaries', 'bt709', '-color_trc', 'bt709', '-pix_fmt', 'yuv420p',
               '-c:a', 'aac', '-ar', '48000', '-b:a', '192k', '-movflags', '+faststart', str(out)]
        with subprocess.Popen(cmd, stdin=subprocess.PIPE) as encoder:
            with encoder.stdin:
                for n in range(FRAMES):
                    t = n/FPS
                    im = background.copy()
                    d = ImageDraw.Draw(im)
                    d.text((960, 120), header, font=font(74,'bold'), fill=IVORY, anchor='mm')
                    d.line((150,208,1770,208), fill='#4b5153', width=2)
                    d.text((960,272),'항부정맥제 본격 사용 전 환자',font=font(38,'regular'),
                           fill='#cccbc4',anchor='mm')
                    if n >= 57:
                        d.text((960,345),'310명',font=font(84,'bold'),fill=IVORY,anchor='mm')
                    reach = phase(t, 1.30, 1.80)
                    for side, color in [(-1,CORAL),(1,BLUE)]:
                        path(d,side,reach,18,'#171c20')
                        path(d,side,min(reach,.31),6,'#adb5b4')
                        path(d,side,reach,6,color,.31)
                    for k in range(math.ceil(t/.29)):
                        u = (t-2.15-.29*k)/1.28
                        if 0 <= u < min(1,reach):
                            side = (-1,1,-1,-1,1,-1,1,-1,-1)[k%9]
                            px,py = route(u,side)
                            d.ellipse((px-7,py-7,px+7,py+7),fill=IVORY)
                    # The pill shares the right label's baseline; its x is derived from the text.
                    for side, label, number, color, cue in [
                            (-1,'PFA 시술','207명',CORAL,4.835),
                            (1,'약물 치료','103명',BLUE,6.605)]:
                        cx = 960 + side*470
                        if reach >= .995:
                            d.ellipse((cx-9,710,cx+9,728),fill=color)
                        if n < 40:
                            continue
                        label_x = 393 if side == -1 else 1160
                        baseline = 826
                        d.text((label_x,baseline),label,font=size,fill=IVORY,anchor='lm')
                        if n < 76:
                            continue
                        count_x = label_x + d.textlength(label,font=size) + 23
                        d.text((count_x,baseline),number,font=size,fill=color,anchor='lm')
                        right = count_x + d.textlength(number,font=size)
                        if side == 1:
                            im.paste(pill,(round(right+16),baseline-27),pill)
                        highlight = phase(t,cue,.27)
                        if highlight:
                            d.rounded_rectangle((label_x,884,label_x+(right-label_x)*highlight,890),
                                                radius=3,fill=color)
                    # Move the actual F03 plate into the PFA label, progressively cropping
                    # its old leader text outside the portrait instead of dissolving the heart.
                    k = phase(t,0,1.48)
                    crop_right = round(W - 657*k)
                    scale = 1 - .854*k
                    tile_size = (round(crop_right*scale),round(H*scale))
                    tile = source.resize(tile_size,Image.Resampling.LANCZOS,box=(0,0,crop_right,H))
                    mask = None
                    if k:
                        mask = portrait_mask.point(lambda a: round(255*(1-k)+a*k))
                        mask = mask.resize(tile_size, Image.Resampling.BILINEAR)
                    im.paste(tile,(round(179*k),round(748*k)),mask)
                    encoder.stdin.write(im.tobytes())
            if encoder.wait():
                raise RuntimeError('F04 export failed')
        out.replace(OUTPUT)


if __name__ == '__main__':
    render()
