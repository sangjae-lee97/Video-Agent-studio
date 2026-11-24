"""Typecast 내레이션 공통 도구 (모든 편에서 사용).

1) build  — 편의 대본 구간 JSON에서 합성 요청·대본·실행용 PowerShell을 만든다(네트워크 사용 안 함).
   python scripts/typecast_compose.py build projects/<편명>/narration/segments.json
2) synth  — Typecast Compose API에 1회 요청해 narration.wav를 만든다(재시도 없음, 중복 실행 거부).
   python scripts/typecast_compose.py synth projects/<편명>/narration

segments.json 형식 (role은 docs/narration-defaults.json의 emotion_by_role 키):
[
  {"role": "opening_question", "focus": "화자에게 읽히지 않는 의도 메모", "lines": ["첫 문장?"]},
  {"role": "explanation", "focus": "...", "lines": ["둘째 문장.", "셋째 문장."]}
]
속도·화자·모델·감정 강도는 docs/narration-defaults.json에서 읽는다. 키는 저장소 루트 .env의 TYPECAST_API_KEY.
에이전트 환경에서 api.typecast.ai가 막혀 있으면 build가 만든 run_narration.ps1을 사용자가 PowerShell에서 실행한다.
3) concat — Compose 한도(2,000자·50구간)를 넘는 긴 원고: 장 경계로 나눈 part 폴더를 각각 build·synth한 뒤
   하나의 narration.wav·source.txt로 잇는다(구간 휴지와 같은 segment_pause_seconds 무음, 재합성 없음).
   python scripts/typecast_compose.py concat projects/<편명>/narration projects/<편명>/narration/part1 ...part2 ...
"""
from array import array
import argparse
import hashlib
import io
import json
from pathlib import Path
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import wave

ROOT = Path(__file__).resolve().parents[1]
API = 'https://api.typecast.ai/v1/text-to-speech/compose'


def build(seg_file: Path) -> None:
    out = seg_file.resolve().parent
    D = json.loads((ROOT / 'docs/narration-defaults.json').read_text(encoding='utf-8'))
    E = D['emotion_by_role']
    SEG = json.loads(seg_file.read_text(encoding='utf-8'))
    lines = [l for s in SEG for l in s['lines']]
    segments, plan, n = [], [], 0
    for s in SEG:
        if s['role'] not in E:
            sys.exit(f"알 수 없는 role: {s['role']} (가능: {', '.join(E)})")
        prompt = dict(E[s['role']])
        if prompt['emotion_type'] == 'smart':  # 실제 앞뒤 문장을 문맥으로 전달
            prompt = {'emotion_type': 'smart', 'previous_text': '\n'.join(lines[max(0, n-2):n]),
                      'next_text': '\n'.join(lines[n+len(s['lines']):n+len(s['lines'])+2])}
        plan.append({'source_lines': [n+1, n+len(s['lines'])], 'role': s['role'],
                     'intended_focus_not_spoken_instruction': s.get('focus', ''), 'prompt': prompt})
        if segments:
            segments.append({'type': 'pause', 'duration_seconds': D['segment_pause_seconds']})
        segments.append({'type': 'tts', 'voice_id': D['voice_id'], 'model': D['model'], 'language': D['language'],
                         'text': '\n'.join(s['lines']), 'prompt': prompt, 'output': D['output']})
        n += len(s['lines'])
    chars = sum(len(l) for l in lines)
    if chars > 2000 or len(segments) > 50:
        sys.exit(f'Compose 한도 초과: {chars}자(최대 2000), {len(segments)}구간(최대 50). 원고를 나눠 주세요.')
    payload = json.dumps({'segments': segments}, ensure_ascii=False, indent=2).encode('utf-8')
    digest = hashlib.sha256(payload).hexdigest()
    (out / 'source.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    (out / 'emotion-plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
    (out / 'request.json').write_bytes(payload)
    md = ['# 낭독 대본', '', '낭독용 원문(발음 표기·강조 부호 보존). 화면 자막은 별도 검증.', '']
    md += [f'{i}. {l}' for i, l in enumerate(lines, 1)]
    md += ['', f"- 줄 {len(lines)}, 구간 {len(SEG)}, {chars}자(=Typecast 약 {chars}크레딧), 속도 {D['output'].get('audio_tempo', 1.0)}배, 요청 sha256 `{digest}`"]
    (out / 'script.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
    rel = out.relative_to(ROOT).as_posix().replace('/', '\\')
    ps1 = f"""# 저장소 루트(Video-Agent-studio)에서 실행: .\\{rel}\\run_narration.ps1
# Typecast Compose 1회 합성(재시도 없음) -> 로컬 Whisper 정렬 -> short-window 음량 보정
$ErrorActionPreference = 'Stop'
$py = '.\\.venv-supertonic\\Scripts\\python.exe'
$n = '{rel}'
& $py scripts\\typecast_compose.py synth $n
if ($LASTEXITCODE -ne 0) {{ Write-Host 'Typecast 합성 실패 - 이후 단계 생략'; exit 1 }}
& $py scripts\\transcribe_narration.py "$n\\narration.wav" "$n\\source.txt" "$n\\local-short-window-v1"
if ($LASTEXITCODE -ne 0) {{ Write-Host '정렬 실패 - 에이전트에게 알려 주세요(단어 시각 수동 매핑)'; exit 1 }}
& $py scripts\\balance_narration_phrases.py "$n\\narration.wav" "$n\\local-short-window-v1\\sentence-boundaries.json" "$n\\local-short-window-v1\\transcription.json" "$n\\local-short-window-v1\\narration_balanced.wav" --mode short-window
Write-Host "완료: $n\\local-short-window-v1\\narration_balanced.wav"
"""
    (out / 'run_narration.ps1').write_text(ps1, encoding='utf-8-sig')
    print(json.dumps({'lines': len(lines), 'segments': len(SEG), 'chars': chars, 'request_sha256': digest,
                      'run': f'.\\{rel}\\run_narration.ps1'}, ensure_ascii=False, indent=2))


def synth(out: Path) -> None:
    out = out.resolve()
    if (out / 'narration.wav').exists() or (out / 'request-started.json').exists():
        sys.exit('이미 합성했거나 시도한 폴더입니다. 중복 과금을 막기 위해 거부합니다. 다시 하려면 새 폴더에서 build하세요.')
    key = ''
    env = ROOT / '.env'
    if env.exists():
        for line in env.read_text(encoding='utf-8-sig').splitlines():
            name, sep, value = line.partition('=')
            if sep and name.strip() == 'TYPECAST_API_KEY':
                key = value.strip().strip('"\'')
    if not key:
        sys.exit('.env의 TYPECAST_API_KEY가 비어 있습니다.')
    payload = (out / 'request.json').read_bytes()
    (out / 'request-started.json').write_text(json.dumps({'request_sha256': hashlib.sha256(payload).hexdigest()}), encoding='utf-8')
    req = Request(API, data=payload, method='POST',
                  headers={'X-API-KEY': key, 'Content-Type': 'application/json', 'Accept': 'audio/wav'})
    start = time.perf_counter()
    try:
        with urlopen(req, timeout=180) as r:
            data = r.read()
    except HTTPError as e:
        sys.exit(f'Typecast HTTP {e.code}; 재시도하지 않음.')
    except (URLError, TimeoutError):
        sys.exit('네트워크 실패 또는 시간 초과; 재시도하지 않음. (에이전트 환경이면 api.typecast.ai 차단 가능성 — run_narration.ps1을 사용자 PC에서 실행)')
    (out / 'narration.wav').write_bytes(data)
    with wave.open(io.BytesIO(data), 'rb') as w:
        frames, sr = w.getnframes(), w.getframerate()
        pcm = array('h', w.readframes(frames))
    if sys.byteorder != 'little':
        pcm.byteswap()
    peak = max(abs(x) for x in pcm)
    clipped = sum(x <= -32768 or x >= 32767 for x in pcm)
    req_json = json.loads(payload)
    tts = [s for s in req_json['segments'] if s['type'] == 'tts']
    report = {'duration_seconds': round(frames / sr, 3), 'request_seconds': round(time.perf_counter() - start, 3),
              'sample_rate': sr, 'tempo': tts[0]['output'].get('audio_tempo', 1.0), 'tts_segments': len(tts),
              'chars': sum(len(s['text'].replace('\n', '')) for s in tts), 'peak_pcm16': peak, 'clipped_samples': clipped,
              'sha256': hashlib.sha256(data).hexdigest(), 'synthesis_requests': 1, 'listening_review': 'pending'}
    (out / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


def concat(out: Path, parts: list) -> None:
    out = out.resolve()
    if (out / 'narration.wav').exists():
        sys.exit('이미 narration.wav가 있습니다. 덮어쓰지 않습니다.')
    D = json.loads((ROOT / 'docs/narration-defaults.json').read_text(encoding='utf-8'))
    pause = D['segment_pause_seconds']
    params, chunks, lines, info, t = None, [], [], [], 0.0
    for i, p in enumerate(parts):
        p = Path(p).resolve()
        with wave.open(str(p / 'narration.wav'), 'rb') as w:
            pr = (w.getnchannels(), w.getsampwidth(), w.getframerate())
            if params and pr != params:
                sys.exit(f'{p.name}: 형식 불일치 {pr} != {params}')
            params = pr
            data = w.readframes(w.getnframes())
            dur = w.getnframes() / pr[2]
        if i:
            chunks.append(b'\x00' * (round(pause * pr[2]) * pr[0] * pr[1]))
            t += pause
        part_lines = (p / 'source.txt').read_text(encoding='utf-8').splitlines()
        info.append({'part': p.name, 'start_seconds': round(t, 3), 'duration_seconds': round(dur, 3),
                     'first_line': len(lines) + 1, 'last_line': len(lines) + len(part_lines),
                     'sha256': hashlib.sha256((p / 'narration.wav').read_bytes()).hexdigest()})
        lines += part_lines
        chunks.append(data)
        t += dur
    out.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out / 'narration.wav'), 'wb') as w:
        w.setnchannels(params[0]); w.setsampwidth(params[1]); w.setframerate(params[2])
        w.writeframes(b''.join(chunks))
    (out / 'source.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    report = {'duration_seconds': round(t, 3), 'sample_rate': params[2], 'parts': info, 'join_pause_seconds': pause,
              'chars': sum(len(l) for l in lines), 'synthesis_requests': len(parts),
              'sha256': hashlib.sha256((out / 'narration.wav').read_bytes()).hexdigest(), 'listening_review': 'pending'}
    (out / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    b = sub.add_parser('build'); b.add_argument('segments_json')
    s = sub.add_parser('synth'); s.add_argument('narration_dir')
    c = sub.add_parser('concat'); c.add_argument('out_dir'); c.add_argument('part_dirs', nargs='+')
    a = ap.parse_args()
    if a.cmd == 'build':
        build(Path(a.segments_json))
    elif a.cmd == 'synth':
        synth(Path(a.narration_dir))
    else:
        concat(Path(a.out_dir), a.part_dirs)
