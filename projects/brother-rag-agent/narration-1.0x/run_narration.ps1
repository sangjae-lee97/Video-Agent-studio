# 저장소 루트(C:\dev\Video-Agent-studio)에서 실행: .\projects\brother-rag-agent\narration-1.0x\run_narration.ps1
# Typecast compose 1회(1.0배속, 재시도 없음). 정렬·보정은 에이전트가 이어서 한다.
$ErrorActionPreference = 'Stop'
& '.\.venv-supertonic\Scripts\python.exe' 'projects\brother-rag-agent\narration-1.0x\render.py'
