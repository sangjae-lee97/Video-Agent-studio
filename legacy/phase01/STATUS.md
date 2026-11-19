# 보관용 Phase 01 PoC

사용자 제공 ZIP의 이전 구현이다. 현재 기준은 [루트 README](../../README.md)를 따른다. 이전 README는 별도 보관하지 않고 최신판으로 교체했다.

## 현재 기준과 다른 부분

- 10장면 × 15초 강제, AI 장면 기본 6개, 1~9개만 허용.
- 기본 3샷·구체적 사건·연속성을 보장하지 않는 단순 Flow 프롬프트.
- 에이전트가 작성한 계획을 가져오는 기능 없음. mock은 실제 조사·대본이 아님.
- live는 OpenAI API에 의존. 기본 모델은 이전 설정이며 현재 지원 여부는 이번 작업에서 검증하지 않음.
- 인용 URL 발견을 verified=True로 표현하지만 사실 검증 완료가 아님.
- 테스트는 이전 구현을 검사하며 새 사양을 규정하지 않음.
- review_required는 이 PoC의 출력 상태이며 영구적인 자동 공개 금지를 의미하지 않음.

## 이전 코드 재현

```powershell
cd C:\dev\Video-Agent-studio\legacy\phase01
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
python main.py "테스트 주제" --mode mock
```

이번 정리에서는 의존성을 설치하지 않았다. mock의 구조 검토 실패는 출처와 실제 주장이 없어 정상이다. live는 별도 API 설정과 비용이 필요하다.

TTS·Flow 제어·자막·합성·YouTube 업로드는 없다. outputs 결과는 제작 준비가 끝난 자산으로 취급하지 않는다.
