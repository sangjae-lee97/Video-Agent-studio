"""Flow 채택본 편집 보정 (글자 깨짐·로고·의미 없는 판독값). 입력 원본은 바꾸지 않고 *_fixed.mp4를 만든다."""
import subprocess, sys, glob, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
UP = '/mnt/user-data/uploads'
SRC = {i: glob.glob(f'{UP}/*-{i}._*_1080p.mp4')[0] for i in range(1, 7)}
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
W, H = 1920, 1080

def read(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).copy()

def write(frames, src, out):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                          '-i', src, '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-crf', '14', '-preset', 'slow', '-pix_fmt', 'yuv420p',
                          '-c:a', 'copy', '-shortest', out], stdin=subprocess.PIPE)
    for f in frames: p.stdin.write(f.tobytes())
    p.stdin.close(); assert p.wait() == 0

def track(frames, ref_i, box, rng, search=40):
    """ref 프레임의 box를 템플릿으로 rng 프레임에서 위치 이동(dx,dy)을 찾는다."""
    x0, y0, x1, y1 = box
    tpl = cv2.cvtColor(frames[ref_i][y0:y1, x0:x1], cv2.COLOR_RGB2GRAY)
    out = {}
    for i in rng:
        sx0, sy0 = max(0, x0 - search), max(0, y0 - search)
        win = cv2.cvtColor(frames[i][sy0:min(H, y1 + search), sx0:min(W, x1 + search)], cv2.COLOR_RGB2GRAY)
        r = cv2.matchTemplate(win, tpl, cv2.TM_CCOEFF_NORMED)
        _, score, _, loc = cv2.minMaxLoc(r)
        out[i] = (sx0 + loc[0] - x0, sy0 + loc[1] - y0, score)
    return out

def soft_blur(img, box, k=61, feather=25):
    x0, y0, x1, y1 = [int(v) for v in box]
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    pad = k
    X0, Y0, X1, Y1 = max(0, x0 - pad), max(0, y0 - pad), min(W, x1 + pad), min(H, y1 + pad)
    region = img[Y0:Y1, X0:X1].astype(np.float32)
    bl = cv2.GaussianBlur(region, (k, k), 0)
    m = np.zeros(region.shape[:2], np.float32); m[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0] = 1
    m = cv2.GaussianBlur(m, (0, 0), feather)[..., None]
    img[Y0:Y1, X0:X1] = (region * (1 - m) + bl * m).astype(np.uint8)

def paint_label(img, box, fill, text, color, size, dx=0, dy=0, radius=6, anchor_x=None):
    x0, y0, x1, y1 = box
    im = Image.fromarray(img); d = ImageDraw.Draw(im)
    d.rounded_rectangle([x0 + dx, y0 + dy, x1 + dx, y1 + dy], radius=radius, fill=tuple(int(c) for c in fill))
    f = ImageFont.truetype(FONT, size, index=1)
    cx = (anchor_x if anchor_x is not None else (x0 + x1) / 2) + dx
    d.text((cx, (y0 + y1) / 2 + dy), text, font=f, fill=color, anchor='mm')
    img[:] = np.asarray(im)

def median_ring(img, box, w=6):
    x0, y0, x1, y1 = box
    edge = np.concatenate([img[y0:y0 + w, x0:x1].reshape(-1, 3), img[y1 - w:y1, x0:x1].reshape(-1, 3)])
    return np.median(edge, axis=0)

log = []
k = sys.argv[1:] or ['1', '2', '3', '4', '5', '6']

if '1' in k:  # F01 마지막 샷: 판독창 위주로 2배 확대(다이얼 바늘이 엉뚱한 글자를 가리킴)
    fr = read(SRC[1])
    for i in range(127, len(fr)):
        c = fr[i][190:730, 480:1440]
        fr[i] = cv2.resize(c, (W, H), interpolation=cv2.INTER_LANCZOS4)
    write(fr, SRC[1], '/home/claude/flowfix/F01_1080p.mp4'); log.append('F01: frames 127-189 crop x480-1440 y190-730 x2')

if '2' in k:  # F02 위에서 본 샷: '1,099 ğańk' → '1,099쪽'
    fr = read(SRC[2]); box = (748, 187, 1172, 277)
    tr = track(fr, 115, (738, 177, 1182, 287), range(59, 116))
    ref = fr[115].copy(); fill = np.median(ref[200:265, 760:780].reshape(-1, 3), axis=0)  # 상자 안쪽 바탕
    amber = (242, 196, 108)
    for i in range(59, 116):
        dx, dy, sc = tr[i] if i >= 70 else tr[70]
        a = 1.0  # 샷 시작(59)부터 바른 라벨로 덮는다(원본 라벨은 62-70프레임에 깨진 채 켜짐)
        before = fr[i].copy(); paint_label(fr[i], box, fill, '1,099쪽', amber, 66, dx, dy, radius=2)
        fr[i] = (before * (1 - a) + fr[i] * a).astype(np.uint8)
    write(fr, SRC[2], '/home/claude/flowfix/F02_1080p.mp4')
    log.append(f'F02: frames 59-115 label patch, track dx range {min(v[0] for v in tr.values())}..{max(v[0] for v in tr.values())}, min score {min(v[2] for v in tr.values()):.2f}, text {amber}')

if '3' in k:  # F03 판독창의 의미 없는 '1.0 … 0' 흐림
    fr = read(SRC[3])
    for i in range(63, 131):
        for _ in range(3): soft_blur(fr[i], (950, 400, 1760, 620), k=151, feather=20)
    for i in range(131, len(fr)):
        for _ in range(3): soft_blur(fr[i], (1150, 380, 1920, 625), k=151, feather=20)
    write(fr, SRC[3], '/home/claude/flowfix/F03_1080p.mp4'); log.append('F03: display digits blurred 63-189')

if '4' in k:  # F04 '홈몸' → '홈' (글자 픽셀만 지우고 다시 씀)
    fr = read(SRC[4]); box = (392, 300, 598, 402)
    tr = track(fr, 114, box, range(67, 115), search=20)
    t = fr[114][315:390, 400:585].reshape(-1, 3); amber = tuple(int(v) for v in np.percentile(t[t.sum(1) > 400], 60, axis=0))
    f = ImageFont.truetype(FONT, 72, index=1)
    for i in range(67, 115):
        dx, dy, sc = tr[i]; x0, y0, x1, y1 = box[0] + dx, box[1] + dy, box[2] + dx, box[3] + dy
        reg = fr[i][y0:y1, x0:x1]; g = cv2.cvtColor(reg, cv2.COLOR_RGB2GRAY)
        m = (g > 70).astype(np.uint8) * 255; m = cv2.dilate(m, np.ones((9, 9), np.uint8))
        fr[i][y0:y1, x0:x1] = cv2.inpaint(reg, m, 9, cv2.INPAINT_TELEA)
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.text((480 + dx, 352 + dy), '홈', font=f, fill=amber + (255,), anchor='mm')
        glow = lay.filter(__import__('PIL.ImageFilter', fromlist=['x']).GaussianBlur(8))
        base = Image.fromarray(fr[i]).convert('RGBA'); base.alpha_composite(glow); base.alpha_composite(lay)
        fr[i] = np.asarray(base.convert('RGB'))
    write(fr, SRC[4], '/home/claude/flowfix/F04_1080p.mp4'); log.append(f'F04: frames 67-114 홈 inpaint+text, color {amber}, min score {min(v[2] for v in tr.values()):.2f}')

if '5' in k:  # F05 '검섬색' → '검색', 배경 프린터 로고·계기판 글자 흐림
    fr = read(SRC[5])
    for rng, box, ref_i, size in [(range(0, 63), (893, 800, 1017, 832), 56, 22), (range(127, 190), (888, 823, 1046, 860), 182, 30)]:
        tr = track(fr, ref_i, box, rng, search=30); ref = fr[ref_i]
        x0, y0, x1, y1 = box; plate = np.median(ref[y0 + 2:y0 + 6, x0 + 4:x1 - 4].reshape(-1, 3), axis=0)
        t = ref[y0:y1, x0:x1].reshape(-1, 3); ink = tuple(int(v) for v in t[np.argmin(t.sum(1))])
        for i in rng:
            dx, dy, sc = tr[i]; paint_label(fr[i], (x0 + 3, y0 + 3, x1 - 3, y1 - 3), plate, '검색', ink, size, dx, dy, radius=1)
        log.append(f'F05 label {rng.start}-{rng.stop-1}: min score {min(v[2] for v in tr.values()):.2f}')
    for i in range(0, 63): soft_blur(fr[i], (905, 362, 985, 440), k=41, feather=10)
    for i in range(127, 190): soft_blur(fr[i], (930, 240, 1015, 318), k=41, feather=10)
    for i in range(63, 127): soft_blur(fr[i], (0, 1005, 760, 1080), k=41, feather=12)
    write(fr, SRC[5], '/home/claude/flowfix/F05_1080p.mp4')

if '6' in k:  # F06 첫 샷 프린터 로고·작은 글자 흐림
    fr = read(SRC[6])
    for i in range(0, 59):
        soft_blur(fr[i], (915, 482, 992, 558), k=41, feather=10); soft_blur(fr[i], (860, 548, 1110, 575), k=31, feather=8)
    write(fr, SRC[6], '/home/claude/flowfix/F06_1080p.mp4'); log.append('F06: logo blur 0-58')
print('\n'.join(log))
