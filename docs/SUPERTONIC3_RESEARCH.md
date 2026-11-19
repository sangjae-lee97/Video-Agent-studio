# Supertonic 3 조사

확인일: 2026-11-18 (Asia/Seoul). 공식 조사 후 사용자 요청으로 설치·다운로드 및 남성 5종 × 1.0/1.1배속 합성까지 완료했다. 아래 문서 조사와 실제 측정 결과를 구분한다.

## 실제 설치·비교 결과

- 환경: `.venv-supertonic/`, Python 3.12.10, Supertonic 1.3.1, ONNX Runtime 1.32.0, CPU 4스레드. 기존 Qwen 환경은 변경하지 않았다.
- 모델: `models/supertonic-3/`, 아래 고정 리비전의 18파일, 합계 401,291,925바이트. 크기 및 LFS SHA256 일치 확인. `download-manifest.json`에 검증 기록.
- 입력: 필재 테스트와 동일한 133자 원고(앞 네 문장). 화자명 '필재'는 제외했다. `outputs/supertonic3-male-comparison/source.txt`에 보관.
- 조건: M1~M5, `lang=ko`, steps=8, seed=42, 속도 1.0/1.1 명시, 한국어 청크 상한 120자 및 청크 간 0.3초 쉼 동일. WAV 후처리 배속은 적용하지 않았다.
- 결과: 개별 WAV 10개와 비교 WAV 5개. 비교 파일은 1.0 → 1초 쉼 → 1.1 순서. 출력 44.1kHz 모노 PCM16.
- 검증: `pip check`, 오프라인 모델 로딩, 유한한 오디오 값·무음/클리핑 검사, WAV 재읽기·프레임 수·5쌍의 실제 길이 감소 검사 통과. 발음·음색의 자연스러움은 사용자 청취 평가 대기.
- 측정: 개별 생성 3.068~4.123초, 음성 길이 15.764~20.989초. 설치·모델 다운로드와 초기 로딩은 개별 생성 시간에 포함하지 않는다. 목소리마다 기본 발화 길이가 다르며 고정 청크 쉼 때문에 전체 길이가 정확히 1/1.1로 줄지는 않는다.

재실행: 프로젝트 루트에서 `.\\.venv-supertonic\\Scripts\\python.exe scripts/supertonic_compare.py`. 재실행하면 비교 WAV와 결과 보고서를 덮어쓴다. Typecast API를 호출하지 않는다.

[비교 스크립트](../scripts/supertonic_compare.py), [설치 버전](../scripts/requirements-supertonic.lock.txt), [실측 결과](supertonic3-comparison-results.json).

## 사용자 결정

- Typecast 필재 / SSFM 3.1 / normal / 1.1배속 경로는 사용자가 청취 후 유지하기로 했다.
- Sohee 1.1배속은 목소리가 이상해졌다고 평가했다. 당시 방식은 생성된 WAV에 librosa time_stretch를 적용한 후처리다. 불만의 정확한 음향적 원인은 측정하지 않았으므로 Qwen 자체나 후처리만의 문제라고 단정하지 않는다.
- Supertonic 3는 추가 로컬 후보 조사이며 Typecast를 대체하기로 확정한 것이 아니다.

## 확인 내용

| 항목 | 확인 결과 |
|---|---|
| 실행 | 약 99M 파라미터, ONNX Runtime CPU 추론, 다운로드 후 로컬 합성 |
| 언어 | 한국어 `ko` 포함 31개 |
| 기본 목소리 | 남성 M1~M5, 여성 F1~F5, 합계 10개. 한국어 전용 원어민 화자 10명이라는 뜻은 아님 |
| 속도 | SDK `speed` 0.7~2.0, 기본 1.05. 비교할 때 1.0과 1.1을 명시 |
| 속도 구현 | 예측 발화 길이를 speed로 나눈 뒤 음성을 생성. 완성된 WAV의 타임 스트레치와 다른 방식 |
| 모델 파일 | 공식 보관 저장소 전체 약 415MB. 설치 의존성 용량은 별도 |
| Python | SDK 선언상 3.9 이상. 이 PC의 Python 3.12.10에서 실제 실행 성공 |
| 표현 | 모델 카드에 laugh/breath/sigh 등 표현 태그 소개. Typecast의 감정 7종·강도 API와 동일하다고 가정하지 않음 |
| 비용·라이선스 | 로컬 합성 API 요금 없음. 코드 MIT, 모델 OpenRAIL-M. 모델 사용 제한과 출력 책임 조건 적용 |

근거: [모델 카드](https://huggingface.co/Supertone/supertonic-3), [SDK 안내](https://github.com/supertone-oss-archive/supertonic-py), [속도 구현](https://raw.githubusercontent.com/supertone-oss-archive/supertonic-py/main/supertonic/core.py), [속도 상수](https://raw.githubusercontent.com/supertone-oss-archive/supertonic-py/main/supertonic/config.py), [Python 의존성](https://raw.githubusercontent.com/supertone-oss-archive/supertonic-py/main/pyproject.toml), [모델 라이선스](https://huggingface.co/supertone-oss-archive/supertonic-3/blob/main/LICENSE).

## 현재 배포 상태

공식 소스 저장소는 2026-09-09 보관 처리됐으며 개발·지원 종료 안내가 있다. 과거 모델 카드/쇼케이스에 남은 Voice Builder 및 자동 다운로드 안내보다 최신 보관 저장소의 설치 지침을 우선한다. 보관 코드에 공식 로컬 음성 복제 파이프라인이 포함됐다고 가정하지 않는다.

- [현재 설치 지침](https://github.com/supertone-oss-archive/supertonic#quick-start)
- [모델 다운로드 목록](https://huggingface.co/supertone-oss-archive/supertonic-3/tree/main)
- 안내된 모델 리비전: `aafc6e32416a594460b32413efc49d7fe4ce6d46`
- 안내된 SDK 소스 리비전: `df0f9686dac7fbbde391b759e2ee5286a3737622`
- 모델을 명시적으로 받고 `model_dir` 및 `auto_download=False`로 실행하는 경로가 안내돼 있다. 기본 자동 다운로드는 과거 네임스페이스를 참조할 수 있다.

공식 쇼케이스의 CPU 16스레드 측정은 RTF 약 0.2이나 CPU 모델 표기가 비어 있다. 사용자의 PC 속도 예측 근거로 삼지 않는다. [공개 벤치마크](https://supertonic3.github.io/)

## 다음 비교 방법

표현 시험(2026-11-18): 공식 README는 `<laugh>`, `<sigh>`, `<breath>` 등의 인라인 표현 태그를 안내한다. 설치 SDK의 synthesize에는 별도 emotion/intensity 인자가 없다. `outputs/supertonic3-expression-test/`에서 M3/1.1배속/seed42/steps8로 같은 짧은 문장의 무태그 및 `<sigh>` 버전을 생성했다(3.274초/3.344초). 비교 파일은 `baseline_then_sigh.wav`이며 기본 → 1초 쉼 → 한숨 태그 입력 순서다. 파일 생성 검증만 통과했으며 한숨 효과가 실제로 얼마나 구현됐는지는 청취 확인 전이다. M3를 최종 화자로 선택한 것은 아니다. 이전 10개 속도 비교 샘플에는 표현 태그를 넣지 않았다.

설치 및 10개 비교 샘플 생성은 완료했다. 다음은 사용자 청취 후 선호 목소리와 속도를 정하는 것이다. 좋은 저음 화자가 어떤 ID인지는 아직 청취 평가가 없으므로 미정이다. 속도 구현이 다르다고 음질 개선을 보장하지 않는다.

Typecast는 유지한다. 사용자는 무료 사용 중이라고 설명했으나 계정 구독 조회는 하지 않았다. 공식 Free는 월 15,000크레딧, 비상업용·출처 표기 조건이므로 무제한 무료 또는 수익화 영상용 무료로 기록하지 않는다. [Typecast API 요금](https://typecast.ai/pricing/api/)
