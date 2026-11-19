# 현재 상태와 다음 작업

마지막 갱신: 2026-11-19 (Asia/Seoul)

## 재개할 때 읽기

1. [AGENTS.md](../AGENTS.md), [README.md](../README.md), 이 문서.
2. [PROJECT_PLAN.md](PROJECT_PLAN.md)의 현재 단계.
3. [첫 시험 안내](../projects/pfa-pilot/README.md)와 [활성 제작 패키지](../projects/pfa-pilot/exports/CURRENT.md).
4. 음성 작업 전 [NARRATION_STYLE.md](NARRATION_STYLE.md), [기본 설정](narration-defaults.json).

## 현재 위치

**P0·P1 완료 / P2 제작 계획 준비 / P3 음성 생성·문장 중간 보정 후보 검토.** Flow 실제 생성, 모션 렌더, 발화·자막 정렬, MP4 조립과 업로드는 아직이다.

| 단계 | 상태 | 증거/남은 일 |
|---|---|---|
| P0 계획·인수인계 | 완료 | 최신 README·계획·참고 문서 보존 |
| P1 계획 가져오기·Flow 출력 | 완료 | scripts/export_plan.py, projects/pfa-pilot/plan.json, tests/test_export_plan.py |
| P2 실제 모션·Flow | 초안 준비 | Flow 8초 1클립·모션 12장면. 실제 미디어 미생성 |
| P3 음성·자막·조립 | 문장 앞뒤 보존·중간 보정 후보 | Typecast 필재. 새 음량 기준 적용·청취 대기. 자막·영상 조립 미완료 |
| P4 약 150초 완성 | 미착수 | 먼저 약 29초 혼합 시험 |
| P5 YouTube 업로드 | 미착수 | OAuth 미연결 |
| P6 확장 자동화 | 보류 | 실제 제작 흐름 검증 후 |

## 최신 승인과 구현 증거

2026-11-19 최신 피드백 및 실행: 사용자는 강조 재합성본을 전체적으로 긍정 평가했으나 12~20초의 말소리가 작아지거나 힘이 빠진다고 지적했다. 이어 문장 첫 0.x초 보호 규칙을 적용한 작은 말소리 보정을 요청했다. 같은 `--mode short-window` 설정을 강조 재합성 원본 전체에 적용해 `outputs/typecast-piljae-pfa-emphasis-1.0x-v1/local-short-window-v1/narration_balanced.wav`를 생성했다. 92.610초, 정렬한 23문장 시작/끝 0.2초 PCM 동일, 원본 해시·길이·샘플레이트 유지, 감쇠 없음, 새 포화 0. 원본의 포화 27샘플과 +0.15dBTP는 유지했다. [실측](piljae-emphasis-local-level-results.json). 새 합성/API 호출 없음. 특정 초별 게인 예외나 설정 재튜닝 없음. ASR이 문장 중간에서 나눈 두 곳은 원문 문장 기준으로 연결했으며 음소 수준 정밀 정렬은 아니다. 보정본 청취는 미승인이다.

2026-11-19 최신 요청: 음량 보정 대신 핵심 말의 감정/강조 배치를 바꾸어 원고 전체를 재합성했다. [강조 기준·설정](NARRATION_EMPHASIS_TRIAL.md), `outputs/typecast-piljae-pfa-emphasis-1.0x-v1/narration.wav`, [합성 보고서](typecast-piljae-emphasis-1.0x-results.json). 필재/SSFM 3.1/1.0배속, 13개 의미 구간, 92.610초. 20줄 원문·순서·출력 설정 확인. 후처리 증폭은 적용하지 않은 비교본이며 청취 미승인. API 반환의 최대값 PCM 27샘플은 검토 항목으로 보존했다. 새 후처리 API 추가 없음. Typecast 기존 합성 API 성공 1회, 기본 네트워크 DNS 실패 기록 별도 보존. 향후 기본 속도 1.05배속과 기존 승인 강도값을 바꾸지는 않았다.

2026-11-19 전체 보정본 재출력 요청 완료: 같은 1.0배속 원본과 `--mode short-window` 공통 설정으로 `outputs/typecast-piljae-pfa-full-1.0x/local-short-window-v1-rerender/narration_full.wav`를 새로 생성했다. 전체 95.180초, 직전 동일 설정 출력과 SHA-256 일치, 원본·보호 영역 유지, 변경 영역 새 포화 0 확인. 원고별 추가 튜닝·새 합성 API 호출 없음. 청취 미승인 상태와 다음 별도 원고 검증은 유지한다.

**2026-11-19 최신 방향:** 사용자가 Auphonic을 제외하고 추가 후처리 API 없이 로컬 해결을 요청했다. 목적은 특정 예시 문장의 튜닝이 아닌 미래 자동화 규칙이다. [로컬 자동화 기준](LOCAL_AUDIO_POLICY.md)을 작성하고 기존 코드에 `--mode short-window` 후보를 추가했다. 동일 설정으로 필재 1.0/1.05배속과 Supertonic M3 세 파일을 실행했다. 원본 해시·길이·보호 영역 보존, 새 포화 0, 원본 샘플 감쇠 없음 확인. [실측](local-level-validation-results.json). 세 파일은 같은 원고 계열이라 다른 주제 일반화·실제 호흡 구분은 미검증이다. API 호출·추가 다운로드·설치 0. 전체 회귀 검사 9개 통과(음성 6개, 계획 내보내기 3개). 전체 제작 연동이나 청취 승인은 아직이다.

2026-11-19 후속 피드백: “103명은”의 작은 발음이 남아 있어 기존 후보는 아직 해결 완료가 아니다. 사용자 요청에 따라 [음량·호흡 처리 도구 조사](AUDIO_LEVELING_RESEARCH.md)를 작성했다. Auphonic, GitHub BreathTamer/Loudness Leveler, FFmpeg speechnorm의 공식 설명과 비용·자동화 한계를 확인했다. 설치·실행·음성 전송·새 보정은 하지 않았으며, 외부 도구의 실제 한국어 품질은 미검증이다.

2026-11-19 최신 요청으로 **원본의 주변 말소리와 비교하는 구절 단위 보정**을 구현했다. 현재 후보는 `scripts/balance_narration_phrases.py`와 `outputs/typecast-piljae-pfa-full-1.0x/relative-phrase-v1/narration_balanced.wav`. 51개 구절 중 18개 보정, 변경 약 18.76초, 길이 95.180초 유지. 구절 RMS 편차 6.55→3.92dB. 23문장 앞뒤 0.2초 및 낮은/애매한 VAD 확률 샘플 불변·새 클리핑 없음 확인. 구절별 이유는 [판단표](piljae-relative-phrase-review.md), [수치](piljae-relative-phrase-results.json). 청취 확인 대기이며 앞으로의 자동화 기준으로 아직 확정 승인된 것은 아니다. 고정 -22dB 판단·단어 전체 보호·추가 VAD 0.16초 패딩은 철회했다.

필재/SSFM 3.1/**1.05배속**과 내용별 감정은 향후 기본값이다. 첫 영상 시험에서는 **1.0배속·95.180초** 원본 기반 중간 보정 후보를 검토한다. 새 기본 속도 변경이나 새 음성 합성 승인을 추정하지 않는다. 이번 작업은 API 호출·Flow 크레딧 사용 없이 진행했다.

P1: JSON 계획 검사와 원고·근거·편집 시트·독립 Flow 프롬프트 내보내기를 구현했다. 생성 길이와 사용 범위, 음성 구간과 시각 장면을 분리했다. 출력은 계획 해시별로 보존하고 CURRENT.md가 활성 버전만 가리킨다. 이전 프롬프트를 자동으로 모두 읽지 않는다. 단위 테스트 3개 통과(정상 가변 타임라인·독립 프롬프트, 17개 오류 변형 거부, 재출력·수동 수정 보호). 원문 20문장 동일, 입력 WAV 해시·95.180초 길이 일치 검증.

## 바로 다음 행동

**현재 들을 파일:** `outputs/typecast-piljae-pfa-emphasis-1.0x-v1/local-short-window-v1/narration_balanced.wav`. 같은 폴더의 `compare_10.5-21_original_then_balanced.wav`는 문제 구간 앞뒤를 원본→보정 순서로 들려준다. 전체적으로 긍정 평가된 감정 배치를 유지하고, 새 보정의 작은 발음·호흡·억양을 확인한다. 최종 음질 합격이나 향후 1.05배속 설정 변경으로 표시하지 않는다.

**가장 최근 비교:** `outputs/typecast-piljae-pfa-emphasis-1.0x-v1/narration.wav`에서 핵심 비교·정정·제한·결론의 발음과 억양을 청취한다. 의미별 연출 기준으로 평가하며, 결과가 승인되기 전에는 감정 재배치가 음량 문제를 해결했다고 쓰지 않는다. 아래 로컬 보정 검증은 별도 후보로 유지한다.

새 강조본 전체 측정은 -18.09 LUFS / +0.15dBTP / LRA 3.4LU다. 로컬 ASR에서 원고 내용과 수치·결론 순서를 확인했지만 전문어 인식 오류가 있어 발음 합격으로 표시하지 않았다. 검사 결과는 같은 출력 폴더의 `quality-review.json`. 출력 원본 무수정, 청취·최종 피크 검토 대기.

**최신 피드백 우선:** `outputs/typecast-piljae-pfa-full-1.0x/local-short-window-v1/narration.wav`와 같은 폴더의 `compare_original_then_local.wav`를 청취하고, 다음은 별도 원고로 독립 검증한다. 구절 평균으로 짧은 발음까지 충분히 크다고 판단하지 않는다. `LOCAL_AUDIO_POLICY.md`의 공통 규칙을 따르고 특정 문구·초별 예외를 추가하지 않는다. 모든 후보는 청취 미승인이다. 영상 계획 경로는 이전 후보로 남아 있어 새 파일을 승인 없이 제작용 확정으로 표시하지 않는다. 필재 원본의 기존 true peak +0.05/+0.10dBTP는 유지됐으므로 최종 출력 피크 검사는 별도로 남는다. 범용 자동 정렬·전체 제작 연결도 미구현이다.

심방세동 AVANT GUARD 원고의 [전체 콘티](../projects/pfa-pilot/exports/CURRENT.md)를 만들었다. 먼저 약 29초: 질문/대상 모션 → Flow F01 단면과 표적 설명 → 배정 모션. 전체는 Flow 8초 한 클립과 모션 12장면이다. 새 시안 charcoal #111111·회색 모형·붉은 강조는 레퍼런스 추출색이 아니다. 생성 시도 예산과 실제 Flow UI 모델/크레딧은 미확인이다.

1. 기존 음성에 원문을 정렬해 앞부분 자막 및 컷 경계를 확정한다. 현재 내부 시간은 초안이며 정확한 문장 타임스탬프가 아니다.
2. M01/M02 움직이는 모션그래픽 실제 렌더. Remotion은 후보이며 아직 설치/선정 전이다.
3. 활성 패키지의 flow-F01.txt로 Flow 웹 생성. 받아온 영상은 projects/pfa-pilot/media/flow/F01-take01.mp4에 보관하고 실제 3샷·해부학·강조·연속성을 검토한다. Flow 대기 동안 1~2번 진행 가능.
4. 실제 영상과 자막·음성으로 약 29초 MP4 조립 후 재생 검토한다. 문서/구조 통과를 영상 완료로 보고하지 않는다.

## 근거 확인 범위와 환경

NEJM 논문은 PubMed 초록을 직접 확인했고, 연구 수행기관 Cleveland Clinic 설명으로 치료 부위·안전성 사건·프로토콜 보완을 확인했다. NEJM 본문은 403으로 미열람했다. 310명은 무작위 효과 비교, 257명은 합산 PFA 안전성 분석. 56%/약30%는 Kaplan–Meier 추정치로 표시한다. 출처 및 주장별 제한은 계획/내보낸 sources.md에 있다.

FFmpeg 7.1은 .venv-supertonic의 imageio-ffmpeg 0.6.0 포함 실행 파일로 설치됐다. PATH의 ffmpeg/ffprobe·영상 조립 연동은 아직이다. 기존 Qwen·Supertonic은 비교 실험으로 보존하며 제작 기본 음성은 Typecast다. 원본 참고 MD와 legacy/phase01은 변경 없이 보존한다.

## 이전 실험 이력 — 현재 기본값은 위 최신 확정 참조

아래의 '최신', '평가 대기', '미정'은 각 실험 당시 기록이며 현재 기본값보다 우선하지 않는다.

최신 요청 완료: 같은 전체 원고·7구간 감정·휴지·음량 설정에서 audio_tempo만 1.05로 바꿔 재합성했다. `outputs/typecast-piljae-pfa-full-1.05x/narration.wav`, 88.032초, API 요청 1회 10.01초. 요청 비교에서 속도 외 변경 없음을 확인했고 기존 1.1배속 WAV 해시도 유지됐다. API 원본의 최대값 PCM 71샘플을 보간해 최종 포화 0, 다른 샘플과 길이 동일 검사 통과. 원본도 별도 보존. [1.05배속 결과](typecast-piljae-full-1.05x-results.json). 사용자 청취 검토 대기이며 이 요청을 향후 기본 속도 변경으로 자동 해석하지 않는다.

최신 전체 합성 완료: 사용자 심방세동/PFA 원고 20줄(화자명 '필재' 제외)을 Typecast 필재/SSFM 3.1/1.1배속으로 생성했다. `outputs/typecast-piljae-pfa-full-1.1x/narration.wav`, 85.126초. 원문·순서를 유지하고 7구간별 Smart/normal/약한 toneup/tonedown을 적용했다. `emotion-plan.json`과 `request.json` 보존. Compose 호출 1회, 760자. API 원본 7개 최대값 PCM 샘플을 이웃 샘플 선형 보간으로 보정했고, 다른 샘플·길이 동일 및 최종 클리핑 0 검증. 원본은 `narration_api_original.wav`에 보존했다. 최초 검사가 중단돼 요청 소요 시간은 기록되지 않았다. [결과 기록](typecast-piljae-full-results.json). 자막은 생성하지 않았으며 발음·감정 자연스러움은 사용자 청취 검토 대기다. 제공 원고 음성화이며 의학적 사실 확인을 수행한 것은 아니다. 다음은 전체 음성 피드백 반영이다.

최신 표현 질문 대응: Supertonic 공식 인라인 laugh/sigh/breath 지원과 설치 SDK에 emotion/intensity 인자가 없음을 확인했다. M3/1.1배속으로 기본 vs 한숨 태그 시험을 `outputs/supertonic3-expression-test/baseline_then_sigh.wav`에 생성했다. 파일 검증은 통과했으나 실제 한숨 효과·자연스러움은 청취 평가 대기다. 기존 10개 비교 샘플에는 표현 태그를 넣지 않았다. M3는 예시 화자이며 최종 선택은 미정이다.

최신 요청 완료: **Typecast 필재 1.1배속 경로는 유지**하면서 Supertonic 3를 `.venv-supertonic/`에 설치했다. 공식 모델 18파일의 크기·LFS 해시를 확인하고 남성 M1~M5 × 1.0/1.1배속 10개를 CPU에서 생성했다. 입력은 필재와 같은 133자. `outputs/supertonic3-male-comparison/`에 개별 WAV와 목소리별 비교 WAV(1.0 → 1초 쉼 → 1.1) 5개를 보관했다. 파일 검증 통과, 사용자 청취 평가 대기. [설치·재실행 안내](SUPERTONIC3_RESEARCH.md), [실측](supertonic3-comparison-results.json). 재실행은 `.\\.venv-supertonic\\Scripts\\python.exe scripts/supertonic_compare.py`. 다음 행동은 사용자가 선호하는 M번호·속도를 확인하는 것이다. Typecast를 철회하거나 Supertonic을 제작용으로 채택했다고 추정하지 않는다. Sohee 1.1배속 음질 불만도 유지한다.

최신 테스트 완료: 사용자의 1.1배속 요청으로 필재/SSFM 3.1/normal/피치 0 샘플을 한 번 생성했다. 원고의 화자명 '필재'를 제외한 앞 네 문장(133자), 결과는 `outputs/typecast-piljae-1.1x/sample.wav` 15.0초, 요청 소요 2.724초, WAV 44.1kHz 모노 PCM16. [측정 기록](typecast-piljae-sample-results.json). WAV 구조·프레임 수를 검사했으며 청취 자연스러움은 사용자 평가 대기다. 한 번의 측정으로 장문 생성 속도를 보장하지 않는다. 자막은 생성하지 않았다. 다음은 이 샘플에 대한 청취 피드백 반영이다.

최신 후속 요청 완료: `.env`의 키로 `GET /v3/voices` 인증 조회 성공. 636개 응답 중 필재(Piljae) 확인. ID `tc_68257f68bc6e3c161ab5078d`, v21/v30/v31 지원. v30/v31은 normal/happy/sad/angry/tonedown/toneup/whisper 지원. [실제 조회 결과](typecast-piljae-check.json)에 키 없이 기록했다. 최초 샌드박스 네트워크 실패 후 허용된 네트워크 실행에서 성공했다. 음성 생성은 하지 않았다. `.env`나 인증 헤더를 출력하지 않는다.

연동 계획은 [TYPECAST_INTEGRATION.md](TYPECAST_INTEGRATION.md)를 따른다. 목록 조회 및 단일 합성 요청은 성공했고, SDK 설치·재사용 가능한 합성 CLI·자막 통합은 아직 하지 않았다.

과거 실험: Ryan·Aiden·Uncle_Fu 비교 샘플은 `outputs/tts-male-comparison/`과 [측정 기록](tts-male-results.json)에 보존했다. 현재 재개할 작업은 이 로컬 후보 선정이 아니다.

과거 실험: Sohee 장문은 `outputs/sohee-pfa-narration/narration.wav` 152.8초, `narration_1.1x.wav` 약 138.91초다. 21구간 순서·프레임 합계·클리핑을 검사했다. 제공 원고 음성화이며 의학 내용 사실 검증은 하지 않았다. 원문의 첫 '필재'도 읽혔으므로 Typecast 시험 시 화자명과 발화 본문을 구분한다. 짧은 샘플에 대한 초기 긍정 평가는 이후 장문 청취 후 Typecast 전환 결정으로 대체됐다.

보존 환경: Qwen 0.6B는 `.venv-tts/`, 모델은 `models/`에 있다. 삭제하거나 재설치하지 않았다. 로컬 샘플의 기술적 생성 성공과 사용자의 제작 품질 채택은 별개다. 최신 우선순위는 Typecast 필재 확인·연동이며 아래 P1 계획은 전체 제작 파이프라인 작업으로 유지한다.

재실행: `./.venv-tts/Scripts/python.exe scripts/tts_smoke.py`

검증: 모델 LFS 해시·CUDA 연산·`pip check`·24kHz 모노 PCM16 WAV 재읽기 통과. 원문의 실제 발음 일치·자연스러움은 별도 청취 확인이 필요하다. 장문 합성 결과는 위 최신 요청 기록을 참조한다. 음성 14.64~16.72초당 생성 17.85~28.44초, 최대 예약 GPU 메모리 2,972 MiB. [실행 안내](TTS_LOCAL.md), [실측 기록](tts-smoke-results.json), [설치 버전](../scripts/requirements-tts.lock.txt)을 참조한다. 모델과 환경은 Git에서 제외했다.

**P1: 에이전트 작성 JSON을 가져와 검증하고 제작 패키지를 출력하는 최소 CLI를 구현한다.**

1. 환경과 현재 파일 상태를 재확인한다. 기존 사용자 변경을 보존한다.
2. 대본 구간·시각 장면·생성 클립·편집 사용 구간을 분리한 최소 형식을 만든다.
3. API 없이 가져오기 → 검사 → 대본/편집 시트/독립 3샷 프롬프트 출력까지 연결한다.
4. placeholder 테스트 입력은 테스트라고 명시한다. 실제 주제의 대본이나 영상 제작 완료로 보고하지 않는다.
5. 잘못된 시간·참조·프롬프트 누락·재출력 처리를 검사하고 실행 명령과 결과를 여기에 기록한다.

이 단계는 첫 주제가 없어도 진행할 수 있다. 실제 콘텐츠로 넘어갈 때 주제·스타일·Flow 예산을 확인한다. 대화에서 'AI 환각'은 예시로만 등장했으므로 첫 영상 주제로 확정하지 않는다.

## 반복하면 안 되는 실수

- 고정 PNG 금지를 '가급적'으로 완화하지 않기.
- Flow 기본 3샷을 비용 때문에 1샷으로 바꾸지 않기.
- 움직임을 막는 제약이나 설명 장치 전부 후반 이관으로 영상의 사건을 없애지 않기.
- 사실 검증을 이유로 재미있는 서사를 백과사전식 요약으로 약화하지 않기.
- legacy의 10 × 15초, AI 6/10, 유료 LLM API 의존을 현재 기본으로 복원하지 않기.
- Typecast 필재/1.05배속/내용별 감정은 확정됐다. 로컬 모델 최종 선정·첫 주제·예산·배경색까지 정해졌다고 추정하지 않기.
- Flow 수동 전달 경로와 완전 무인 자동화를 혼동하지 않기.

## 작업 종료 시 갱신 항목

- 현재 단계와 완료된 산출물 경로.
- 실제 실행 명령 및 성공/실패, 검증하지 못한 범위.
- 막힌 원인과 필요한 입력. 비밀키·토큰은 기록하지 않음.
- 다음 한 가지 행동과 그 전에 확인할 조건.
- 변경된 결정은 README/계획에도 반영. 미완료를 완료로 표시하지 않음.

