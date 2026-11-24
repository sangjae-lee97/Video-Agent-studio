# 저장소 루트에서 실행: .\projects\rag-concepts-longform\narration\run_alignment.ps1
# 합성은 끝났음(재합성·크레딧 없음). 로컬 Whisper 정렬 -> short-window 보정만 다시 실행.
$ErrorActionPreference = 'Stop'
$py = '.\.venv-supertonic\Scripts\python.exe'
$n = 'projects\rag-concepts-longform\narration'
& $py scripts\transcribe_narration.py "$n\narration.wav" "$n\source.txt" "$n\local-short-window-v1"
if ($LASTEXITCODE -ne 0) { Write-Host '정렬 실패 - ASR 단어는 local-short-window-v1\asr-words.json에 저장됨. 에이전트에게 알려 주세요'; exit 1 }
& $py scripts\balance_narration_phrases.py "$n\narration.wav" "$n\local-short-window-v1\sentence-boundaries.json" "$n\local-short-window-v1\transcription.json" "$n\local-short-window-v1\narration_balanced.wav" --mode short-window
Write-Host "완료: $n\local-short-window-v1\narration_balanced.wav"
