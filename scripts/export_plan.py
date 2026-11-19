"""Validate an agent-authored plan and export a versioned production package, offline."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re

EXCLUSIONS = ('no burned-in captions, '
              'no karaoke-style word-by-word timing, no logos, no dissolve, no morph, '
              'no static hold, no empty ending, no background music, no speech or generated narration')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def index(rows, label):
    require(isinstance(rows, list), label + ': expected list')
    result = {}
    for row in rows:
        require(isinstance(row, dict), label + ': expected object')
        key = row.get('id', '')
        require(isinstance(key, str) and re.fullmatch(r'[A-Za-z0-9_-]+', key), label + ': invalid ID')
        require(key not in result, label + ': duplicate ID ' + key)
        result[key] = row
    return result


def filled(row, keys, label):
    for key in keys:
        require(isinstance(row.get(key), str) and row[key].strip(), label + ': missing ' + key)


def refs(row, key, available, label):
    values = row.get(key)
    require(isinstance(values, list) and values, label + ': missing ' + key)
    require(all(isinstance(v, str) and v in available for v in values), label + ': unknown ' + key)


def validate(plan):
    require(plan.get('version') == 1, 'Unsupported plan version')
    project = plan['project']
    filled(project, ['id', 'title', 'aspect_ratio', 'timing_status', 'style'], 'project')
    require(project['aspect_ratio'] == '16:9', 'Current production format is 16:9')
    duration = project.get('duration_seconds')
    require(number(duration) and duration > 0, 'Invalid project duration')
    require(project['timing_status'] in ('draft', 'aligned'), 'Invalid timing status')
    require(project.get('flow_attempt_budget') is None or
            (type(project['flow_attempt_budget']) is int and project['flow_attempt_budget'] >= 0), 'Invalid budget')
    sources = index(plan['sources'], 'sources')
    claims = index(plan['claims'], 'claims')
    narration = index(plan['narration'], 'narration')
    media = index(plan['media'], 'media')
    edits = index(plan['edits'], 'edits')
    require(narration and media and edits, 'Empty production plan')
    for row in sources.values():
        filled(row, ['title', 'url', 'checked_on', 'access_scope'], row['id'])
        require(row['url'].startswith('https://'), row['id'] + ': HTTPS source required')
    for row in claims.values():
        filled(row, ['summary', 'verification', 'limits'], row['id'])
        require(row['verification'] in ('checked', 'pending'), 'Invalid verification status')
        refs(row, 'source_ids', sources, row['id'])
    for row in narration.values():
        filled(row, ['text', 'role'], row['id'])
        refs(row, 'claim_ids', claims, row['id'])
    for row in media.values():
        key = row['id']
        filled(row, ['purpose', 'reason', 'start_state', 'end_state', 'status'], key)
        require(row.get('kind') in ('flow', 'motion'), key + ': only Flow or motion supported')
        require(number(row.get('duration_seconds')) and row['duration_seconds'] > 0, key + ': invalid duration')
        refs(row, 'narration_ids', narration, key)
        if row['kind'] == 'motion':
            filled(row, ['action', 'labels', 'review'], key)
            continue
        filled(row, ['subject', 'look', 'graphics', 'continuity', 'audio', 'review'], key)
        require(not re.search(r'위와 동일|클립.?과 동일|same as|\[반복\]|TODO|TBD', row['subject'], re.I), key + ': non-independent subject')
        shots = row.get('shots', [])
        if len(shots) != 3:
            require(len(shots) in (2, 4) and row.get('shot_exception_reason'), key + ': default is three shots')
        cursor = 0
        for shot in shots:
            filled(shot, ['event', 'camera'], key + ' shot')
            start, end = shot.get('start'), shot.get('end')
            require(number(start) and number(end) and end > start and abs(start - cursor) < .001,
                    key + ': shot overlap/gap/invalid duration')
            camera = shot['camera'].lower()
            require(not ('push-in' in camera and 'pull-back' in camera), key + ': contradictory camera')
            require(not ('locked off' in camera and 'handheld' in camera), key + ': contradictory camera')
            require(not all(s in camera for s in ('orbit', 'lateral', 'crane')), key + ': too many camera directions')
            cursor = end
        require(abs(cursor - row['duration_seconds']) < .001, key + ': shot sum mismatch')
        prompt = flow_prompt(row).lower()
        require(not any(s in prompt for s in ('no cuts', 'no rotation or cuts', 'outlines will be added later')),
                key + ': conflicting motion restriction')
    cursor = 0
    used_ranges = {}
    for row in edits.values():
        require(row.get('media_id') in media, row['id'] + ': unknown media')
        values = [row.get(k) for k in ('start', 'end', 'source_in', 'source_out')]
        require(all(number(v) for v in values), row['id'] + ': invalid time')
        start, end, source_in, source_out = values
        require(end > start and abs(start - cursor) < .001, row['id'] + ': timeline overlap/gap')
        require(0 <= source_in < source_out <= media[row['media_id']]['duration_seconds'] + .001,
                row['id'] + ': source range outside media')
        require(abs((end - start) - (source_out - source_in)) < .001, row['id'] + ': unplanned speed change')
        clip = media[row['media_id']]
        source = (clip.get('input_sha256') or clip.get('input_asset') or
                  clip.get('source_sha256') or clip.get('source_asset') or clip['id'])
        offset = clip.get('input_offset_seconds', 0)
        require(number(offset) and offset >= 0, row['id'] + ': invalid source offset')
        a,b = source_in + offset,source_out + offset
        previous = used_ranges.setdefault(source, [])
        for old_a,old_b,old_id in previous:
            require(min(b,old_b)-max(a,old_a) < .000001,
                    f"{row['id']}: source footage overlaps {old_id}")
        previous.append((a,b,row['id']))
        cursor = end
    require(abs(cursor - duration) < .001, 'Timeline does not match narration duration')
    warnings = []
    if project['timing_status'] != 'aligned':
        warnings.append('장면 경계는 초안: 발화 정렬/자막 타이밍 확인 전 최종 편집에 사용하지 않기')
    if project.get('flow_attempt_budget') is None:
        warnings.append('Flow 생성 시도 예산 미정: 무제한 자동 재시도 금지')
    if any(c['verification'] != 'checked' for c in claims.values()):
        warnings.append('미확인 주장 존재: 사실 검토 필요')
    if any(m['status'] != 'reviewed' for m in media.values()):
        warnings.append('실제 미디어 생성/품질 검토 대기')
    return warnings


def flow_prompt(clip):
    lines = [f"FORMAT: {clip['duration_seconds']:g}-second video, landscape 16:9. Hard cuts between shots.",
             '\nSUBJECT: ' + clip['subject'], '\nLOOK: ' + clip['look']]
    for n, shot in enumerate(clip['shots'], 1):
        lines.append(f"\nSHOT {n} [{shot['start']:g}-{shot['end']:g}s]: {shot['event']}\nCAMERA: {shot['camera']}")
    lines.extend(['\n' + clip.get('graphics_heading', 'RED GRAPHICS') + ': ' + clip['graphics'], '\nCONTINUITY: ' + clip['continuity'],
                  '\nEXCLUSIONS: ' + EXCLUSIONS + '.', '\nAUDIO: ' + clip['audio']])
    return '\n'.join(lines)


def export(plan_path, output):
    plan = json.loads(Path(plan_path).read_text(encoding='utf-8-sig'))
    warnings = validate(plan)
    canonical = json.dumps(plan, ensure_ascii=False, indent=2) + '\n'
    content_hash = hashlib.sha256(canonical.encode())
    files = {'plan.json': canonical}
    for clip in plan['media']:
        if clip['kind'] == 'flow':
            prompt = flow_prompt(clip) + '\n'
            files[f"flow-{clip['id']}.txt"] = prompt
            content_hash.update(prompt.encode())
    if project_subtitles := plan['project'].get('subtitles'):
        captions = (Path(__file__).resolve().parents[1] / project_subtitles).read_text(encoding='utf-8')
        files['captions.ko.srt'] = captions
        content_hash.update(captions.encode())
    digest = content_hash.hexdigest()[:12]
    # Versioned directories make old prompts inactive without deleting user media.
    base = Path(output).resolve()
    version = base / digest
    version.mkdir(parents=True, exist_ok=True)
    files['script.md'] = '# 내레이션 원문\n\n' + '\n\n'.join(f"{n['id']} — {n['text']}" for n in plan['narration']) + '\n'
    files['sources.md'] = '# 근거와 확인 범위\n\n' + '\n\n'.join(
        f"- {s['id']}: [{s['title']}]({s['url']}) — {s['checked_on']}, {s['access_scope']}" for s in plan['sources'])
    files['sources.md'] += '\n\n' + '\n\n'.join(
        f"- {c['id']} ({c['verification']}, {', '.join(c['source_ids'])}): {c['summary']}\n  한계: {c['limits']}" for c in plan['claims']) + '\n'
    edit_text = ['# 혼합 편집 시트', '', '장면 경계 상태: ' + plan['project']['timing_status'], '',
                 '| 시간(초) | 미디어 | 유형 | 목적 |', '|---|---|---|---|']
    media = {m['id']: m for m in plan['media']}
    for e in plan['edits']:
        m = media[e['media_id']]
        edit_text.append(f"| {e['start']:g}–{e['end']:g} | {m['id']} | {m['kind']} | {m['purpose']} |")
    edit_text += ['', '## 움직임·제작·검토 지시', '']
    for m in plan['media']:
        edit_text += [f"### {m['id']} — {m['purpose']}", '',
                     f"- 선택 이유: {m['reason']}", f"- 음성 연결: {', '.join(m['narration_ids'])}",
                     f"- 시작 → 끝: {m['start_state']} → {m['end_state']}",
                     f"- 움직임: {m.get('action', 'Flow 프롬프트의 세 샷 참조')}",
                     f"- 라벨: {m.get('labels', '프롬프트의 '+m.get('graphics_heading', 'RED GRAPHICS')+' 참조')}", f"- 검토: {m['review']}", '']
    files['edit-sheet.md'] = '\n'.join(edit_text) + '\n'
    flows = [m for m in plan['media'] if m['kind'] == 'flow']
    manifest = {'plan_hash': digest, 'structural_validation': 'passed', 'warnings': warnings,
                'flow_clip_count': len(flows), 'planned_generation_seconds': sum(m['duration_seconds'] for m in flows),
                'flow_attempt_budget': plan['project'].get('flow_attempt_budget'),
                'generation_attempts': 0, 'video_quality_review': 'pending', 'files': sorted(files)}
    if imported := [m for m in plan['media'] if m.get('source_asset') and m.get('source_kind', m['kind']) == 'flow']:
        manifest.update(imported_flow_assets=[m['source_asset'] for m in imported],
                        generation_attempts=None, additional_generation_attempts=0)
    files['manifest.json'] = json.dumps(manifest, ensure_ascii=False, indent=2) + '\n'
    for name, content in files.items():
        path = version / name
        if path.exists():
            require(path.read_text(encoding='utf-8') == content, f'Export was modified: {path}; preserve it and use a new output folder')
        else:
            path.write_text(content, encoding='utf-8')
    current = f"# 현재 활성 제작 패키지\n\n버전: `{digest}`. 다른 버전 폴더는 이전 출력이며 자동 입력으로 수집하지 않는다.\n\n"
    current += '\n'.join(f'- [{name}]({digest}/{name})' for name in sorted(files))
    current += '\n\n' + '\n'.join('- ' + w for w in warnings) + '\n'
    temp = base / 'CURRENT.tmp'
    temp.write_text(current, encoding='utf-8')
    temp.replace(base / 'CURRENT.md')
    return version, manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        if args.output:
            path, manifest = export(args.plan, args.output)
            print(path)
            print(json.dumps(manifest, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({'structural_validation': 'passed', 'warnings': validate(json.loads(args.plan.read_text(encoding='utf-8-sig')))}, ensure_ascii=False, indent=2))
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(1, f'Plan error: {error}\n')
