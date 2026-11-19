"""Offline regression checks for actual production-plan failure cases."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('export_plan', ROOT / 'scripts/export_plan.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PlanTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT / 'projects/pfa-pilot/plan.json').read_text(encoding='utf-8'))

    def test_valid_variable_timeline_and_independent_prompt(self):
        warnings = module.validate(self.plan)
        self.assertEqual(any('장면 경계' in w for w in warnings),
                         self.plan['project']['timing_status'] != 'aligned')
        clip = self.plan['media'][1]
        prompt = module.flow_prompt(clip)
        self.assertIn(clip['subject'], prompt)
        self.assertEqual(prompt.count('\nSHOT '), 3)
        self.assertIn('no burned-in captions', prompt)
        self.assertNotRegex(prompt.lower(), r'(?:bottom|lower)\s+\d+%|clear for subtitles')

    def test_reject_invalid_plans(self):
        cases = [
            lambda p: p['edits'][1].update(start=8.5),
            lambda p: p['edits'][1].update(start=9.5),
            lambda p: p['edits'][0].update(media_id='missing'),
            lambda p: p['edits'][1].update(source_out=10),
            lambda p: p['media'][1].update(subject=''),
            lambda p: p['media'][1].update(subject='same as previous clip'),
            lambda p: p['media'][1]['shots'][1].update(start=2.6),
            lambda p: p['media'][1]['shots'][2].update(end=7.5),
            lambda p: p['media'][1]['shots'][0].update(camera='push-in and pull-back'),
            lambda p: p['media'][1]['shots'][0].update(camera='no cuts'),
            lambda p: p['media'][1].update(shots=p['media'][1]['shots'][:1]),
            lambda p: p['media'][0].update(kind='static_png'),
            lambda p: p['narration'][0].update(claim_ids=['missing']),
            lambda p: p['claims'][0].update(source_ids=['missing']),
            lambda p: p['project'].update(duration_seconds=float('nan')),
            lambda p: p['project'].update(flow_attempt_budget=-1),
            lambda p: p['media'].append(copy.deepcopy(p['media'][0])),
        ]
        for i, mutate in enumerate(cases):
            with self.subTest(case=i):
                plan = copy.deepcopy(self.plan)
                mutate(plan)
                with self.assertRaises(ValueError):
                    module.validate(plan)

    def test_alias_does_not_allow_a_second_use_of_the_same_frames(self):
        plan = json.loads((ROOT / 'projects/pfa-pilot/production-plan.json').read_text('utf-8'))
        copied = copy.deepcopy(next(m for m in plan['media'] if m['id']=='SRC-F03'))
        copied['id'] = 'second-copy'
        plan['media'].append(copied)
        next(e for e in plan['edits'] if e['id']=='E09a').update(
            media_id='second-copy', source_in=.875, source_out=3.875)
        with self.assertRaisesRegex(ValueError, 'source footage overlaps'):
            module.validate(plan)

    def test_reexport_does_not_activate_stale_prompts(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, output = root / 'plan.json', root / 'exports'
            source.write_text(json.dumps(self.plan), encoding='utf-8')
            old, _ = module.export(source, output)
            again, _ = module.export(source, output)
            self.assertEqual(old, again)
            self.plan['media'][1].update(kind='motion', action='Draw region boundaries', labels='PFA')
            source.write_text(json.dumps(self.plan), encoding='utf-8')
            new, manifest = module.export(source, output)
            self.assertNotEqual(old, new)
            self.assertEqual(manifest['flow_clip_count'], 0)
            self.assertTrue((old / 'flow-F01.txt').exists())
            self.assertFalse((new / 'flow-F01.txt').exists())
            current = (output / 'CURRENT.md').read_text(encoding='utf-8')
            self.assertNotIn(old.name, current)
            self.assertNotIn('flow-F01.txt', current)
            # Manual edits must survive re-export rather than being silently overwritten.
            (new / 'script.md').write_text('manual changes', encoding='utf-8')
            with self.assertRaises(ValueError):
                module.export(source, output)
            self.assertEqual((new / 'script.md').read_text(encoding='utf-8'), 'manual changes')


if __name__ == '__main__':
    unittest.main()
