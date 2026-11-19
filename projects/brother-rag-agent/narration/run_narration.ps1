# 저장소 루트(C:\dev\Video-Agent-studio)에서 실행: .\projects\brother-rag-agent\narration\run_narration.ps1
# Typecast compose 1회(재시도 없음) -> Whisper 정렬 -> short-window 로컬 보정
$ErrorActionPreference = 'Stop'
$py = '.\.venv-supertonic\Scripts\python.exe'
$n = 'projects\brother-rag-agent\narration'
& $py "$n\render.py"
if ($LASTEXITCODE -ne 0) { Write-Host 'Typecast 합성 실패 - 이후 단계 생략'; exit 1 }
& $py scripts\transcribe_narration.py "$n\narration.wav" "$n\source.txt" "$n\local-short-window-v1"
if ($LASTEXITCODE -ne 0) { Write-Host 'ASR 단계 실패 - 보정 생략'; exit 1 }
& $py scripts\balance_narration_phrases.py "$n\narration.wav" "$n\local-short-window-v1\sentence-boundaries.json" "$n\local-short-window-v1\transcription.json" "$n\local-short-window-v1\narration_balanced.wav" --mode short-window
Write-Host '완료: projects\brother-rag-agent\narration\local-short-window-v1\narration_balanced.wav'
