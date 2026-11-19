import subprocess, glob
U='/mnt/user-data/uploads/'; O='/mnt/user-data/outputs/flow/'
g=lambda p: glob.glob(U+p)[0]
M='/home/claude/bra/motion/out/'
WAV=U+'Video-Agent-studio/projects/brother-rag-agent/narration/local-short-window-v1/narration_balanced.wav'
# (name, path, select-expr(source frame), n_out, extra filter)
seq=[
('M00',M+'M00.mp4',None,72,''),
('F01',O+'F01_1080p.mp4',"between(n\\,119\\,189)",71,''),
('F02',g('7b3eba64*.mp4'),"between(n\\,1\\,169)",169,''),
('M01',M+'M01.mp4',None,72,''),
('M02',M+'M02.mp4',None,199,''),
('F03',g('31d447d8*.mp4'),"lte(n\\,155)",158,"boxblur=lr=20:enable='lt(t,2.46)':cr=10[__b];"),  # placeholder replaced below
('M03',M+'M03.mp4',None,128,''),
('M04',M+'M04.mp4',None,216,''),
('M05',M+'M05.mp4',None,221,''),
('M06',M+'M06.mp4',None,110,''),
('F04',O+'F04_1080p.mp4',"lte(n\\,172)",173,''),
('M07',M+'M07.mp4',None,187,''),
('M08',M+'M08.mp4',None,190,''),
('M09',M+'M09.mp4',None,148,''),
('M10',M+'M10.mp4',None,204,''),
('M11',M+'M11.mp4',None,111,''),
('M12',M+'M12.mp4',None,129,''),
('F05',O+'F05_1080p.mp4',"lte(n\\,151)",152,''),
('F06',O+'F06_1080p.mp4',"lte(n\\,145)",146,''),
('M13',M+'M13.mp4',None,147,''),
]
tot=sum(s[3] for s in seq); print('frames',tot,tot/24)
args=['ffmpeg','-v','error','-y']
for s in seq: args+=['-i',s[1]]
args+=['-i',WAV]
fl=[]
for i,(nm,p,sel,n,_) in enumerate(seq):
    chain=f"[{i}:v]"
    if sel: chain+=f"select='{sel}',"
    chain+="setpts=N/24/TB,fps=24,scale=1920:1080,setsar=1,format=yuv420p"
    if nm=='F03':
        # soften blurred background printer logo (top-left) in shot 1 only
        fl.append(chain+f"[s{i}]"); fl.append(f"[s{i}]split[a{i}][b{i}]")
        fl.append(f"[b{i}]crop=1920:300:0:0,gblur=sigma=16,format=yuva420p,geq=lum='lum(X,Y)':cb='cb(X,Y)':cr='cr(X,Y)':a='clip((290-Y)*255/90,0,255)'[c{i}]")
        fl.append(f"[a{i}][c{i}]overlay=0:0:enable='lt(t\\,2.46)'[d{i}]"); chain=f"[d{i}]"
        fl.append(chain+f"tpad=stop_mode=clone:stop=4,trim=end_frame={n},setpts=PTS-STARTPTS[v{i}]"); continue
    if nm=='F05':
        chain+=",delogo=x=940:y=70:w=90:h=56:enable='gte(t\\,4.5)'"
    fl.append(chain+f",tpad=stop_mode=clone:stop=4,trim=end_frame={n},setpts=PTS-STARTPTS[v{i}]")
fl.append(''.join(f'[v{i}]' for i in range(len(seq)))+f"concat=n={len(seq)}:v=1:a=0[v]")
fl.append(f"[{len(seq)}:a]alimiter=limit=0.891:level=false:attack=1:release=50,apad,atrim=end={tot/24}[a]")
args+=['-filter_complex',';'.join(fl),'-map','[v]','-map','[a]','-c:v','libx264','-crf','16','-preset','medium','-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','nocap.mp4']
subprocess.run(args,check=True)
t=0
for s in seq: print(f"{s[0]} {t/24:8.3f} {(t+s[3])/24:8.3f} {s[3]}"); t+=s[3]
