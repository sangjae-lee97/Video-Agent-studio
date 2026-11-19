# Flow 일괄 요청 — Brother 기술지원 RAG Agent (6클립)

기준 음성: `narration/narration.wav` 125.097초 (sha256 a4a41cfa…), 보정본 `narration/local-short-window-v1/narration_balanced.wav`(시각 동일), 문장 시각 `narration/local-short-window-v1/sentence-boundaries.json`.
공통 설정: Google Flow 웹 · 가로 16:9 · 720p(1280×720) · **8초** 생성 · 채택 테이크만 1080p 업스케일. 돌려줄 파일명: `F01_1080p.mp4` … `F06_1080p.mp4` (`projects/brother-rag-agent/media/flow/`에 넣어 주세요).
생성 순서: **F01 먼저 → 채택 → 편집점 5.94초 화면을 `F01-frame-5.94s.png`로 저장 → F02**(시작 프레임) · F03~F06은 언제든.
입력 방식 개정(2026-11-19 사용자 지정): 앞 영상의 이미지를 넣어 이어지게 하는 것은 소재가 아니라 프레임이다. F02를 프레임으로 바꾸고, F05는 직전이 모션그래픽이라 소재 · 이미지 없음으로 바꿨다.
브랜드 로고·실제 제품 외형은 쓰지 않는다(일반 프린터). 장면 안 라벨은 영문/숫자 위주로 지정하고, 철자가 틀리면 편집에서 덮어 보정한다.

| ID | 본편 구간(초) | 사용 길이 | 생성 | 입력 방식 |
|---|---|---:|---:|---|
| F01 | 0.00–5.94 | 5.94 | 8초 | 소재 · 이미지 없음 |
| F02 | 5.94–13.00 | 7.06 | 8초 | 프레임 · 편집점 프레임 업로드 (`F01-frame-5.94s.png`) |
| F03 | 24.20–32.20 | 8.00 | 8초 | 소재 · 이미지 없음 |
| F04 | 59.00–66.20 | 7.20 | 8초 | 소재 · 이미지 없음 |
| F05 | 106.60–112.90 | 6.30 | 8초 | 소재 · 이미지 없음 |
| F06 | 112.90–119.00 | 6.10 | 8초 | 소재 · 이미지 없음 |

Flow 합계 40.60초 / 125.10초 = 32.5% (모션그래픽 84.50초).

공통 대상 — **PRINTER**(F01·F02·F05에서 같은 문장 그대로 사용): a compact A4 inkjet multifunction printer with a matte white body and dark charcoal-grey top scanner lid, a small color touchscreen on the front left, a pull-out paper tray at the bottom front, and four small transparent ink-tank windows on the front right showing black, cyan, magenta and yellow ink levels; no brand logo or brand name anywhere on the printer.

---

## F01 · 본편 0.00–5.94초

**① 해당 대본**

> 1. 이름이 숫자 하나만 다른 프린터 두 대. AI는 내 모델의 답을, 정확히 골라낼 수 있을까요?  (0.00–5.22)

**② Flow 입력 방식: 소재 · 이미지 없음 (텍스트 → 동영상)** — 영상의 첫 장면이라 직전 구간이 없고 참고 이미지도 없다. 대상 설명 전문으로 장면을 세운다. 채택본의 5.94초 화면이 F02의 시작 프레임이 되므로 **가장 먼저 생성·채택**한다.

**③ 프롬프트 및 적용 방법** — 텍스트 → 동영상, 가로 16:9, 720p, 8초, 이미지 없음. 아래 블록 전체 붙여넣기. 채택 테이크만 1080p 업스케일 → `F01_1080p.mp4`. 본편에는 0–5.94초만 쓴다. 채택 테이크의 **5.94초 화면**(Shot 3, 두 프린터 화면에 물음표, 카메라가 올라가는 중)을 ‘프레임 저장’ → `F01-frame-5.94s.png`. 또는 F01 파일을 주시면 에이전트가 정확한 편집점 프레임을 추출해 드린다.

```text
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.5s): eye-level wide shot of two identical printers standing side by side on a light oak desk, 30 cm apart. Slow dolly-in toward the gap between them. A small white plastic name plate stands in front of each printer: the left plate reads "DCP-T830DW", the right plate reads "DCP-T835DW", black bold letters, both readable.
Shot 2 (2.5–5.0s): low close-up sliding left to right along the two name plates at plate height. When the camera reaches the digits, a thin amber underline draws itself under the "0" of "830" on the left plate and under the "5" of "835" on the right plate, at the same moment.
Shot 3 (5.0–8.0s): medium shot from slightly above, both printers in frame. Both touchscreens light up at the same time showing one large white question mark on a blue screen. The camera slowly rises above the two printers.

SUBJECT (keep identical in every shot): two identical printers. Each PRINTER: a compact A4 inkjet multifunction printer with a matte white body and dark charcoal-grey top scanner lid, a small color touchscreen on the front left, a pull-out paper tray at the bottom front, and four small transparent ink-tank windows on the front right showing black, cyan, magenta and yellow ink levels; no brand logo or brand name anywhere on the printer. Same size, same color, same orientation (front facing camera). Name plates: small white plastic desk plates, left "DCP-T830DW", right "DCP-T835DW".
BACKGROUND: a bright modern tech-support office in daytime; soft window light from the left; out-of-focus white shelves with grey binders and a potted green plant behind the desk; clean pale-grey wall. The background stays the same in all three shots.
STYLE: photoreal product-style cinematography, 35 mm lens, shallow depth of field, clean daylight, amber used only for highlighting differences. Fill the whole 16:9 frame edge to edge. All label text is bold clean sans-serif, crisp and fully legible.
EXCLUSIONS: no subtitles, no caption bar, no bottom text overlay, no burned-in captions, no karaoke-style word-by-word timing, no brand logos, no watermark.
```

## F02 · 본편 5.94–13.00초

**① 해당 대본**

> 2. 이번 프로젝트는 브라더 프린터와 복합기 열 개 모델의 기술지원 질문에, 공식 문서로 답하는 래그 에이전트를 만드는 겁니다.  (5.94–12.62, 13.00부터 M01 ‘3~4명 · 5일 · 40시간’)

**② Flow 입력 방식: 프레임 · 편집점 프레임 업로드 (프레임 → 동영상)** — 직전 구간은 F01이고, 프린터 두 대 위로 올라가던 카메라를 그대로 이어 받아 프로젝트 테이블을 드러낸다. F01은 8초 중 0–5.94초만 쓰고 끝을 잘라 쓰므로 **이어 붙이기(확장)는 하지 않는다**. **시작 프레임: `F01-frame-5.94s.png`** = F01 채택 테이크의 소스 5.94초 화면(Flow ‘프레임 저장’, 또는 F01 파일을 주시면 에이전트가 추출). F01 채택 후 생성한다.

**③ 프롬프트 및 적용 방법** — 프레임 → 동영상, **시작 프레임** 칸에 `F01-frame-5.94s.png` 1장(끝 프레임 없음), 가로 16:9, 720p, 8초. 채택 테이크만 1080p 업스케일 → `F02_1080p.mp4`. 본편에는 0–7.06초. 첫 샷은 시작 프레임에서 컷 없이 이어지고, 두 프린터 화면의 물음표는 Shot 1 동안 그대로 둔다.

```text
Start exactly from the provided start frame and continue it without a cut.
8-second clip: one continuous opening shot, then two hard-cut shots.
Shot 1 (0.0–2.6s, continuous from the start frame): the camera keeps rising smoothly above the two identical printers and tilts down until the view becomes top-down. It reveals that the two printers stand side by side at the top end of a large light oak meeting table; on the table below them lie two thick printed manuals with plain dark-blue covers and two open laptops, and four people's hands and forearms (no faces) rest around the table. Both printer screens keep showing the white question mark on blue. The white name plates stay in front of the printers.
Shot 2 (2.6–5.2s): hard cut to a straight top-down view of the middle of the same table, camera still. The hands place ten small white cards in two neat rows of five between the two manuals; the left row sits next to the left manual, the right row next to the right manual. Each card shows only a tiny grey printer icon. A white label "10 MODELS" appears above the two rows at 4.0s.
Shot 3 (5.2–8.0s): hard cut to a low push-in toward one open laptop. Its screen shows a simple chat window with a blinking cursor in an empty input box and a small cyan magnifying-glass icon; the ten cards and one manual stay visible out of focus in the foreground.

SUBJECT (keep identical to the start frame in every shot): two identical printers. Each PRINTER: a compact A4 inkjet multifunction printer with a matte white body and dark charcoal-grey top scanner lid, a small color touchscreen on the front left, a pull-out paper tray at the bottom front, and four small transparent ink-tank windows on the front right showing black, cyan, magenta and yellow ink levels; no brand logo or brand name anywhere on the printer. Name plates: left "DCP-T830DW", right "DCP-T835DW". Two thick printed manuals (about 5 cm thick) with plain dark-blue covers and no text. Ten small white cards with a tiny grey printer icon.
BACKGROUND: the same bright modern tech-support office in daytime as the start frame; light oak table filling most of the frame; pale-grey floor visible at the frame edges; soft window light from the left; out-of-focus white shelves with grey binders and a potted green plant. The background stays the same in all three shots.
STYLE: photoreal cinematography matching the start frame, soft daylight, amber used only for highlighting differences, cyan used only for search icons. Fill the whole 16:9 frame edge to edge. All label text is bold clean sans-serif, crisp and fully legible.
EXCLUSIONS: no subtitles, no caption bar, no bottom text overlay, no burned-in captions, no karaoke-style word-by-word timing, no faces, no brand logos, no watermark.
```

## F03 · 본편 24.20–32.20초

**① 해당 대본**

> 5. 그런데, 함정이 있습니다.  (24.40–25.56)
> 6. 한 권에 다섯 모델이 함께 들어 있어서, 표의 한 행이나 각주 하나가 일부 모델에만 해당할 수 있습니다. 다른 모델의 절차를 그대로 가져오면, 그럴듯한 오답이 됩니다.  (26.38–35.68, 32.20부터는 M03 ‘그럴듯한 오답’ 도식)

**② Flow 입력 방식: 소재 · 이미지 없음 (텍스트 → 동영상)** — 직전 구간은 M02 모션그래픽(두 권의 PDF와 페이지 수)이다. 도식에서 사진풍 책 페이지 접사로 하드컷하는 새 구도라 프레임이 아니고, 직전이 Flow가 아니므로 이어 붙이기도 없다. 펼친 페이지는 대상 설명 전문으로 충분하다.

**③ 프롬프트 및 적용 방법** — 텍스트 → 동영상, 가로 16:9, 720p, 8초, 이미지 없음. 채택 테이크만 1080p 업스케일 → `F03_1080p.mp4`. 본편에는 0–8.00초 전부.

```text
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.5s): close-up of a thick manual lying open on a light oak desk. The right-hand page shows one large printed specification table: five columns with bold headers "A", "B", "C", "D", "E" across the top, and eight rows of small black text and check marks. The camera glides slowly from the left column to the right column at a low angle across the page.
Shot 2 (2.5–5.5s): straight top-down view of the same table, camera still. One single row lights up with a soft amber highlight only across columns "A" and "B"; the same row in columns "C", "D" and "E" stays plain white. A small amber check mark appears inside the highlighted cells at 3.2s.
Shot 3 (5.5–8.0s): macro shot of the bottom of the same page. A tiny printed asterisk footnote line sits under the table; the asterisk glows amber, and a thin amber leader line draws itself from the asterisk up to the highlighted row, ending exactly on the highlighted cell in column "B". The camera slowly pulls back so the footnote, the line and the highlighted row are all in frame.

SUBJECT (keep identical in every shot): a thick printed product manual, about 5 cm thick, open flat at the middle, matte off-white paper with black print. The right-hand page holds one specification table with exactly five columns labeled "A", "B", "C", "D", "E" and eight rows; a single asterisk footnote line under the table. The amber highlight covers only columns A and B of one row.
BACKGROUND: a bright tech-support office desk in daytime; soft window light from the left; out-of-focus pale-grey wall and the corner of a white printer at the far top edge of the frame. The background stays the same in all three shots.
STYLE: photoreal tabletop macro cinematography, shallow depth of field, clean daylight, amber used only for the table highlight, the check marks and the footnote line. Fill the whole 16:9 frame edge to edge. All label text is bold clean sans-serif, crisp and fully legible.
EXCLUSIONS: no subtitles, no caption bar, no bottom text overlay, no burned-in captions, no karaoke-style word-by-word timing, no brand logos, no watermark.
```

## F04 · 본편 59.00–66.20초

**① 해당 대본**

> 10. 그럼, 자료에 없는 걸 물어보면요?  (59.12–61.40)
> 11. 답을 지어내지 않고, 확인할 수 없다고 말하는 게 정답입니다!  (62.08–65.66)

**② Flow 입력 방식: 소재 · 이미지 없음 (텍스트 → 동영상)** — 직전 구간은 M06 모션그래픽(답변 카드와 인용 칩)이다. 도식에서 사진풍 카드 목록함으로 하드컷하는 새 구도라 프레임이 아니고, 이어 붙이기도 없다. ‘근거를 찾았는데 없다’를 실제 사물의 빈 서랍으로 보여 준다.

**③ 프롬프트 및 적용 방법** — 텍스트 → 동영상, 가로 16:9, 720p, 8초, 이미지 없음. 채택 테이크만 1080p 업스케일 → `F04_1080p.mp4`. 본편에는 0–7.20초.

```text
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.5s): medium shot of a tall wooden card-catalog cabinet with twenty small drawers in a 5 by 4 grid, each drawer with a brass handle and an empty brass label holder. One drawer in the middle row slides open by itself toward the camera; a thin cyan beam of light sweeps across the front of the drawers just before it opens. Slow dolly-in.
Shot 2 (2.5–5.0s): top-down close-up looking straight into the open drawer. The drawer is completely empty: bare wood bottom and one wooden divider, no cards at all. The cyan beam passes slowly over the empty drawer from left to right and finds nothing.
Shot 3 (5.0–8.0s): close-up on the top of the cabinet. A single blank white index card lies there; a wooden rubber stamp presses down on it and lifts away, leaving the red stamped text "NO EVIDENCE" in bold capital letters in the center of the card. The camera stays still while the stamp lifts, then slowly pushes in on the card.

SUBJECT (keep identical in every shot): a tall honey-brown wooden card-catalog cabinet with exactly twenty small drawers in a 5-wide by 4-high grid, brass handles, empty brass label holders. The searching AI is always shown as a thin horizontal beam of cyan light. One blank white index card and one wooden rubber stamp with red ink.
BACKGROUND: a quiet archive room with warm lamp light from the upper right, out-of-focus rows of shelves with grey document boxes in soft shadow, pale beige walls. The background stays the same in all three shots.
STYLE: photoreal cinematography, 50 mm lens, warm lamp light against soft cool shadows, cyan used only for the search beam, red used only for the stamp text. Fill the whole 16:9 frame edge to edge. All label text is bold clean sans-serif, crisp and fully legible.
EXCLUSIONS: no subtitles, no caption bar, no bottom text overlay, no burned-in captions, no karaoke-style word-by-word timing, no faces, no brand logos, no watermark.
```

## F05 · 본편 106.60–112.90초

**① 해당 대본**

> 18. 문항당 제한 시간은 육십 초. 실패와 타임아웃도 지우지 않고 그대로 기록합니다.  (107.20–112.34)

**② Flow 입력 방식: 소재 · 이미지 없음 (텍스트 → 동영상)** — 직전 구간은 M12 모션그래픽(0.40 기준선 → 효율 0점)이고, 도식에서 사진풍 책상으로 하드컷하는 새 구도라 이어지는 장면이 아니다. 앞 영상의 이미지를 넣어 잇는 경우가 아니므로 프레임이 아니다. 배경의 프린터는 대상 설명 전문(PRINTER)으로 F01과 맞춘다.

**③ 프롬프트 및 적용 방법** — 텍스트 → 동영상, 가로 16:9, 720p, 8초, 이미지 없음. 채택 테이크만 1080p 업스케일 → `F05_1080p.mp4`. 본편에는 0–6.30초. 그래서 시계바늘이 60에 닿는 순간을 Shot 2 끝(약 4.5초)으로 앞당겼다.

```text
8-second clip, three hard-cut shots. Only ONE printer appears, small and out of focus in the background.
Shot 1 (0.0–2.0s): close-up of a large silver analog stopwatch lying on a light oak desk. Its white dial is marked 0 to 60 seconds, with "60" printed bold at the top and a short red arc painted on the dial just before 60. A finger presses the top crown and the single black second hand starts sweeping.
Shot 2 (2.0–4.5s): tight close-up on the dial, camera still. The second hand sweeps fast through the numbers and reaches the "60" mark at 4.4s; the red arc glows.
Shot 3 (4.5–8.0s): top-down shot of a printed paper log sheet next to the stopwatch. The sheet has ruled rows with short lines of grey printed text; a black pen writes a new row at the bottom, and a red label "TIMEOUT" appears at the right end of that new row at 5.3s. The earlier rows stay visible above it; nothing is crossed out.

SUBJECT (keep identical in every shot): one large silver analog stopwatch with a white 0–60 second dial, bold "60" at the top, a short red arc before 60, one black second hand. A paper log sheet with ruled rows. PRINTER in the background: a compact A4 inkjet multifunction printer with a matte white body and dark charcoal-grey top scanner lid, a small color touchscreen on the front left, a pull-out paper tray at the bottom front, and four small transparent ink-tank windows on the front right showing black, cyan, magenta and yellow ink levels; no brand logo or brand name anywhere on the printer.
BACKGROUND: the same bright modern tech-support office in daytime; light oak desk; soft window light from the left; out-of-focus white shelves and pale-grey wall. The background stays the same in all three shots.
STYLE: photoreal tabletop cinematography, shallow depth of field, clean daylight, red used only for the time-limit arc and the TIMEOUT label. Fill the whole 16:9 frame edge to edge. All label text is bold clean sans-serif, crisp and fully legible.
EXCLUSIONS: no subtitles, no caption bar, no bottom text overlay, no burned-in captions, no karaoke-style word-by-word timing, no faces, no brand logos, no watermark.
```

## F06 · 본편 112.90–119.00초

**① 해당 대본**

> 19. 마지막 날에는 다른 팀원이 같은 버전으로 다시 실행해서, 결과가 재현되는지 확인합니다.  (112.92–118.24)

**② Flow 입력 방식: 소재 · 이미지 없음 (텍스트 → 동영상)** — 직전 구간 F05는 8초 중 0–6.30초만 쓰고 끝을 잘라 쓴다. 게다가 스톱워치에서 두 노트북으로 넘어가는 새 구도의 하드컷이라 이어 붙이기·편집점 프레임을 쓰지 않는다. 노트북 두 대는 대상 설명 전문으로 맞춘다.

**③ 프롬프트 및 적용 방법** — 텍스트 → 동영상, 가로 16:9, 720p, 8초, 이미지 없음. 채택 테이크만 1080p 업스케일 → `F06_1080p.mp4`. 본편에는 0–6.10초. 그래서 ‘SAME RESULT’ 라벨을 5.2초에 띄운다.

```text
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.0s): close-up of the left laptop on a light oak desk. A hand with a dark-blue sweater sleeve presses the Enter key; on the screen a thin cyan progress bar fills from left to right under a small white tag "v1.0".
Shot 2 (2.0–4.5s): close-up of a second, identical laptop at the right end of the same desk. A different hand with a light-grey hoodie sleeve presses the Enter key; the same white tag "v1.0" and the same cyan progress bar fill on its screen.
Shot 3 (4.5–8.0s): wide shot from the front showing both laptops side by side. Both screens now display the same simple bar chart with four bars of identical heights in the same colors. A green label "SAME RESULT" appears floating between the two screens at 5.2s; the camera slowly pulls back.

SUBJECT (keep identical in every shot): two identical silver laptops with dark screens, placed side by side 60 cm apart on a light oak desk. Each screen shows a small white tag "v1.0", a cyan progress bar, and later the same four-bar chart (bars in teal, teal, amber, teal, identical heights on both screens). Two different people's hands only: left person in a dark-blue sweater, right person in a light-grey hoodie.
BACKGROUND: the same bright modern tech-support office in late afternoon; soft window light from the left; out-of-focus white shelves, a potted green plant and pale-grey wall. The background stays the same in all three shots.
STYLE: photoreal cinematography, 35 mm lens, shallow depth of field, cyan used only for progress bars, green used only for the SAME RESULT label. Fill the whole 16:9 frame edge to edge. All label text is bold clean sans-serif, crisp and fully legible.
EXCLUSIONS: no subtitles, no caption bar, no bottom text overlay, no burned-in captions, no karaoke-style word-by-word timing, no faces, no brand logos, no watermark.
```

---

# 재생성 요청 — 1차 검수 (2026-11-19)

수령: F01~F06 6개 모두 1920×1080·24fps·7.93초(190프레임). F04·F05·F06은 채택. 아래 3개를 다시 생성한다.

| ID | 문제(소스 시각) | 설명이 어떻게 달라지나 | 수정 |
|---|---|---|---|
| F01 | 3.85–5.0초 앰버 밑줄이 ‘0’/‘5’가 아니라 두 명판의 ‘DW’ 아래 | 두 모델이 같은 ‘DW’ 부분에서 다르다고 읽힘(실제 차이는 숫자 하나) | 밑줄 대신 **다른 숫자 자체를 앰버색으로 인쇄**, Shot 2에서 그 숫자만 빛남 |
| F02 | 0–0.29초 F01 첫 장면 정지 후 하드컷, 프린터 1대 | F01→F02 연결이 안 됨. 시작 프레임이 편집점(5.94초) 화면이 아니었음 | F01 재채택 후 **에이전트가 편집점 프레임 PNG를 추출해 전달** → 그 이미지로 프레임 생성, Shot 1을 끊김 없는 한 동작으로 단순화 |
| F03 | 2.5–5.5초 열 머리글이 A B / B C D E로 ‘B’ 중복, 표·각주 글자가 의미 없는 영문 | 다섯 모델 열이 여섯으로 보임 | 표를 오른쪽 한 페이지에만, 머리글 A~E 각 1회, 행 이름·각주는 글자 대신 회색 막대 |

선택: F05 배경 프린터가 F01과 모양이 다름(흐린 배경이라 채택 유지).

## F01 재생성 (F01-r2)

**① 해당 대본** — 1. 이름이 숫자 하나만 다른 프린터 두 대. AI는 내 모델의 답을, 정확히 골라낼 수 있을까요? (0.00–5.22)

**② Flow 입력 방식: 소재 · 이미지 없음 (텍스트 → 동영상)** — 첫 장면이라 직전 구간이 없다. 기존 테이크의 배경·프린터 외형이 좋아도, 이미 만든 영상의 화면을 소재로 넣어 새 구도를 만드는 것은 지침상 쓰지 않으므로 대상 설명 전문으로 다시 세운다.

**③ 프롬프트 및 적용 방법** — 텍스트 → 동영상, 16:9, 720p, 8초, 이미지 없음. 채택 테이크만 1080p 업스케일 → `F01_1080p.mp4`. 본편 0–5.94초. 채택본을 주시면 에이전트가 5.94초 화면을 `F01-frame-5.94s.png`로 추출해 F02용으로 드린다.

```text
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.5s): eye-level wide shot of two identical printers standing side by side on a light oak desk, 30 cm apart. Slow dolly-in toward the gap between them. A small white plastic name plate stands in front of each printer: the left plate reads "DCP-T830DW", the right plate reads "DCP-T835DW". On both plates every character is printed in black except ONE digit printed in bright amber: the "0" of 830 on the left plate and the "5" of 835 on the right plate.
Shot 2 (2.5–5.0s): low close-up sliding left to right along the two name plates at plate height, both plates fully readable. At 3.5s only the two amber digits, "0" on the left plate and "5" on the right plate, pulse with a soft amber glow at the same moment; all other characters stay plain black. No underline, no extra marks.
Shot 3 (5.0–8.0s): medium shot from slightly above, both printers and both name plates in frame. Both touchscreens light up at the same time showing one large white question mark on a blue screen. The camera slowly rises above the two printers.

SUBJECT (keep identical in every shot): two identical printers. Each PRINTER: a compact A4 inkjet multifunction printer with a matte white body and dark charcoal-grey top scanner lid, a small color touchscreen on the front left, a pull-out paper tray at the bottom front, and four small transparent ink-tank windows on the front right showing black, cyan, magenta and yellow ink levels; no brand logo or brand name anywhere on the printer. Same size, same color, same orientation (front facing camera). Name plates: small white plastic desk plates, left "DCP-T830DW" with the "0" in amber, right "DCP-T835DW" with the "5" in amber, all other characters black.
BACKGROUND: a bright modern tech-support office in daytime; soft window light from the left; out-of-focus white shelves with grey binders and a potted green plant behind the desk; clean pale-grey wall. The background stays the same in all three shots.
STYLE: photoreal product-style cinematography, 35 mm lens, shallow depth of field, clean daylight, amber used only for the two differing digits. Fill the whole 16:9 frame edge to edge. All label text is bold clean sans-serif, crisp and fully legible.
EXCLUSIONS: no subtitles, no caption bar, no bottom text overlay, no burned-in captions, no karaoke-style word-by-word timing, no underlines, no brand logos, no watermark.
```

## F02 재생성 (F02-r2) — F01-r2 채택 뒤

**① 해당 대본** — 2. 이번 프로젝트는 브라더 프린터와 복합기 열 개 모델의 기술지원 질문에, 공식 문서로 답하는 래그 에이전트를 만드는 겁니다. (5.94–12.62, 13.00부터 M01)

**② Flow 입력 방식: 프레임 · 편집점 프레임 업로드 (프레임 → 동영상)** — 직전 F01을 0–5.94초만 쓰고 끝을 잘라 쓰므로 이어 붙이기는 하지 않는다. 시작 프레임 = F01-r2 채택본의 소스 5.94초 화면 `F01-frame-5.94s.png`(에이전트 추출). 1차 테이크는 F01 첫 장면을 넣어 생성돼 연결되지 않았다.

**③ 프롬프트 및 적용 방법** — 프레임 → 동영상, **시작 프레임** 칸에 `F01-frame-5.94s.png`(끝 프레임 없음), 16:9, 720p, 8초. 채택 테이크만 1080p 업스케일 → `F02_1080p.mp4`. 본편 0–7.06초. 첫 2.6초는 컷 없이 시작 프레임에서 이어져야 한다.

```text
Start exactly from the provided start frame. The first 2.6 seconds are ONE unbroken camera move with no cut: the first video frame is identical to the start frame.
8-second clip: one continuous opening move, then two hard-cut shots.
Shot 1 (0.0–2.6s, continuous from the start frame): the camera slowly cranes straight up and tilts down over the same two printers, which stay in frame the whole time with their blue question-mark screens and their name plates. As the camera rises, the large light oak meeting table in front of the printers comes into view: two thick printed manuals with plain dark-blue covers, two open laptops, and four people's hands and forearms (no faces) resting around the table.
Shot 2 (2.6–5.2s): hard cut to a straight top-down view of the middle of the same table, camera still. The hands place ten small white cards in two neat rows of five between the two manuals; the left row sits next to the left manual, the right row next to the right manual. Each card shows only a tiny grey printer icon. A white label "10 MODELS" appears above the two rows at 4.0s.
Shot 3 (5.2–8.0s): hard cut to a low push-in toward one open laptop. Its screen shows a simple chat window with a blinking cursor in an empty input box and a small cyan magnifying-glass icon; the ten cards and one manual stay visible out of focus in the foreground.

SUBJECT (keep identical to the start frame in every shot): two identical printers. Each PRINTER: a compact A4 inkjet multifunction printer with a matte white body and dark charcoal-grey top scanner lid, a small color touchscreen on the front left, a pull-out paper tray at the bottom front, and four small transparent ink-tank windows on the front right showing black, cyan, magenta and yellow ink levels; no brand logo or brand name anywhere on the printer. Name plates: left "DCP-T830DW", right "DCP-T835DW". Two thick printed manuals (about 5 cm thick) with plain dark-blue covers and no text. Ten small white cards with a tiny grey printer icon.
BACKGROUND: the same bright modern tech-support office in daytime as the start frame; light oak table filling most of the frame; soft window light from the left; out-of-focus white shelves with grey binders and a potted green plant. The background stays the same in all three shots.
STYLE: photoreal cinematography matching the start frame, soft daylight, cyan used only for search icons. Fill the whole 16:9 frame edge to edge. All label text is bold clean sans-serif, crisp and fully legible.
EXCLUSIONS: no subtitles, no caption bar, no bottom text overlay, no burned-in captions, no karaoke-style word-by-word timing, no faces, no brand logos, no watermark.
```

## F03 재생성 (F03-r2)

**① 해당 대본** — 5. 그런데, 함정이 있습니다. (24.40–25.56) / 6. 한 권에 다섯 모델이 함께 들어 있어서, 표의 한 행이나 각주 하나가 일부 모델에만 해당할 수 있습니다. … (26.38–, 32.20부터 M03)

**② Flow 입력 방식: 소재 · 이미지 없음 (텍스트 → 동영상)** — 직전 M02가 모션그래픽이고 책 페이지 접사로 하드컷하는 새 구도다. 대상 설명 전문으로 충분하다.

**③ 프롬프트 및 적용 방법** — 텍스트 → 동영상, 16:9, 720p, 8초, 이미지 없음. 채택 테이크만 1080p 업스케일 → `F03_1080p.mp4`. 본편 0–8.00초 전부.

```text
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.5s): close-up of a thick manual lying open on a light oak desk. The left-hand page holds only grey placeholder text lines. The right-hand page holds ONE specification table with exactly five columns; the header row shows the five letters "A", "B", "C", "D", "E" once each, left to right, white on dark grey. The camera glides slowly from column A to column E at a low angle.
Shot 2 (2.5–5.5s): straight top-down view of the right-hand page only, camera still. The table has exactly five columns A, B, C, D, E and eight rows. Each row's name cell is a short grey bar, not words. Every other cell holds only a black check mark or a short black dash. One single row lights up with a soft amber highlight only across columns "A" and "B"; the same row in columns "C", "D" and "E" stays plain white. Small amber check marks appear in the two highlighted cells at 3.2s.
Shot 3 (5.5–8.0s): macro shot of the bottom of the same page. Under the table is one footnote line: a black asterisk followed by a short grey bar. The asterisk glows amber, and a thin amber leader line draws itself from the asterisk up to the highlighted row, ending exactly on the highlighted cell in column "B". The camera slowly pulls back so the footnote, the line and the highlighted row are all in frame.

SUBJECT (keep identical in every shot): a thick printed product manual, about 5 cm thick, open flat at the middle, matte off-white paper. Left page: grey placeholder lines only. Right page: one table with exactly five columns headed "A", "B", "C", "D", "E" (each letter appears exactly once) and eight rows; row names are grey bars; cells contain only check marks or dashes; one asterisk footnote line under the table. The amber highlight covers only columns A and B of one row.
BACKGROUND: a bright tech-support office desk in daytime; soft window light from the left; out-of-focus pale-grey wall and the corner of a white printer at the far top edge of the frame. The background stays the same in all three shots.
STYLE: photoreal tabletop macro cinematography, shallow depth of field, clean daylight, amber used only for the table highlight, the check marks in it and the footnote line. Fill the whole 16:9 frame edge to edge. The only readable characters are the five column letters; all label text is bold clean sans-serif, crisp and fully legible.
EXCLUSIONS: no subtitles, no caption bar, no bottom text overlay, no burned-in captions, no karaoke-style word-by-word timing, no extra columns, no repeated column letters, no brand logos, no watermark.

---

# F01-r2 수령 검수 · F02 최종 요청 (2026-11-19)

F01-r2 `Two_printers_on_office_desk_1a81fafd_1.mp4` → `media/flow/F01_1080p.mp4` (1920×1080, 24fps, 190프레임). 컷: 2.458초(59프레임), 4.958초(119프레임).
- Shot 1(0–58): 왼쪽 ‘0’만 앰버, 오른쪽 ‘5’는 검정. 사용.
- Shot 2(59–189 중 59–79): 59–79는 ‘DCP-T830DW’(앰버 0) 정상. **약 3.3초 이후 글자 변형**(DCDCP-T830DW, DCP-T85530DW, DCP-T855DW, 앰버 ‘3’) → 사용 금지.
- Shot 3(119–189): 물음표 화면, 명판 정상. 사용.
- **본편 편집**: 소스 0–71(72프레임) + 119–189(71프레임) = 143프레임 = 0–5.958초. 편집점 마지막 프레임 = 소스 189 = 테이크의 마지막 프레임.
- 한계: 오른쪽 ‘5’ 강조 없음 → 결말 M13에서 두 명판의 0/5를 함께 강조해 보완.

## F02 최종 (F02-r3)

**① 해당 대본** — 2. 이번 프로젝트는 브라더 프린터와 복합기 열 개 모델의 기술지원 질문에, 공식 문서로 답하는 래그 에이전트를 만드는 겁니다. (5.94–12.62)

**② Flow 입력 방식: 프레임 · 이어 붙이기 (확장/Extend)** — 직전 F01-r2를 편집에서 **테이크의 마지막 프레임(소스 189)까지** 쓰고, 카메라 상승이 끊김 없이 이어진다 → 공통 지침 표의 ‘Flow, 채택 테이크 끝까지 사용 · 동작·카메라 연속’. 이어 붙일 클립: F01-r2(Two_printers_on_office_desk_1a81fafd). 이미지 업로드 없음. 확장이 안 되면 대안: 프레임 → 동영상, 시작 프레임 `media/flow/F01-frame-end.png`(소스 189 추출, 에이전트 제공).

**③ 프롬프트 및 적용 방법** — Flow 장면 빌더에서 F01-r2 클립 뒤에 **확장(Extend)**, 16:9, 720p, 8초. 프롬프트는 이어 붙인 뒤 새로 일어날 사건부터. 채택한 확장 부분만 1080p 업스케일 → `F02_1080p.mp4`(F01 부분 제외, 확장 8초만). 본편 0–7.06초.

```text
Continue directly from the last frame with no cut for the first 2.6 seconds.
Shot 1 (0.0–2.6s, continuous): the camera keeps rising slowly and tilts down over the same two printers, which stay in frame the whole time with their blue question-mark screens and their white name plates "DCP-T830DW" and "DCP-T835DW". As the camera rises, a large light oak meeting table in front of the printers comes into view: two thick printed manuals with plain dark-blue covers, two open laptops, and four people's hands and forearms (no faces) resting around the table.
Shot 2 (2.6–5.2s): hard cut to a straight top-down view of the middle of the same table, camera still. The hands place ten small white cards in two neat rows of five between the two manuals; the left row next to the left manual, the right row next to the right manual. Each card shows only a tiny grey printer icon. A white label "10 MODELS" appears above the two rows at 4.0s.
Shot 3 (5.2–8.0s): hard cut to a low push-in toward one open laptop. Its screen shows a simple chat window with a blinking cursor in an empty input box and a small cyan magnifying-glass icon; the ten cards and one manual stay visible out of focus in the foreground.

SUBJECT (keep identical to the previous clip): two identical printers. Each PRINTER: a compact A4 inkjet multifunction printer with a matte white body and dark charcoal-grey top scanner lid, a small color touchscreen on the front left, a pull-out paper tray at the bottom front, and four small transparent ink-tank windows on the front right; no brand logo or brand name anywhere. Two thick printed manuals with plain dark-blue covers and no text. Ten small white cards with a tiny grey printer icon.
BACKGROUND: the same bright modern tech-support office in daytime; light oak table; soft window light from the left; out-of-focus white shelves with grey binders and a potted green plant. The background stays the same in all three shots.
STYLE: photoreal cinematography matching the previous clip, soft daylight, cyan used only for search icons. Fill the whole 16:9 frame edge to edge. All label text is bold clean sans-serif, crisp and fully legible.
EXCLUSIONS: no subtitles, no caption bar, no bottom text overlay, no burned-in captions, no karaoke-style word-by-word timing, no faces, no brand logos, no watermark.
```
