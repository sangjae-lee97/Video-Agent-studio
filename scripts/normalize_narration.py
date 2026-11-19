"""Legacy experiment, superseded by boost_sentence_middles.py on 2026-11-19."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

import imageio_ffmpeg
import numpy as np
import soundfile as sf
from protect_speech_gaps import protect

LEVEL_FILTER = ('acompressor=threshold=0.1:ratio=3:attack=5:release=80:knee=2.8,'
                'dynaudnorm=f=100:g=5:p=0.85:m=6:r=0.18:t=0.01:b=1')
LOUD_FILTER = 'loudnorm=I=-16:TP=-2:LRA=5:print_format=json'


def ffmpeg(*args):
    result = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner',
                             '-nostdin', *map(str, args)], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr[-3000:])
    return result.stderr


def loudness(path):
    log = ffmpeg('-i', path, '-af', LOUD_FILTER, '-f', 'null', '-')
    measured = json.loads(re.findall(r'\{[^{}]+\}', log)[-1])
    return {k: float(measured['input_' + v]) for k, v in
            [('integrated_lufs', 'i'), ('true_peak_dbtp', 'tp'), ('lra_lu', 'lra')]}


def frame_power(audio, sr):
    hop = round(sr * .02)
    frames = audio[:len(audio) // hop * hop].reshape(-1, hop, audio.shape[1])
    return np.mean(frames ** 2, axis=(1, 2))


def speech_stats(audio, sr, source_mask):
    powers = frame_power(audio, sr)
    levels = []
    # Same source-derived mask for before/after: gain cannot change the test population.
    for i in range(0, len(powers) - 49, 25):
        mask = source_mask[i:i + 50]
        if mask.sum() >= 15:
            levels.append(10 * np.log10(max(float(np.mean(powers[i:i + 50][mask])), 1e-20)))
    if not levels:
        raise ValueError('Insufficient active audio for a one-second speech assessment')
    p10, median, p90 = np.percentile(levels, [10, 50, 90])
    return {'window_count': len(levels), 'p10_dbfs': round(p10, 3),
            'median_dbfs': round(median, 3), 'p90_dbfs': round(p90, 3),
            'p90_minus_p10_db': round(p90 - p10, 3),
            'windows_below_minus22_dbfs': int(np.sum(np.array(levels) < -22))}


def normalize(source, target):
    source, target = Path(source).resolve(), Path(target).resolve()
    report_path = target.with_suffix('.report.json')
    if source == target or target.exists() or report_path.exists():
        raise ValueError('Use a new output path; existing files are preserved')
    audio, sr = sf.read(source, always_2d=True)
    if audio.shape[1] not in (1, 2) or not np.isfinite(audio).all():
        raise ValueError('Expected finite mono/stereo narration')
    mask = frame_power(audio, sr) > 10 ** (-40 / 10)
    before = speech_stats(audio, sr, mask)
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    target.parent.mkdir(parents=True, exist_ok=True)
    measured_log = ffmpeg('-i', source, '-af', LEVEL_FILTER + ',' + LOUD_FILTER,
                          '-f', 'null', '-')
    measured = json.loads(re.findall(r'\{[^{}]+\}', measured_log)[-1])
    normalizer = LOUD_FILTER + ''.join(':' + key + '=' + measured[value] for key, value in
        [('measured_I', 'input_i'), ('measured_TP', 'input_tp'),
         ('measured_LRA', 'input_lra'), ('measured_thresh', 'input_thresh'),
         ('offset', 'target_offset')])
    applied_filter = LEVEL_FILTER + ',' + normalizer
    with tempfile.TemporaryDirectory(dir=target.parent) as temporary:
        rendered = Path(temporary) / 'leveled.wav'
        ffmpeg('-i', source, '-af', applied_filter,
               '-ar', sr, '-c:a', 'pcm_s16le', rendered)
        gap_protection = protect(source, rendered)
        output, out_sr = sf.read(rendered, always_2d=True)
        if out_sr != sr or output.shape != audio.shape or not np.isfinite(output).all():
            raise RuntimeError('Output timing/channel/finite-sample check failed')
        clipped = int(np.count_nonzero((output >= 32767 / 32768) | (output <= -1)))
        after = speech_stats(output, sr, mask)
        before_loudness, after_loudness = loudness(source), loudness(rendered)
        if clipped or after_loudness['true_peak_dbtp'] > -1.5:
            raise RuntimeError('Peak check failed; no final file published')
        if abs(after_loudness['integrated_lufs'] + 16) > .5:
            raise RuntimeError('Loudness target missed; no final file published')
        warnings = []
        if gap_protection.get('warning'):
            warnings.append(gap_protection['warning'])
        if after['p90_minus_p10_db'] > 4:
            warnings.append('Speech window spread exceeds 4 dB; review quieter sections')
        if after['windows_below_minus22_dbfs'] / after['window_count'] > .05:
            warnings.append('More than 5% of active windows remain quiet')
        if hashlib.sha256(source.read_bytes()).hexdigest() != source_hash:
            raise RuntimeError('Source changed during processing')
        report = {'source': str(source), 'source_sha256': source_hash, 'output': str(target),
                  'filter': applied_filter,
                  'ffmpeg_version': imageio_ffmpeg.get_ffmpeg_version(),
                  'duration_seconds': len(audio) / sr, 'sample_rate': sr,
                  'before': {**before, **before_loudness}, 'after': {**after, **after_loudness},
                  'measurement': '1s RMS windows, 0.5s hop; source 20ms frames > -40dBFS; minimum 30% active. This is an energy gate, not semantic speech detection.',
                  'sample_count_preserved': True, 'clipped_samples': clipped,
                  'new_api_requests': 0, 'warnings': warnings, 'listening_review': 'pending',
                  'gap_protection': gap_protection,
                  'output_sha256': hashlib.sha256(rendered.read_bytes()).hexdigest()}
        rendered.rename(target)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    return report


def self_test():
    with tempfile.TemporaryDirectory() as temporary:
        folder = Path(temporary)
        sr = 24000
        tone = np.sin(2 * np.pi * 180 * np.arange(sr * 3) / sr)
        fixture = np.concatenate([tone * .04, np.zeros(sr), tone * .35,
                                  np.zeros(sr), tone * .08])
        source, target = folder / 'input.wav', folder / 'output.wav'
        sf.write(source, fixture, sr)
        report = normalize(source, target)
        assert report['after']['p90_minus_p10_db'] < report['before']['p90_minus_p10_db']
        assert report['sample_count_preserved'] and report['clipped_samples'] == 0
        try:
            normalize(source, target)
        except ValueError:
            pass
        else:
            raise AssertionError('Existing output must be protected')
        silent = folder / 'silent.wav'
        sf.write(silent, np.zeros(sr * 2), sr)
        try:
            normalize(silent, folder / 'silent-output.wav')
        except ValueError:
            pass
        else:
            raise AssertionError('Silence must not pass as speech')
    print('Self-test passed: leveling, timing, peaks, overwrite protection, silence rejection')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', nargs='?', type=Path)
    parser.add_argument('output', nargs='?', type=Path)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--legacy-experiment', action='store_true', help='Explicitly run the superseded whole-file experiment')
    args = parser.parse_args()
    if args.self_test:
        self_test()
    elif args.source and args.output:
        if not args.legacy_experiment:
            parser.error('Whole-file normalization is no longer the default. Use boost_sentence_middles.py with reviewed sentence boundaries.')
        print(json.dumps(normalize(args.source, args.output), ensure_ascii=False, indent=2))
    else:
        parser.error('Provide source and output WAV paths, or --self-test')
