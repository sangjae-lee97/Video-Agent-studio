# rag-concepts-longform 본편 조립(자막 전): Flow 12 + 모션 31, 보정 내레이션, 최종 마스터 alimiter(-1 dBFS)
import subprocess, sys
sys.path.insert(0,'/home/claude/motion'); import scenes
FL='/home/claude/flow/'; M='/home/claude/motion/out/'
WAV='/mnt/user-data/uploads/Video-Agent-studio/projects/rag-concepts-longform/narration/local-short-window-v1/narration_balanced.wav'
flow={'F01':(0,190),'F02':(190,190),'F03':(1927,190),'F04':(3538,190),'F05':(4106,164),'F06':(6595,190),'F07':(9101,190),
      'F08':(9458,190),'F09':(10282,180),'F10':(11450,190),'F11':(12365,190),'F12':(14698,190)}
seq=[(k,FL+k+'_1080p.mp4',a,n) for k,(a,n) in flow.items()]+[(k,M+k+'.mp4',s,e-s) for k,(s,e,_) in scenes.S.items()]
seq.sort(key=lambda x:x[2])
t=0
for k,p,a,n in seq:
    assert a==t,(k,a,t); t+=n
END=t; print('frames',END,END/24)
args=['ffmpeg','-v','error','-y']
for s in seq: args+=['-i',s[1]]
args+=['-i',WAV]; fl=[]
for i,(k,p,a,n) in enumerate(seq):
    fl.append(f"[{i}:v]setpts=N/24/TB,fps=24,scale=1920:1080,setsar=1,format=yuv420p,tpad=stop_mode=clone:stop=2,trim=end_frame={n},setpts=PTS-STARTPTS[v{i}]")
fl.append(''.join(f'[v{i}]' for i in range(len(seq)))+f"concat=n={len(seq)}:v=1:a=0[v]")
fl.append(f"[{len(seq)}:a]alimiter=limit=0.891:level=false:attack=1:release=50,apad,atrim=end={END/24}[a]")
args+=['-filter_complex',';'.join(fl),'-map','[v]','-map','[a]','-c:v','libx264','-crf','17','-preset','medium','-pix_fmt','yuv420p','-r','24',
       '-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','/home/claude/asm/nocap.mp4']
subprocess.run(args,check=True)
with open('/home/claude/asm/edl.txt','w') as f:
    for k,p,a,n in seq: f.write(f"{k} {a/24:8.3f} {(a+n)/24:8.3f} {n}\n")
