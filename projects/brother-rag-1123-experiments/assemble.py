"""brother-rag-1123-experiments v2 본편 조립(자막 전): Flow 8개(편집 보정본) + 모션 19개(M01~M11, M17~M24), narration-v2 보정 음성,
최종 마스터 alimiter(-1 dBFS). 클라우드 작업 공간 경로 기준. 저장소에서는 FL/M/WAV 경로만 바꾸면 된다.
Flow 값: (본편 시작초, 본편 끝초, 파일, 소스 시작 프레임)"""
import subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'motion')); import scenes
FL = '/home/claude/flowfix/'; M = str(HERE / 'motion/out') + '/'
WAV = '/mnt/user-data/uploads/Video-Agent-studio/projects/brother-rag-1123-experiments/narration-v2/local-short-window-v1/narration_balanced.wav'
F = lambda t: round(t * 24)
flow = {'F01': (0.0, 7.9, 'F01_1080p.mp4', 0), 'F02': (15.2, 21.5, 'F02_1080p.mp4', 0), 'F03': (44.3, 52.2, 'F03_1080p.mp4', 0),
        'F04': (79.1, 86.1, 'F04_1080p.mp4', 0),
        'F05': (110.2, 114.25, 'F05_1080p.mp4', 24),     # 노브 셋 → 바늘이 100 쪽으로
        'F07': (125.4, 132.9, 'F07_1080p.mp4', 0),
        'F06': (155.2, 159.3, 'F06v2_1080p.mp4', 59),    # 49.0 dB → "인쇄" 링
        'F08': (170.3, 176.9, 'F08_1080p.mp4', 0)}
seq = [(k, FL + f, F(a), F(b) - F(a), s) for k, (a, b, f, s) in flow.items()] + [(k, M + k + '.mp4', s, e - s, 0) for k, (s, e, _) in scenes.S.items()]
seq.sort(key=lambda x: x[2])
t = 0
for k, p, a, n, s in seq:
    assert a == t, (k, a, t); t += n
END = t; print('frames', END, END / 24)
args = ['ffmpeg', '-v', 'error', '-y']
for s in seq: args += ['-i', s[1]]
args += ['-i', WAV]; fl = []
for i, (k, p, a, n, s) in enumerate(seq):
    fl.append(f"[{i}:v]setpts=N/24/TB,fps=24,scale=1920:1080,setsar=1,format=yuv420p,tpad=stop_mode=clone:stop=2,trim=start_frame={s}:end_frame={s+n},setpts=PTS-STARTPTS[v{i}]")
fl.append(''.join(f'[v{i}]' for i in range(len(seq))) + f"concat=n={len(seq)}:v=1:a=0[v]")
fl.append(f"[{len(seq)}:a]alimiter=limit=0.891:level=false:attack=1:release=50,apad,atrim=end={END/24}[a]")
args += ['-filter_complex', ';'.join(fl), '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', '24',
         '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', str(HERE / 'asm/nocap.mp4')]
subprocess.run(args, check=True)
with open(HERE / 'asm/edl.txt', 'w') as f:
    for k, p, a, n, s in seq: f.write(f"{k} {a/24:8.3f} {(a+n)/24:8.3f} {n} src+{s}\n")
