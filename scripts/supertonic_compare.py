"""Generate five male voices at two native synthesis speeds, entirely offline."""
import hashlib
import json
import os
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[1]
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['HF_HOME'] = str(ROOT / '.cache' / 'huggingface')

import numpy as np
import soundfile as sf
from supertonic import TTS


def main():
    out = ROOT / 'outputs' / 'supertonic3-male-comparison'
    out.mkdir(parents=True, exist_ok=True)
    source = json.loads((ROOT / 'outputs/typecast-piljae-1.1x/request.json').read_text(encoding='utf-8'))['text']
    (out / 'source.txt').write_text(source, encoding='utf-8')
    started = time.perf_counter()
    tts = TTS(model='supertonic-3', model_dir=ROOT / 'models/supertonic-3', auto_download=False,
              intra_op_num_threads=4, inter_op_num_threads=1)
    report = {'model': 'supertonic-3', 'model_revision': 'aafc6e32416a594460b32413efc49d7fe4ce6d46',
              'load_seconds': round(time.perf_counter() - started, 3), 'language': 'ko',
              'text_characters': len(source), 'text_sha256': hashlib.sha256(source.encode()).hexdigest(),
              'steps': 8, 'seed': 42, 'cpu_threads': 4, 'chunk_limit': 120, 'chunk_silence_seconds': 0.3,
              'speed_method': 'native synthesis duration control; no audio time stretch',
              'listening_review': 'pending', 'samples': []}
    for voice in ('M1', 'M2', 'M3', 'M4', 'M5'):
        style = tts.get_voice_style(voice)
        pair = []
        for speed in (1.0, 1.1):
            np.random.seed(42)
            start = time.perf_counter()
            audio, _ = tts.synthesize(source, voice_style=style, lang='ko', speed=speed,
                                      total_steps=8, max_chunk_length=120, silence_duration=0.3)
            elapsed = time.perf_counter() - start
            audio = np.asarray(audio).reshape(-1)
            assert audio.size > tts.sample_rate and np.isfinite(audio).all(), 'Invalid audio'
            peak = float(np.max(np.abs(audio)))
            assert peak > 0.001, 'Silent output'
            # Preserve raw synthesis amplitude; fail instead of silently clipping or normalizing.
            assert peak < 1.0, f'Clipping risk in {voice} {speed}: {peak}'
            path = out / f'{voice}_{speed:.1f}x.wav'
            sf.write(path, audio, tts.sample_rate, subtype='PCM_16')
            saved, sr = sf.read(path, dtype='float32')
            assert sr == tts.sample_rate and len(saved) == len(audio)
            pair.append(saved)
            item = {'voice': voice, 'speed': speed, 'file': path.name,
                    'duration_seconds': round(len(saved) / sr, 3), 'generation_seconds': round(elapsed, 3),
                    'rtf': round(elapsed / (len(saved) / sr), 3), 'peak': round(peak, 5), 'sample_rate': sr}
            report['samples'].append(item)
            print(json.dumps(item), flush=True)
        assert len(pair[1]) < len(pair[0]), f'1.1x did not shorten {voice}'
        combined = np.concatenate([pair[0], np.zeros(tts.sample_rate, dtype=np.float32), pair[1]])
        pair_path = out / f'{voice}_compare_1.0_then_1.1.wav'
        sf.write(pair_path, combined, tts.sample_rate, subtype='PCM_16')
        assert sf.info(pair_path).frames == sum(map(len, pair)) + tts.sample_rate
    assert len(report['samples']) == 10
    encoded = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    (out / 'report.json').write_text(encoded, encoding='utf-8')
    (ROOT / 'docs/supertonic3-comparison-results.json').write_text(encoded, encoding='utf-8')
    print('COMPLETE: 10 samples and 5 comparison pairs', flush=True)


if __name__ == '__main__':
    main()
