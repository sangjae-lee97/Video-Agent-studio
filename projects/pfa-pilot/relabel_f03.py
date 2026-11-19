"""Replace the burned-in F03 leaders and captions on take 44a227c2."""
import argparse
import hashlib
import subprocess

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

from render_opening import FFMPEG, HERE, PROJECT, ROOT, font


TAKE = HERE / 'media/flow/F03-44a227c2-720p.mp4'
OUT = HERE / 'renders/F03-44a227c2-relabel-1080p.mp4'
VOICE = HERE / 'renders/F03-44a227c2-relabel-narration-1080p.mp4'


def clean_leader(frame, bounds, root, slope, factor=1):
    """Repair the narrow ink footprint using adjacent tissue pixels."""
    left, top, right, bottom = (round(n*factor) for n in bounds)
    roi = frame[top:bottom, left:right]
    ys, xs = np.ogrid[top:bottom, left:right]
    cx, cy = (n*factor for n in root)
    near_line = (xs >= cx - 2*factor) & (abs(ys - cy - slope * (xs-cx)) < 11*factor)
    near_dot = (xs-cx)**2 + (ys-cy)**2 < (16*factor)**2
    rgb = roi.astype(np.int16)
    # The old ink is pale cream, on dark red tissue or neutral background.
    ink = (rgb[:,:,1] > 145) & (rgb[:,:,2] > 92) & (rgb[:,:,0]-rgb[:,:,1] < 68)
    mask = ndimage.binary_dilation((near_line | near_dot) & ink, iterations=round(3*factor))
    if not mask.any():
        return
    coords = ndimage.distance_transform_edt(mask, return_indices=True, return_distances=False)
    yy, xx = np.where(mask)
    repaired = roi.astype(np.float32)
    repaired[yy, xx] = roi[coords[0, yy, xx], coords[1, yy, xx]]
    # Diffuse only over the erased pixels, preserving everything outside.
    for _ in range(round(28*factor*factor)):
        repaired[yy, xx] = (repaired[yy-1,xx] + repaired[yy+1,xx]
                             + repaired[yy, np.maximum(xx-1,0)]
                             + repaired[yy, np.minimum(xx+1,roi.shape[1]-1)]) / 4
    roi[yy,xx] = np.rint(repaired[yy,xx]).astype(np.uint8)


def leader(img, start, label_xy, wording, color, age):
    # Coordinates below are in the original 720p plate.
    d = ImageDraw.Draw(img)
    scale = 1.5
    sx,sy = (round(n*scale) for n in start)
    tx,ty = (round(n*scale) for n in label_xy)
    end = tx-23
    growth = min(1.,(age+1)/5)
    d.line([(sx,sy),(round(sx+(end-sx)*growth),sy)],fill=color,width=3)
    d.ellipse((sx-5,sy-5,sx+5,sy+5),fill=color)
    if age >= 3:
        d.text((tx,ty),wording,font=font(56,'bold'),fill='#f7ead3',anchor='lm',
               stroke_width=1,stroke_fill='#393734')


def render(flow_1080p=False):
    take, out, voice = TAKE, OUT, VOICE
    width, height = 1280, 720
    if flow_1080p:
        take = HERE / 'media/flow/F03-44a227c2-flow-1080p.mp4'
        out = HERE / 'renders/F03-44a227c2-flow1080-relabel.mp4'
        voice = HERE / 'renders/F03-44a227c2-flow1080-relabel-narration.mp4'
        width, height = 1920, 1080
    factor = width / 1280
    label_area = (slice(round(195*factor), round(455*factor)),
                  slice(round(839*factor), round(1140*factor)))
    # The 24 fps Flow upscale ends at frame 189. Extend the final labeled
    # frame across the remaining two frames of the established 8-second cut.
    pad = ['-vf','tpad=stop_mode=clone:stop=2'] if flow_1080p else []
    run = [FFMPEG,'-v','error','-y']
    reader = subprocess.Popen(run+['-i',str(take),'-an']+pad+['-frames:v','192','-pix_fmt','rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE)
    writer = subprocess.Popen(run+['-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080',
        '-r','24','-i','-','-an','-c:v','libx264','-preset','fast','-crf','16',
        '-vf','scale=out_color_matrix=bt709','-colorspace','bt709','-color_primaries','bt709',
        '-color_trc','bt709','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
    with reader.stdout, writer.stdin:
        for i in range(192):
            frame = np.frombuffer(reader.stdout.read(width*height*3),np.uint8).reshape(height,width,3).copy()
            if i == 98:
                clean_background = frame[label_area].copy()
            if i >= 98:
                progress = (i-98)/93
                clean_leader(frame,(599,216,845,338),(623-3*progress,311-5*progress),-.245,factor)
                if i >= 140:
                    progress = (i-140)/51
                    clean_leader(frame,(560,351,845,504),(590-4*progress,470+9*progress),-.345,factor)
                # The labels occupy a blank stationary section of the backdrop.
                frame[label_area] = clean_background
            img = Image.fromarray(frame)
            if not flow_1080p:
                img = img.resize((1920,1080),Image.Resampling.LANCZOS)
            if i >= 100:
                leader(img,(672,310),(882,310),'폐정맥 주변','#ffce88',i-100)
            if i >= 144:
                leader(img,(473,389),(882,389),'좌심방 후벽','#ffd2b0',i-144)
            writer.stdin.write(img.tobytes())
    if reader.wait() or writer.wait():
        raise RuntimeError('F03 relabel failed')
    wav = ROOT / PROJECT['audio_path']
    assert hashlib.sha256(wav.read_bytes()).hexdigest() == PROJECT['audio_sha256']
    subprocess.run(run+['-i',str(out),'-ss','7.750','-i',str(wav),'-map','0:v','-map','1:a',
        '-t','8','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(voice)],check=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--flow-1080p', action='store_true')
    render(parser.parse_args().flow_1080p)
