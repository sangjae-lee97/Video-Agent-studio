# 저장소 루트에서 실행: .\projects\rag-concepts-longform\narration\run_balance.ps1
# 정렬은 에이전트가 91줄 수동 대조로 완료(local-short-window-v1\transcription.json). short-window 보정만 실행. 크레딧 없음.
$ErrorActionPreference = 'Stop'
$py = '.\.venv-supertonic\Scripts\python.exe'
$n = 'projects\rag-concepts-longform\narration\local-short-window-v1'
& $py scripts\balance_narration_phrases.py 'projects\rag-concepts-longform\narration\narration.wav' "$n\sentence-boundaries.json" "$n\transcription.json" "$n\narration_balanced.wav" --mode short-window
Write-Host "완료: $n\narration_balanced.wav"
