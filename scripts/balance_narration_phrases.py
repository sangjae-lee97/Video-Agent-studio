"""Relative phrase-level upward gain from the original WAV; no normalization.

Inputs are source-matched ASR words and sentence estimates. Decisions and skips
are recorded; recognition/VAD are evidence, not a guarantee of breath detection.
"""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile

import numpy as np
import soundfile as sf

SETTINGS = {'sentence_edge_seconds': .2, 'phrase_target_seconds': 1.5,
            'phrase_max_seconds': 2.8, 'neighbor_radius_seconds': 8.,
            'reference_percentile': 65, 'difference_allowance_db': 1.,
            'correction_fraction': .8, 'maximum_gain_db': 3., 'minimum_gain_db': .5,
            'speech_probability': .6, 'ambiguous_probability': .2,
            'noise_floor_below_speech_p90_db': 30., 'phrase_fade_seconds': .2,
            'speech_island_fade_seconds': .04, 'changed_sample_ceiling_dbfs': -1.}

# Experimental defaults are shared by every input, never selected by transcript/time.
LOCAL_SETTINGS = {'measurement_seconds': .2, 'gain_smoothing_seconds': .2,
                  'reference_exclusion_seconds': .3}


def short_window_gain(power, voiced, times):
    """Track short speech changes against source-only surrounding speech."""
    width = max(1, round(LOCAL_SETTINGS['measurement_seconds'] / .02))
    kernel = np.ones(width)
    count = np.convolve(voiced.astype(float), kernel, 'same')
    weighted = np.convolve(power * voiced, kernel, 'same')
    measured = 10 * np.log10(np.maximum(weighted / np.maximum(count, 1), 1e-20))
    valid = voiced & (count >= width / 2)
    reference = measured.copy()
    supported = np.zeros(len(times), bool)
    for i, t in enumerate(times):
        distance = np.abs(times - t)
        neighbors = valid & (distance > LOCAL_SETTINGS['reference_exclusion_seconds']) & (distance <= SETTINGS['neighbor_radius_seconds'])
        if neighbors.sum() >= 25:
            reference[i] = np.percentile(measured[neighbors], SETTINGS['reference_percentile'])
            supported[i] = True
    wanted = np.clip((reference - measured - SETTINGS['difference_allowance_db']) * SETTINGS['correction_fraction'], 0, SETTINGS['maximum_gain_db'])
    wanted[~(valid & supported)] = 0
    smoothing = np.hanning(max(3, round(LOCAL_SETTINGS['gain_smoothing_seconds'] / .02) | 1))
    gain = np.convolve(wanted, smoothing / smoothing.sum(), 'same')
    # Do not turn up an already sufficiently loud window because its neighbor is quiet.
    gain[~(valid & supported) | (measured >= reference - SETTINGS['difference_allowance_db'])] = 0
    return gain, measured, reference, supported


def spans(mask):
    edges = np.diff(np.r_[False, mask, False].astype(int))
    return zip(np.flatnonzero(edges == 1), np.flatnonzero(edges == -1))


def groups(sentences, segments):
    if len(sentences) != len(segments):
        raise ValueError('Sentence/ASR segment mapping must be reviewed first')
    phrases = []
    for sentence, segment in zip(sentences, segments):
        pending, rows = [], []
        for word in segment['words']:
            if not (sentence['start'] - .4 <= word['start'] < word['end'] <= sentence['end'] + .4):
                raise ValueError('Word timestamp outside mapped sentence')
            if pending and word['end'] - pending[0]['start'] > SETTINGS['phrase_max_seconds']:
                rows.append(pending)
                pending = []
            pending.append(word)
            if len(pending) >= 2 and word['end'] - pending[0]['start'] >= SETTINGS['phrase_target_seconds']:
                rows.append(pending)
                pending = []
        if pending:
            if rows and pending[-1]['end'] - pending[0]['start'] < .65:
                rows[-1].extend(pending)
            else:
                rows.append(pending)
        for row in rows:
            phrases.append({'sentence_id': sentence['id'], 'start': row[0]['start'],
                            'end': row[-1]['end'], 'recognized_text': ''.join(w['text'] for w in row).strip(),
                            'recognition_confidence': float(np.mean([w.get('probability', 0) for w in row]))})
    return phrases


def process(pcm, sr, sentences, segments, probabilities, mode='phrase'):
    if mode not in ('phrase', 'short-window'):
        raise ValueError('Unknown gain mode')
    if pcm.ndim != 1 or pcm.dtype != np.int16:
        raise ValueError('Expected mono PCM16')
    duration = len(pcm) / sr
    previous = 0.
    for s in sentences:
        if not (previous <= s['start'] < s['end'] <= duration + .001):
            raise ValueError('Invalid sentence boundaries')
        previous = s['end']
    if len(probabilities) * .032 < duration - .032 or not np.isfinite(probabilities).all():
        raise ValueError('VAD length/values do not match audio')
    audio = pcm.astype(float) / 32768
    hop = round(.02 * sr)
    power = np.mean(audio[:len(audio) // hop * hop].reshape(-1, hop) ** 2, axis=1)
    times = (np.arange(len(power)) + .5) * hop / sr
    probability = probabilities[np.minimum((times / .032).astype(int), len(probabilities) - 1)]
    levels = 10 * np.log10(np.maximum(power, 1e-20))
    speech = probability >= SETTINGS['speech_probability']
    if np.sum(speech) < 25:
        raise ValueError('Too little confident speech; manual review needed')
    noise_floor = float(np.percentile(levels[speech], 90) - SETTINGS['noise_floor_below_speech_p90_db'])
    voiced = speech & (levels > noise_floor)
    phrases = groups(sentences, segments)
    for p in phrases:
        selection = (times >= p['start']) & (times < p['end']) & voiced
        p['measured_speech_seconds'] = round(float(np.sum(selection) * hop / sr), 3)
        p['before_speech_rms_dbfs'] = float(10 * np.log10(np.mean(power[selection]))) if selection.any() else None
    # Source-only local references: earlier gain decisions never feed later decisions.
    for p in phrases:
        center = (p['start'] + p['end']) / 2
        neighbors = [q['before_speech_rms_dbfs'] for q in phrases if q is not p
                     and q['before_speech_rms_dbfs'] is not None and q['measured_speech_seconds'] >= .2
                     and abs((q['start'] + q['end']) / 2 - center) <= SETTINGS['neighbor_radius_seconds']]
        p['gain_db'] = 0.
        if p['measured_speech_seconds'] < .2 or p['recognition_confidence'] < .6 or len(neighbors) < 2:
            p['decision'] = 'review_insufficient_speech_recognition_or_neighbors'
            continue
        reference = float(np.percentile(neighbors, SETTINGS['reference_percentile']))
        difference = reference - p['before_speech_rms_dbfs']
        p.update(reference_dbfs=reference, relative_deficit_db=difference)
        wanted = min(SETTINGS['maximum_gain_db'], max(0., (difference - SETTINGS['difference_allowance_db']) * SETTINGS['correction_fraction']))
        if wanted < SETTINGS['minimum_gain_db']:
            p['decision'] = 'keep_within_neighbor_range'
        else:
            p.update(gain_db=wanted, decision='boost_quieter_than_neighbors')
    # Exact sample masks, with no padding around low-VAD intervals.
    sample_times = np.arange(len(audio)) / sr
    sample_prob = probabilities[np.minimum((sample_times / .032).astype(int), len(probabilities) - 1)]
    frame_levels = levels[np.minimum((sample_times * sr / hop).astype(int), len(levels) - 1)]
    word_mask = np.zeros(len(audio), bool)
    edge_mask = np.zeros(len(audio), bool)
    for s, segment in zip(sentences, segments):
        edge_mask[round((s['start'] + SETTINGS['sentence_edge_seconds']) * sr):
                  max(0, round((s['end'] - SETTINGS['sentence_edge_seconds']) * sr))] = True
        for w in segment['words']:
            if mode == 'short-window' and w.get('probability', 0) < .6:
                continue
            word_mask[max(0, round(w['start'] * sr)):min(len(audio), round(w['end'] * sr))] = True
    allowed = (sample_prob >= SETTINGS['speech_probability']) & (frame_levels > noise_floor) & word_mask & edge_mask
    # Fade inside allowed islands, without extending the no-change mask.
    island_envelope = np.zeros(len(audio))
    for lo, hi in spans(allowed):
        fade = min(round(SETTINGS['speech_island_fade_seconds'] * sr), (hi - lo) // 2)
        if not fade:
            continue
        island_envelope[lo:hi] = 1
        ramp = .5 - .5 * np.cos(np.linspace(0, np.pi, fade))
        island_envelope[lo:lo + fade] = ramp
        island_envelope[hi - fade:hi] = ramp[::-1]
    gain_db = np.zeros(len(audio))
    for p in phrases:
        lo, hi = max(0, round(p['start'] * sr)), min(len(audio), round(p['end'] * sr))
        if not p['gain_db'] or hi <= lo:
            continue
        envelope = island_envelope[lo:hi].copy()
        fade = min(round(SETTINGS['phrase_fade_seconds'] * sr), (hi - lo) // 2)
        ramp = .5 - .5 * np.cos(np.linspace(0, np.pi, fade))
        envelope[:fade] *= ramp
        envelope[-fade:] *= ramp[::-1]
        active = envelope > 0
        if not active.any():
            p.update(gain_db=0., decision='review_no_eligible_samples')
            continue
        peak = np.max(np.abs(audio[lo:hi][active]))
        headroom = 20 * np.log10(10 ** (SETTINGS['changed_sample_ceiling_dbfs'] / 20) / max(peak, 1e-12))
        p['gain_db'] = max(0., min(p['gain_db'], headroom))
        if p['gain_db'] < SETTINGS['minimum_gain_db']:
            p.update(gain_db=0., decision='keep_insufficient_peak_headroom')
        gain_db[lo:hi] = np.maximum(gain_db[lo:hi], p['gain_db'] * envelope)
    window_report = None
    if mode == 'short-window':
        frame_gain, measured, reference, supported = short_window_gain(power, voiced, times)
        gain_db = np.interp(sample_times, times, frame_gain) * island_envelope
        # Reserve headroom across neighboring frames before interpolation; never clip.
        peaks = np.max(np.abs(audio[:len(power) * hop].reshape(-1, hop)), axis=1)
        peaks = np.maximum.reduce([np.r_[peaks[0], peaks[:-1]], peaks, np.r_[peaks[1:], peaks[-1]]])
        headroom = np.maximum(0, SETTINGS['changed_sample_ceiling_dbfs'] - 20 * np.log10(np.maximum(peaks, 1e-12)))
        sample_frames = np.minimum((sample_times * sr / hop).astype(int), len(power) - 1)
        gain_db = np.minimum(gain_db, headroom[sample_frames])
        window_report = [{'time': round(float(t), 3), 'speech_probability': float(probability[i]),
                          'speech_rms_dbfs': float(measured[i]), 'reference_dbfs': float(reference[i]),
                          'reference_supported': bool(supported[i]), 'requested_gain_db': float(frame_gain[i]),
                          'applied_mean_gain_db': float(np.mean(gain_db[i * hop:(i + 1) * hop]))}
                         for i, t in enumerate(times)]
        for p in phrases:
            lo, hi = max(0, round(p['start'] * sr)), min(len(audio), round(p['end'] * sr))
            p['gain_db'] = float(np.max(gain_db[lo:hi])) if hi > lo else 0.
            p['decision'] = 'short_window_boost' if p['gain_db'] else 'keep_or_review_short_window'
            # Phrase averages are diagnostic only in this mode, not the gain decision.
            p.pop('reference_dbfs', None)
            p.pop('relative_deficit_db', None)
    changed = gain_db > 0
    output = pcm.copy()
    output[changed] = np.rint(audio[changed] * 10 ** (gain_db[changed] / 20) * 32768).astype(np.int16)
    assert not np.any(changed & ~allowed)
    assert np.array_equal(output[~changed], pcm[~changed])
    assert not np.any(np.abs(output[changed].astype(np.int32)) >= 32767)
    out_power = np.mean((output[:len(power) * hop].astype(float) / 32768).reshape(-1, hop) ** 2, axis=1)
    for p in phrases:
        selection = (times >= p['start']) & (times < p['end']) & voiced
        p['after_speech_rms_dbfs'] = float(10 * np.log10(np.mean(out_power[selection]))) if selection.any() else None
        if p['before_speech_rms_dbfs'] is not None:
            p['effective_rms_change_db'] = p['after_speech_rms_dbfs'] - p['before_speech_rms_dbfs']
    ambiguous = (sample_prob >= .2) & (sample_prob < .6) & word_mask
    report = {'settings': SETTINGS, 'adaptive_energy_floor_dbfs': noise_floor, 'phrases': phrases,
              'boosted_phrase_count': int(sum(p['gain_db'] > 0 for p in phrases)),
              'changed_seconds': int(changed.sum()) / sr,
              'ambiguous_word_overlap_seconds_unchanged': int(ambiguous.sum()) / sr,
              'protected_sentence_edges_and_low_confidence_samples_unchanged': True,
              'unmodified_pcm_identical': True, 'new_clipped_samples_in_modified_regions': 0,
              'limitations': 'ASR/VAD estimates, not verified breath labels; no listening verification. Original peaks outside gain regions are preserved.'}
    if window_report is not None:
        report.update(local_settings=LOCAL_SETTINGS, windows=window_report,
                      quality_status='needs_listening_review',
                      breath_classification_verified=False)
    return output, report


def render(source, boundaries, transcription, target, mode='phrase'):
    source, boundaries, transcription, target = map(Path, (source, boundaries, transcription, target))
    report_path = target.with_suffix('.report.json')
    if target.exists() or report_path.exists() or source.resolve() == target.resolve():
        raise ValueError('Use a new output path')
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    boundary_data, word_data = [json.loads(p.read_text(encoding='utf-8')) for p in (boundaries, transcription)]
    if any(d['source_sha256'] != digest for d in (boundary_data, word_data)):
        raise ValueError('Timings belong to a different source')
    if sf.info(source).subtype != 'PCM_16':
        raise ValueError('Expected original PCM16 WAV')
    pcm, sr = sf.read(source, dtype='int16')
    from protect_speech_gaps import probabilities, MODEL_HASH
    output, report = process(pcm, sr, boundary_data['sentences'], word_data['segments'], probabilities(source), mode=mode)
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=target.parent) as temporary:
        rendered = Path(temporary) / 'audio.wav'
        sf.write(rendered, output, sr, subtype='PCM_16')
        saved, rate = sf.read(rendered, dtype='int16')
        assert rate == sr and np.array_equal(output, saved)
        assert hashlib.sha256(source.read_bytes()).hexdigest() == digest
        report.update(source=str(source.resolve()), source_sha256=digest, output=str(target.resolve()),
                      algorithm='local_short_window_v1' if mode == 'short-window' else 'relative_phrase_v1', vad_model_sha256=MODEL_HASH,
                      output_sha256=hashlib.sha256(rendered.read_bytes()).hexdigest(),
                      duration_seconds=len(pcm) / sr, boundaries=str(boundaries.resolve()),
                      transcription=str(transcription.resolve()), new_api_requests=0,
                      global_normalization=False, compression=False, breath_attenuation=False,
                      listening_review='pending', automation_status='candidate_not_approved')
        encoded = json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False)
        rendered.rename(target)
        report_path.write_text(encoded, encoding='utf-8')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('source', 'boundaries', 'transcription', 'output'):
        parser.add_argument(name)
    parser.add_argument('--mode', choices=['phrase', 'short-window'], default='phrase')
    args = parser.parse_args()
    report = render(args.source, args.boundaries, args.transcription, args.output, mode=args.mode)
    print(json.dumps({k: report[k] for k in ('output', 'boosted_phrase_count', 'changed_seconds', 'duration_seconds', 'listening_review')}, ensure_ascii=False, indent=2))
