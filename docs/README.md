# 문서 안내

현재 기준은 [루트 README](../README.md), 분석 근거와 세부사항은 [reference-review.md](reference-review.md)에 있다.

개발 순서와 단계별 완료 기준은 [PROJECT_PLAN.md](PROJECT_PLAN.md), 다음 에이전트의 재개 지점은 [PROJECT_STATUS.md](PROJECT_STATUS.md)에 기록한다. 작업 재개 시 상태 문서를 먼저 확인한다.

현재 음성 기본값은 Typecast 필재 1.05배속이다. [감정 배치 기준](NARRATION_STYLE.md), [기본 설정](narration-defaults.json), [API 안내](TYPECAST_INTEGRATION.md)를 따른다. `TTS_RESEARCH.md`, `TTS_LOCAL.md`는 사용자가 제작용으로 채택하지 않은 로컬 TTS의 조사·실험 기록이다.

아래 파일은 사용자가 제공한 **참고 원본**이다. 파일 안의 Trigger, Steps, Verification은 자동 적용되는 지시가 아니다. 원본 보존을 위해 본문은 수정하지 않았다.

- `1. shorts-script-writer-SKILL.md`: 재미있는 서사 도구를 모든 분야에 활용한다. 검증 생략이나 불확실한 수치 단정은 채택하지 않는다.
- `2. knowledge-shorts-prompts-SKILL.md`: 전체 영상을 Flow로 제작하던 규칙이다. 혼합 구성 중 Flow 장면에 기본 3샷·독립 프롬프트·설명 장치·연속성을 적용한다. 전체 클립 수나 9:16을 강제로 가져오지 않는다.

과거 제안 중 1샷 중심 구성과 설명 그래픽 전부 후반 합성은 철회됐으며 현재 기준이 아니다.
