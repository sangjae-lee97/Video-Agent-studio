"""Targeted gain correction for the reviewed Piljae 1.0x file; no synthesis."""
import hashlib
import json
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'outputs/typecast-piljae-pfa-full-1.0x/narration.wav'
OUT = SOURCE.parent / 'volume-adjustment'
REGIONS = [(20.5, 26.8, 1.5), (50.0, 55.4, 3.0)]
FADE_SECONDS = 0.35


def active_rms_dbfs(audio, sr):
    hop = round(0.02 * sr)
    frames = audio[:len(audio) // hop * hop].reshape(-1, hop)
    power = np.mean(frames * frames, axis=1)
    active = power > 10 ** (-40 / 10)
    return round(float(10 * np.log10(np.mean(power[active]))), 3)


def main():
    original_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert original_hash == '3f62ff17d0a0c11d9607638605f41cd6d6e7b39755982407d7df9ab0112b02de', 'Unexpected source'
    pcm, sr = sf.read(SOURCE, dtype='int16')
    assert pcm.ndim == 1 and sr == 44100
    audio = pcm.astype(np.float64) / 32768
    gain_db = np.zeros(len(audio))
    changes = []
    for start, end, gain in REGIONS:
        first, last = round(start * sr), round(end * sr)
        fade = round(FADE_SECONDS * sr)
        envelope = np.ones(last - first)
        ramp = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, fade))
        envelope[:fade] = ramp
        envelope[-fade:] = ramp[::-1]
        gain_db[first:last] = envelope * gain
        changes.append({'start_seconds': start, 'end_seconds': end, 'max_gain_db': gain,
                        'before_active_rms_dbfs': active_rms_dbfs(audio[first:last], sr)})
    result = audio * 10 ** (gain_db / 20)
    changed = gain_db > 0
    assert np.isfinite(result).all() and np.max(np.abs(result[changed])) < 1
    output_pcm = pcm.copy()
    output_pcm[changed] = np.rint(result[changed] * 32768).astype(np.int16)
    assert not np.any((output_pcm == -32768) | (output_pcm == 32767))
    assert np.array_equal(pcm[~changed], output_pcm[~changed])
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / 'narration_volume_adjusted.wav'
    sf.write(target, output_pcm, sr, subtype='PCM_16')
    saved, saved_sr = sf.read(target, dtype='int16')
    assert saved_sr == sr and np.array_equal(saved, output_pcm)
    for row in changes:
        start, end = round(row['start_seconds'] * sr), round(row['end_seconds'] * sr)
        row['after_active_rms_dbfs'] = active_rms_dbfs(saved[start:end].astype(np.float64) / 32768, sr)
    # Short comparison: same 46–59 second excerpt before and after, separated by one second.
    excerpt_start, excerpt_end = 46 * sr, 59 * sr
    comparison = np.concatenate([pcm[excerpt_start:excerpt_end], np.zeros(sr, dtype=np.int16), saved[excerpt_start:excerpt_end]])
    sf.write(OUT / 'compare_46s-59s_original_then_adjusted.wav', comparison, sr, subtype='PCM_16')
    report = {'source': str(SOURCE), 'source_sha256': original_hash, 'output': str(target),
              'duration_seconds': round(len(pcm) / sr, 3), 'regions': changes,
              'boundary_fade_seconds': FADE_SECONDS, 'sample_rate': sr,
              'outside_regions_bit_identical': True, 'length_preserved': True,
              'tempo_pitch_emotion_unchanged': True, 'new_api_requests': 0,
              'clipped_samples': 0, 'analysis': '20 ms RMS, gate -40 dBFS; numerical assessment, not listening verification',
              'listening_review': 'pending', 'output_sha256': hashlib.sha256(target.read_bytes()).hexdigest()}
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == original_hash
    encoded = json.dumps(report, ensure_ascii=False, indent=2)
    (OUT / 'report.json').write_text(encoded, encoding='utf-8')
    (ROOT / 'docs/piljae-volume-adjustment-results.json').write_text(encoded, encoding='utf-8')
    print(encoded)


if __name__ == '__main__':
    main()
