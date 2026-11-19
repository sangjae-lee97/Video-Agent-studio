# 다음 영상 편집 인수인계

새 주제나 문서로 시험할 때는 [새 채팅에서 한 편을 만드는 순서](VIDEO_PRODUCTION_GUIDE.md#새-채팅에서-한-편을-만드는-순서)에서 시작한다. 아래 음성·장면·출력은 PFA 파일럿을 이어 만드는 기록이다.

F07의 반복 카테터 컷을 미사용 Flow 테이크 0f8e1484의 치료 선택 갈림점으로 교체했다. 직전 본편과 전체 디코딩 해시를 대조해 1266~1337번(0부터 계산) 72프레임만 변경되고 나머지 2,151프레임과 AAC 음성 데이터가 일치함을 확인했다.

원본 F09의 제목·테두리를 살리고 원본 여백의 질감과 실제 조명을 이용해 본문 두 열을 다시 합성했다. 직전 판과 자막 영역 2,223프레임 및 모니터 영역을 대조했고 AAC 데이터가 일치한다. 마지막 컷의 시작·손짓·끝 표본을 확인했다.

자막 42개에 영문 약어·숫자·단위 표기를 적용하고 문장부호와 호흡용 쉼표를 생략했다. 이전판과 자막 시각 및 AAC 데이터가 일치한다.

먼저 AGENTS.md, README.md, docs/PROJECT_STATUS.md, docs/PROJECT_PLAN.md의 P2/P3, docs/reference-review.md, docs/NARRATION_STYLE.md, docs/narration-defaults.json, docs/NARRATION_APPROVAL.json을 확인한다. [기존 Notion 프로젝트](https://app.notion.com/p/41ddb49922e5814f82e2c2ce00a50017) 본문에 완성 결과를 기록한다.

## 현재 편집점

사용자가 F09 원본 874d16d5를 채택했다. 원본과 보정본 해시는 프로젝트 flow-state.json에 기록했다. 치료 성공 추정치와 해석 컷은 0~100% 축·막대·끝값을 공유한다. 안전성 분석 257명 중 13명과 그중 6명을 같은 격자에 표시한다. 연구 중단 표식은 절차 보완과 재개까지 같은 시간선에 유지하고, 해당 발화의 조치 한 행을 강조한다.

[최신 1080p 본편](../projects/pfa-pilot/renders/AVANT-GUARD_완성본_1080p.mp4). Flow 27.777초(30.0%)와 모션그래픽 64.833초로 완성했다. F07 치료 선택 갈림점은 52.750–55.750초, F09 진료실은 85.750–92.610초다. 세 컷의 모니터에 승인된 56%·약 30% 그래프를 합성하고 종이의 효과 아래에 ‘1년간 PFA 우세’, 위험 아래에 ‘257명 중 뇌졸중 6명’을 표시했다. 다음 행동은 사용자 본편 검토다.

### 이전 20:80 마스터 검수

[완성 영상](../projects/pfa-pilot/renders/AVANT-GUARD-final-1080p.mp4)과 [썸네일](../projects/pfa-pilot/renders/AVANT-GUARD-thumbnail.jpg)은 이전 편집 산출물이다. 92.610초 · 1920×1080 H.264 · AAC 48kHz · 2,223프레임. 24fps 간격으로 편집했고 마지막 프레임 표시 길이를 내레이션 끝에 맞췄다. 승인 WAV를 한 번 사용했으며 MP4 마스터에만 −2dB를 적용했다. 최종 −19.7 LUFS, −1.9dBTP, 원음과 AAC 상관 0.999975. 42개 자막의 글자·외곽선과 경계를 전체 디코딩 화면에 대조했다.

### 이전 F04 검수 기록

[F04 승인 음성 포함 1080p MP4](../projects/pfa-pilot/renders/F04-assignment-1080p.mp4)를 렌더했다. 영상·음성 각 8.875초. 1920×1080, 24fps, 213프레임 전부 디코딩. F03 마지막과 첫 프레임 RGB 평균 절대차 1.42/255. 승인 WAV 15.625–24.500초와 디코딩 음성 상관 0.99998. 8개 시점 표본에서 질문 1개, 공통 입구와 좌우 인원 표기, 오른쪽 약물 라벨 옆 알약 확인. 전체 310명은 클립 2.375초, 세 인원수 동시 표시는 3.167초부터다. 사용자 확인 후 F05와 연결한다.

[장면별 제작 지시와 F04 로컬 프롬프트](../projects/pfa-pilot/FLOW_PROMPT_REVIEW.md), [현재 30:70 계획](../projects/pfa-pilot/production-plan.json), [편집 패키지](../projects/pfa-pilot/exports/CURRENT.md), [진행 상태](../projects/pfa-pilot/flow-state.json)를 함께 읽는다. F01·F02·F03·F05·F09 소스와 로컬 모션그래픽을 편집했다. 이전 20:80 버전에서 F09는 F01의 15프레임을 재사용했다. 현재 30:70 버전은 위의 F09 새 요청문을 사용한다.

앞서 만든 [24.500초 시험 편집](../projects/pfa-pilot/renders/pfa-opening-24.5s.mp4)과 이전 Flow 요청 기록은 이력이다.

승인 WAV는 `outputs/typecast-piljae-pfa-emphasis-1.0x-v1/local-short-window-v1/narration_balanced.wav`, SHA-256 `85d5ecfa7f9da4b86abf81de378e5c4c119c1755b527ea7b08c444da6f0ecbdc`. 현재 1.0배속 음성을 그대로 쓴다. 향후 새 원고 기본은 필재/SSFM 3.1/1.05배속이다. 감정·로컬 보정은 승인 기록을 따른다.

## 작업 기록

예상 소요 시간을 먼저 알리고 완료 범위와 실제 검증을 로컬 기록과 기존 Notion 프로젝트에 남긴다.
