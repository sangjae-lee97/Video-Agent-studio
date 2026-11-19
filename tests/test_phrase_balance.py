"""Local relative decisions, breath-gap preservation and no hidden edge padding."""
from pathlib import Path
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from balance_narration_phrases import process


class PhraseBalanceTests(unittest.TestCase):
    def fixture(self, quiet=True):
        sr = 16000
        time = np.arange(sr * 12) / sr
        wave = .15 * np.sin(2 * np.pi * 160 * time)
        if quiet:
            wave[4 * sr:8 * sr] *= .35
        sentences = [{'id': str(i), 'start': i * 4., 'end': (i + 1) * 4.} for i in range(3)]
        segments = [{'words': [{'start': i * 4 + j, 'end': i * 4 + j + 1., 'text': ' word',
                                'probability': .99} for j in range(4)]} for i in range(3)]
        pcm = np.rint(wave * 32768).astype(np.int16)
        return sr, pcm, sentences, segments, np.ones(375)

    def test_quiet_phrases_first_word_edges_and_gap(self):
        sr, pcm, sentences, segments, scores = self.fixture()
        # Confident non-speech inside a word span must remain bit-identical.
        scores[170:177] = .05
        out, report = process(pcm, sr, sentences, segments, scores)
        self.assertGreater(report['boosted_phrase_count'], 0)
        self.assertTrue(np.array_equal(out[170 * 512:177 * 512], pcm[170 * 512:177 * 512]))
        # Voice immediately after a gap is not excluded by the old .16s blanket padding.
        lo, hi = 177 * 512 + 700, 177 * 512 + 1300
        self.assertFalse(np.array_equal(out[lo:hi], pcm[lo:hi]))
        self.assertFalse(np.array_equal(out[round(4.3 * sr):round(4.8 * sr)], pcm[round(4.3 * sr):round(4.8 * sr)]))
        for s in sentences:
            for start, end in [(s['start'], s['start'] + .2), (s['end'] - .2, s['end'])]:
                self.assertTrue(np.array_equal(out[round(start * sr):round(end * sr)], pcm[round(start * sr):round(end * sr)]))
        self.assertEqual(len(out), len(pcm))
        self.assertLess(np.max(np.abs(out.astype(int))), 32767)
        for p in report['phrases']:
            self.assertLessEqual(p['gain_db'], 3)

    def test_uniformly_quiet_audio_is_not_globally_normalized(self):
        sr, pcm, sentences, segments, scores = self.fixture(quiet=False)
        pcm = (pcm * .2).astype(np.int16)
        out, report = process(pcm, sr, sentences, segments, scores)
        self.assertTrue(np.array_equal(pcm, out))
        self.assertEqual(report['boosted_phrase_count'], 0)

    def test_ambiguous_detection_and_bad_boundaries(self):
        sr, pcm, sentences, segments, scores = self.fixture()
        scores[170:177] = .4
        out, report = process(pcm, sr, sentences, segments, scores)
        self.assertTrue(np.array_equal(out[170 * 512:177 * 512], pcm[170 * 512:177 * 512]))
        self.assertGreater(report['ambiguous_word_overlap_seconds_unchanged'], 0)
        sentences[1]['start'] = 3.
        with self.assertRaises(ValueError):
            process(pcm, sr, sentences, segments, scores)

    def test_short_dip_hidden_inside_an_average_phrase(self):
        sr, pcm, sentences, segments, scores = self.fixture(quiet=False)
        # A brief quiet syllable inside an otherwise normal phrase; no real-script timestamps.
        lo, hi = round(5.2 * sr), round(5.6 * sr)
        pcm[lo:hi] = np.rint(pcm[lo:hi] * .55).astype(np.int16)
        old, _ = process(pcm, sr, sentences, segments, scores)
        out, report = process(pcm, sr, sentences, segments, scores, mode='short-window')
        a, b = lo + round(.1 * sr), hi - round(.1 * sr)
        rms = lambda x: np.sqrt(np.mean(x[a:b].astype(float) ** 2))
        self.assertGreater(rms(out) / rms(pcm), 1.2)
        self.assertLess(rms(old) / rms(pcm), 1.05)
        self.assertFalse(report['breath_classification_verified'])

    def test_short_window_scale_invariance_and_protected_noise(self):
        sr, pcm, sentences, segments, scores = self.fixture()
        scores[170:177] = .05
        scores[230:235] = .4
        original = pcm.copy()
        out, _ = process(pcm, sr, sentences, segments, scores, mode='short-window')
        half = np.rint(pcm.astype(float) / 2).astype(np.int16)
        out_half, _ = process(half, sr, sentences, segments, scores, mode='short-window')
        # A quieter whole input must not get a completely different gain prescription.
        self.assertLess(np.max(np.abs(out.astype(float) / 2 - out_half)), 3)
        for lo, hi in [(170 * 512, 177 * 512), (230 * 512, 235 * 512), (4 * sr, round(4.2 * sr))]:
            self.assertTrue(np.array_equal(out[lo:hi], pcm[lo:hi]))
        self.assertTrue(np.array_equal(pcm, original))
        self.assertTrue(np.all(np.abs(out.astype(int)) >= np.abs(pcm.astype(int))))
        self.assertLessEqual(np.max(np.abs(out.astype(float)) / np.maximum(np.abs(pcm.astype(float)), 1)), 10 ** (3 / 20) + .01)

    def test_short_window_constant_audio_and_peak_headroom(self):
        sr, pcm, sentences, segments, scores = self.fixture(quiet=False)
        out, _ = process(pcm, sr, sentences, segments, scores, mode='short-window')
        self.assertTrue(np.array_equal(pcm, out))
        pcm[4 * sr:8 * sr] = np.rint(pcm[4 * sr:8 * sr] * .3).astype(np.int16)
        pcm[round(5.4 * sr)] = 32000  # Loud transient inside an otherwise quiet region.
        out, _ = process(pcm, sr, sentences, segments, scores, mode='short-window')
        self.assertEqual(out[round(5.4 * sr)], 32000)
        self.assertLess(np.max(np.abs(out.astype(int))), 32767)


if __name__ == '__main__':
    unittest.main()
