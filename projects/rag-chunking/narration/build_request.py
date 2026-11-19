"""Builds script.md, source.txt, emotion-plan.json and request.json from one segment list."""
import json, hashlib
from pathlib import Path
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
D = json.loads((ROOT / 'docs/narration-defaults.json').read_text(encoding='utf-8'))
E = D['emotion_by_role']
# (role, focus, [lines])
SEG = [
 ('opening_question', '정답이 있는데 못 찾는다', ['문서에는 분명히 정답이 있는데, AI는 왜 그걸 못 찾을까요?']),
 ('explanation', '래그 정의, 통째로 넣으면 섞임', [
   '래그는 AI가 문서를 검색해서, 찾은 근거로 답하게 만드는 방식입니다.',
   '그런데 긴 문서를 통째로 다루면, 주제가 섞여 필요한 부분을 가려내기 어렵습니다.']),
 ('clarification', '청크·청킹 정의', ['그래서 문서를 검색할 수 있는 조각, 청크로 나눕니다. 이걸 청킹이라고 부릅니다.']),
 ('definition_details', '자르기와 임베딩은 다른 작업', ['자른 조각은 다시 임베딩해서 벡터로 바꿉니다. 자르는 일과 숫자로 바꾸는 일은, 서로 다른 작업이죠.']),
 ('safety_transition', '진짜 문제: 어디서 자르나', ['진짜 문제는, 어디서 자르느냐입니다.']),
 ('balanced_comparison', '고정 크기 / 문단', ['가장 단순한 건 글자 수마다 자르는 고정 크기 방식, 다른 하나는 빈 줄마다 자르는 문단 방식입니다.']),
 ('explanation', '각각의 장단점', ['고정 크기는 예측이 쉽지만 문장 중간이 잘릴 수 있고, 문단 방식은 경계를 지키지만 조각 길이가 들쭉날쭉합니다.']),
 ('risk_or_serious_event', '정답이 두 조각으로', ['강의 예시에서 육십 자씩 자르자, 정답 문구인 금요일 오후 여섯 시가 두 조각으로 갈라졌습니다. 검색 결과를 열 개까지 늘려도, 찾지 못했습니다.']),
 ('response_measures', '오버랩 정의', ['그래서 쓰는 장치가 오버랩입니다. 앞 조각의 끝부분을, 다음 조각 첫머리에 조금 겹쳐 넣는 거죠.']),
 ('definition_details', '160/30 → 130자 뒤', [
   '백육십 자씩 자르고 삼십 자를 겹치면, 다음 조각은 백삼십 자 뒤에서 시작합니다.',
   '랭체인의 재귀 분할기는 빈 줄, 줄바꿈, 공백 순서로 자를 자리를 찾습니다.']),
 ('safety_transition', '반전 질문', ['그럼, 많이 겹칠수록 좋을까요?']),
 ('key_result', '오히려 밀렸다', ['강의의 교육용 실험에서는 오히려 반대였습니다! 겹침을 육십 자로 늘리자 같은 문의 안내가 두 조각에 반복돼 위를 차지했고, 정답 조각은 이 위에서 삼 위로 밀렸습니다.']),
 ('uncertainty_limit', '일반 법칙 아님, 측정 필요', ['단어 개수로 만든 교육용 벡터라 일반 법칙은 아닙니다. 그래서 자른 방식은, 반드시 검색 결과로 확인해야 합니다.']),
 ('explanation', 'Hit@3', ['첫 번째 잣대는 히트 앳 쓰리. 상위 세 개 안에 정답 근거가 있으면 일, 없으면 영입니다.']),
 ('definition_details', 'MRR 계산', ['두 번째는 엠알알입니다. 정답이 일 위면 일, 이 위면 이분의 일, 삼 위면 삼분의 일을 주고, 질문들의 평균을 냅니다.']),
 ('balanced_comparison', '같은 Hit, 다른 MRR', ['세 질문 모두 히트 앳 쓰리가 일이어도, 순위가 일, 이, 삼 위라면 엠알알은 약 영 점 육일일입니다.']),
 ('clarification', '정답률 아님', ['이건 정답률 육십일 퍼센트가 아니라, 정답을 얼마나 앞에서 찾았는지 보는 점수입니다.']),
 ('safety_transition', '찾았다고 맞나', ['그런데, 근거를 찾았다고 답이 맞는 걸까요?']),
 ('risk_or_serious_event', '잘못 읽고 덧붙일 수 있음', ['아닙니다. 모델이 찾은 문단을 잘못 읽거나, 없는 내용을 덧붙일 수도 있습니다.']),
 ('response_measures', '원문+출처, Document, HOLD', [
   '그래서 근거는 원문 그대로, 출처와 함께 보여 줍니다. 랭체인의 다큐먼트가 본문과 출처를 함께 담는 이유죠.',
   '근거를 확인하지 못하면, 답을 지어내지 않고 보류합니다. 이걸 홀드라고 합니다.']),
 ('uncertainty_limit', 'HOLD·temperature 한계', [
   '다만 홀드는 답이 없다는 증명이 아닙니다. 자른 방식 때문에 놓쳤을 수도 있으니까요.',
   '템퍼러처를 낮추면 답은 일관돼지지만, 틀린 근거를 정답으로 바꿔 주진 않습니다.']),
 ('balanced_conclusion', '별칭 결말', ['문서에 정답이 있어도 못 찾는 이유는, 자른 자리에 있을 수 있습니다. 좋은 청킹은 잘게 써는 칼질이 아니라, 근거를 끊지 않는 칼질입니다.']),
]
lines = [l for _, _, ls in SEG for l in ls]
segments, plan = [], []
n = 0
for i, (role, focus, ls) in enumerate(SEG):
    text = '\n'.join(ls)
    prompt = dict(E[role])
    if prompt['emotion_type'] == 'smart':
        prev = lines[max(0, n-2):n]; nxt = lines[n+len(ls):n+len(ls)+2]
        prompt = {'emotion_type': 'smart', 'previous_text': '\n'.join(prev), 'next_text': '\n'.join(nxt)}
    plan.append({'source_lines': [n+1, n+len(ls)], 'role': role, 'intended_focus_not_spoken_instruction': focus, 'prompt': prompt})
    if segments:
        segments.append({'type': 'pause', 'duration_seconds': D['segment_pause_seconds']})
    segments.append({'type': 'tts', 'voice_id': D['voice_id'], 'model': D['model'], 'language': D['language'],
                     'text': text, 'prompt': prompt, 'output': D['output']})
    n += len(ls)
source = '\n'.join(lines) + '\n'
rejoined = '\n'.join(s['text'] for s in segments if s['type'] == 'tts') + '\n'
assert rejoined == source, 'segments do not rebuild script'
chars = sum(len(l) for l in lines)
assert chars <= 2000 and len([s for s in segments]) <= 50
(OUT / 'source.txt').write_text(source, encoding='utf-8')
(OUT / 'emotion-plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
payload = json.dumps({'segments': segments}, ensure_ascii=False, indent=2).encode('utf-8')
(OUT / 'request.json').write_bytes(payload)
md = ['# 낭독 대본 — RAG 청킹과 검색 품질', '', '낭독용 원문(발음 표기·강조 부호 보존). 화면 자막은 별도 검증. 근거: [analysis.md](analysis.md).', '']
k = 0
for role, focus, ls in SEG:
    for l in ls:
        k += 1; md.append(f'{k}. {l}')
md += ['', f'- 줄 수 {len(lines)}, 구간 {len(SEG)}, 글자 수 {chars}(공백 포함), 요청 sha256 `{hashlib.sha256(payload).hexdigest()}`']
(OUT.parent / 'script.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
print(len(lines), len(SEG), chars, hashlib.sha256(payload).hexdigest())
