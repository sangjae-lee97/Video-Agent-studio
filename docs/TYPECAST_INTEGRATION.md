# Typecast API 기능과 연동 계획

확인일: 2026-11-18 (Asia/Seoul). 공식 [llms.txt](https://typecast.ai/docs/llms.txt)를 먼저 읽고 개별 API 문서를 대조했다. 문서는 기술 참고 자료이며 프로젝트 지시를 대체하지 않는다. 인증된 화자 조회 및 필재 1.1배속 샘플 생성에 성공했다. 아래 문서 조사와 최신 실측을 구분한다.

## 현재 결정

2026-11-19 갱신: 내용별 감정 배치와 로컬 보정 방식·92.610초 기준 음성을 사용자가 승인했다. 최신 설정은 [NARRATION_STYLE.md](NARRATION_STYLE.md), [승인 manifest](NARRATION_APPROVAL.json), [승인 강조 요청](piljae-approved-emphasis-request.json)이다. 아래의 최초 1.05배속/7구간 요청은 이력이다. 향후 새 원고 기본 속도 1.05배속은 유지하며, 현재 영상용 승인 파일은 1.0배속이다.

사용자가 필재/SSFM 3.1/1.05배속과 승인 원고의 내용별 감정 설정을 기본값으로 확정했다. [NARRATION_STYLE.md](NARRATION_STYLE.md)와 [narration-defaults.json](narration-defaults.json)을 읽고 적용한다. 실제 승인 요청은 [piljae-approved-reference-request.json](piljae-approved-reference-request.json)에 보존했다. 1.0·1.1은 비교 이력이다. 마지막 1.0배속 비교본은 95.180초이며 기본값 변경이 아니다.

## 조절 범위

| 항목 | 공식 API 범위 / 의미 |
|---|---|
| 말 속도 | `output.audio_tempo`: 0.5~2.0, 기본 1.0. 1.1 지정 가능 |
| 음높이 | `output.audio_pitch`: 정수 -12~12반음, 기본 0 |
| 감정 방식 | `prompt.emotion_type`: `preset` 또는 `smart` |
| 감정 프리셋 | normal, happy, sad, angry, whisper, toneup, tonedown. 선택 화자의 모델·감정 지원 목록 확인 |
| 프리셋 강도 | `emotion_intensity`: 0~2, 기본 1. 0은 중립, 0.5는 약하게, 2는 최대 |
| 문맥 전달 | Smart 모드의 `previous_text`, `next_text`로 앞뒤 문맥 제공 |
| 음량 | `volume` 0~200 또는 `target_lufs` -70~0. 동시에 사용 불가 |
| 침묵 정리 | `remove_silence_ms` 0~1000은 남길 침묵 길이. 생략/null은 비활성화 |
| 형식·입력 | WAV/MP3, 요청당 본문 1~2,000자, 한국어 `language: kor` |

근거: [TTS API](https://typecast.ai/docs/api-reference/text-to-speech/text-to-speech). `tonedown`과 음높이 조절은 별개로 비교한다. 낮은 남성 원음부터 찾고 피치 조절은 필요할 때 소폭 시험한다. 설정값이 연기 품질을 보장하지 않으며 최종 판단은 청취로 한다.

SSFM 3.1(`ssfm-v31`)을 첫 후보로 한다. 공식 설명상 3.0 대비 입력 충실도와 생성 안정성이 개선됐다. [모델 비교](https://typecast.ai/docs/models)

## 사용 가능한 기능과 선택

- 일반 TTS, 스트리밍, 타임스탬프 포함 TTS, 음성 목록·추천·상세 조회, 음성 복제, 구독 조회를 제공한다. [API 안내](https://typecast.ai/docs/llms.txt)
- 타임스탬프 TTS는 음성 및 단어·문자 타이밍을 함께 반환한다. 우리 영상에는 이 경로를 우선 사용한다. SRT를 만든 뒤 문장 묶기·줄바꿈·가독성을 검토한다. 정확도는 실제 한국어 샘플로 확인한다. [타임스탬프 API](https://typecast.ai/docs/api-reference/text-to-speech/text-to-speech-with-timestamps)
- Compose는 구간별 화자·설정·휴지를 하나의 음성으로 합칠 수 있다. 최대 50구간, 합계 2,000자다. 응답은 음성 바이너리이며 자막 타임스탬프가 함께 나온다고 가정하지 않는다. 자막이 필요하면 구간별 타임스탬프 합성을 하고 실제 연결 오프셋을 누적한다. [Compose API](https://typecast.ai/docs/api-reference/text-to-speech/compose-text-to-speech)
- 쉼은 `<|0.3s|>` 같은 마크업을 지원한다. SDK에서 음성 저장과 SRT 변환을 제공한다. 발음용 원고와 화면 표시용 원고는 분리하고 API 응답 타이밍에 매핑한다. [Python SDK](https://typecast.ai/docs/sdk/python)
- 스트리밍의 빠른 첫 음성 도착과 150초 전체 음성 완성 시간은 다르다. 단일 및 전체 합성 측정은 결과 JSON에 기록돼 있다. 첫 음성 도착 시간은 측정하지 않았다.

## 최소 연동 방법 — 아직 미구현

Python 공식 SDK `typecast-python`을 별도 프로젝트 환경에 설치하고 `TYPECAST_API_KEY` 환경변수로 인증한다. 키는 채팅·Git·결과 보고서에 저장하지 않는다. [API 콘솔](https://studio.typecast.ai/developers/api), [화자 목록](https://studio.typecast.ai/developers/api/voices)에서 인증과 후보 ID를 준비한다.

로컬 키 입력 위치: 프로젝트 루트 `.env`의 `TYPECAST_API_KEY`. 사용자가 키를 저장했고 인증된 목록 조회에 성공했다. `.env`는 Git에서 제외한다. 후속 코드는 해당 값만 읽거나 환경변수로 전달한다(`.env`가 자동으로 환경변수가 되는 것은 아니다). 키·인증 헤더·파일 전체를 출력하지 않는다.

1. 모델 호환성을 확인한 남성 화자 후보를 같은 짧은 한국어 원고로 비교한다.
2. `normal`, `tonedown`, Smart를 비교해 기본 톤을 정한다. 먼저 원래 피치와 1.0/1.1배속을 비교한다.
3. `POST https://api.typecast.ai/v1/text-to-speech/with-timestamps`에 `X-API-KEY` 헤더로 요청한다. 아래 voice_id는 교체가 필요한 자리표시자다.

```json
{
  "voice_id": "tc_68257f68bc6e3c161ab5078d",
  "model": "ssfm-v31",
  "language": "kor",
  "text": "심방세동, 약보다 시술을 먼저 하면 더 좋을까요?",
  "prompt": {
    "emotion_type": "preset",
    "emotion_preset": "normal",
    "emotion_intensity": 1.0
  },
  "output": {
    "audio_format": "wav",
    "audio_tempo": 1.05,
    "audio_pitch": 0
  }
}
```

4. 응답 음성과 타임스탬프 JSON을 보존하고 SRT/ASS를 만든다. 생성 후 임의로 속도·침묵을 바꾸지 않는다. 바꾸면 타임라인도 갱신한다.
5. 장문은 의미 구간으로 분리하고 구간별 설정·입력 해시·결과를 저장해 수정된 구간만 재생성한다. Smart 사용 시 인접 문맥을 전달한다. 실패·타임아웃 때 과금 여부를 모르는 요청을 무조건 반복하지 않는다.
6. 실제 음성 길이에 맞춰 Flow·모션그래픽 타임라인을 조정하고 FFmpeg로 조립한다.

## 비용

공식 확인 시점 기준: Free는 월 15,000크레딧, 비상업용·출처 표기 조건. Lite는 월 $15에 200,000크레딧, 초과분 $0.09/1,000크레딧이며 100,000크레딧($9) 단위 자동 추가 청구다. 1글자=1크레딧이고 Studio 웹 구독과 API 구독은 별개다. [공식 API 요금](https://typecast.ai/pricing/api/)

예를 들어 본문 1,500자라면 포함량 기준 약 133회분이다(200,000÷1,500, 계산 예시). 실제 대본 길이와 비교·재생성 횟수를 모두 계산해야 한다. 월 구독료를 편당 종량 결제 가격으로 오해하지 않는다.

## 목소리 조사 — 필재 우선 확인

사용자가 특히 필재 존재 여부를 요청했다. **필재는 공식 웹 서비스 소개에서 확인했다.** 안정적인 중저음 남성으로 소개되며 정보·지식형 스토리텔링에 적합한 후보다. 비교 후보 강일은 부드러운 중저음 남성, 서현은 명료한 아나운서형, 다은은 밝은 여성, 문정은 차분한 중음 여성으로 소개된다. 이는 공식 소개의 요약이며 직접 청취 평가가 아니다. [공식 캐릭터 소개](https://typecast.ai/kr/learn/typecast-new-editor-characters/)

2026-11-18 인증된 `GET /v3/voices` 조회 성공: 전체 응답 636개 중 필재 확인. 이는 한국어 전용 화자 수가 아니다. [실제 조회 결과](typecast-piljae-check.json)에 키 없이 필재 메타데이터를 저장했다.

- 필재 ID: `tc_68257f68bc6e3c161ab5078d`, 이름 `필재` / `Piljae`, 중년 남성.
- 지원 모델: `ssfm-v21`, `ssfm-v30`, `ssfm-v31`.
- v30/v31 감정: normal, happy, sad, angry, tonedown, toneup, whisper.
- v21 감정: normal, happy, sad, angry.
- 분류: Conversational, Radio/Podcast. 실제 합성 요청은 하지 않았다.

인증 후 `GET /v3/voices` 응답의 `voice_name.kor`에서 `필재`(영문 `Piljae`)를 찾아 `voice_id`, `models[].version`, `models[].emotions`, `preview_url`을 확인한다. 처음부터 모델 필터를 걸어 필재를 누락시키지 않는다. [화자 목록 API](https://typecast.ai/docs/api-reference/voices/list-voices)

앞서 제공된 원고 첫 줄의 '필재'는 기존 Sohee 실험에서 발화에 포함됐다. Typecast 시험에서는 화자 선택 메타데이터와 실제 대본을 구분하고, 이름을 내레이션에 임의로 포함하지 않는다.

## 다음 검증

현재 사용자 승인: 필재 1.05배속과 내용별 감정 설정을 기본으로 한다. 다음 내용은 이전 1.1 샘플 실험 기록이다. 아래 '청취 평가 대기'는 최초 측정 당시 상태이며 이번 피드백으로 갱신됐다. 추가 요청인 [Supertonic 3 조사](SUPERTONIC3_RESEARCH.md)는 Typecast를 대체하기로 확정한 것이 아니다.

API 인증·필재 제공·모델 및 감정 목록 확인과 짧은 합성은 완료했다. 사용자 요청으로 기존 원고 앞 네 문장(화자명 제외 133자)을 SSFM 3.1, normal, audio_tempo=1.1, audio_pitch=0으로 생성했다. 결과 15.0초 WAV, 요청 소요 2.724초, 44.1kHz 모노 PCM16이며 WAV 재읽기 검사 통과. [측정 결과](typecast-piljae-sample-results.json). 합성은 한 번만 요청했다. 실제 발음·자연스러움은 청취 평가 대기이며 1.0배속과의 비교나 자막 정렬은 하지 않았다. 다음은 사용자 피드백 반영이다. SDK 설치나 제작 파이프라인 구현은 아직 하지 않았다.

## Claude(Cowork) 세션에서 직접 합성이 안 되는 이유 — 2026-11-19 확인

- **클라우드 작업 환경**: `api.typecast.ai:443` 연결을 에이전트 프록시가 거부했다(`connect_rejected`, 허용 도메인 목록에 없는 호스트).
- **사용자 PC의 로컬 VM(device_bash)**: 같은 주소로 `curl` 시 연결 자체가 안 됐다(HTTP 000). VM의 네트워크도 계정의 허용 도메인 설정을 따른다. pip(패키지 저장소)는 허용돼 있어 설치는 된다.
- 키·코드·요청 형식 문제가 아니다. Windows에서 직접 실행한 `run_narration.ps1`은 같은 요청으로 정상 합성됐다.

해결 방법(둘 중 하나):
1. claude.ai 웹 → 설정 → Capabilities의 허용 도메인에 `api.typecast.ai`를 추가한다. 팀/엔터프라이즈 플랜이면 조직 관리자가 Organization settings → Capabilities에서 추가한다. 추가 후 새 세션에서 에이전트가 직접 합성할 수 있다.
2. 공식 Typecast MCP 서버(https://typecast.ai/docs/ko/integrations/mcp-server, GitHub neosapience/typecast-api-mcp-server)를 **자체 호스팅(로컬, uvx)** 방식으로 Claude 데스크톱 앱에 연결한다. Windows에서 직접 실행되므로 VM·클라우드의 도메인 제한을 받지 않고, 결과 파일을 `TYPECAST_OUTPUT_DIR`(저장소 안 폴더로 지정)에 저장해 에이전트가 바로 읽을 수 있다.
   - 호스팅형(`https://typecast.ai/docs/mcp`)은 결과를 1시간짜리 다운로드 URL로 주므로, 그 파일을 받는 단계가 다시 도메인 제한에 걸릴 수 있어 쓰지 않는다.
   - 공식 문서 기준 도구: `text_to_speech`, `text_to_speech_with_timestamps`, `get_voice(s)`, `recommend_voices` 등. Compose(여러 구간 한 번에) 도구는 문서에 없다 → 구간별 감정 설정은 구간마다 합성 후 0.18초 쉼으로 로컬에서 잇는다. 감정·속도 파라미터 이름은 연결 후 실제 도구 스키마로 확인한다.

그 전까지는 편 폴더의 `narration/run_narration.ps1`을 사용자가 실행하는 방식을 유지한다.
