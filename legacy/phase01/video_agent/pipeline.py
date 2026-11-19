import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from .schemas import Plan, Scene, Source

TARGET_SECONDS = 150


def mock_plan(topic: str, ai_scenes: int = 6) -> tuple[Plan, list[Source]]:
    """Offline wiring test only. Deliberately makes no factual claims or fake sources."""
    if not 1 <= ai_scenes <= 9:
        raise ValueError("ai_scenes must be 1..9 for a hybrid production")
    stages = [
        '질문 던지기', '왜 중요한가', '오해 확인', '핵심 개념 소개', '기본 원리',
        '작동 과정', '생활 속 사례', '다른 관점', '검증할 질문', '마무리',
    ]
    scenes = []
    for i, stage in enumerate(stages):
        scenes.append(Scene(
            scene_id=i + 1, start_sec=i * 15, duration_sec=15,
            narration=f'{topic}. 이번 장면에서는 {stage}를 다룹니다. 실제 근거를 조사한 뒤 내용을 채워 넣어야 합니다.',
            visual_type='ai_video' if i in _ai_scene_indices(ai_scenes) else 'motion_graphics',
            visual_prompt=f'16:9 cinematic educational documentary, widescreen 1920x1080, {topic}, {stage}, clean visual, no lettering',
            on_screen_text=stage,
        ))
    return Plan(topic=topic, title=f'[데모] {topic}', claims=[], scenes=scenes,
                notes=['MOCK ONLY: 실제 웹 조사와 사실 검증이 이루어지지 않았습니다.']), []


def _ai_scene_indices(ai_scenes: int) -> set[int]:
    """Spread generated scenes evenly through the 10-scene timeline."""
    if not 1 <= ai_scenes <= 9:
        raise ValueError('ai_scenes must be 1..9')
    return {int((i + 0.5) * 10 / ai_scenes) for i in range(ai_scenes)}


def _get_citation_sources(response) -> list[Source]:
    result = []
    seen = set()
    for output in getattr(response, 'output', []):
        for content in getattr(output, 'content', []):
            for ann in getattr(content, 'annotations', []) or []:
                url = getattr(ann, 'url', None)
                if not url or url in seen or urlparse(url).scheme not in ('https', 'http'):
                    continue
                seen.add(url)
                title = getattr(ann, 'title', None) or urlparse(url).netloc
                result.append(Source(id=f'S{len(result)+1}', title=title, url=url, verified=True))
    return result


def live_plan(topic: str, model: str, ai_scenes: int = 6) -> tuple[Plan, list[Source]]:
    if not 1 <= ai_scenes <= 9:
        raise ValueError("ai_scenes must be 1..9 for a hybrid production")
    from openai import OpenAI
    client = OpenAI()
    research = client.responses.create(
        model=model,
        tools=[{'type': 'web_search'}],
        input=(
            '한국어 교육용 영상 리서치. 다음 주제를 신뢰할 만한 공개 자료에 근거하여 조사하고 '
            '사실, 불확실성, 다른 해석을 분리하라. 각 핵심 주장에 근거가 있는 자료를 인용하라. '
            '인터넷 검색 없이 사실을 추정하지 말라. 주제: ' + topic
        ),
    )
    sources = _get_citation_sources(research)
    if not sources:
        raise RuntimeError('웹 검색 인용 URL을 확보하지 못했습니다. 근거 없는 원고 생성을 중지합니다.')
    source_text = '\n'.join(f'{s.id}: {s.title} ({s.url})' for s in sources)
    result = client.responses.parse(
        model=model,
        text_format=Plan,
        input=(
            '너는 한국어 근거중심 숏폼 영상 작가다. 아래 조사 결과만 사용해 16:9 가로형 교육 영상 제작 계획을 작성하라. '
            '주장에 사용할 수 있는 source_ids는 제공된 S번호뿐이다. URL을 새로 만들지 마라. '
            '내용상 검증되지 않은 주장은 쓰지 마라. 근거가 불충분한 부분은 notes에 남겨라. '
            '정확히 10개의 scene, 각 15초, start_sec는 0,15,...,135로 설정하라. '
            f'시각 자료는 ai_video 장면 {ai_scenes}개, motion_graphics 장면 {10-ai_scenes}개로 구성한다. '
            'narration은 자연스러운 구어체로 작성하되 15초 발화에 적절한 길이로 맞춘다. '
            'target_duration_sec=150, aspect_ratio=16:9, publication_status=review_required. '
            '차트·숫자·연구 결과는 반드시 해당 출처를 연결하라. '
            f'주제: {topic}\n허용 출처:\n{source_text}\n조사 메모:\n{research.output_text}'
        ),
    )
    plan = result.output_parsed
    if plan is None:
        raise RuntimeError('모델이 구조화된 제작 계획을 반환하지 않았습니다.')
    return plan, sources


def review(plan: Plan, sources: list[Source], mode: str, ai_scenes: int = 6) -> dict:
    errors = []
    warnings = []
    if plan.target_duration_sec != TARGET_SECONDS or plan.aspect_ratio != '16:9':
        errors.append('영상 목표는 150초 / 16:9이어야 합니다.')
    if len(plan.scenes) != 10:
        errors.append('장면이 10개가 아닙니다.')
    if sum(s.duration_sec for s in plan.scenes) != TARGET_SECONDS:
        errors.append('장면 길이의 합계가 150초가 아닙니다.')
    for i, scene in enumerate(plan.scenes):
        if scene.scene_id != i+1 or scene.start_sec != i*15 or scene.duration_sec != 15:
            errors.append(f'{i+1}번 장면 타임라인 오류')
        if not scene.narration.strip() or not scene.visual_prompt.strip():
            errors.append(f'{i+1}번 장면 필수 텍스트 누락')
    types = [s.visual_type for s in plan.scenes]
    if types.count('ai_video') != ai_scenes or types.count('motion_graphics') != 10-ai_scenes:
        errors.append(f'영상/모션그래픽 비율이 {ai_scenes}:{10-ai_scenes}이 아닙니다.')
    valid_ids = {s.id for s in sources}
    for claim in plan.claims:
        if not claim.source_ids or not set(claim.source_ids).issubset(valid_ids):
            errors.append(f'근거가 없거나 잘못 연결된 주장: {claim.text[:40]}')
    for scene in plan.scenes:
        if not set(scene.source_ids).issubset(valid_ids):
            errors.append(f'{scene.scene_id}번 장면에 잘못된 출처 ID가 있습니다.')
    if len({source.id for source in sources}) != len(sources):
        errors.append('중복된 출처 ID가 있습니다.')
    if any(urlparse(source.url).scheme not in ('http','https') for source in sources):
        errors.append('잘못된 출처 URL이 있습니다.')
    if mode == 'mock':
        warnings.append('데모 실행: 자료 조사/출처 확인/실제 대본이 아님')
    if not sources:
        errors.append('출처가 없어 사람 검토 통과 불가')
    if not plan.claims:
        errors.append('검증 가능한 핵심 주장이 없음')
    if any(not s.source_ids for s in plan.scenes):
        warnings.append('출처 연결이 없는 장면이 있음: 사람 검토 필요')
    warnings.append('실제 TTS 음성 길이와 자막 싱크는 2단계에서 확인해야 함')
    warnings.append('출처 URL의 존재는 사실 검증과 동일하지 않음: 사람이 원문과 주장 일치 여부 확인 필요')
    return {'structural_pass': not errors, 'approval': 'review_required',
            'errors': errors, 'warnings': warnings, 'source_count': len(sources)}


def save_outputs(plan: Plan, sources: list[Source], report: dict, folder: Path) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    (folder/'plan.json').write_text(plan.model_dump_json(indent=2), encoding='utf-8')
    (folder/'sources.json').write_text(json.dumps([s.model_dump() for s in sources], ensure_ascii=False, indent=2), encoding='utf-8')
    (folder/'review.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    (folder/'script.txt').write_text('\n\n'.join(f'[{s.start_sec:03d}–{s.start_sec+s.duration_sec:03d}s] {s.narration}' for s in plan.scenes), encoding='utf-8')
    lines = [f'# {plan.title}', '', f'- 주제: {plan.topic}', '- 화면: 16:9 (권장 렌더링 1920×1080)', '- 목표: 150초 (장면 배분 계획; 실제 음성 길이는 미측정)', '- 상태: 검토 필요', '', '## 주요 주장과 출처']
    for claim in plan.claims:
        lines.append(f'- {claim.text} ({", ".join(claim.source_ids)})')
    lines += ['', '## 장면별 콘티']
    for s in plan.scenes:
        lines.extend([f'### {s.scene_id}. {s.start_sec}–{s.start_sec+s.duration_sec}초 / {s.visual_type}',
                      f'- 나레이션: {s.narration}', f'- 화면 문구: {s.on_screen_text}',
                      f'- 영상 프롬프트: {s.visual_prompt}', f'- 출처 ID: {", ".join(s.source_ids) or "없음"}', ''])
    lines += ['## 참고 자료']
    lines += [f'- {s.id}: [{s.title}]({s.url})' for s in sources]
    lines += ['', '## 검토 결과', f'- 구조 검사 통과: {report["structural_pass"]}']
    lines += [f'- 오류: {e}' for e in report['errors']]
    lines += [f'- 주의: {w}' for w in report['warnings']]
    (folder/'storyboard.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    flow_dir = folder/'flow_prompts'
    flow_dir.mkdir(exist_ok=True)
    manifest = []
    for scene in plan.scenes:
        entry = {
            'scene_id': scene.scene_id,
            'visual_type': scene.visual_type,
            'start_sec': scene.start_sec,
            'duration_sec': scene.duration_sec,
            'aspect_ratio': '16:9',
            'prompt': scene.visual_prompt,
            'status': 'pending_manual_review',
            'file_path': None,
        }
        manifest.append(entry)
        if scene.visual_type == 'ai_video':
            (flow_dir/f'scene_{scene.scene_id:02d}.txt').write_text(
                f'SCENE {scene.scene_id:02d} / {scene.duration_sec} sec timeline budget\n'
                '16:9 widescreen. Do not include subtitles or logos.\n\n'
                f'{scene.visual_prompt}\n', encoding='utf-8')
    (folder/'production_manifest.json').write_text(
        json.dumps({'aspect_ratio': '16:9', 'resolution_target': '1920x1080',
                    'video_provider': 'unselected', 'human_review_required': True,
                    'scenes': manifest}, ensure_ascii=False, indent=2), encoding='utf-8')
    return folder


def output_path(topic: str, base: Path) -> Path:
    safe = re.sub(r'[^\w가-힣-]+', '_', topic).strip('_')[:35] or 'topic'
    return base / f'{datetime.now().strftime("%Y%m%d_%H%M%S_%f")}_{safe}'
