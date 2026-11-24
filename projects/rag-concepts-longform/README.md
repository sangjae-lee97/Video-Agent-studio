# 처음 읽는 래그 — 질문 하나가 답이 되기까지 (개념 공유용 롱폼)

출처: Notion 「처음 읽는 Brother RAG · 질문 하나로 배우는 핵심 개념」 + 프로젝트 발제 문서 — [analysis.md](analysis.md).
표준(약 150초)보다 긴 롱폼. 사용자가 길이 제한을 풀었다(2026-11-20).

| 단계 | 상태 | 파일 |
|---|---|---|
| 1 분석 | 완료 | analysis.md |
| 2 낭독 대본 | 완료 (91줄·10장·5,371자, 1.05배속 추정 약 10분 30초~10분 57초). 사용자 결정 반영: Supabase 고정, 방법 A(Supabase + Python rank_bm25) | script.md |
| 3 Typecast 합성 | 완료 — 4개 요청, 이어 붙인 원본 625.690초(sha256 ba6de965…), 원본 최대값 샘플 316개(최종 마스터에서 alimiter) | narration/narration.wav, report.json, part1~4/ |
| 3b 정렬·보정 | 완료. 자동 정렬이 46·48번 줄 끝 단어를 못 찾음 → asr-words.json(1,290단어)을 difflib 문자 정렬로 91줄 매핑, 줄 끝 전부 대조, 0초 경계 6곳을 실측 무음으로 이동. short-window 보정(에이전트 VM): 문장 끝 0.2초 보호 PCM 동일, 새 포화 0, 329구간 236초 변경. **청취 확인 대기**: 9·18·21·65·79·81·84번 줄 | narration/local-short-window-v1/ |
| 4 편집표·Flow 요청 | 완료. 23구간(F12·M11), Flow 94.3초 = 15.0%(사용자 합의). 12클립 모두 소재·이미지 없음(하드컷) | production-plan.json, flow-request.md, flow-state.json |

## 실행 (저장소 루트 PowerShell)

```powershell
.\projects\rag-concepts-longform\narration\run_narration.ps1
```

- part 단위로 1회씩 합성하고(재시도 없음), 이미 받은 part는 건너뛴다. 실패하면 그 part 폴더에 `request-started.json`만 남는다 — 에이전트에게 알리면 새 폴더로 다시 build한다.
- part 폴더의 run_narration.ps1은 단독 실행용이 아니다(안내만 출력).
- 장 경계 이음에서 Smart 감정의 앞뒤 문맥은 part 안의 문장만 쓴다(part2·3·4 첫 구간은 각각 explanation·explanation·explanation 프리셋이라 영향 없음).

## 검증한 것
- part1~4 source.txt를 이으면 script.md 91줄과 정확히 일치.
- concat: 더미 WAV 2개로 프레임 수(본문+0.18초 무음)와 source 줄 순서 확인.
| 5 Flow 수령 | 완료. 12개 모두 1920×1080·24fps·7.917초(190프레임), 전부 채택. 흠: F01 명판에 큰 앰버 숫자 0/8이 따로 붙음(차이는 더 잘 보여 유지), F06 열 번호 '03' 중복, F11 체크칸 5개, F12 오른쪽 화면 켜짐 | media/flow/ |
| 6 모션그래픽 | 완료. M01~M31(532.5초) — 템플릿 '물류 센터 출고 라인'. 컨테이너 Playwright 24fps, 장면별 3시점 프레임 검수 후 겹침 수정(M02 도장, M21 화살표, M23·M25 장 전환 제목) | motion/scenes.py |
| 7 자막 | 300큐. 낭독 대본을 쉼표·문장 단위로 나누고 difflib로 단어 시각에 매핑, 코드·숫자 토큰 경계 보정, 0.8초 미만 큐 병합. 표기 사전 caption-terms.ko.json(MFC-L2805·BM25·RRF·Supabase·pgvector·ts_rank·rank_bm25·Hit@5·P50/P95·숫자) | captions.ko.srt, make_srt.py |
| 8 완성 | **renders/RAG-핵심개념_완성본_1080p.mp4** 626.79초·15,043프레임·24fps, 통합 −17.7 LUFS(alimiter −1 dBFS, AAC 후 피크 −0.2 dBFS), 썸네일 renders/RAG-핵심개념_썸네일.jpg(F01 0.8초 장면, 카피 위쪽 2색) | assemble.py, edl.txt |

## 검증 범위
- 확인함: 영상·음성 길이(626.79초), 프레임 수, 편집 구간 연속성(assemble.py가 프레임 단위로 검사), 33개 시점 프레임의 장면·자막 겹침, 썸네일 1280×720·320×180 가독성.
- 하지 않음: 연속 시청 검수(대표 프레임만), 청취 확인 대기 7줄(9·18·21·65·79·81·84).
- Flow의 우하단 ✦ 표시(AI 생성 워터마크)는 지우지 않았다.

빈 `narration/local-short-window-v1/tmpye2cxzan/`은 보정 스크립트의 임시 폴더(VM에서 삭제 권한 없음)로, 사용하지 않는다.

## 썸네일 버전 (2026-11-20)
- 이전 `renders/RAG-핵심개념_썸네일.jpg`는 brother-rag-agent 편(숫자 하나 다른 두 프린터)과 장면·문구가 겹친다는 사용자 지적으로 교체 대상.
- A `renders/RAG-핵심개념_썸네일_A-1099쪽.jpg`: F02 0.6초(물류 센터 전경, '1,099 PAGES' 배너). 카피 아래쪽 2줄 “1,099쪽 매뉴얼에서 / 답 하나를 찾는 법”, 노랑 '1,099쪽' + 초록 '답 하나'. 소형 문구 좌상단.
- B `renders/RAG-핵심개념_썸네일_B-모른다.jpg`: F08 5.6초(HOLD 상자에 보류 도장 찍힌 주문 카드). 카피 위쪽 2줄 “AI가 ‘모른다’고 / 말해야 할 때는?”, 빨강 '모른다'. 소형 문구 좌하단.
- 두 안 모두 1280×720·320×180에서 배너/HOLD 증거가 가려지지 않음을 확인. 사용자 선택 대기.
