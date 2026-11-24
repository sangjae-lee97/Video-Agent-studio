# 모션그래픽 효과 라이브러리 — 파티클·빛·타이포·전환

장면 방법(설명 패턴·카메라·타이포·데이터·전환·PPT 방식·도구 선택)은 [모션그래픽 제작 방법 모음](MOTION_DESIGN_METHODS.md)에 있고, 이 문서는 그 방법을 구현하는 **코드 부품**을 다룬다.

새 편의 모션그래픽을 설계하거나 고칠 때 [공통 제작 지침의 모션그래픽 절](VIDEO_PRODUCTION_GUIDE.md#모션그래픽-제작과-검수)과 함께 읽는다. 어떤 모양으로 보일지는 편마다 정하는 메타포(`.agents/skills/flow-motion-template`)가 결정하고, 이 문서는 **움직임의 부품**과 그 부품을 언제 쓰는지를 정리한다. 효과는 대사가 말하는 변화를 보여 줄 때만 쓴다. 장식만을 위한 효과는 넣지 않는다.

- 코드: [`scripts/motion/effects.js`](../scripts/motion/effects.js) — 파티클 7종 + 등장·강조 8종 + 카메라·공간 3종 + 가리기·드러내기 4종 + 상태 보간(PPT 모프식) + 타이포 1종 + SVG 모핑. 공통 렌더러(`scripts/motion/render.py`)와 같이 쓴다.
- 미리보기: `python scripts/motion/render.py scripts/motion/effects_demo_scenes.py outputs/fx-demo --preview` (장면 4개 A~D, 마지막 프레임 jpg). 전체 렌더는 `--preview`를 빼면 된다.
- 작성 2026-11-24. 효과 코드는 클라우드 작업 공간의 Playwright Chromium으로 시연 장면 A~D의 13개 시점을 렌더해 페이지 오류 0건, 같은 시각을 다른 시각 뒤에 다시 그려도 화면이 바이트 단위로 같음(결정성)을 확인했다. 실제 편 장면에 적용한 결과 검수는 아직 없다.

## 1. 먼저 지킬 규칙

1. **화면은 시각 T만으로 정해져야 한다.** 렌더러는 프레임마다 `R(T)`를 부르고, 미리보기는 마지막 프레임 하나만 그린다. 그래서 이전 프레임 상태를 쌓는 방식(캔버스를 반투명으로 덮어 꼬리 만들기, 매 프레임 위치 누적, `Math.random()`, `requestAnimationFrame`, CSS `@keyframes`·`transition`)은 쓰지 않는다. 난수는 `FX.rng(seed)`로 고정하고, 꼬리는 지나온 위치를 T에서 거꾸로 계산해 그린다. 웹의 흔한 파티클 예제는 대부분 상태 누적형이므로 그대로 붙여 넣지 않는다.
2. **효과 하나 = 대사 속 사건 하나.** 숫자가 확정되는 순간, 두 대상이 합쳐지는 순간, 오류가 드러나는 순간에 맞춘다. 시작 시각은 발화 단어 시각(편의 `sentence-boundaries.json`·`asr-words.json`)에 맞추고, 결과를 읽을 시간을 컷 전에 남긴다.
3. **한 화면에 주인공 효과는 하나.** 배경 효과(dust·flow·grain)는 불투명도 0.2~0.5 이하로 깔고, 전경 파티클(burst·converge·comet·ripple)은 같은 순간에 하나만 쓴다. 주목 대상끼리 경쟁시키지 않는다(IBM Design Language의 staging 원칙).
4. **하단 약 14%는 자막 자리다.** 전경 파티클·숫자·라벨을 그 영역에 두지 않는다. 배경 효과는 지나가도 된다.
5. **색과 밝기는 편의 template-spec(메타포)을 따른다.** 어두운 배경에서는 `lighter`(가산) 합성으로 빛나게, 밝은 배경에서는 가산 합성이 하얗게 날아가므로 진한 색·보통 합성으로 바꾼다. 색의 의미(통과=초록, 오류=빨강 등)는 편의 template-spec을 따른다.
6. **정확한 숫자·글자는 DOM 텍스트로 쓴다.** 파티클로 숫자 모양을 만들면 읽기 어렵다. `converge`는 “모여서 무엇이 된다”는 움직임만 맡고, 도착하는 순간 실제 텍스트가 `data-blurin`·`data-pop`으로 나타나게 한다.
7. **Flow 위에는 얹지 않는다.** 모션그래픽은 독립 장면이다. Flow에서는 라벨 철자 보정만 한다.
8. **`effects.js` 안에는 닫는 script 태그 문자열을 쓰지 않는다.** 장면 HTML에 스크립트로 넣는 순간 브라우저가 거기서 끊는다(실제로 겪은 오류).
9. **효과는 덜 쓰는 쪽이 기본이다.** 고조회 코드 모션 작품들은 파티클 폭발·발광·흔들림·튀는 이징을 아예 금지 목록에 넣었다([방법 모음 11장](MOTION_DESIGN_METHODS.md)). 편의 template-spec에 쓸 효과와 금지 효과를 함께 적는다.
10. **카메라로 확대되는 요소에는 `will-change`를 주지 않는다**(글자가 흐려짐). 3D 변환 요소는 opacity·filter를 감싼 요소에 준다.

### 렌더러 옵션 (2026-11-24 추가)
- `render.py`는 장면마다 새 페이지를 연다. 이전에는 한 페이지를 재사용해 앞 장면의 전역 변수·`window.extra`가 다음 장면에 남았다(`Identifier 'ease' has already been declared` 오류 확인).
- `--subframes 3`: 프레임마다 반 프레임 폭(180도 셔터) 안의 3시점을 찍어 ffmpeg `tmix`로 평균 → 모션 블러. 렌더 시간 약 3배. 시연 장면 D에서 72프레임 유지, 정지 프레임은 블러 없는 렌더와 화소 차 0, 움직이는 막대에 블러 확인.

## 2. 지금까지 각 편에서 쓴 움직임 (2026-11-24 코드 조사)

| 편 | 렌더 방식 | 쓴 효과 | 위치 |
|---|---|---|---|
| pfa-pilot | Python PIL로 프레임 직접 그림 | 방사형 그라데이션 배경(은은한 빛), 선 그리기 `stroke(amt)`, 점 하나=참가자 한 명인 점 격자, 지시선 콜아웃 | `projects/pfa-pilot/render_film.py` 등 |
| brother-rag-agent | 공통 HTML 렌더러(base.py) | 떠오르며 등장 `data-in`, 막대 성장 `data-grow`, 숫자 카운트 `data-count`, 흐리기 `data-dim`, 테두리 강조 `data-hl`, 비율 막대가 빨갛게 줄어듦(효율 0점), 명판 숫자 한 자리 색·크기 맥박 | `projects/brother-rag-agent/motion/scenes.py` |
| rag-chunking | Canvas JS(자체 lib.js) | 방사형 배경 + 옅은 격자, 그림자 발광 상자 `box({glow})`, 화살표·선 그리기, 청록 발광 스캔 막대, ✓/✕ 표시, 둥근 태그 | `projects/rag-chunking/motion/lib.js` |
| rag-concepts-longform | 공통 HTML 렌더러 | 도장 찍기 `data-stamp`(0.12초 눌림), 송장 라벨 행 순차 등장, 화살표 그리기, 경로 지도 점등 | `projects/rag-concepts-longform/motion/scenes.py` |

정리: 지금까지는 **등장·성장·카운트·강조·선 그리기**만 썼고 파티클·빛 반사·전환 효과는 없었다. 같은 장치가 편마다 반복되는 것을 피하려면 아래 카탈로그에서 그 편의 메타포에 맞는 것을 골라 모양만 바꿔 쓴다.

## 3. 효과 카탈로그

표의 “속성”은 장면 HTML에 다는 이름이다. 길이는 기본값이다. base.py 효과(`data-in`·`data-grow`·`data-count`·`data-dim`·`data-hl`·`data-draw`)는 그대로 쓸 수 있다.

### 3-1. 파티클 (캔버스, `<i class="fxp" data-fx="종류" data-t="시작초">`)

| 효과 | 설명에 쓰는 의미 | 쓰지 말 때 | 주요 값 |
|---|---|---|---|
| `dust` 떠다니는 먼지 | 공간의 깊이·조용한 분위기. 정보 없음 | 이미 화면이 복잡할 때, 밝은 배경(먼지가 얼룩처럼 보임) | `n`=60, `a`=.25, 깊이별 크기·속도 다름 |
| `flow` 흐르는 입자장 | 데이터·신호가 계속 흐르는 상태(검색 중, 처리 중) | 특정 방향 이동을 설명할 때(그때는 comet) | `n`=220, `speed`=60px/s, 수명 2~5초 순환, 처음 15%·끝 20% 페이드 |
| `burst` 불꽃 터짐 | 확정·통과·제출 성공 같은 “딱 정해지는 순간” | 오류·위험(축하처럼 보임), 한 편에 3회 이상 | `n`=28, `r`=180, 0.9초, 약한 중력 |
| `converge` 모여듦 | 흩어진 조각이 하나의 결과로 합쳐짐(청크→답, 표본→점수) | 흩어지는 의미(그때는 burst를 작게) | 목표 사각형 `x,y,w,h`, 1.1초, 지연 0~35% 분산 후 0.4초 페이드 |
| `comet` 경로를 따라가는 빛 | 질문→검색→답처럼 순서 있는 흐름, 연결 | 경로가 화면을 가로지르며 글자를 덮을 때 | `path`="x,y x,y …", 1.0초, 꼬리 18% |
| `ripple` 동심원 파문 | 탐지·신호 발생·“여기”를 가리킴 | 정확한 위치를 지시선으로 짚어야 할 때 | 3겹, 반경 220, 1.2초, 0.22초 간격 |
| `grain` 필름 그레인 | 아날로그 질감(문서·기록 메타포) | 깨끗한 디지털·HUD 메타포 | `a`=.06, 24fps마다 결정적 노이즈 |

모든 캔버스 효과는 `data-until="초"`로 끝 시각을 지정할 수 있다.

### 3-2. 등장·강조 (DOM 속성)

| 효과 | 의미 | 길이 | 비고 |
|---|---|---|---|
| `data-pop` 스프링 등장 | 새로 생긴 결과, 짧은 단어·배지 | 0.6초 | 감쇠 진동 오버슈트. 긴 문단에는 쓰지 않는다 |
| `data-blurin` 초점 맞추며 등장 | “드러남”, 정답 공개 | 0.5초 | blur 14px→0 |
| `data-wipe` 왼쪽부터 드러냄 | 순서대로 읽히는 문장, 진행 | 0.5초(`data-d`) | clip-path |
| `data-type` 타자 | 입력·질문·코드 | 초당 18자(`data-cps`) | 한글은 음절 단위로 나옴 |
| `data-sheen` 빛 반사 1회 | 확정된 수치·완성품의 표면 | 0.7초 | 카드에 position 필요. 밝은 카드에서는 효과가 약함 |
| `data-glowp` 발광 맥박 2회 | “이 숫자를 보라” 강조 | 1.4초 | 드롭섀도 발광, 끝나면 사라짐 |
| `data-shake` 흔들림 | 충돌·오류·예상 밖 결과 | 0.35초 | `data-amp`=10px. 한 편에 남발 금지 |
| `data-roll` 숫자 롤링 | 점수·수치가 정해지는 과정 | 0.9초 | 끝에서 정확히 목표값. `data-from`으로 시작값 지정(예: 4.75→9.66). `data-count`보다 고정폭 숫자라 흔들림 적음 |

### 3-3. 카메라·공간·드러내기·상태 보간 (DOM 속성)

| 효과 | 의미 | 값 |
|---|---|---|
| `data-cam="t:s,x,y; …"` | 무대 위 카메라 이동·확대(디테일↔전체) | s=배율, x,y=화면 중심에 올 무대 좌표 |
| `data-pan="t0,t1,dx,dy"` | 층별 다른 이동 = 2.5D 패럴랙스, 막대 자리 이동 | px |
| `data-follow` + `data-path` | 점·아이콘이 경로를 따라감(절차, 데이터 이동) | `data-d` 초 |
| `data-iris` | 원형 마스크로 열림(장 시작, “여기서”) | `data-cx/cy` % |
| `data-marker` | 형광펜(신호) | `data-c` 반투명 색 |
| `data-strike` | 취소선(정정) | `data-c` |
| `data-flipin` | 카드 뒤집혀 등장(이전/이후 카드) | 0.6초 |
| `data-split` | 단어 차례 등장(짧은 구호) | `data-stagger` |
| `path[data-morph]` + `data-to` | 도형 변형(같은 대상의 상태 변화) | 두 경로 숫자 개수 같아야 함 |
| `data-kf="t:키=값,…; t:…"` | **PPT 모프식 상태 보간** — 위치·크기·색·불투명도·회전·배율 | left top w h o r s bg c fs |

### 3-4. 장면 전환 (구현 방법만 기록, 공통 코드 없음)

- 하드컷이 기본이다. Flow↔모션은 항상 하드컷.
- 모션끼리 이어질 때는 같은 기준물(진행선·축·패널)을 남긴 채 내용만 바뀌게 한다(공통 지침의 ‘같은 진행선’). 굳이 전환 효과가 필요하면 메타포에서 파생한다: 문서=페이지 넘김, 기계·계측=스캔라인으로 지워짐, 지도=줌, 물류=컨베이어 슬라이드. 길이는 0.25~0.5초.
- 디졸브·모핑은 쓰지 않는다.

## 4. 대사 → 효과 고르기

| 대사가 하는 일 | 1순위 | 함께 쓸 수 있는 것 |
|---|---|---|
| 숫자·점수 발표 | `data-roll` + 도착 순간 `data-glowp` | 결과가 성공이면 작은 `burst` |
| 비교 결과 발표 | base.py `data-grow` 막대 + 끝값 `data-pop` | 진 쪽 `data-dim` |
| 오류·함정 공개 | 빨강 `data-hl`/표시 + `data-shake` 한 번 | `ripple`(빨강)로 위치 지목 |
| 원인·정정 | 앞 화면 유지 + 해당 행만 강조(`data-dim`으로 나머지 낮춤) | `data-wipe`로 정정 문구 |
| 흐름·과정 | `comet` 경로 | 배경 `flow` 낮은 불투명도 |
| 여러 조각이 하나로 | `converge` → 결과 텍스트 `data-blurin` | — |
| 시간 경과 | 진행선 끝점 이동(`data-draw`) | 마커 `data-pop` |
| 결말·질문 | 정지에 가까운 구도 + 질문 텍스트 `data-type` | `dust` 아주 옅게 |

## 5. 사용 예

```python
# projects/<편>/motion/scenes.py
from pathlib import Path
FX = (Path(__file__).resolve().parents[3] / 'scripts/motion/effects.js').read_text(encoding='utf-8')
CV = '<canvas class="abs fx" width="1920" height="1080" style="left:0;top:0"></canvas>'
S = {}
S['M07'] = (int(68.1*24), int(73.1*24), CV
  + '<i class="fxp" data-fx="dust" data-t="68.1" data-a=".2"></i>'
  + '<div class="abs" style="left:700px;top:380px;font-size:150px;font-weight:900">'
  + '<span data-roll="71.0" data-v="91.26" data-dec="2" data-glowp="71.9">0</span></div>'
  + '<i class="fxp" data-fx="burst" data-t="71.9" data-x="960" data-y="460" data-n="20"></i>'
  + '<script>' + FX + '</script>')   # FX는 장면 HTML 맨 끝에. 장면 자체 window.extra는 FX보다 앞에 정의
```

- 캔버스 `.fx`는 장면당 하나, 맨 앞(뒤에 깔리게)에 둔다. 전경 위에 그리고 싶으면 z-index를 준다.
- 장면이 `window.extra`를 직접 정의하면 그 스크립트를 FX보다 **앞에** 둔다. FX가 기존 extra를 감싸서 함께 부른다.
- 무거운 효과: `flow`는 매 프레임 각 입자의 경로를 처음부터 다시 계산한다. `n`을 300 이하로 둔다.

## 6. 근거와 참고

- 공통 지침: 모션그래픽 절(기준물·변화·결론, 색 톤 일치, 검수 3시점) — [VIDEO_PRODUCTION_GUIDE.md](VIDEO_PRODUCTION_GUIDE.md).
- 움직임 원칙: IBM Design Language, *Classic animation principles* — 정밀하게(과한 늘어남 없이), 한 번에 하나의 동작으로 시선 유도(staging), 빠르게 출발해 부드럽게 멈춤(slow in/out), 장식이 아니라 기능을 보여 주는 과장. https://www.ibm.com/design/language/animation/classic-principles
- 스프링 오버슈트: 감쇠 진동으로 ‘넘었다가 정착’하는 움직임(UI 애니메이션 원칙 정리). https://mintlify.com/raphaelsalaja/userinterface-wiki/animation/12-principles-of-animation
- 입자 수명 페이드(처음 12.5%·끝 16% 페이드, 수명 200~500프레임, 600~2,000개)와 상태 누적형 꼬리 방식: kokonutui Flow Field 설명. 이 저장소에서는 꼬리를 상태 누적 대신 역계산으로 바꿨다. https://www.mintlify.com/kokonut-labs/kokonutui/components/backgrounds/flow-field
- 흐름장(벡터장 + 입자) 개념: BIT-101 *Flow Fields, Part II*. https://www.bit-101.com/2017/2017/10/flow-fields-part-ii
- 파티클이 갑자기 나타나지 않게 불투명도 그라데이션으로 페이드: Apple Motion 사용 설명서 *Particle System Examples*. https://help.apple.com/motion/mac/5.0/help/English/en/motion/usermanual/chapter_14_section_11.html
- 발광은 필터 하나보다 흐린 복제층을 겹치는 편이 자연스럽다: Creative Bloq *50 Motion Graphics Tips*. https://www.creativebloq.com/computer-arts/50-motion-graphics-tips-12089189

## 7. 이 문서를 고치는 법

새 효과를 실제 편에 쓰고 검수했으면 3장 표에 한 줄 추가하고, 그 편 이름과 검수한 시점(변화 직전·완료·다음 컷 첫 화면)을 적는다. 실패한 효과(읽기 방해, 자막과 겹침, 의미 혼동)는 지우지 말고 “쓰지 말 때” 칸에 사례로 남긴다.
