# 저장소 루트(Video-Agent-studio)에서 실행: .\projects\brother-rag-1123-experiments\narration-v2\run_narration.ps1
# part1 = 기존 음성 1~17번 줄(이미 잘라 둠, 합성 없음) / part2 = 새 끝부분 18~26번 줄만 Typecast 1회 합성
# -> 이어 붙이기 -> 로컬 Whisper 정렬 -> short-window 음량 보정
$ErrorActionPreference = 'Stop'
$py = '.\.venv-supertonic\Scripts\python.exe'
$n = 'projects\brother-rag-1123-experiments\narration-v2'
if (-not (Test-Path "$n\part2\narration.wav")) {
  & $py scripts\typecast_compose.py synth "$n\part2"
  if ($LASTEXITCODE -ne 0) { Write-Host 'Typecast 합성 실패 - 이후 단계 생략'; exit 1 }
}
& $py scripts\typecast_compose.py concat $n "$n\part1" "$n\part2"
if ($LASTEXITCODE -ne 0) { exit 1 }
& $py scripts\transcribe_narration.py "$n\narration.wav" "$n\source.txt" "$n\local-short-window-v1"
if ($LASTEXITCODE -ne 0) { Write-Host '정렬 실패 - 에이전트에게 알려 주세요(단어 시각 수동 매핑)'; exit 1 }
& $py scripts\balance_narration_phrases.py "$n\narration.wav" "$n\local-short-window-v1\sentence-boundaries.json" "$n\local-short-window-v1\transcription.json" "$n\local-short-window-v1\narration_balanced.wav" --mode short-window
Write-Host "완료: $n\local-short-window-v1\narration_balanced.wav"
