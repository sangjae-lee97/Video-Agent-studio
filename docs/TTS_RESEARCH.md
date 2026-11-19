# 한국어 로컬 TTS 조사와 다운로드 확인

확인일: 2026-11-18 (Asia/Seoul)

## 결론과 사용 방향

**최신 결정(2026-11-18): 로컬 Qwen 장문과 1.1배속 결과 검토 후 사용자가 Typecast로 전환했다.** [현재 Typecast 연동 계획](TYPECAST_INTEGRATION.md)을 우선한다. 아래 내용은 비용 절감용 로컬 TTS를 검토하던 당시의 조사 기록이며 기본 제작 방식으로 적용하지 않는다.

당시에는 Sohee 기반 로컬 미리듣기와 Typecast 최종 합성을 함께 검토했다. 현재는 이 혼합 TTS 경로를 기본으로 추진하지 않는다. 최종 Typecast 음성을 기준으로 자막 정렬과 편집 시간을 계산한다.

## 직접 확인한 PC 환경

- NVIDIA GeForce RTX 5060 Laptop GPU, 총 VRAM 8,151 MiB, 조회 당시 여유 7,302 MiB.
- NVIDIA 드라이버 592.01, Python 3.12.10.
- C 드라이브 여유 약 624 GB (십진 단위).
- CIM 조회 제한으로 시스템 RAM은 확인하지 못했다.
- 작은 GPU TTS를 시험할 만한 환경이라는 판단이다. VRAM 수치는 실행 성공이나 속도 보장이 아니며 CUDA/PyTorch/Windows 호환성과 실제 메모리를 검증해야 한다.

## 후보 비교

| 후보 | 공식 확인 내용 | 다운로드 용량 / 판단 |
|---|---|---|
| Qwen3-TTS 0.6B CustomVoice | 한국어·기본 화자 Sohee, Apache-2.0 모델 | 저장소 약 2.50 GB. 첫 시험 후보 |
| Qwen3-TTS 1.7B CustomVoice | 한국어·화자·자연어 스타일 제어, Apache-2.0 | 저장소 약 4.52 GB. 0.6B 실측 후 필요할 때 검토 |
| MeloTTS-Korean | 한국어, MIT 모델. 프로젝트는 CPU 실시간 추론을 안내 | 한국어 저장소 약 208 MB. 부가 모델·의존성 별도. Windows 공식 안내는 Docker 권장 |

위 크기는 Hugging Face API의 저장소 파일 크기 합계이며 Python 환경·PyTorch·캐시까지 포함한 전체 설치 용량이나 VRAM 사용량이 아니다. Melo의 CPU 속도는 공식 설명이며 이 PC 실측 결과가 아니다.

Qwen 0.6B 모델 카드에는 스타일 제어 문구가 있지만 공식 GitHub 모델 표는 1.7B CustomVoice에만 instruction control을 표시한다. 따라서 0.6B의 감정·연출 지시 지원을 보장하지 않는다. 첫 실험에서는 기본 화자 한국어 발음·속도·반복 안정성부터 평가한다.

Apache-2.0/MIT는 상업 이용을 허용하는 라이선스이며 적용되는 고지 등 조건을 지켜야 한다. 이번에는 공식 모델·코드 라이선스 표시를 확인했으며 임의의 음성 복제나 제3자 자료의 권리까지 확인한 것은 아니다.

## 이번에 우선 선택하지 않은 후보

- OpenVoice V2: 한국어와 MIT 공개가 확인되지만 목소리 변환/복제 중심이어서 첫 기본 내레이션 실험에서는 단계를 줄이기 위해 제외.
- XTTS-v2: 한국어 지원은 있지만 공식 모델 라이선스가 모델 및 출력의 비상업적 사용으로 제한한다. 수익화 가능성이 있는 프로젝트의 기본 무료 경로로 선택하지 않는다.
- Kokoro-82M: 확인한 공식 모델 카드에서 한국어 지원을 확인하지 못했으므로 현재 한국어 후보에 넣지 않는다. 모든 변형 모델이 한국어를 지원하지 않는다는 주장은 아니다.

## 다운로드 확인 범위

세 후보 모두 공식 Hugging Face API에서 `gated=false`를 확인했다. 로그인 토큰 없이 각 고정 리비전의 config.json을 실제로 읽고 JSON 해석까지 성공했다. 공개 파일 목록과 크기도 받았다.

원시 확인 기록: [tts-download-check.json](tts-download-check.json).

최초 조사에서는 설정 파일 접근만 확인했다. 이후 사용자 승인으로 **Qwen 0.6B 전체 다운로드·해시 검사·설치·로컬 GPU 합성을 완료**했다. 1.7B와 Melo는 여전히 설정 파일 접근 확인 단계다. [실행 방법과 결과](TTS_LOCAL.md), [실측 기록](tts-smoke-results.json)을 참조한다. 한국어 발음·자연스러움은 사용자 청취 확인 대기다.

최초 셸 네트워크 요청은 DNS 제한으로 실패했고, 허용된 네트워크 접근을 통해 위 소규모 조회가 성공했다. 모델 취득은 공식 배포 경로를 사용한다.

## 다음 실험

아래 1~5의 환경 구성·다운로드·합성·기술 측정은 완료했다. 남은 것은 샘플 청취 평가와 그 결과에 따른 150초 실험이다.

1. 프로젝트 안의 격리 환경과 모델 저장 위치를 정하고 캐시·가중치를 Git 추적에서 제외.
2. RTX 5060을 지원하는 PyTorch 환경 확인. 공식 Qwen 설치 지침에 맞춰 구성하되 FlashAttention을 Windows에서 무조건 설치하지 않고 지원되는 실행 경로 확인.
3. 0.6B CustomVoice의 기록된 리비전을 다운로드. 현재 저장소에 포함된 speech_tokenizer 파일도 확인해 불필요한 중복 취득 피하기.
4. Sohee/Korean으로 짧은 한국어 3종 합성: 일반 설명, 숫자·단위·영문 혼합, 질문·반전 문장.
5. 생성 시간, 음성 길이, 최대 VRAM, 끊김·반복·누락·발음·억양을 기록하고 실제 WAV를 사용자에게 제공.
6. 짧은 샘플이 통과하면 문장 단위로 약 150초 생성해 일관성과 비용 절감 실효성을 확인. 부족하면 Melo 또는 Typecast와 같은 원고로 비교.

대본 파일이 같아도 다른 TTS의 길이는 같지 않다. 최종 목소리로 교체할 때 전체 영상을 무조건 늘이거나 줄이지 말고 내레이션 구간별 타이밍과 자막을 갱신한다.

## 공식 출처

- [Qwen 모델·설치·화자 표](https://github.com/QwenLM/Qwen3-TTS)
- [Qwen 0.6B 모델 카드](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice)
- [Qwen 1.7B 모델 카드](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice)
- [MeloTTS 코드와 CPU 안내](https://github.com/myshell-ai/MeloTTS)
- [Melo 한국어 모델](https://huggingface.co/myshell-ai/MeloTTS-Korean)
- [Melo 설치 안내](https://github.com/myshell-ai/MeloTTS/blob/main/docs/install.md)
- [OpenVoice](https://github.com/myshell-ai/OpenVoice)
- [XTTS 모델 라이선스](https://huggingface.co/coqui/XTTS-v2/raw/main/LICENSE.txt)
- [Kokoro 공식 모델](https://huggingface.co/hexgrad/Kokoro-82M)
