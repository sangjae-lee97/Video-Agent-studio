# 저장소 루트(Video-Agent-studio)에서 실행: .\projects\brother-rag-1123-experiments\narration\run_narration.ps1
# Typecast Compose 1회 합성(재시도 없음) -> 로컬 Whisper 정렬 -> short-window 음량 보정
$ErrorActionPreference = 'Stop'
$py = '.\.venv-supertonic\Scripts\python.exe'
$n = 'projects\brother-rag-1123-experiments\narration'
& $py scripts\typecast_compose.py synth $n
if ($LASTEXITCODE -ne 0) { Write-Host 'Typecast 합성 실패 - 이후 단계 생략'; exit 1 }
& $py scripts\transcribe_narration.py "$n\narration.wav" "$n\source.txt" "$n\local-short-window-v1"
if ($LASTEXITCODE -ne 0) { Write-Host '정렬 실패 - 에이전트에게 알려 주세요(단어 시각 수동 매핑)'; exit 1 }
& $py scripts\balance_narration_phrases.py "$n\narration.wav" "$n\local-short-window-v1\sentence-boundaries.json" "$n\local-short-window-v1\transcription.json" "$n\local-short-window-v1\narration_balanced.wav" --mode short-window
Write-Host "완료: $n\local-short-window-v1\narration_balanced.wav"
