from pathlib import Path
from video_agent.pipeline import mock_plan, review, save_outputs
from video_agent.schemas import Claim, Source


def test_mock_timeline_and_ratio():
    plan, sources = mock_plan('AI 환각')
    assert plan.target_duration_sec == 150
    assert plan.aspect_ratio == '16:9'
    assert [(s.start_sec, s.duration_sec) for s in plan.scenes] == [(i*15, 15) for i in range(10)]
    assert sum(s.visual_type == 'ai_video' for s in plan.scenes) == 6
    assert len(sources) == 0


def test_mock_cannot_be_approved():
    plan, sources = mock_plan('AI 환각')
    report = review(plan, sources, 'mock')
    assert not report['structural_pass']
    assert report['approval'] == 'review_required'


def test_unknown_source_rejected():
    plan, _ = mock_plan('AI 환각')
    plan.claims = [Claim(text='근거 검증 대상', source_ids=['S99'])]
    report = review(plan, [Source(id='S1', title='sample', url='https://example.org')], 'live')
    assert any('잘못 연결된' in e for e in report['errors'])


def test_outputs_saved(tmp_path: Path):
    plan, sources = mock_plan('AI 환각')
    folder = save_outputs(plan, sources, review(plan, sources, 'mock'), tmp_path/'run')
    assert (folder/'plan.json').exists()
    assert 'AI 환각' in (folder/'script.txt').read_text(encoding='utf-8')
    assert (folder/'storyboard.md').exists()
    assert '16:9' in (folder/'storyboard.md').read_text(encoding='utf-8')
    assert (folder/'production_manifest.json').exists()
    assert len(list((folder/'flow_prompts').glob('*.txt'))) == 6


def test_aspect_ratio_cannot_be_swapped():
    plan, sources = mock_plan('AI 환각')
    # Assignment is validated by Pydantic at parse time; supported ratio is 16:9.
    from pydantic import ValidationError
    import pytest
    with pytest.raises(ValidationError):
        plan.model_copy(update={'aspect_ratio': '9:16'}).model_validate(
            plan.model_copy(update={'aspect_ratio': '9:16'}).model_dump()
        )

def test_publication_never_auto_approved():
    plan, _ = mock_plan('AI 환각')
    plan.claims = [Claim(text='검토 대상', source_ids=['S1'])]
    for scene in plan.scenes:
        scene.source_ids = ['S1']
    sources = [Source(id='S1', title='Example', url='https://example.org')]
    report = review(plan, sources, 'live')
    assert report['structural_pass']
    assert report['approval'] == 'review_required'


def test_select_custom_ai_video_ratio():
    plan, sources = mock_plan('주제', ai_scenes=8)
    assert sum(s.visual_type == 'ai_video' for s in plan.scenes) == 8
    result = review(plan, sources, 'mock', ai_scenes=8)
    assert not any('비율' in error for error in result['errors'])
