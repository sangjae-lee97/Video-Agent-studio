"""Render the eight-second F03 insert and its narration preview."""
import hashlib
import subprocess

import numpy as np
from PIL import Image, ImageDraw

from render_opening import FFMPEG, HERE, ROOT, PROJECT, font, phase

SOURCE = HERE / 'renders/F03-0240a1b3-background-review-1080p.mp4'
SILENT = HERE / 'renders/F03-pfa-targets-1080p.mp4'
VOICED = HERE / 'renders/F03-pfa-targets-narration-1080p.mp4'
GOLD, CORAL, IVORY = '#ffd097', '#ff9d88', '#f4eee4'


def text(draw, point, value, size, color=IVORY, family='bold'):
    draw.text(point, value, font=font(size, family), fill=color, anchor='lm')


def target(draw, frame):
    # The four lateral openings and central field retain the existing
    # target_diagram geometry, enlarged for this full-height insert.
    x0, y0 = 655, 197
    def box(x, y, w, h):
        return (x0 + x*2, y0 + y*2, x0 + (x+w)*2, y0 + (y+h)*2)

    draw.rounded_rectangle(box(0, 0, 510, 359), 276, fill='#683139', outline='#cc8c81', width=6)
    draw.rounded_rectangle(box(25, 24, 460, 311), 230, outline='#86464d', width=3)
    text(draw, (96, 270), '좌심방', 84)
    text(draw, (101, 367), '안쪽에서 본 개념도', 33, '#bec4c0', 'regular')

    for x in (88, 422):
        for y in (105, 256):
            draw.ellipse(box(x-32, y-39, 64, 78), fill='#321c23', outline='#bd7771', width=8)
            if frame >= 100:
                sweep = 25 + 335*phase(frame, 100, 16)
                draw.arc(box(x-43, y-50, 86, 100), -90, -90+sweep, fill=GOLD, width=9)
    if frame >= 100:
        text(draw, (101, 501), '폐정맥 주변', 61, GOLD)
        # Target end sits on the outer top rim of the upper-left opening.
        tip = (x0+176, y0+110)
        draw.line([(103, 555), (552, 555), (680, tip[1]), tip], fill=GOLD, width=4)
        draw.ellipse((tip[0]-6, tip[1]-6, tip[0]+6, tip[1]+6), fill=GOLD)

    if frame >= 144:
        amt = phase(frame, 144, 15)
        width = 30 + round(70*amt)
        draw.rounded_rectangle(box(255-width, 74, 2*width, 216), 45,
                               fill='#a25358', outline=CORAL, width=5)
        text(draw, (101, 687), '좌심방 후벽', 61, CORAL)
        tip = (x0+510, y0+360)
        draw.line([(103, 742), (560, 742), (747, tip[1]), tip], fill=CORAL, width=4)
        draw.ellipse((tip[0]-7, tip[1]-7, tip[0]+7, tip[1]+7), fill=CORAL)


def render():
    wav = ROOT / PROJECT['audio_path']
    assert hashlib.sha256(wav.read_bytes()).hexdigest() == PROJECT['audio_sha256']
    y,x = np.ogrid[:1080, :1920]
    glow = np.exp(-(((x-950)/1250)**2 + ((y-380)/700)**2))
    backdrop = Image.fromarray((np.array([22, 26, 28])+glow[..., None]*[9, 10, 10]).astype('uint8'))
    crop = (1070, 780)
    decoder = subprocess.Popen([FFMPEG, '-v', 'error', '-i', str(SOURCE), '-frames:v', '98',
                                '-vf', 'crop=1070:780:850:160', '-pix_fmt', 'rgb24',
                                '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
    encoder = subprocess.Popen([FFMPEG, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                                '-s', '1920x1080', '-r', '24', '-i', '-', '-an', '-c:v', 'libx264',
                                '-preset', 'fast', '-crf', '17', '-vf', 'scale=out_color_matrix=bt709',
                                '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                                '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(SILENT)], stdin=subprocess.PIPE)
    with decoder.stdout, encoder.stdin:
        for i in range(192):
            img = backdrop.copy()
            d = ImageDraw.Draw(img)
            if i < 98:
                data = decoder.stdout.read(crop[0]*crop[1]*3)
                panel = Image.frombytes('RGB', crop, data)
                img.paste(panel, (754, 150))
                text(d, (96, 352), 'PFA', 135, IVORY, 'latin')
                text(d, (101, 512), '짧은 전기 펄스', 70, GOLD)
                text(d, (104, 608), '목표 조직에 작용', 42, '#bec4c0', 'regular')
            else:
                target(d, i)
            encoder.stdin.write(img.tobytes())
    if decoder.wait() or encoder.wait():
        raise RuntimeError('F03 video export failed')
    subprocess.run([FFMPEG, '-v', 'error', '-y', '-i', str(SILENT), '-ss', '7.750', '-i', str(wav),
                    '-t', '8', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac',
                    '-b:a', '192k', '-movflags', '+faststart', str(VOICED)], check=True)


if __name__ == '__main__':
    render()
