# 저장소 루트(Video-Agent-studio)에서 실행: .\projects\rag-concepts-longform\narration\run_narration.ps1
# 긴 원고(5,371자)라 Compose 한도 2,000자에 맞춰 4개 요청으로 나눠 합성한다(약 5,400크레딧).
# part1~4 각 1회 합성(재시도 없음, 이미 받은 part는 건너뜀) -> 0.18초 휴지로 이어 붙임 -> 로컬 Whisper 정렬 -> short-window 보정
$ErrorActionPreference = 'Stop'
$py = '.\.venv-supertonic\Scripts\python.exe'
$n = 'projects\rag-concepts-longform\narration'
foreach ($p in 'part1','part2','part3','part4') {
  if (Test-Path "$n\$p\narration.wav") { Write-Host "$p 이미 합성됨 - 건너뜀"; continue }
  & $py scripts\typecast_compose.py synth "$n\$p"
  if ($LASTEXITCODE -ne 0) { Write-Host "$p 합성 실패 - 이후 단계 생략. 에이전트에게 알려 주세요."; exit 1 }
}
& $py scripts\typecast_compose.py concat $n "$n\part1" "$n\part2" "$n\part3" "$n\part4"
if ($LASTEXITCODE -ne 0) { Write-Host '이어 붙이기 실패 - 에이전트에게 알려 주세요'; exit 1 }
& $py scripts\transcribe_narration.py "$n\narration.wav" "$n\source.txt" "$n\local-short-window-v1"
if ($LASTEXITCODE -ne 0) { Write-Host '정렬 실패 - 합성 음성은 받았습니다. 에이전트에게 알려 주세요(단어 시각 수동 매핑)'; exit 1 }
& $py scripts\balance_narration_phrases.py "$n\narration.wav" "$n\local-short-window-v1\sentence-boundaries.json" "$n\local-short-window-v1\transcription.json" "$n\local-short-window-v1\narration_balanced.wav" --mode short-window
Write-Host "완료: $n\local-short-window-v1\narration_balanced.wav"
