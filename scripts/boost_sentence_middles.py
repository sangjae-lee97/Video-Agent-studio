"""Legacy fixed-threshold experiment; current candidate is balance_narration_phrases.py."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import soundfile as sf


def boost(pcm, sr, sentences, speech_scores):
    audio = pcm.astype(np.float64) / 32768
    if audio.ndim != 1:
        raise ValueError('This first implementation accepts mono PCM16 narration')
    # Protect a brief edge only; first/last word spans must not expand this mask.
    allowed = np.zeros(len(audio), bool)
    previous_end = 0
    for sentence in sentences:
        start, end = sentence['start'], sentence['end']
        if not (np.isfinite(start) and np.isfinite(end) and previous_end <= start < end <= len(audio) / sr + .001):
            raise ValueError('Invalid or overlapping sentence boundaries')
        interior_start = start + .2
        interior_end = end - .2
        first, last = round(interior_start * sr), round(interior_end * sr)
        if last > first:
            allowed[first:last] = True
        previous_end = end
    # Conservatively protect every VAD gap and 0.16s on either side, even inside sentences.
    for i in np.flatnonzero(speech_scores < .2):
        allowed[max(0, round((i * .032 - .16) * sr)):
                min(len(audio), round(((i + 1) * .032 + .16) * sr))] = False
    hop = round(sr * .1)
    frame_count = len(audio) // hop
    power = np.mean(audio[:frame_count * hop].reshape(-1, hop) ** 2, axis=1)
    # Measure 0.3s, ignoring near-silent blocks. Only the changed block must be allowed:
    # requiring the full measurement window added another hidden protection margin.
    active = power > 10 ** (-40 / 10)
    average = np.convolve(power * active, np.ones(3), 'same') / np.maximum(
        np.convolve(active.astype(float), np.ones(3), 'same'), 1)
    levels = 10 * np.log10(np.maximum(average, 1e-20))
    candidates = np.zeros(frame_count, bool)
    for i in range(1, frame_count - 1):
        candidates[i] = active[i] and levels[i] < -22 and allowed[i * hop:(i + 1) * hop].all()
    boundaries = np.diff(np.r_[False, candidates, False].astype(int))
    gain_db = np.zeros(len(audio))
    regions = []
    for start, end in zip(np.flatnonzero(boundaries == 1), np.flatnonzero(boundaries == -1)):
        if end - start < 2:
            continue
        first, last = start * hop, end * hop
        peak = np.max(np.abs(audio[first:last]))
        ceiling = 20 * np.log10(10 ** (-1 / 20) / max(peak, 1e-12))
        gain = min(3., -20 - float(np.median(levels[start:end])), ceiling)
        if gain < 1:
            continue
        envelope = np.ones(last - first)
        fade = round(.08 * sr)
        ramp = .5 - .5 * np.cos(np.linspace(0, np.pi, fade))
        envelope[:fade], envelope[-fade:] = ramp, ramp[::-1]
        gain_db[first:last] = gain * envelope
        regions.append({'start': first / sr, 'end': last / sr, 'max_gain_db': round(gain, 3),
                        'before_local_rms_dbfs': round(float(np.median(levels[start:end])), 3)})
    changed = gain_db > 0
    assert not np.any(changed & ~allowed)
    output = pcm.copy()
    output[changed] = np.rint(audio[changed] * 10 ** (gain_db[changed] / 20) * 32768).astype(np.int16)
    assert np.array_equal(output[~changed], pcm[~changed])
    assert not np.any(np.abs(output[changed].astype(np.int32)) >= 32767)
    return output, regions, int(np.sum(changed))


def render(source, boundaries, output):
    source, boundaries, output = map(Path, (source, boundaries, output))
    report_path = output.with_suffix('.report.json')
    if output.exists() or report_path.exists() or source.resolve() == output.resolve():
        raise ValueError('Use a new output path; originals are never overwritten')
    data = json.loads(boundaries.read_text(encoding='utf-8'))
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    if data['source_sha256'] != source_hash:
        raise ValueError('Sentence timing was derived from a different audio file')
    if sf.info(source).subtype != 'PCM_16':
        raise ValueError('Expected PCM16 WAV to preserve unaffected samples exactly')
    pcm, sr = sf.read(source, dtype='int16')
    from protect_speech_gaps import probabilities
    result, regions, changed = boost(pcm, sr, data['sentences'], probabilities(source))
    output.parent.mkdir(parents=True, exist_ok=True)
    sf.write(output, result, sr, subtype='PCM_16')
    saved, rate = sf.read(output, dtype='int16')
    assert rate == sr and np.array_equal(saved, result)
    assert hashlib.sha256(source.read_bytes()).hexdigest() == source_hash
    report = {'source': str(source.resolve()), 'source_sha256': source_hash,
              'output': str(output.resolve()), 'output_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
              'boundaries': str(boundaries.resolve()), 'boundary_status': data['status'],
              'duration_seconds': len(pcm) / sr, 'sentence_edge_protection_seconds': .2,
              'first_last_word_protection': False, 'measurement_window_seconds': .3,
              'minimum_quiet_run_seconds': .2, 'gain_fade_seconds': .08,
              'vad_gap_protection_seconds': .16, 'quiet_threshold_dbfs': -22,
              'maximum_boost_db': 3, 'regions': regions, 'changed_seconds': changed / sr,
              'all_other_pcm_identical_to_original': True, 'new_clipping_in_modified_regions': 0,
              'global_normalization': False, 'compression': False, 'breath_attenuation': False,
              'new_api_requests': 0, 'listening_review': 'pending'}
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    return report


def self_test():
    sr = 16000
    t = np.arange(sr * 6) / sr
    a = .2 * np.sin(2 * np.pi * 150 * t)
    a[2 * sr:4 * sr] *= .15
    pcm = np.rint(a * 32768).astype(np.int16)
    output, regions, changed = boost(pcm, sr, [{'start': 0., 'end': 6.}], np.ones(188))
    assert regions and changed and np.array_equal(output[:sr], pcm[:sr])
    assert np.array_equal(output[-sr:], pcm[-sr:])
    assert np.mean(output[3 * sr:round(3.2 * sr)].astype(float) ** 2) > np.mean(pcm[3 * sr:round(3.2 * sr)].astype(float) ** 2)
    output, regions, _ = boost(pcm, sr, [{'start': 0., 'end': 6.}], np.zeros(188))
    assert not regions and np.array_equal(pcm, output)
    quiet = np.rint(.03 * np.sin(2 * np.pi * 150 * t) * 32768).astype(np.int16)
    output, regions, _ = boost(quiet, sr, [{'start': 0., 'end': 6., 'first_word_end': 2., 'last_word_start': 4.}], np.ones(188))
    assert np.array_equal(output[:round(.2 * sr)], quiet[:round(.2 * sr)])
    assert np.array_equal(output[-round(.2 * sr):], quiet[-round(.2 * sr):])
    assert not np.array_equal(output[sr // 2:sr], quiet[sr // 2:sr])
    assert not np.array_equal(output[5 * sr:round(5.5 * sr)], quiet[5 * sr:round(5.5 * sr)])
    print('Passed: 0.2s edges unchanged, no whole-word exclusion, quiet speech boosted, no boosting non-speech')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', nargs='?')
    parser.add_argument('boundaries', nargs='?')
    parser.add_argument('output', nargs='?')
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--legacy-experiment', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        self_test()
    elif all((args.source, args.boundaries, args.output)):
        if not args.legacy_experiment:
            parser.error('Fixed-threshold processing is superseded. Use balance_narration_phrases.py for the current candidate.')
        print(json.dumps(render(args.source, args.boundaries, args.output), ensure_ascii=False, indent=2))
    else:
        parser.error('Provide original.wav boundaries.json new.wav, or --self-test')
