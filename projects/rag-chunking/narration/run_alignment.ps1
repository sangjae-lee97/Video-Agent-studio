# 합성은 끝났으므로 정렬·보정만 실행 (Typecast 요청 없음)
$py = '.\.venv-supertonic\Scripts\python.exe'
$n = 'projects\rag-chunking\narration'
& $py scripts\transcribe_narration.py "$n\narration.wav" "$n\source.txt" "$n\local-short-window-v1"
if ($LASTEXITCODE -ne 0) { Write-Host 'ASR 단계 실패 - 보정 생략'; exit 1 }
& $py scripts\balance_narration_phrases.py "$n\narration.wav" "$n\local-short-window-v1\sentence-boundaries.json" "$n\local-short-window-v1\transcription.json" "$n\local-short-window-v1\narration_balanced.wav" --mode short-window
