"""Burn timed SRT cues into a video using the studio's transparent Korean caption style."""
import argparse
import json
import os
import re
import shutil
import struct
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
FONT = Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc')  # container: static Black(900) = VF axis 900


def ffmpeg_path():
    if binary := os.environ.get('FFMPEG_BINARY') or shutil.which('ffmpeg'):
        return binary
    return str(next((ROOT / '.venv-supertonic/Lib/site-packages/imageio_ffmpeg/binaries').glob('ffmpeg*.exe')))


def display_srt(file):
    """Format cue bodies with the project's verified spellings and original timecodes."""
    file = Path(file)
    glossary = file.with_name('caption-terms.ko.json')
    terms = json.loads(glossary.read_text('utf-8-sig')) if glossary.exists() else {}
    pattern = None
    if terms:
        keys = sorted(terms, key=len, reverse=True)
        pattern = re.compile(r'(?<!\w)(?:' + '|'.join(map(re.escape, keys)) + ')')
    blocks = []
    for block in re.split(r'\n\s*\n', file.read_text('utf-8-sig').strip()):
        if not block:
            continue
        index, timing, cue = block.split('\n', 2)
        if pattern:
            cue = pattern.sub(lambda match: terms[match[0]], cue)
        # A decimal point or thousands separator inside a number carries meaning.
        cue = re.sub(r'[.!?,…。！？？，]+(?=[”’」』"\')\]]*(?:\s|$))', '', cue)
        if not cue.strip():
            raise ValueError(f'Caption {index} has no display text')
        blocks.append(f'{index}\n{timing}\n{cue}')
    return '\n\n'.join(blocks) + '\n'


def cues_from_srt(file):
    def seconds(stamp):
        h, m, s, ms = map(int, re.split('[:,.]', stamp))
        return ((h*60+m)*60+s)*1000+ms

    cues = []
    for block in display_srt(file).strip().split('\n\n'):
        if not block:
            continue
        _, times, text = block.split('\n', 2)
        start, stop = (seconds(x.strip()) for x in times.split('-->'))
        if start < 0 or stop <= start or (cues and start < cues[-1][1]):
            raise ValueError(f'Invalid or overlapping caption timing: {times}')
        cues.append((start, stop, text))
    return cues


def caption_sprites(cues, width, height, work):
    # Physical sizes at 1080p; a single scale preserves the style at other resolutions.
    scale = height / 1080
    face = ImageFont.truetype(str(FONT), max(12, round(60*scale)), index=1)
    stroke = max(1, round(4.5*scale))
    margin = max(1, round(42*scale))
    spacing = max(1, round(8*scale))
    lines = []
    for _, _, cue in cues:
        wrapped = []
        for paragraph in cue.splitlines():
            line = ''
            for word in paragraph.split():
                if line and face.getlength(line+' '+word) > width*.91:
                    wrapped.append(line)
                    line = ''
                for char in (' ' if line else '') + word:
                    if line and face.getlength(line+char) > width*.91:
                        wrapped.append(line)
                        line = ''
                    line += char
            wrapped.append(line)
        lines.append('\n'.join(wrapped))
    line_height = sum(face.getmetrics())+spacing
    strip_h = min(height, margin + (max(s.count('\n') for s in lines)+1)*line_height + 4*stroke)
    strip_h += strip_h % 2
    clear = Image.new('RGBA', (width,strip_h))
    clear.save(work/'blank.png')
    events = []
    cursor = 0
    for i, ((begin,end,_),line) in enumerate(zip(cues,lines)):
        mask = Image.new('L', clear.size)
        draw = ImageDraw.Draw(mask)
        style = dict(font=face, spacing=spacing, align='center', anchor='ma')
        # Use a fixed baseline so different final syllables do not shift the row.
        ascent, descent = face.getmetrics()
        y = strip_h-margin-ascent-(line.count('\n')*line_height)
        point = (width//2,y)
        draw.multiline_text((point[0]+round(scale),y+round(3*scale)),line,
                            fill=165,stroke_width=stroke,stroke_fill=165,**style)
        sprite = clear.copy()
        sprite.putalpha(mask.filter(ImageFilter.GaussianBlur(max(.5,1.5*scale))))
        ink = clear.copy()
        ImageDraw.Draw(ink).multiline_text(point,line,fill='white',stroke_width=stroke,
                                           stroke_fill='#131313',**style)
        sprite.alpha_composite(ink)
        name = f'cue-{i:05}.png'
        sprite.save(work/name)
        if begin > cursor:
            events.append(('blank.png',begin-cursor))
        events.append((name,end-begin))
        cursor = end
    content = ['ffconcat version 1.0']
    for name, ms in events:
        content.extend([f"file '{name}'",'option framerate 1000',f'duration {ms/1000:.3f}'])
    content.extend(["file 'blank.png'",'option framerate 1000'])
    (work/'captions.ffconcat').write_text('\n'.join(content)+'\n',encoding='ascii')


def burn(video, srt, output):
    video, srt, output = (Path(x).resolve() for x in (video,srt,output))
    if output in (video,srt):
        raise ValueError('Choose a separate output file.')
    exe = ffmpeg_path()
    frame = subprocess.check_output([exe,'-v','error','-i',str(video),'-map','0:v:0','-frames:v','1',
                                     '-c:v','png','-f','image2pipe','-'])
    w,h = struct.unpack('>II',frame[16:24])
    cues = cues_from_srt(srt)
    if not cues:
        raise ValueError('Empty SRT')
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as folder:
        work = Path(folder)
        caption_sprites(cues,w,h,work)
        target = work/'captioned.mp4'
        subprocess.run([exe,'-hide_banner','-loglevel','error','-y','-i',str(video),
                        '-f','concat','-safe','0','-i',str(work/'captions.ffconcat'),
                        '-filter_complex','[0:v:0][1:v]overlay=x=0:y=H-h:eof_action=pass[v]',
                        '-map','[v]','-map','0:a?','-c:a','copy','-c:v','libx264',
                        '-threads','6','-crf','16','-preset','veryfast','-bf','0',
                        '-pix_fmt','yuv420p','-fps_mode','passthrough','-video_track_timescale','24000',
                        '-movflags','+faststart',str(target)],check=True)
        target.replace(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('video','srt','output'):
        parser.add_argument(name,type=Path)
    args = parser.parse_args()
    burn(args.video,args.srt,args.output)
