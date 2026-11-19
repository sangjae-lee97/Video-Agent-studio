"""Local word timings for a new narration (faster-whisper small, no API).

Maps ASR words onto the script lines by normalized character position and writes
source-hash-matched transcription.json and sentence-boundaries.json for
balance_narration_phrases.py. ASR text never replaces the script; mapping is a
candidate that must be reviewed (report lists per-line recognized text).
"""
import argparse, hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def norm(text):
    return re.sub(r'[^0-9A-Za-z가-힣]', '', text)


def asr(wav, lines):
    from faster_whisper import WhisperModel
    model = WhisperModel(str(ROOT / 'models/faster-whisper-small'), device='cpu', compute_type='int8')
    # Decode with soundfile + numpy FFT resample to 16 kHz (avoids PyAV/faster-whisper version mismatch).
    import numpy as np, soundfile as sf
    pcm, sr = sf.read(str(wav), dtype='float32', always_2d=True)
    x = pcm.mean(axis=1)
    n_out = round(len(x) * 16000 / sr)
    audio = (np.fft.irfft(np.fft.rfft(x)[:n_out // 2 + 1], n_out) * (n_out / len(x))).astype(np.float32)
    segs, _ = model.transcribe(audio, language='ko', word_timestamps=True, beam_size=5,
                               initial_prompt=' '.join(lines)[:600])
    words = [{'start': round(w.start, 3), 'end': round(w.end, 3), 'text': w.word, 'probability': float(w.probability)}
             for s in segs for w in s.words if norm(w.word)]
    return words

def map_lines(lines, words):
    """Anchor each script line's final word to an ASR word (last two letters match),
    choosing the candidate nearest the proportional character position and preferring
    a following pause. Digits in ASR (e.g. 60자) make pure proportion mapping drift."""
    total = sum(len(norm(l)) for l in lines)
    n = len(words)
    ends, c, pos = [], 0, 0
    for li, l in enumerate(lines[:-1]):
        c += len(norm(l))
        expected = c / total * n
        tail = norm(l.split()[-1])[-2:]
        best = None
        for j in range(pos, n - 1):
            if not norm(words[j]['text']).endswith(tail):
                continue
            gap = words[j + 1]['start'] - words[j]['end']
            score = abs(j + 1 - expected) - (6 if gap >= .15 else 0) - (3 if words[j]['text'].strip()[-1:] in '.?!' else 0)
            if best is None or score < best[0]:
                best = (score, j)
        if best is None:
            raise SystemExit(f'No anchor for line {li + 1}; review manually.')
        ends.append(best[1] + 1); pos = best[1] + 1
    ends.append(n)
    groups, prev = [], 0
    for e in ends:
        groups.append(words[prev:e]); prev = e
    return groups

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('wav'); ap.add_argument('script_lines'); ap.add_argument('out_dir')
    ap.add_argument('--words-from', help='reuse words of an earlier transcription.json for the same WAV')
    a = ap.parse_args()
    wav, out = Path(a.wav), Path(a.out_dir)
    digest = hashlib.sha256(wav.read_bytes()).hexdigest()
    lines = [l for l in Path(a.script_lines).read_text(encoding='utf-8').splitlines() if l.strip()]
    if a.words_from:
        prior = json.loads(Path(a.words_from).read_text(encoding='utf-8'))
        if prior['source_sha256'] != digest:
            raise SystemExit('words belong to another WAV')
        words = [w for seg in prior['segments'] for w in seg['words']]
    else:
        words = asr(wav, lines)
    groups = map_lines(lines, words)
    segments, sentences = [], []
    for i, (l, g) in enumerate(zip(lines, groups), 1):
        segments.append({'start': g[0]['start'], 'end': g[-1]['end'], 'script': l,
                         'recognized': ''.join(w['text'] for w in g).strip(), 'words': g})
        sentences.append({'id': str(i), 'start': g[0]['start'], 'end': g[-1]['end']})
    out.mkdir(parents=True, exist_ok=True)
    (out / 'transcription.json').write_text(json.dumps({'source_sha256': digest, 'mapping': 'line-final-word anchors; review required', 'segments': segments}, ensure_ascii=False, indent=2), encoding='utf-8')
    (out / 'sentence-boundaries.json').write_text(json.dumps({'source_sha256': digest, 'sentences': sentences}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'lines': len(lines), 'asr_words': len(words)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
