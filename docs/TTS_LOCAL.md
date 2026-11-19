# 로컬 한국어 TTS 실험

이 문서는 Qwen3-TTS 0.6B 실험을 재현하기 위한 과거 실험 기록이다. **2026-11-18 최신 결정: 사용자가 장문과 1.1배속 음성을 검토한 뒤 Typecast로 전환했다. 로컬 TTS는 기본 제작 경로가 아니다.** 현재 작업은 [Typecast 연동 계획](TYPECAST_INTEGRATION.md)을 따른다. 아래 설치 환경과 샘플은 보존한다.

## 구성

최신 피드백: 사용자는 Sohee의 1.1배속 결과에서 목소리가 이상해졌다고 평가했다. 이 버전은 완성된 WAV에 librosa time_stretch를 적용한 것이며 원래 합성과 후처리의 영향을 분리해 측정하지 않았다. Typecast 필재 1.1배속은 유지하고, 별도 [Supertonic 3](SUPERTONIC3_RESEARCH.md)를 추가 후보로 조사했다.

- Python 3.12 전용 환경: `.venv-tts/`
- PyTorch / torchaudio: `2.9.1`, 공식 CUDA 12.8 Windows wheel 사용
- Qwen 패키지: `qwen-tts==0.1.1`
- 모델: `Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice`
- 모델 리비전: `85e237c12c027371202489a0ec509ded67b5e4b5`
- 모델 경로: `models/Qwen3-TTS-12Hz-0.6B-CustomVoice/`
- 화자: `Sohee`, 언어: `Korean`, attention: `sdpa`
- 실행 스크립트: [scripts/tts_smoke.py](../scripts/tts_smoke.py)

가상환경·가중치·캐시·출력 음성은 Git 추적에서 제외한다. 전역 Python이나 시스템 CUDA를 변경하지 않는다. FlashAttention은 이 실험에서 설치하지 않는다.

새 환경을 준비할 때는 프로젝트 루트에서 아래 순서로 설치한다. 이미 설치된 환경에서는 다시 만들 필요가 없다.

```powershell
python -m venv .venv-tts
$env:PIP_CACHE_DIR = Join-Path (Get-Location) '.cache/pip'
./.venv-tts/Scripts/python.exe -m pip install torch==2.9.1 torchaudio==2.9.1 --index-url https://download.pytorch.org/whl/cu128
./.venv-tts/Scripts/python.exe -m pip install -r scripts/requirements-tts.txt
```

모델은 위 고정 리비전의 공식 저장소에서 speech_tokenizer 하위 파일까지 받아야 한다. 최초 설치에서는 공식 파일 목록의 크기와 LFS SHA-256을 확인했고 모델 폴더에 download-manifest.json을 남겼다. 런타임 패키지 설치는 모델 다운로드와 별개다.

## 실행

설치와 모델 다운로드가 완료된 환경에서 프로젝트 루트에서 실행한다:

```powershell
./.venv-tts/Scripts/python.exe scripts/tts_smoke.py
```

기본 샘플 3개: 일반 설명, 숫자·영문 혼합, 질문·반전. 테스트 문장이며 실제 영상의 사실 검증된 대본은 아니다.

다른 UTF-8 원고를 시험할 때:

```powershell
./.venv-tts/Scripts/python.exe scripts/tts_smoke.py --text-file <원고.txt> --output-dir outputs/tts-custom
```

단일 입력은 최대 600자로 제한한다. 장문 내레이션은 의미 단위로 나눠 별도 시험한다. 같은 출력 폴더로 실행하면 이전 동명 샘플을 교체하므로 비교할 실행은 서로 다른 폴더를 지정한다.

긴 원고는 한 줄을 한 발화 구간으로 작성하고 `--split-lines`를 사용한다. 이 모드는 화자 한 명만 허용하며 각 줄은 최대 600자다. 문장별 WAV를 보존하고 문장 사이에 0.18초를 추가해 `narration.wav`로 연결한다. report.json에 각 구간의 시작·끝 시간도 기록한다. 이 시간은 단어별 자막 정렬 결과가 아니다.

```powershell
./.venv-tts/Scripts/python.exe scripts/tts_smoke.py --speakers Sohee --split-lines --text-file <원고.txt> --output-dir outputs/narration
```

화자 비교도 같은 스크립트에서 지원한다. 기본 화자는 Sohee이며 다음 명령은 남성 3종을 같은 원고로 합성한다:

```powershell
./.venv-tts/Scripts/python.exe scripts/tts_smoke.py --speakers Ryan Aiden Uncle_Fu --text-file docs/tts-male-comparison.txt --output-dir outputs/tts-male-comparison
```

2026-11-18 남성 비교: 3개 모두 로컬 합성 및 WAV 검사 성공. Ryan 16.64초 / Aiden 15.60초 / Uncle_Fu 16.80초. 생성 시간은 각각 21.37 / 19.09 / 20.71초. [원문](tts-male-comparison.txt), [측정 결과](tts-male-results.json). 남성 기본 화자는 영어/중국어 기반이며 한국어 청취 평가는 사용자 확인 대기다. 한국어 남성 기본 화자는 이 모델에 없다. 현재 남성 목소리가 최종 선정된 것은 아니다.

## 결과

`outputs/tts-smoke/`에 WAV, 원문 TXT, report.json을 저장한다. 생성 스크립트는 네트워크 사용을 비활성화하고 로컬 모델만 읽는다. 다운로드 실패나 누락 파일이 있으면 실행 오류를 해결한 뒤 재시도한다.

- duration_seconds: 합성된 음성 길이
- generation_seconds: GPU 작업 완료까지 걸린 시간 (모델 로딩 제외)
- rtf: 생성 시간 / 음성 길이. 1보다 작으면 이 실험에서 실시간보다 빠름
- peak_allocated_mib / peak_reserved_mib: PyTorch의 최대 할당/예약 GPU 메모리. 전체 시스템 VRAM 사용량과 다름
- clipped_fraction: 원본 출력에서 절댓값 1 이상인 샘플 비율
- listening_review: 청취 검토 상태. 파일 생성 성공만으로 자연스러움·발음·원문 일치를 통과 처리하지 않음

다른 프로그램의 GPU 사용과 첫 실행 초기화가 시간에 영향을 줄 수 있다. 0.6B의 감정 지시 제어는 보장하지 않는다. 최종 Typecast 음성으로 교체하면 자막·편집 시간도 다시 맞춘다.

## 검증 상태

2026-11-18: 설치·모델 다운로드·로컬 GPU 추론 성공. 공식 LFS 해시 검사, CUDA 연산, pip check, WAV 재읽기 검사를 통과했다. 사용자는 초기 샘플 청취 후 목소리가 괜찮다고 평가했다. 이후 사용자 제공 원고의 21개 구간을 Sohee로 합성하고 연결해 152.8초 WAV를 생성했다(`outputs/sohee-pfa-narration/narration.wav`). 구간 순서·파일·최종 프레임 합계·수치상 클리핑을 검사했다. 장문 원문의 실제 발음 일치와 자연스러움은 사용자 청취 확인 대기다. 최초 생성 JSON의 청취 대기 상태는 당시 측정 기록으로 보존한다.

| 샘플 | 음성 길이 | 생성 시간 | RTF |
|---|---:|---:|---:|
| 일반 설명 | 16.080초 | 28.439초 | 1.769 |
| 숫자·영문 | 16.720초 | 21.029초 | 1.258 |
| 질문·반전 | 14.640초 | 17.852초 | 1.219 |

모델 로딩은 3.428초, 최대 PyTorch GPU 할당 2,558.9 MiB / 예약 2,972 MiB. 첫 샘플은 초기화 비용의 영향을 받을 수 있다. 모든 WAV는 24kHz 모노 PCM16이며 수치상 클리핑이 없었다. 이 속도는 음성 재생 길이보다 느리지만 로컬 미리듣기 작업은 실행 가능하다. 실제 150초 생성 시간은 미측정이다.

실제 결과: [측정 기록](tts-smoke-results.json). 전체 설치 버전: [requirements-tts.lock.txt](../scripts/requirements-tts.lock.txt). 새 환경에서는 CUDA wheel 설치 후 lock 파일로 나머지를 맞출 수 있다.

실행 시 SoX 실행 파일 부재와 FlashAttention 부재 안내가 출력됐지만, 이번 CustomVoice + SDPA + soundfile 경로의 3개 합성은 정상 완료됐다. SoX가 필요한 다른 기능까지 검증된 것은 아니다. 추가 도구를 불필요하게 전역 설치하지 않았다.
