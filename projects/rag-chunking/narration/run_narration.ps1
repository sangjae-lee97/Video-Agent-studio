# 저장소 루트(C:\dev\Video-Agent-studio)에서 실행: .\projects\rag-chunking\narration\run_narration.ps1
$ErrorActionPreference = 'Stop'
$py = '.\.venv-supertonic\Scripts\python.exe'
$n = 'projects\rag-chunking\narration'
& $py "$n\render.py"                                   # Typecast compose 1회 (재시도 없음)
& $py scripts\transcribe_narration.py "$n\narration.wav" "$n\source.txt" "$n\local-short-window-v1"
& $py scripts\balance_narration_phrases.py "$n\narration.wav" "$n\local-short-window-v1\sentence-boundaries.json" "$n\local-short-window-v1\transcription.json" "$n\local-short-window-v1\narration_balanced.wav" --mode short-window
