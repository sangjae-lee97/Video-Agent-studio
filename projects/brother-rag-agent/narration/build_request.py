"""Builds script.md, source.txt, emotion-plan.json and request.json from one segment list."""
import json, hashlib
from pathlib import Path
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
D = json.loads((ROOT / 'docs/narration-defaults.json').read_text(encoding='utf-8'))
E = D['emotion_by_role']
# (role, focus, [lines])
SEG = [
 ('opening_question', '숫자 하나 다른 두 모델', ['이름이 숫자 하나만 다른 프린터 두 대. AI는 내 모델의 답을, 정확히 골라낼 수 있을까요?']),
 ('explanation', '과제 정체', [
   '이번 프로젝트는 브라더 프린터와 복합기 열 개 모델의 기술지원 질문에, 공식 문서로 답하는 래그 에이전트를 만드는 겁니다.',
   '서너 명이 한 팀으로, 닷새, 사십 시간 안에요.']),
 ('definition_details', 'PDF 2종 페이지', ['자료는 한국어 공식 피디에프 두 권. 잉크젯 다섯 모델의 사백육십육 쪽, 흑백 레이저 다섯 모델의 육백삼십삼 쪽입니다.']),
 ('safety_transition', '함정', ['그런데, 함정이 있습니다.']),
 ('risk_or_serious_event', '다섯 모델이 한 권에', ['한 권에 다섯 모델이 함께 들어 있어서, 표의 한 행이나 각주 하나가 일부 모델에만 해당할 수 있습니다. 다른 모델의 절차를 그대로 가져오면, 그럴듯한 오답이 됩니다.']),
 ('response_measures', '메타데이터로 역추적', ['그래서 조각마다 문서 아이디와 페이지, 그리고 적용 모델을 붙입니다. 어떤 주장이든 원문과 모델까지 거슬러 올라갈 수 있게요.']),
 ('balanced_comparison', '검색기 3종', ['검색기는 세 가지를 같은 조건에서 비교합니다. 의미로 찾는 벡터 검색, 여기에 키워드 검색 비엠이십오를 더한 하이브리드, 그리고 후보를 다시 채점하는 리랭킹입니다.']),
 ('explanation', '인용', ['답변에는 실제로 찾아낸 문서의 제목과 페이지를 함께 인용합니다.']),
 ('safety_transition', '반전 질문', ['그럼, 자료에 없는 걸 물어보면요?']),
 ('key_result', '거부가 정답', ['답을 지어내지 않고, 확인할 수 없다고 말하는 게 정답입니다!']),
 ('uncertainty_limit', '부당 거부·오류 구분', ['반대로 답이 있는 질문을 거부하면, 오답으로 처리됩니다. 근거 부족과 검색 오류, 생성 오류도 따로 구분해서 보여 줘야 하죠.']),
 ('response_measures', '최적화·모델 비교', ['속도와 비용도 챙깁니다. 캐싱이나 쿼리 리라이트를 하나 이상 적용하고, 같은 근거와 프롬프트로 생성 모델 두 개 이상을 비교합니다.']),
 ('explanation', '공개 10 / 비공개 100', ['개발에는 공개 질문 열 개를 쓰고, 최종 평가는 교수자의 비공개 백 문항으로 합니다.']),
 ('definition_details', '문항 유형', ['기능과 사양, 설정과 오류 해결이 각각 스물다섯, 유사 제품 구분과 복합 조건이 각각 스물, 그리고 근거 없는 질문이 열 개입니다.']),
 ('key_result', '배점 45', ['백 점 가운데, 답변 정확도와 근거 신뢰성이 사십오 점입니다!']),
 ('risk_or_serious_event', '0.40 미만 → 효율 0점', ['답변 정확도가 영 점 사 미만이면, 속도와 비용 효율 십오 점은 통째로 영 점이 됩니다.']),
 ('uncertainty_limit', '60초·실패 기록', ['문항당 제한 시간은 육십 초. 실패와 타임아웃도 지우지 않고 그대로 기록합니다.']),
 ('explanation', '재현', ['마지막 날에는 다른 팀원이 같은 버전으로 다시 실행해서, 결과가 재현되는지 확인합니다.']),
 ('balanced_conclusion', '결말', ['숫자 하나 다른 두 프린터. 좋은 에이전트는 맞는 모델의 근거로 답하고, 근거가 없으면 모른다고 말합니다.']),
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
assert chars <= 2000 and len(segments) <= 50
(OUT / 'source.txt').write_text(source, encoding='utf-8')
(OUT / 'emotion-plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
payload = json.dumps({'segments': segments}, ensure_ascii=False, indent=2).encode('utf-8')
(OUT / 'request.json').write_bytes(payload)
md = ['# 낭독 대본 — Brother 기술지원 RAG Agent', '', '낭독용 원문(발음 표기·강조 부호 보존). 화면 자막은 별도 검증. 근거: [analysis.md](analysis.md).', '']
k = 0
for role, focus, ls in SEG:
    for l in ls:
        k += 1; md.append(f'{k}. {l}')
md += ['', f'- 줄 수 {len(lines)}, 구간 {len(SEG)}, 글자 수 {chars}(공백 포함), 요청 sha256 `{hashlib.sha256(payload).hexdigest()}`']
(OUT.parent / 'script.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
print(len(lines), len(SEG), chars, hashlib.sha256(payload).hexdigest())
