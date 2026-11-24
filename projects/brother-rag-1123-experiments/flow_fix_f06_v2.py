"""F06 v2 사용 구간(소스 59-157) 보정: 다이얼 둘레의 뜻 없는 라벨(패병·찹용·nmN / 쇄테·인상블)을 지운다.
입력은 v1 보정본 F06_1080p.mp4, 출력 F06v2_1080p.mp4."""
import subprocess, numpy as np, cv2
W, H = 1920, 1080
src = '/home/claude/flowfix/F06_1080p.mp4'
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).copy()
BOX = {range(59, 110): [(740, 920, 875, 982), (650, 978, 780, 1052), (1135, 992, 1275, 1052)],
       range(110, 190): [(740, 675, 872, 765), (650, 728, 828, 826)]}
for rng, boxes in BOX.items():
    for i in rng:
        for x0, y0, x1, y1 in boxes:
            reg = fr[i][y0:y1, x0:x1].copy()
            m = (cv2.cvtColor(reg, cv2.COLOR_RGB2GRAY) > 62).astype(np.uint8)
            m = cv2.dilate(m, np.ones((11, 11), np.uint8))
            fr[i][y0:y1, x0:x1] = cv2.inpaint(reg, m * 255, 6, cv2.INPAINT_TELEA)
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                      '-c:v', 'libx264', '-crf', '14', '-preset', 'slow', '-pix_fmt', 'yuv420p', '/home/claude/flowfix/F06v2_1080p.mp4'], stdin=subprocess.PIPE)
for f in fr: p.stdin.write(f.tobytes())
p.stdin.close(); assert p.wait() == 0
