import json, re
T=json.load(open('/mnt/user-data/uploads/Video-Agent-studio/projects/rag-concepts-longform/narration/local-short-window-v1/transcription.json',encoding='utf-8'))
terms=json.load(open('caption-terms.ko.json',encoding='utf-8'))
pat=re.compile('|'.join(map(re.escape,sorted(terms,key=len,reverse=True))))
disp=lambda s: pat.sub(lambda m:terms[m[0]],s)
norm=lambda s: re.sub(r'[^0-9A-Za-z가-힣]','',s)
END=626.79
def chunks(line):
    parts=[p for p in re.split(r'(?<=[,.?!])\s+',line) if p]
    out=[]
    for p in parts:
        if out and not re.search(r'[.?!]$',out[-1]) and (len(norm(disp(p)))<7 or len(norm(disp(out[-1])))<7) and len(disp(out[-1]+' '+p))<=27: out[-1]+=' '+p
        else: out.append(p)
    res=[]
    for p in out:
        while len(disp(p))>27:
            w=p.split(' '); best=None
            for i in range(1,len(w)):
                if re.match(r'^(개|매|위|장|쪽|번|퍼센트)',w[i]): continue
                a=' '.join(w[:i]); d=abs(len(disp(a))-len(disp(p))/2)
                if len(disp(a))<=27 and (best is None or d<best[0]): best=(d,i)
            i=best[1]; res.append(' '.join(w[:i])); p=' '.join(w[i:])
        res.append(p)
    return res
def clean(s):
    s=disp(s)
    s=re.sub(r',(?=\s)','',s); s=re.sub(r'(?<!\d),(?!\d)','',s); s=re.sub(r'[.!?…]+(?=\s|$)','',s)
    return s.strip()
cues=[]
for seg in T['segments']:
    W=seg['words']; line=seg['script']; cs=chunks(line)
    import difflib
    S=norm(line); R=''; own=[]
    for i,w in enumerate(W):
        t=norm(w['text']); R+=t; own+=[i]*len(t)
    m={}
    for a0,b0,n in difflib.SequenceMatcher(None,S,R,autojunk=False).get_matching_blocks():
        for q in range(n): m[a0+q]=b0+q
    pos=0; starts=[]
    for ch in cs:
        q=pos-1
        while q>=0 and q not in m: q-=1
        idx=own[m[q]]+1 if q>=0 else 0
        idx=min(idx,len(W)-1)
        if starts and idx<=starts[-1]: idx=min(starts[-1]+1,len(W)-1)
        starts.append(0 if pos==0 else idx); pos+=len(norm(ch))
    for k,ch in enumerate(cs):
        a=starts[k]; b=(starts[k+1]-1) if k+1<len(cs) else len(W)-1
        b=max(a,b)
        cues.append([W[a]['start'],W[b]['end']+0.25,clean(ch),''.join(w['text'] for w in W[a:b+1]).strip(),W[a:b+1]])
# 코드·숫자로 끝나는 큐: ASR이 다음 큐 첫 단어로 붙인 숫자 토큰을 앞 큐로 옮긴다
for i in range(len(cues)-1):
    if not re.search(r'(L2885|아니면 0)$',cues[i][2]): continue
    nw=cues[i+1][4]
    if len(nw)>1 and re.match(r'^\s*[0-9.]',nw[0]['text']):
        k=1
        while k<len(nw)-1 and not nw[k]['text'].startswith(' '): k+=1
        mv=nw[:k]
        cues[i][1]=mv[-1]['end']+0.25; cues[i+1][0]=nw[k]['start']; cues[i][4]=cues[i][4]+mv; cues[i+1][4]=nw[k:]
        cues[i][3]+=''.join(w['text'] for w in mv); cues[i+1][3]=''.join(w['text'] for w in nw[k:]).strip()
i=0
while i<len(cues)-1:
    if min(cues[i][1],cues[i+1][0])-cues[i][0]<0.8 and cues[i+1][0]-cues[i][1]<0.6:
        cues[i]=[cues[i][0],cues[i+1][1],cues[i][2]+' '+cues[i+1][2],cues[i][3]+' '+cues[i+1][3],cues[i][4]+cues[i+1][4]]; del cues[i+1]
    else: i+=1
for i in range(len(cues)-1): cues[i][1]=min(cues[i][1],cues[i+1][0]-0.02)
cues[-1][1]=min(cues[-1][1],END)
def ts(x):
    ms=round(x*1000); h,ms=divmod(ms,3600000); m,ms=divmod(ms,60000); s,ms=divmod(ms,1000); return f"{h:02}:{m:02}:{s:02},{ms:03}"
bad=[(i,c) for i,c in enumerate(cues,1) if c[1]-c[0]<0.7]
open('captions.ko.srt','w',encoding='utf-8').write('\n'.join(f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n" for i,(a,b,t,_,__) in enumerate(cues,1)))
json.dump([c[:4] for c in cues],open('cues.json','w'),ensure_ascii=False)
print(len(cues),'short:',bad[:5])
