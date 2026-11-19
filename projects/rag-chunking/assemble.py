import subprocess, glob
U='/mnt/user-data/uploads/'
g=lambda p: glob.glob(U+p)[0]
M='/home/claude/motion/out/'
seq=[('F01',g('1e8eb51a*.mp4'),190),('M01',M+'M01.mp4',290),('M02',M+'M02.mp4',153),('F02',g('020dce63*.mp4'),190),
('M03',M+'M03.mp4',233),('F03',g('58f7925e*.mp4'),190),('M04',M+'M04.mp4',302),('M05',M+'M05.mp4',202),('F04','/home/claude/asm/F04_fixed.mp4',190),
('M06',M+'M06.mp4',312),('M07',M+'M07.mp4',143),('M08',M+'M08.mp4',210),('M09',M+'M09.mp4',322),('F05',g('da39405a*.mp4'),190),
('M10',M+'M10.mp4',297),('M11',M+'M11.mp4',236),('F06',g('09bb0963*.mp4'),190),('M12',M+'M12.mp4',19)]
tot=sum(n for *_,n in seq); print('frames',tot, tot/24)
args=['ffmpeg','-v','error','-y']
for _,p,_ in seq: args+=['-i',p]
args+=['-i','/mnt/user-data/uploads/Video-Agent-studio/projects/rag-chunking/narration/local-short-window-v2/narration_balanced.wav']
fl=[]
for i,(_,p,n) in enumerate(seq):
    fl.append(f"[{i}:v]fps=24,scale=1920:1080,setsar=1,format=yuv420p,tpad=stop_mode=clone:stop=2,trim=end_frame={n},setpts=PTS-STARTPTS[v{i}]")
fl.append(''.join(f'[v{i}]' for i in range(len(seq)))+f"concat=n={len(seq)}:v=1:a=0[v]")
fl.append(f"[{len(seq)}:a]alimiter=limit=0.891:level=false:attack=1:release=50,apad,atrim=end={tot/24}[a]")
args+=['-filter_complex',';'.join(fl),'-map','[v]','-map','[a]','-c:v','libx264','-crf','16','-preset','medium','-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','nocap.mp4']
subprocess.run(args,check=True)
# edit table with frame ranges
t=0
for name,p,n in seq: print(f"{name} {t/24:8.3f} {(t+n)/24:8.3f} {n}"); t+=n
