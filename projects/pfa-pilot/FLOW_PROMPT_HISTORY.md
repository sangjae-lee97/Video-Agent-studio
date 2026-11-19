# 92.610초 승인 음성에 맞춘 Flow 프롬프트 점검

## 어느 원본을 대조했나

- [95.180초 파일럿 계획](exports/0a9498f9c4c4/plan.json)과 [92.610초 계획](plan.json)의 내레이션 20행은 내용과 순서가 모두 같다. 구판 내보내기 4개에서 Flow 텍스트는 모두 동일한 PFA 클립 한 개였다. 구판의 9–17초는 실제 발화 정렬 전 편집 배분이었다.
- 프로젝트 밖에서 [구 6장면 프롬프트](<C:/dev/video/medicial-review/gpt+claude/Flow_Omni_Flash_1.2_최종프롬프트_6장면.txt>), [구판 편집표](<C:/dev/video/medicial-review/gpt+claude/AVANT_GUARD_타입캐스트_90초_편집타임라인.txt>), [v3 F01~F09 전문](<C:/dev/video/medicial-review/gpt+claude/Flow_프롬프트_v3_건축사전스타일.txt>)을 확인했다. v3는 11월 17일의 약 90.23초 녹음과 9:16을 전제로 작성됐다. 6장면 문서에는 106초까지 가는 예상 편집 지시도 있다. 어느 쪽도 95.180초에 2.570초 차이를 빼서 환산할 수 없다.
- 아래 번호는 **v3**를 따른다. 업로드한 **파일럿 F01은 v3 F03**에 해당한다. v3 F01은 도입 심장이다. 시험 MP4는 앞 24.500초의 편집 실험이다. 이 표는 전체 영상에 대한 제작 검토안이며 생성 완료 목록은 별도로 표시했다.
- 기준은 [승인 음성](../../docs/NARRATION_APPROVAL.json)과 [원문 SRT](captions.ko.srt)다. 표의 초는 완성 영상에 배치할 **편집 구간 제안**이다. 일부 경계는 문장 사이 휴지에 뒀다. 실제 생성본의 소스 타임코드는 파일을 받은 뒤에 정한다.

## 장면별 판정

| v3 · 구 6장면 대응 | 이전 v3 편집 초 | 새 편집 초 · 대사 | 맞는 부분과 수정할 부분 |
|---|---:|---|---|
| F01 도입 · 01 | 0–3.400 | 0–3.833 · 약보다 시술을 먼저? | 질문과 심장 전경 유지. 양쪽 선택지를 고르게 보인다. 기존 도입 후보를 먼저 확인한다. |
| F02 질환 · 02 | 3.400–8.250 | 3.833–7.750 · 일주일 넘게 이어지는 지속성 심방세동 | 질문에서 질환 범위로 전환한다. 기존 전기 파동만으로는 ‘7일 초과’가 빠진다. 심방 단면에 기간 모션을 연결하고 심실이 규칙적으로 뛴다는 묘사는 뺀다. |
| F03 원리·부위 · 03+04 | 8.250–16.520 | 7.750–15.625 · PFA 원리 → 폐정맥 주변 → 좌심방 뒤쪽 벽 | 원리와 표적의 순서는 유지. 약 11.90초에 부위 설명 시작, 13.72초에 뒤쪽 벽 발화. 제공 영상 앞 두 샷 사용 가능. 마지막 심실 방향 강조는 교체 대상. 시험본은 도식으로 대체했다. |
| F04 연구 배정 · 구판은 그래픽 | 16.520–21.548 | 15.625–20.250 · 치료 전 환자 310명, 무작위 비교 | 공통 입구 310명, 왼쪽 PFA 시술 207명, 오른쪽 약물 치료 103명을 F04 안에서 함께 제시한다. 20.46초와 22.23초의 후속 발화도 같은 배치로 잇는다. |
| F05 모니터 · 05 | 25.998–30.398 | 24.500–29.125 · 삽입형 모니터 → 1년 뒤 비교 | 핵심 사건 유지. 27.24초부터 추적 기간으로 전환. 심장에 자극을 주는 모습 대신 피부 밑 장치에서 기록·시간축으로 시선을 옮긴다. |
| F06 성공 기준 · 구판은 그래픽 | 43.327–52.607 | 42.375–52.750 · 초기 성공 → 90일 이후 재발 기준 → 추가 시술·약물 조건 | 세 기준의 순서는 맞는다. 구슬이 세 관문을 모두 통과하면 전원 성공처럼 보인다. 평가할 항목이 드러나는 구조로 수정하고 48.90초에 추가 시술·약물 조건을 전환한다. |
| F07 안전성 질문 · 구판은 그래픽 | 52.607–56.297 | 52.750–57.8125 · 모두 시술부터? → 안전성도 살펴봐야 | 질문 두 문장을 함께 담는다. 55.91초부터 안전성 관점을 열고 다음 분모 257명은 별도 모집단 그래픽에서 표시한다. |
| F08 대응 · 구판은 그래픽 | 68.577–76.757 | 70.4375–78.3125 · 환자 선정·시술 전 검사 → 항응고 관리·연구 재개 | 검사는 맞지만 기존 ‘깨끗하고 빈 내부’와 스캔만으로는 대사 범위가 좁다. 검사 장면 뒤 74.90초부터 항응고 관리, 76.48초부터 재개를 연결한다. 검사 결과와 위험 해소를 연출하지 않는다. |
| F09 끝 질문 회수 · 06 | 85.797–90.227 | 88.000–92.610 · 누구에게 먼저? 효과와 위험을 함께 판단 | 앞 문장 N19는 87.81초까지 효과를 해석한다. N20 앞 휴지에서 도입 구도로 복귀하고 90.36초부터 두 관점을 함께 보여준다. 마지막 2초 정지 지시는 제거한다. |

표 사이의 구간도 원문에 대응한다. 29.125–38.375초는 12개월 성공 추정치, 38.375–42.375초는 완치와의 구별이다. 57.8125–70.4375초는 안전성 분모·사건·연구 중단, 78.3125–82.5625초는 변경 후 해석의 한계, 82.5625–88.000초는 효과의 해석이다. 수치·조건은 기존 근거와 정확한 모션 라벨을 쓴다.

## 확보 상태

[F03 확정본](renders/F03-44a227c2-flow1080-relabel.mp4) 사용자 채택 완료. 현재 F04 프롬프트 전달, 생성본 대기.

[F02 사용자 확정본](renders/F02-7days-flow-1080p.mp4) 채택 완료. 현재 F03의 720p·8초 테이크 수령 대기.

F01 도입 후보는 다운로드 이름이 `F05_1080p.mp4`였던 [심장·두 갈래 영상](media/flow/F01-6cbe653d-1080p.mp4)이다. 다운로드 이름 `F01_1080p.mp4`는 확정 F05와 SHA-256이 일치한다. [F02 후보](media/flow/F02-d10a3653-1080p.mp4)는 심근 색과 단면이 보이지만 심방 입구 테두리와 별개로 금빛 파동이 심실 표면에 나타나고 기간선 끝이 말린다. 두 후보 모두 1920×1080·24fps·94프레임(3.917초)이다. F02는 첫 전경과 로컬 심방 강조·7일 초과 시간선 조합을 권한다.

F01(4초) → F02(4초)부터 번호순으로 진행한다. F05 차례에는 이미 채택한 1080p 파일을 사용한다.

[F05 채택본 · 1080p](media/flow/F05-faf62b0d-1080p.mp4) 확보. 사용자가 선택한 `faf62b0d`로 확정했다. 영상은 1920×1080, 24fps, 143프레임(5.958초), 파일 전체는 5.970초다. 컷은 27·64프레임(1.125초·2.667초). 전 프레임에서 이전의 하단 흰 띠가 검출되지 않았다. 단면에 피하 기록기 한 개가 보이고 마지막 샷에서 시간축이 그려진다. 마지막에는 첫 샷보다 갈비뼈 노출 범위가 넓다. 이 특성을 포함해 채택한 소스이며 재생성 대상에서 제외한다. ‘일 년 뒤’는 전체 27.240초의 승인 자막에서 표시한다.

[파일럿 F01](media/flow/F01-take01.mp4)은 **v3 F03의 앞 두 샷**에 사용했다.

과거 작업의 `heart_v2.mp4`는 도입·결론 후보, `infographic*.mp4`와 `calendar_check.mp4`는 도입·기간 설명 후보, `pfa_join.mp4`와 `pfa_result.mp4`는 세로 PFA 후보였다. 현재 가로 편집본에 채택할지는 미확정이다. F04는 이미 렌더한 배정 모션으로도 연결할 수 있다.

## 생성 설정과 편집 길이

가로 16:9·1280×720으로 생성한다. 720p에서 컷·색·표적·기기 개수를 확인하고, 채택한 테이크만 Flow의 무료 1080p 업스케일로 받아 편집한다. 아래 표에서 장면별 길이를 고른다. F05는 채택 이력이며 추가 요청에서 제외한다. 생성 길이는 모델에 요청할 값이며, 편집 길이는 승인 음성에서 확보한 시간이다. 4·6·8초 선택을 전제로 작성했고 현재 세션에서 모델별 메뉴나 크레딧은 조회하지 않았다. 최종본은 각 클립을 정상 속도로 편집한다. 샷 경계는 요청값이므로 받은 파일에서 실제 사건 프레임을 확인한다.

| 장면 | 타임라인(초) | 생성 요청 | 편집 구간 길이 | 세 샷의 소스 시각(초) |
|---|---|---:|---:|---|
| F01 도입 질문 | 0–3.833 | 4초 | 3.833초 | 0–0.75 / 0.75–1.5 / 1.5–4 |
| F02 지속성 심방세동 | 3.833–7.750 | 4초 | 3.917초 | 0–0.75 / 0.75–1.65 / 1.65–4 |
| F03 PFA 원리와 치료 부위 | 7.750–15.625 | 8초 | 7.875초 | 0–1.4 / 1.4–4.15 / 4.15–8 |
| F04 무작위 배정 | 15.625–20.250 | 6초 | 4.625초 | 0–1.15 / 1.15–3.15 / 3.15–6 |
| F05 삽입형 모니터와 1년 추적 | 24.500–29.125 | 6초 | 4.625초 | 0–1.1 / 1.1–2.74 / 2.74–6 |
| F06 치료 성공의 복합 평가 기준 | 42.375–52.750 | 8초 | 10.375초 | 0–2.05 / 2.05–6.525 / 6.525–8 |
| F07 안전성으로 전환 | 52.750–57.8125 | 6초 | 5.0625초 | 0–1.55 / 1.55–3.16 / 3.16–6 |
| F08 선정·검사·항응고 관리·연구 재개 | 70.4375–78.3125 | 8초 | 7.875초 | 0–2.3 / 2.3–4.46 / 4.46–8 |
| F09 효과와 위험을 함께 보는 결론 | 88.000–92.610 | 6초 | 4.61초 | 0–1.15 / 1.15–2.36 / 2.36–6 |

F06은 10.375초 중 Flow 8초와 움직이는 조건 도식 2.375초를 사용한다. 나머지는 필요한 장면이 편집 종료점 전에 보이도록 세 번째 샷 안에 여유를 뒀다. F05 표의 경계는 요청값이다. 채택한 1080p에서 실제 시간축 샷은 소스 2.667초에 시작한다.

## 이전 테이크에서 확인한 오류와 다음 생성 기준

| 실제로 보인 문제 | 프롬프트와 검수에 적용할 기준 |
|---|---|
| PFA 모형이 회백색이었고 마지막 강조가 심실로 이어짐 | 심근은 적갈색, 단면은 분홍, 기기는 금속 은색으로 지정한다. 후벽 강조는 네 폐정맥 입구 사이에 고정하고 컷 전후 위치를 비교한다. |
| PFA 소스가 세로 360×640·10초로 전달됨 | Flow 메뉴에서 가로 720p와 장면별 4·6·8초를 선택하고 실제 파일의 가로세로·재생시간·컷 프레임을 확인한다. |
| F05 초기본 `70b88cee`에서 피부 조각이 들리고 장치가 피부 밖과 안에 중복된 듯 보임 | 원래부터 열린 작은 단면을 쓰고 기기 한 개의 위치·깊이·크기를 고정한다. 구조 공개는 카메라 이동으로 처리한다. |
| F05 비교본 `798aafa1` 중간에 화면 아래를 가로지르는 흰 띠가 생김 | 배경·재질이 화면 끝까지 자연스럽게 이어지게 한다. 자막을 위한 여백·하단 띠 지시는 쓰지 않는다. 컷 직전·직후와 중간 프레임에서 확인한다. |
| 몸통의 작은 창이 마지막 샷에서 넓은 흉곽 노출로 바뀜 | 같은 모형, 같은 방향, 같은 절단 범위를 세 샷에 유지한다. 강조선·카메라·시간축만 움직인다. |
| F05 이전 후보의 영어 표기가 최종 선택본에는 없음 | 서로 다른 테이크 사이의 차이다. 장면 내 기간 라벨은 대본과 대조하고 실제 누락·오자는 편집에서 보완한다. |

## 16:9 복사용 프롬프트

### F01 도입 질문 · 4초

약물·시술 두 갈래가 약 1.48초부터 보여야 한다. 기존 도입 소스가 적합하면 재사용.

승인 대사 · 심방세동, 약보다 시술을 먼저 하면 더 좋을까요?

```text
Create a 4-second landscape 16:9 educational animation at 1280×720. Three shots with hard cuts.
One adult heart on a charcoal plinth, upper chambers above ventricles, deep brick-red muscle and warm pink cut edges. Soft upper-left light, dark charcoal background. Keep the same anatomy, orientation and tissue colors across cuts.
The existing cut face stays the same size. Track around the model to reveal depth. Red muscle retains its color under highlights.
0–0.75 s: A slight lateral track reveals the cut face of the gently beating heart.
0.75–1.5 s: Hard cut closer. A fine amber outline traces the two upper chambers as the camera tilts up.
1.5–4 s: Hard cut to a frontal view. Two equal paths draw out from the plinth, one coral and one blue. Both paths are fully readable by 3.2 seconds; keep both visible as the heart moves.
As the two paths open, identify the coral path with “시술” and the blue path with “약물”. Use matching red label boxes with crisp white Korean type and equal visual weight.
Carry the scene background and its texture continuously to all four frame edges. No subtitles, caption bars, logos, speech or music.
```

### F02 지속성 심방세동 · 4초

0일부터 7일까지 일곱 칸. 마지막 눈금은 7일이고 선 끝만 그 오른쪽으로 조금 더 나간다. [4초 무음 편집 비교본](renders/F02-week-threshold-review.mp4)은 이전 27f8fe45의 앞 38프레임에 직접 그린 시간선을 연결했다.

승인 대사 · 이번 연구는 일주일 넘게 이어지는 지속성 심방세동을 다뤘습니다.

```text
Create a 4-second landscape 16:9 medical teaching animation at 1280×720. Use three shots with hard cuts.

Use one fixed cutaway model of the upper half of an adult heart on a matte charcoal plinth. Show the two atria above the atrioventricular valve openings. Frame the model above the ventricles throughout. The atrial muscle is deep brick red, its cut edges warm pink. Use soft upper-left light and a charcoal background extending to every edge.

0.00–0.75 s — Start close on both open atria. A short sideways camera move reveals the thin inner wall of the nearer atrium. Keep the cut surfaces fixed.

0.75–1.65 s — Hard cut directly to a macro view inside that atrium. Its inner wall fills the frame. Keep the camera still. Small amber ripples are already moving across separate patches of this wall in the first macro frame. Let successive ripples overlap in time so some are still visibly moving in the final frame. Cut mid-motion to the time scale.

1.65–4.00 s — Hard cut to an overhead view of a flat horizontal time scale printed on the charcoal plinth. The entire scale is visible on the cut. Label the leftmost tick “0일”. Place six short ticks for days 1 through 6, then a taller tick labeled “7일”. This makes seven equal one-day spaces between the two labeled ticks. Use clear ivory Korean lettering. The “7일” tick is the last tick, near the right edge of the frame. The printed scale ends there. Keep the scale and both labels fixed.

A bright amber line starts at the “0일” tick and extends smoothly to the right along the flat scale. Its tip passes each daily tick, crosses “7일” while the shot is still in progress, and extends half a day-spacing beyond that last tick. Keep both labels and the moving tip in view through the final frame.
No subtitles, caption bars, logos, speech or music.
```

### F03 PFA 원리와 치료 부위 · 8초

사용자 지시에 따라 추가 생성 종료. [8초 혼합 편집본](renders/F03-pfa-targets-1080p.mp4)을 검토한다. 아래 영문은 당시 요청안이다.

원리 → 11.90초 연구 부위 → 13.72초 후벽. 받은 세로 원본은 앞 두 샷만 사용 가능. 시험본의 후벽 도식을 유지하거나 이 가로 프롬프트로 교체.

이 모형은 좌우 두 개씩 독립된 폐정맥 입구가 있는 흔한 형태를 예시한다. 실제 사람에서는 공통 입구·추가 입구 등의 변이가 있다. [해부 연구](https://pubmed.ncbi.nlm.nih.gov/26793429/)

승인 대사 · 피에프에이는 짧은 전기 펄스로 목표 조직을 치료하는 시술입니다. 이 연구에서는 폐정맥 주변과 좌심방 뒤쪽 벽을 치료했습니다.

```text
Create an 8-second landscape 16:9 medical teaching animation at 1280×720. Three shots, two hard cuts.

Set: A matte charcoal plinth stands against a seamless, dim charcoal-gray studio background, approximately #1B2021, extending to every edge. Soft upper-left light falls on the model. Keep the backdrop dark at the same exposure in all three shots.

Model: Use the common four-ostium anatomical pattern for this teaching model. Show an isolated adult left atrium with the front wall already cut away. Face the posterior wall straight on. Exactly four oval pulmonary-vein openings pierce the wall: two on screen left, one above the other, and two on screen right, one above the other. The center between the pairs is solid, uninterrupted muscle. These four ovals are the only visible holes. Use deep brick-red tissue, warm pink cut edges and one silver flower-tipped catheter. Keep this geometry and orientation throughout.

0.00–1.40 s — Show all four openings. The catheter enters from screen right and touches the upper lip of the lower-right opening. Its dark oval remains visible directly beneath the tip. Ease toward that contact point and cut during the approach.

1.40–4.15 s — Match cut slightly closer on the same axis, keeping all four openings in frame. The tip touches the same upper lip. A brief amber pulse lights only the tissue touching the electrode and fades. Continue the gentle camera move up to the cut.

4.15–8.00 s — Return to the opening wide view and lock the camera. Trace a thin amber contour on the tissue bordering each of the four openings. On the upper-right contour, place a solid amber dot on the rim itself. Draw a fine leader outward from that dot to the ivory Korean label “폐정맥 주변” on the dark backdrop.

At 5.97 s, a rose-gold patch spreads across the solid central wall between the two pairs. Place a second solid dot inside the colored patch and draw a separate leader to “좌심방 후벽”. Keep both labels legible and both dots fixed on their tissue targets through the last frame. Leave all four dark lumens clear.

No subtitles, caption bars, logos, speech or music.
```

### F04 무작위 배정 · 6초

F03 확정본 마지막 화면을 시작 프레임으로 사용한다. 좌심방 그림을 비교 도표 왼쪽 PFA 항목에 연결한다. 이번 요청에 따라 두 군의 수를 F04 안에서 함께 미리 보여준다. 이어지는 발화에서도 같은 좌우·이름·인원을 유지한다. [Flow 시작 프레임](renders/F03-44a227c2-flow1080-relabel-frame191.png).

승인 대사 · 항부정맥제를 본격적으로 쓰기 전인 환자 삼백십 명을 무작위로 비교했습니다.

이어지는 승인 대사 · 이백칠 명은 피에프에이에, 백삼 명은 약물 치료에 배정했습니다.

```text
Create a 6-second landscape clinical trial animation, 16:9, 1280×720, in three shots. Use the supplied image as the exact first frame. Keep the matte charcoal background and soft upper-left light throughout.

0.00–1.15 s — Begin on the supplied left atrial cutaway. Preserve its orientation, tissue color and anatomical labels. Ease back from the stationary heart to reveal that this same illustration is mounted on the left side of a clinical study diagram.

1.15–3.15 s — Continue wider on the same diagram. At the top, reveal a single fixed heading printed on one line, exactly once: “약보다 시술을 먼저 하면?” Copy the Korean lettering exactly. Keep this one heading in place through the final shot. At 2.35 s, frame the open common inlet at the center, labeled “310명”. The inlet carries only the total patient count. Ivory beads roll down its single groove toward the fork.

3.15–6.00 s — Cut overhead on the rolling beads. Show the full Y-shaped diagram. At the lower-left coral endpoint, place “PFA 시술 207명” beside the same heart illustration. At the lower-right slate-blue endpoint, place “약물 치료 103명” with one small pill icon printed immediately to the right of the final character on the same baseline. The pill and its label form one fixed unit at this endpoint throughout the clip.

Keep all three counts readable together from 3.15 s through the final frame. Only the beads move on the diagram. Each bead rolls into exactly one branch. Preserve the same heading and labels across cuts. No subtitles, speech or music.
```

### F05 삽입형 모니터와 1년 추적 · 6초

**채택 완료 · 재요청 불필요.** 아래는 이전 요청안 보관용이다. 편집은 위의 1080p 채택본과 승인 자막을 사용한다.

```text
Create a 6-second landscape 16:9 educational animation. Three shots with hard cuts.
A faceless adult upper-torso teaching model, warm natural skin, pale-gold subcutaneous fat, rose muscle, charcoal background, soft light from the upper left. Exactly one slim silver cardiac rhythm recorder lies inside the fat just beneath the skin of the left upper chest, above the ribs. The outer skin is bare. Keep this same recorder fixed in place across cuts.
0–1.1 s: Track toward a small transparent teaching window in the left upper chest. The skin surface is continuous and bare; the single recorder becomes visible through it.
1.1–2.74 s: Hard cut to a side cross-section of the same window. Slide along the skin edge to reveal the recorder below the skin and above the ribs. No external patch, second device, wires or pacing pulses.
2.74–6 s: Hard cut wider. Beside the same torso, recording marks advance along a horizontal timeline and reach its distinct end marker by 4.4 seconds. Continue a gentle camera track for the remaining time.
Full-frame composition, edge to edge. No generated text, numbers, logos, speech or music.
```

### F06 치료 성공의 복합 평가 기준 · 8초

Flow 42.375–50.375초. 50.375–52.750초는 추가 시술·약물 조건을 묶는 모션 2.375초. 조건 탭 시작은 발화 48.90초.

승인 대사 · 초기 치료가 성공했는지, 또 구십 일 이후 기준에 해당하는 부정맥이 재발했는지를 봤습니다. 추가 시술과 약물 사용 조건까지 함께 따진 복합 기준입니다!

```text
Create an 8-second landscape 16:9 educational animation at 1280×720. Three shots with hard cuts.
One charcoal tabletop timeline with an initial assessment marker, a later day-boundary marker, and two treatment-condition tabs. Amber markers, muted blue tabs, soft upper-left light. Keep the same markers and their order across cuts. No patient token or success checkmarks.
Keep a single left-to-right rail on the charcoal tabletop. The two blue tabs are hinged to that rail; show the same pair when the camera moves closer.
0–2.05 s: Track along the start of the timeline as the initial-treatment assessment marker opens.
2.05–6.525 s: Hard cut to the later boundary. Track beyond it. A second assessment frame unfolds to mark the interval in which rhythm recurrence is evaluated.
6.525–8 s: Hard cut closer. Two adjacent tabs open together for additional procedures and medication use. The camera settles into an overhead angle with the initial and later markers still visible, ready for the editor’s matching diagram.
At the start of shot two, show “90일” in crisp white Korean type inside a red label fixed to the day-boundary marker. Track the evaluation interval beyond that marker.
Carry the scene background and its texture continuously to all four frame edges. No subtitles, caption bars, logos, speech or music.
```

### F07 안전성으로 전환 · 6초

두 번째 질문의 ‘안전성도’가 시작되는 55.91초에 두 번째 관점을 연다.

승인 대사 · 그렇다면 모두 시술부터 하면 될까요? 안전성도 살펴봐야 합니다.

```text
Create a 6-second landscape 16:9 educational animation at 1280×720. Three shots with hard cuts.
One adult heart on a charcoal plinth, upper chambers above ventricles, deep brick-red muscle and warm pink cut edges. Soft upper-left light, dark charcoal background. Keep the same anatomy, orientation and tissue colors across cuts.
Keep the exposed atrial surface identical in all three views. Both markers belong to the plinth; light changes affect the markers while the tissue keeps its color.
0–1.55 s: Track back from the atrial cutaway while the previous effectiveness highlight gently recedes.
1.55–3.16 s: Hard cut wider. Move sideways to reveal the second, unlit marker beside the effectiveness marker. Keep the model moving gently.
3.16–6 s: Hard cut to a level two-sided view. The second marker lights in amber for the safety question. Both perspectives are visible by 4.7 seconds. No patient injury or alarm imagery.
When the second marker lights, reveal the white Korean word “안전성” on its red face. Keep it attached to the marker.
Carry the scene background and its texture continuously to all four frame edges. No subtitles, caption bars, logos, speech or music.
```

### F08 선정·검사·항응고 관리·연구 재개 · 8초

검사 → 74.90초 항응고 관리 → 76.48초 연구 재개. 재개 뒤 효과나 위험 해소를 확정하는 연출은 제외.

승인 대사 · 이후 연구진은 환자 선정 기준과 시술 전 검사를 강화했습니다. 항응고 관리도 강화한 뒤, 연구를 다시 시작했습니다.

```text
Create an 8-second landscape 16:9 educational animation at 1280×720. Three shots with hard cuts.
One isolated adult left atrium viewed from inside through an open anterior teaching section, with four patent pulmonary-vein openings in two lateral pairs and the posterior wall between them. Deep brick-red muscle, warm pink cut edges, charcoal plinth, soft upper-left light. Keep the same chamber, openings and orientation across cuts; keep ventricles outside the frame. A selection card, a separate medication-review tab and a study timeline sit beside the plinth.
Keep the chamber and its cut surface fixed in size. One translucent imaging plane moves through this existing section. The card, medication tab and timeline stay on the tabletop, separate from the tissue.
0–2.3 s: Track across the selection card as its criteria unfold, revealing the cutaway chamber behind it.
2.3–4.46 s: Hard cut closer. A translucent imaging plane sweeps across the atrium and its appendage as the camera tracks the plane. Show the examination process, without declaring a finding.
4.46–8 s: Hard cut to the medication-review tab as it opens. At about 6.04 seconds, the camera follows the study timeline beyond its pause mark as the line resumes. Keep the risk marker in view; complete the reveal by 7.5 seconds.
When the medication-review tab opens, reveal the white Korean label “항응고 관리” on its red tab. Keep it legible during the move to the study timeline.
Carry the scene background and its texture continuously to all four frame edges. No subtitles, caption bars, logos, speech or music.
```

### F09 효과와 위험을 함께 보는 결론 · 6초

N19 효과 해석이 끝난 뒤 도입 구도로 돌아간다. 전체 90.36초부터 두 관점을 동등하게 표시.

승인 대사 · 하지만 누구에게 먼저 시행할지는, 효과와 위험을 함께 판단해야 합니다.

```text
Create a 6-second landscape 16:9 educational animation at 1280×720. Three shots with hard cuts.
One adult heart on a charcoal plinth, upper chambers above ventricles, deep brick-red muscle and warm pink cut edges. Soft upper-left light, dark charcoal background. Keep the same anatomy, orientation and tissue colors across cuts.
Match the opening heart’s cut surface, colors and frontal orientation. Anchor two equal markers to the plinth and keep their positions fixed while light changes.
0–1.15 s: Track away from the atrial cutaway toward the orientation of the opening heart.
1.15–2.36 s: Hard cut to the plinth. A lateral camera move reveals two fixed, unlit markers beneath the model.
2.36–6 s: Hard cut to the frontal view. The two markers illuminate with equal prominence for benefit and risk. Establish the complete comparison by 4.2 seconds. Drift gently while both stay visible; no winner or cure imagery.
In the final frontal view, reveal matching red labels on the two markers. Use crisp white Korean type reading “효과” on one and “위험” on the other.
Carry the scene background and its texture continuously to all four frame edges. No subtitles, caption bars, logos, speech or music.
```
