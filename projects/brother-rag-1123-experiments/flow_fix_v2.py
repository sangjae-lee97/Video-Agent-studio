"""v2 Flow 채택본 보정 (F07, F08). 원본은 그대로 두고 F07_1080p.mp4, F08_1080p.mp4를 만든다.
F07 1샷: 판독창의 의미 없는 숫자 → 7세그먼트 "100.00"(실제 세그먼트 모양을 잘라 조립), 깨진 라벨 "인쇠보"→"인쇄", "애회/애괴" 지움
F07 3샷: 결과지 머리글 "인식뭔 됨" 지움, 줄 번호 자리의 뜻 없는 글자 지움
F08 2샷: "인쇄보" → "인쇄"("보" 글자만 지움)
"""
import subprocess, sys, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
W, H = 1920, 1080
D = '/home/claude/flowfix'
FONT_M = '/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc'

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
    x0, y0, x1, y1 = box
    tpl = cv2.cvtColor(frames[ref_i][y0:y1, x0:x1], cv2.COLOR_RGB2GRAY)
    out = {}
    for i in rng:
        sx0, sy0 = max(0, x0 - search), max(0, y0 - search)
        win = cv2.cvtColor(frames[i][sy0:min(H, y1 + search), sx0:min(W, x1 + search)], cv2.COLOR_RGB2GRAY)
        r = cv2.matchTemplate(win, tpl, cv2.TM_CCOEFF_NORMED)
        _, sc, _, loc = cv2.minMaxLoc(r)
        out[i] = (sx0 + loc[0] - x0, sy0 + loc[1] - y0, sc)
    return out

def crop(img, box, dx=0, dy=0):
    x0, y0, x1, y1 = box
    return img[y0 + dy:y1 + dy, x0 + dx:x1 + dx]

def blend_into(img, box, dx, dy, patch, alpha):
    x0, y0, x1, y1 = box
    reg = img[y0 + dy:y1 + dy, x0 + dx:x1 + dx].astype(np.float32)
    a = alpha[..., None]
    img[y0 + dy:y1 + dy, x0 + dx:x1 + dx] = (reg * (1 - a) + patch.astype(np.float32) * a).clip(0, 255).astype(np.uint8)

def occlusion_keep(cur, ref, thr=38, grow=9):
    """cur가 ref와 다른 곳(손이 가린 곳)=1. 그 곳은 원본을 남긴다."""
    a = cv2.GaussianBlur(cur.astype(np.float32), (5, 5), 0); b = cv2.GaussianBlur(ref.astype(np.float32), (5, 5), 0)
    d = np.abs(a - b).max(2)
    m = (d > thr).astype(np.uint8)
    m = cv2.dilate(m, np.ones((grow, grow), np.uint8))
    return cv2.GaussianBlur(m.astype(np.float32), (0, 0), 2.5)

def glove_mask(reg, k=13, grow=1, sig=0.8):
    """장갑(밝은 회색의 큰 덩어리)=1. 가는 흰 글자 획은 열림 연산으로 빠진다."""
    hsv = cv2.cvtColor(reg, cv2.COLOR_RGB2HSV)
    m = ((hsv[..., 2] > 75) & (hsv[..., 1] < 70)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((k, k), np.uint8))
    m = cv2.dilate(m, np.ones((grow, grow), np.uint8))
    return cv2.GaussianBlur(m.astype(np.float32), (0, 0), sig)

def text_mask(region, thr=120, dark=False):
    g = cv2.cvtColor(region, cv2.COLOR_RGB2GRAY)
    return ((g < thr) if dark else (g > thr)).astype(np.uint8)

log = []
todo = sys.argv[1:] or ['7', '8']

if '7' in todo:
    src = f'{D}/F07_raw_1080p.mp4'; fr = read(src)
    # ---------- 1샷(0-58): 라벨 ----------
    REF = 50
    tr = track(fr, REF, (525, 560, 878, 800), range(0, 59))
    L = (850, 545, 1140, 642)
    ref = fr[REF].copy(); Q = crop(ref, L).copy()
    tm = np.zeros(Q.shape[:2], np.uint8)
    for (x0, y0, x1, y1) in [(876, 555, 948, 593), (1044, 564, 1096, 599), (1078, 602, 1132, 636)]:
        sub = text_mask(ref[y0:y1, x0:x1], 120)
        tm[y0 - L[1]:y1 - L[1], x0 - L[0]:x1 - L[0]] |= sub
    tm = cv2.dilate(tm, np.ones((5, 5), np.uint8))
    Qc = cv2.inpaint(Q, tm * 255, 5, cv2.INPAINT_TELEA)
    im = Image.fromarray(Qc); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT_M, 30, index=1)
    d.text((947 - L[0], 574 - L[1]), '인쇄', font=f, fill=(212, 216, 222), anchor='rm')
    Qc = np.asarray(im).copy()
    newm = (np.abs(Qc.astype(int) - cv2.inpaint(Q, tm * 255, 5, cv2.INPAINT_TELEA).astype(int)).max(2) > 10).astype(np.uint8)
    Qc = cv2.GaussianBlur(Qc, (0, 0), 0.6)
    edit = cv2.GaussianBlur(cv2.dilate(tm | newm, np.ones((7, 7), np.uint8)).astype(np.float32), (0, 0), 2)
    # ---------- 1샷: 판독창 "100.00" ----------
    # 30번 프레임(세그먼트 전부 꺼짐)의 판독창을 바탕으로 쓰고, 꺼진 '8' 모양에서 세그먼트 자리를 찾아 필요한 것만 켠다.
    o30 = np.array(tr[30][:2])
    S = (628, 370, 1108, 522)
    base = crop(fr[30], S).astype(np.float32).copy()
    amb = cv2.GaussianBlur(base[..., 0] - base[..., 2], (0, 0), 1.0)
    gm = ((amb - cv2.GaussianBlur(amb, (0, 0), 9)) > 3).astype(np.uint8)
    gm = cv2.morphologyEx(gm, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(gm)
    digs = sorted([i for i in range(1, n) if st[i, 4] > 1500], key=lambda i: st[i, 0])
    dps = sorted([i for i in range(1, n) if 40 < st[i, 4] < 400], key=lambda i: st[i, 0])
    assert len(digs) == 5, [st[i] for i in range(1, n)]
    lit_m = np.zeros(gm.shape, np.uint8)
    ON = {'1': 'bc', '0': 'abcdef'}
    dpxy = None
    for k, (ch, di) in enumerate(zip('10000', digs)):
        ys, xs = np.where(lab == di)
        top, bot = ys.min(), ys.max(); hh = bot - top
        ry = np.unique(ys)
        kl = np.polyfit(ry, [xs[ys == y].min() for y in ry], 1); kr = np.polyfit(ry, [xs[ys == y].max() for y in ry], 1)
        l = np.polyval(kl, ys); r = np.polyval(kr, ys); ww = (r - l).mean()
        # 매끈한 세그먼트를 다시 그린다(4배 해상도에서 그려 줄임). 바깥 경계선 기울기와 높이는 꺼진 '8'에서 잰 값.
        SS = 4; t = 10.0; gap = 1.6
        def P(X, Y):  # 기울지 않은 좌표 → 화면 좌표(배율 SS)
            yy = top + Y
            return ((np.polyval(kl, yy) + X) * SS, yy * SS)
        def hbar(Y0, x0, x1):
            yc = Y0 + t / 2
            pts = [(x0, yc), (x0 + t / 2, Y0), (x1 - t / 2, Y0), (x1, yc), (x1 - t / 2, Y0 + t), (x0 + t / 2, Y0 + t)]
            return [P(*p) for p in pts]
        def vbar(X0, y0, y1):
            xc = X0 + t / 2
            pts = [(xc, y0), (X0 + t, y0 + t / 2), (X0 + t, y1 - t / 2), (xc, y1), (X0, y1 - t / 2), (X0, y0 + t / 2)]
            return [P(*p) for p in pts]
        Wd = ww
        geo = {'a': hbar(0, gap, Wd - gap), 'g': hbar(hh / 2 - t / 2, gap, Wd - gap), 'd': hbar(hh - t, gap, Wd - gap),
               'f': vbar(0, gap, hh / 2 - gap), 'b': vbar(Wd - t, gap, hh / 2 - gap),
               'e': vbar(0, hh / 2 + gap, hh - gap), 'c': vbar(Wd - t, hh / 2 + gap, hh - gap)}
        canvas = Image.new('L', (gm.shape[1] * SS, gm.shape[0] * SS), 0); dr = ImageDraw.Draw(canvas)
        for kk in ON[ch]: dr.polygon(geo[kk], fill=255)
        if k == 2:
            bx, by = P(Wd + 7, hh - 5); dr.ellipse([bx - 5.5 * SS, by - 5.5 * SS, bx + 5.5 * SS, by + 5.5 * SS], fill=255); dpxy = (bx / SS, by / SS)
        lit_m |= (np.asarray(canvas.resize((gm.shape[1], gm.shape[0]), Image.LANCZOS)) > 110).astype(np.uint8)
    dist = cv2.distanceTransform(lit_m, cv2.DIST_L2, 3)
    core = np.clip(dist / 2.6, 0, 1)[..., None]
    yel = np.array([255, 232, 80], np.float32); org = np.array([255, 150, 10], np.float32)
    col = org * (1 - core) + yel * core
    al = cv2.GaussianBlur(lit_m.astype(np.float32), (0, 0), 0.8)[..., None]
    glow = cv2.GaussianBlur(lit_m.astype(np.float32), (0, 0), 6)[..., None]
    disp = (base * (1 - al) + col * al + org * glow * 0.75).clip(0, 255).astype(np.uint8)
    np.save('/tmp/disp100.npy', disp)
    o10 = o30
    dmask = np.zeros(disp.shape[:2], np.float32); dmask[6:-6, 6:-6] = 1; dmask = cv2.GaussianBlur(dmask, (0, 0), 3)
    LIT = [i for i in range(0, 59) if not (24 <= i <= 37)]
    for i in range(0, 59):
        dx, dy, sc = tr[i]
        cur = crop(fr[i], L, dx, dy)
        keep = glove_mask(cur)
        blend_into(fr[i], L, dx, dy, Qc, edit * (1 - keep))
        if i in LIT:
            ox, oy = int(dx - o10[0]), int(dy - o10[1])
            reg = crop(fr[i], S, ox, oy)
            glove = glove_mask(reg)
            blend_into(fr[i], S, ox, oy, disp, dmask * (1 - glove))
    log.append(f'F07 shot1 track dx {min(v[0] for v in tr.values())}..{max(v[0] for v in tr.values())} min score {min(v[2] for v in tr.values()):.2f}')
    # ---------- 3샷(119-189): 머리글·줄 번호 지움 ----------
    REF3 = 150
    t3 = track(fr, REF3, (620, 238, 752, 470), range(119, 190))
    ref3 = fr[REF3]
    polys = [np.array([[562, 236], [626, 236], [603, 930], [556, 930]]), np.array([[1004, 236], [1050, 236], [1053, 930], [1006, 930]])]
    heads = [(785, 172, 882, 214), (1205, 172, 1302, 214)]
    for i in range(119, 190):
        dx, dy, sc = t3[i]
        img = fr[i]
        for hb in heads:
            reg = crop(img, hb, dx, dy).copy()
            m = cv2.dilate(text_mask(reg, 200, dark=True), np.ones((5, 5), np.uint8))
            img[hb[1] + dy:hb[3] + dy, hb[0] + dx:hb[2] + dx] = cv2.inpaint(reg, m * 255, 6, cv2.INPAINT_TELEA)
        for pg in polys:
            x0, y0 = pg.min(0); x1, y1 = pg.max(0); b = (int(x0) - 4, int(y0), int(x1) + 4, int(y1))
            reg = crop(img, b, dx, dy).copy()
            area = np.zeros(reg.shape[:2], np.uint8); cv2.fillPoly(area, [pg - [b[0], b[1]]], 1)
            hsv = cv2.cvtColor(reg, cv2.COLOR_RGB2HSV)
            m = ((hsv[..., 2] < 185) & (hsv[..., 1] < 45)).astype(np.uint8) & area
            m = cv2.dilate(m, np.ones((5, 5), np.uint8)) & area
            img[b[1] + dy:b[3] + dy, b[0] + dx:b[2] + dx] = cv2.inpaint(reg, m * 255, 5, cv2.INPAINT_TELEA)
    log.append(f'F07 shot3 track dx {min(v[0] for v in t3.values())}..{max(v[0] for v in t3.values())} dy {min(v[1] for v in t3.values())}..{max(v[1] for v in t3.values())} min score {min(v[2] for v in t3.values()):.2f}')
    write(fr, src, f'{D}/F07_1080p.mp4')

if '8' in todo:
    src = f'{D}/F08_raw_1080p.mp4'; fr = read(src)
    REF = 98
    tr = track(fr, REF, (650, 200, 1290, 440), range(49, 102))
    B = (790, 608, 850, 668)
    ref = fr[REF]; Q = crop(ref, B).copy()
    m = text_mask(Q, 120)
    yy, xx = np.mgrid[0:Q.shape[0], 0:Q.shape[1]]
    m[((xx + B[0] - 849) ** 2 + (yy + B[1] - 676) ** 2) < 15 ** 2] = 0   # 눈금 점은 남긴다
    m[:, :max(0, 793 - B[0])] = 0
    m = cv2.dilate(m, np.ones((7, 7), np.uint8))
    g = cv2.cvtColor(Q, cv2.COLOR_RGB2GRAY)
    panel = np.median(Q[(g < 70) & (m == 0)], axis=0)
    # 패널 질감: 주변 패널을 크게 흐린 바탕 + 원래 잔결 대신 가까운 패널 조각을 붙인다
    Qc = Q.copy(); Qc[m > 0] = panel
    Qc = np.where(m[..., None] > 0, cv2.GaussianBlur(Qc, (0, 0), 3), Q)
    edit = cv2.GaussianBlur(cv2.dilate(m, np.ones((5, 5), np.uint8)).astype(np.float32), (0, 0), 2)
    for i in range(49, 102):
        dx, dy, sc = tr[i]
        cur = crop(fr[i], B, dx, dy)
        keep = glove_mask(cur)
        blend_into(fr[i], B, dx, dy, Qc, edit * (1 - keep))
    log.append(f'F08 shot2 track dx {min(v[0] for v in tr.values())}..{max(v[0] for v in tr.values())} dy {min(v[1] for v in tr.values())}..{max(v[1] for v in tr.values())} min score {min(v[2] for v in tr.values()):.2f}')
    write(fr, src, f'{D}/F08_1080p.mp4')

print('\n'.join(log))
