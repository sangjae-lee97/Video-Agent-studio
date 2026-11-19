"""One authorized compose request. Does not retry failures or print credentials."""
from array import array
import hashlib
import io
import json
from pathlib import Path
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import wave

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
if (OUT / 'narration.wav').exists() or (OUT / 'request-started.json').exists():
    sys.exit('Existing output or previous attempt found; refusing automatic duplicate synthesis.')
key = ''
for line in (ROOT / '.env').read_text(encoding='utf-8-sig').splitlines():
    name, sep, value = line.partition('=')
    if sep and name.strip() == 'TYPECAST_API_KEY':
        key = value.strip().strip('\"\'')
        break
if not key:
    sys.exit('TYPECAST_API_KEY is empty.')
payload = (OUT / 'request.json').read_bytes()
request = Request('https://api.typecast.ai/v1/text-to-speech/compose', data=payload,
                  headers={'X-API-KEY': key, 'Content-Type': 'application/json', 'Accept': 'audio/wav'}, method='POST')
(OUT / 'request-started.json').write_text(json.dumps({'request_sha256': hashlib.sha256(payload).hexdigest()}), encoding='utf-8')
start = time.perf_counter()
try:
    with urlopen(request, timeout=180) as response:
        data = response.read()
except HTTPError as error:
    sys.exit(f'Typecast HTTP {error.code}; not retried.')
except (URLError, TimeoutError):
    sys.exit('Network failure or timeout; not retried.')
elapsed = time.perf_counter() - start
(OUT / 'narration.wav').write_bytes(data)
with wave.open(io.BytesIO(data), 'rb') as wav:
    assert wav.getsampwidth() == 2 and wav.getnchannels() == 1
    frames, sr = wav.getnframes(), wav.getframerate()
    pcm = array('h', wav.readframes(frames))
    if sys.byteorder != 'little':
        pcm.byteswap()
    assert len(pcm) == frames and frames > sr
    peak = max(abs(x) for x in pcm)
    assert peak > 0
    clipping = sum(x <= -32768 or x >= 32767 for x in pcm)
    report = {'voice':'Piljae', 'model':'ssfm-v31', 'tempo':1.05, 'tts_segments':22,
              'emotion_plan':'emotion-plan.json', 'duration_seconds':round(frames/sr,3),
              'request_seconds':round(elapsed,3), 'sample_rate':sr, 'channels':1,
              'sample_width_bytes':2, 'peak_pcm16':peak, 'clipped_samples':clipping,
              'sha256':hashlib.sha256(data).hexdigest(), 'synthesis_requests':1,
              'source_lines':26, 'postprocessing_applied':False, 'emphasis_plan':'approved content-based roles (narration-defaults.json)', 'listening_review':'pending',
              'subtitles_generated':False, 'content_fact_check':'script checked against analysis.md'}
    report['requires_clipping_review'] = clipping > 0
(OUT / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
