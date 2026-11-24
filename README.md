# Video Agent Studio

> **처음 받으셨다면** → [처음 시작하기 (설치 · Claude 연결 · Typecast PowerShell 실행 · Google Flow 설정)](docs/SETUP_GUIDE.md)

주제 하나에서 **재미있는 약 2분 30초 한국어 지식 영상**을 만드는 프로젝트입니다. 모든 분야를 다루며 Google Flow 웹 영상과 모션그래픽을 혼합합니다.

> **현재 결과** · [게시 영상(YouTube)](https://www.youtube.com/watch?v=b8K9VsvDLNQ) (완성 MP4·썸네일은 로컬 `projects/pfa-pilot/renders/`에만 있고 저장소에는 없음) · [공통 자막 프로그램](scripts/apply_captions.py) · [검증 및 재현 기록](projects/pfa-pilot/README.md).

[Notion 프로젝트 홈](https://app.notion.com/p/41ddb49922e5814f82e2c2ce00a50017) · [승인 내레이션 기록](https://app.notion.com/p/41ddb49922e581cf9244eedf38132608).

**새 채팅에서 시작하기** · 이 프로젝트를 열고 주제 한 줄이나 문서를 보내면 됩니다. 에이전트가 분석 문서를 먼저 저장하고, 그 근거로 대본과 Typecast 내레이션을 만듭니다. 보정 음성의 실제 발화 시각으로 전편을 설계한 뒤 필요한 Flow 요청과 이미지를 한 메시지로 전달합니다. 생성본을 모아 올리면 에이전트가 모션그래픽을 제작하고, 화면용 표기를 별도로 검증한 자막과 함께 완성본을 조립합니다. [공통 제작 순서](docs/VIDEO_PRODUCTION_GUIDE.md#새-채팅에서-한-편을-만드는-순서)

## 현재 결정

사용자에게 전달하는 1080p 완성 영상의 파일명은 `주제_완성본_1080p.mp4`로 통일합니다. 매 편 완성본과 16:9 썸네일의 파일 링크, 유튜브에 바로 붙여 넣을 제목과 설명을 함께 전달합니다. 설명 본문에는 영상의 근거 자료명과 원문 URL을 포함합니다.

새 영상과 재개 작업 모두 장면 설계 전에 [공통 제작 지침](docs/VIDEO_PRODUCTION_GUIDE.md) 전문을 읽습니다. 모션그래픽 장면을 만들거나 수정할 때마다 [모션그래픽 제작과 검수](docs/VIDEO_PRODUCTION_GUIDE.md#모션그래픽-제작과-검수)를 다시 읽고 렌더 결과를 대조합니다.

Flow는 가로 16:9·720p(1280×720)로 생성하고, 채택한 테이크만 무료 1080p(1920×1080) 업스케일해 편집한다. 모형의 색·방향·기기 수·위치와 노출 범위를 컷 사이에 유지한다. 화면 끝까지 장면을 채우고, 의미를 전달하는 기간·숫자·명칭은 Flow의 장면 내 라벨로 지정한다. 내레이션 자막은 편집에서 발화에 맞춰 얹는다.

- 자막은 편집할 때 영상 위에 겹쳐 넣습니다. Flow는 장면에 맞춰 전체 화면을 사용하며 자막용 공간을 따로 지정하지 않습니다.

- 재미와 몰입을 우선하며 신비한 건축사전의 질문·모순·반전·인과·별칭 서사를 적극 배웁니다. 없는 사건·수치·인과관계는 만들지 않습니다.
- Google Flow는 기존 구독의 웹을 사용합니다. 수동 프롬프트 복붙·영상 전달도 정상 제작 경로입니다.
- **Flow 기본 3샷**은 클립 내부 구성입니다. 8초 기준 2.5+2.5+3초로 출발하며 이유 없이 1샷으로 줄이지 않습니다. 전체 Flow 클립 수를 세 개로 고정하는 뜻은 아닙니다.
- Flow 요청은 해당 대본 → Flow 입력 방식(프레임·이어 붙이기 / 프레임·시작 프레임 업로드 / 소재 / 소재·이미지 없음)과 선택 이유·이미지 출처 → 복붙용 프롬프트 및 적용 방법 순서로 전달합니다. [판정 기준](docs/VIDEO_PRODUCTION_GUIDE.md#flow-프롬프트를-쓰는-법) 직전 영상과 이어지는 장면에는 시작 프레임 이미지를 붙입니다. 대상 설명 전문·사건·카메라와 앞뒤 장면의 연결을 명시합니다. 단면·치수선·강조를 모두 후반으로 미루거나 움직임을 막는 제약을 넣지 않습니다.
- **고정 PNG 장면은 사용하지 않습니다.** 긴 정지 화면이나 단순 줌으로 대체하지 않습니다. 이미지는 정보를 전달하는 모션그래픽의 구성 요소로 사용할 수 있습니다.
- 완성 영상의 주 화면 재생시간을 기준으로 Google Flow 약 30%, Codex가 직접 만드는 로컬 모션그래픽 약 70%를 배정한다. 본편에 이미 등장한 장면은 다시 쓰지 않고, 자막이나 라벨을 겹친 시간은 한 번만 센다.
- 16:9 출발점이며 실제 음성 길이에 맞춰 편집합니다. 150초는 제품 목표이고 현재 승인 시험 원고는 92.610초입니다.
- FFmpeg로 최종 조립합니다. Remotion은 모션 후보, Manim은 필요한 수식/기하 장면에서 검토합니다. 두 엔진 모두 제작용 확정·구현 전입니다.

## 승인한 내레이션 방식

2026-11-19 사용자 승인: **내용별 감정 배치 → Typecast 합성 → 원본 기반 로컬 음량 보정 → 검사·청취**.

- 화자 필재/SSFM 3.1, **새 원고 기본 1.05배속**(2026-11-20 완성 영상 검토 후 사용자 변경). 2026-11-19의 **1.0배속·92.610초 승인 파일은 과거 실험/완성본 기록**으로 보존합니다.
- 비교 양쪽을 같은 강도로 강조하고, 핵심 결과·오해 정정·제한·결론은 의미 단위로 배치합니다. 위험은 차분하게 읽되 지나친 tonedown으로 묻히지 않게 합니다.
- 로컬 보정은 문장 시작/끝 **0.2초 보존**, 약 200ms 말소리 창의 주변 대비 부족분만 완만하게 올리며 **최대 +3dB**입니다. 전체 정규화·감쇠·호흡 제거는 하지 않습니다.
- Auphonic 및 추가 후처리 API는 사용하지 않습니다. 특정 문구·시간대에만 적용하는 증폭 예외도 만들지 않습니다.
- [감정 기준](docs/NARRATION_STYLE.md), [기본 설정](docs/narration-defaults.json), [음량 규칙](docs/LOCAL_AUDIO_POLICY.md), [승인 파일·해시](docs/NARRATION_APPROVAL.json).
- 승인 파일: `outputs/typecast-piljae-pfa-emphasis-1.0x-v1/local-short-window-v1/narration_balanced.wav`.
- 23문장 보호 구간·길이 보존, 새 포화 0 확인. 원본의 최대값 27샘플과 +0.15dBTP는 최종 영상 마스터 단계의 검토 사항입니다. [실측](docs/piljae-emphasis-local-level-results.json).
- 승인 방식은 다른 원고에 재사용하되 새 결과의 발음·억양·호흡과 전체 음량을 다시 확인합니다. 서로 다른 주제의 품질까지 검증된 것은 아닙니다.

## 기존 PFA 파일럿을 이어갈 때

[장면별 진행 상태](projects/pfa-pilot/flow-state.json)에서 현재 장면, 기다리는 입력과 다음 행동을 읽는다.

[복사할 인수인계 프롬프트](docs/VIDEO_HANDOFF_PROMPT.md).

[30:70 완성 MP4](projects/pfa-pilot/renders/AVANT-GUARD_완성본_1080p.mp4) · [활성 편집 계획](projects/pfa-pilot/production-plan.json) · [검증 기록](projects/pfa-pilot/README.md). Flow 27.777초(30.0%)와 모션그래픽 64.833초로 완성했다. F07 치료 선택 갈림점은 52.750–55.750초, F09 진료실은 85.750–92.610초다. 세 컷의 모니터에 승인된 56%·약 30% 그래프를 합성하고 종이의 효과 아래에 ‘1년간 PFA 우세’, 위험 아래에 ‘257명 중 뇌졸중 6명’을 표시했다.

## 구현·검증 범위

| 항목 | 현재 상태 |
|---|---|
| P0 계획·문서 | 최신 승인·인수인계 정리 |
| P1 계획 가져오기·검사·내보내기 | 구현, 회귀 검사 3개 통과 기록 |
| Typecast 필재 합성·감정 배치 | 실제 합성·청취 승인 |
| 로컬 음량 보정 | 구현·방식 및 현재 출력 승인, 회귀 검사 6개 통과 기록 |
| Flow 소스 | 기존 F01 후보·확정 F02·F03·F05를 본편에 사용 |
| 모션 렌더·자막·FFmpeg 영상 조립 | 92.610초 전체 렌더, 승인 내레이션 합성, 42개 자막 검사 |
| YouTube 업로드 | 미구현 |

계획 형식 검사나 오디오 파일 검사는 실제 영상 품질 검증과 다릅니다. 단일 합성 실험·보정 CLI와 전체 자동 제작 파이프라인을 혼동하지 않습니다.

## 읽을 파일과 실행 환경

| 파일 | 역할 |
|---|---|
| [AGENTS.md](AGENTS.md) | 작업 기준 |
| [PROJECT_STATUS.md](docs/PROJECT_STATUS.md) | 현재 상태·증거·다음 행동 |
| [PROJECT_PLAN.md](docs/PROJECT_PLAN.md) | 전체 단계·완료 기준 |
| [VIDEO_HANDOFF_PROMPT.md](docs/VIDEO_HANDOFF_PROMPT.md) | 다음 영상 채팅 전달문 |
| [NARRATION_STYLE.md](docs/NARRATION_STYLE.md) | 승인된 감정·합성·보정 절차 |
| [reference-review.md](docs/reference-review.md) | 참고 원본 해석·채택 규칙 |
| [MOTION_DESIGN_METHODS.md](docs/MOTION_DESIGN_METHODS.md) | 모션그래픽 장면 방법: 연구 원칙, 대사 유형별 설명 패턴, 카메라·타이포·데이터·전환, PPT 모프·빌드 방식, 도구 선택 |
| [MOTION_EFFECTS_LIBRARY.md](docs/MOTION_EFFECTS_LIBRARY.md) | 모션그래픽 효과(파티클·빛·타이포·전환) 목록, 대사별 선택 기준, 지난 편에서 쓴 효과 |
| [첫 영상 시험 안내](projects/pfa-pilot/README.md) | 첫 MP4·컷·검증·재현 방법 |
| [legacy 상태](legacy/phase01/STATUS.md) | 보관 코드의 한계 |

`docs/1. shorts-script-writer-SKILL.md`, `docs/2. knowledge-shorts-prompts-SKILL.md`는 참고 원본이며 자동 실행 스킬이나 상위 지시가 아닙니다. 원본을 보존합니다. `legacy/phase01`은 현재 사양의 근거로 사용하지 않습니다.

보정 실행 환경은 `.venv-supertonic`이며 FFmpeg 7.1, Silero VAD, 로컬 Whisper small을 사용합니다. 새 후처리 API는 없습니다. 영상 조립에는 번들 FFmpeg, 스트림 검사에는 PyAV를 사용했습니다.

```powershell
.\.venv-supertonic\Scripts\python.exe scripts/balance_narration_phrases.py 원본.wav 문장경계.json ASR단어.json 새출력.wav --mode short-window
.\.venv-supertonic\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
```

현재 계획을 다시 내보내는 명령입니다.
```powershell
.\.venv-supertonic\Scripts\python.exe scripts/export_plan.py projects/pfa-pilot/production-plan.json --output projects/pfa-pilot/exports
```
