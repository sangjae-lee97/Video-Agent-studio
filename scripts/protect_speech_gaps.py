"""Limit leveling gain in likely speech gaps, preserving surrounding phonemes.

Silero ONNX input/state protocol: https://github.com/snakers4/silero-vad (MIT).
This is a speech detector, not a breath classifier; short/ambiguous gaps are kept.
"""
import hashlib
from pathlib import Path
import subprocess
import tempfile

import imageio_ffmpeg
import numpy as np
import onnxruntime as ort
import soundfile as sf

MODEL = Path(__file__).resolve().parents[1] / 'models/silero-vad/silero_vad.onnx'
MODEL_HASH = '1a153a22f4509e292a94e67d6f9b85e8deb25b4988682b7e174c65279d8788e3'


def probabilities(source):
    if hashlib.sha256(MODEL.read_bytes()).hexdigest() != MODEL_HASH:
        raise ValueError('Unexpected speech detection model')
    with tempfile.TemporaryDirectory() as folder:
        analysis = Path(folder) / 'analysis.wav'
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-nostdin',
                        '-i', str(source), '-ar', '16000', '-ac', '1', str(analysis)], check=True)
        audio, _ = sf.read(analysis, dtype='float32')
    options = ort.SessionOptions()
    options.intra_op_num_threads = options.inter_op_num_threads = 1
    session = ort.InferenceSession(str(MODEL), sess_options=options, providers=['CPUExecutionProvider'])
    state, context = np.zeros((2, 1, 128), np.float32), np.zeros((1, 64), np.float32)
    scores = []
    for i in range(0, len(audio), 512):
        chunk = audio[i:i + 512]
        chunk = np.pad(chunk, (0, 512 - len(chunk)))[None]
        joined = np.concatenate([context, chunk], axis=1)
        probability, state = session.run(None, {'input': joined, 'state': state, 'sr': np.array(16000, np.int64)})
        context = joined[:, -64:]
        scores.append(float(probability[0, 0]))
    return np.array(scores)


def limit_gaps(original, leveled, sr, scores):
    """Retain .096s on both sides; smooth attenuation inside gaps >= .32s."""
    speech = scores >= .2
    report = {'model_sha256': MODEL_HASH, 'speech_threshold': .2, 'padding_seconds': .096,
              'boundary_fade_seconds': .048, 'max_attenuation_db': 18,
              'speech_frame_fraction': round(float(np.mean(speech)), 4), 'regions': []}
    if np.mean(speech) < .2:
        report['warning'] = 'Insufficient detected speech; gap attenuation skipped for manual review'
        return leveled.copy(), report
    gaps = np.diff(np.r_[False, ~speech, False].astype(int))
    gain = np.ones(len(leveled))
    for start, end in zip(np.flatnonzero(gaps == 1), np.flatnonzero(gaps == -1)):
        first = max(0, round((start * .032 + (.096 if start else 0)) * sr))
        last = min(len(leveled), round((end * .032 - (.096 if end < len(scores) else 0)) * sr))
        if last - first < round(.128 * sr):
            continue
        before_rms = float(np.sqrt(np.mean(original[first:last] ** 2)))
        after_rms = float(np.sqrt(np.mean(leveled[first:last] ** 2)))
        if after_rms < 10 ** (-65 / 20):
            continue
        # Restore the gap to at most its original RMS; no hard mute and no re-leveling.
        factor = max(10 ** (-18 / 20), min(1., before_rms / max(after_rms, 1e-12)))
        if factor > 10 ** (-2 / 20):
            continue
        envelope = np.ones(last - first)
        fade = round(.048 * sr)
        ramp = .5 - .5 * np.cos(np.linspace(0, np.pi, fade))
        envelope[:fade] = ramp
        envelope[-fade:] = ramp[::-1]
        gain[first:last] = 10 ** ((20 * np.log10(factor) * envelope) / 20)
        report['regions'].append({'start': round(first / sr, 3), 'end': round(last / sr, 3),
                                   'attenuation_db': round(float(-20 * np.log10(factor)), 2)})
    output = leveled * gain[:, None]
    unchanged = gain == 1
    assert np.array_equal(output[unchanged], leveled[unchanged])
    assert output.shape == leveled.shape and np.isfinite(output).all()
    report['outside_regions_unchanged'] = True
    return output, report


def protect(source, leveled_path):
    original, sr = sf.read(source, always_2d=True)
    leveled, rate = sf.read(leveled_path, always_2d=True)
    if sr != rate or original.shape != leveled.shape:
        raise ValueError('Original and leveled WAV must have matching length, rate and channels')
    result, report = limit_gaps(original, leveled, sr, probabilities(source))
    # Preserve unmodified PCM samples exactly (including negative samples).
    pcm = np.rint(result * 32768).astype(np.int16)
    sf.write(leveled_path, pcm, sr, subtype='PCM_16')
    return report


def self_test():
    sr = 16000
    original = np.full((sr * 3, 1), .02)
    leveled = original * 4
    scores = np.ones(94)
    scores[30:48] = 0
    output, report = limit_gaps(original, leveled, sr, scores)
    assert len(report['regions']) == 1
    assert np.array_equal(output[:sr // 2], leveled[:sr // 2])
    assert np.max(np.abs(output[sr:sr + 500])) <= .08
    assert np.mean(output[round(1.2 * sr):round(1.3 * sr)]) < .025
    assert output.shape == leveled.shape
    output, report = limit_gaps(original, leveled, sr, np.zeros(94))
    assert np.array_equal(output, leveled) and report.get('warning')
    print('Gap protection checks passed')


if __name__ == '__main__':
    self_test()
