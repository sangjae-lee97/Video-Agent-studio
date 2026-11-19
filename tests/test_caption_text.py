import json
import tempfile
import unittest
from pathlib import Path

from scripts.apply_captions import display_srt


class CaptionTextTests(unittest.TestCase):
    def test_display_forms_preserve_timestamps_units_and_particles(self):
        with tempfile.TemporaryDirectory() as folder:
            srt = Path(folder) / 'test.srt'
            timing = '00:00:01,100 --> 00:00:04,250'
            srt.write_text(f'1\n{timing}\n피에프에이는 1,000명 중 5.1%,\n약 26%p일까요?!\n', 'utf-8')
            srt.with_name('caption-terms.ko.json').write_text(
                json.dumps({'피에프에이': 'PFA'}), 'utf-8')
            expected = f'1\n{timing}\nPFA는 1,000명 중 5.1%\n약 26%p일까요\n'
            self.assertEqual(display_srt(srt), expected)
            srt.write_text(expected, 'utf-8')
            self.assertEqual(display_srt(srt), expected)
