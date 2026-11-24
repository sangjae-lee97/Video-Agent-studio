# Flow 일괄 요청 — Brother RAG 실험 기록 (6클립)

공통 설정: Google Flow 웹 · 가로 16:9 · 720p(1280×720) · **8초** 생성 · 채택 테이크만 무료 1080p 업스케일. 돌려줄 파일명: `F01_1080p.mp4` … `F06_1080p.mp4`.
입력 방식: 6클립 모두 **소재 · 이미지 없음**(텍스트 → 동영상). 모든 Flow 구간의 직전 구간이 모션그래픽이거나(F01은 첫 장면) 새 구도로 하드컷하므로 프레임·이어 붙이기 대상이 없고, 업로드할 이미지도 없다. 순서: F01 먼저(수미상관 F06의 기준) → 나머지 자유.
메타포: 무향실 계측 벤치(template-spec.md). 장면 안 한글 라벨(인쇄·저소음·대기·1,099쪽·홈·전원·취소·청크·검색·생성)은 결과에서 철자를 확인하고, 틀리면 편집에서 덮어 보정한다. 프린터에 로고가 생기면 편집에서 지운다.

| ID | 본편 구간 | 사용 길이 | 대사 |
|---|---|---|---|
| F01 | 0.00–7.90초 | 7.90초 | 1번·2번 |
| F02 | 15.20–21.50초 | 6.30초 | 4번 |
| F03 | 44.30–52.20초 | 7.90초 | 8번·9번 |
| F04 | 79.10–86.10초 | 7.00초 | 14번 |
| F05 | 124.60–132.50초 | 7.90초 | 20번 |
| F06 | 134.40–141.10초 | 6.70초 | 21번 |

Flow 합계 43.70초 / 145.43초 = 30.0%.

---

## F01 · 본편 0.00–7.90초 (소스 0.00–7.90초 전부)

**① 해당 대본**

> 1. 프린터가 인쇄할 때 몇 데시벨이냐고 물었습니다.  (0.00–2.52)
> 2. AI는 설명서의 정답 페이지를 정확히 펼쳐 놓고, 삼십 데시벨이라고 답했습니다.  (3.10–8.08, 7.90 이후는 M01 계측 패널로 이어짐)

**② Flow 입력 방식:** **소재 · 이미지 없음 (텍스트 → 동영상)** — 영상의 첫 장면이라 직전 구간이 없고, 참고할 이미지도 없다. 대상 설명 전문으로 무향실을 세운다. F06이 이 클립과 같은 앵글로 끝맺으므로(수미상관) 가장 먼저 생성해 보여 주면 F06 프롬프트를 실제 화면에 맞출 수 있다.

**③ 프롬프트 및 적용 방법** — Flow 텍스트 → 동영상, 가로 16:9, 720p, 8초, 이미지 입력 없음. 아래 블록 전체 붙여넣기. 채택 테이크만 1080p 업스케일 후 `F01_1080p.mp4`로 저장.

```text
8-second clip, three hard-cut shots.

Shot 1 (0.0–2.6s): wide shot from slightly above, camera slowly pushing in toward the printer. The printer is actively printing: one white sheet slides out onto the front tray and a second sheet starts to emerge. The microphone and the sound level meter are clearly visible in the foreground.

Shot 2 (2.6–5.2s): hard cut to a low side view at microphone height. The camera tracks slowly along the black cable from the microphone tip to the sound level meter, showing that the microphone is aimed exactly at the printer. The printer is in soft focus in the background and has stopped printing; the paper lies still in the tray.

Shot 3 (5.2–8.0s): hard cut to a straight-on close-up of the sound level meter. The amber seven-segment digits flicker, then settle at 6.4s on "30.0" with a small amber "dB" next to it, and stay. The mode selector knob below the display is visible in the frame and points to "대기". The camera holds steady with a very slight push-in.

SUBJECT (keep identical in every shot): a compact matte light-grey office laser printer with no logo and no brand text anywhere, a front paper output tray, and a small dark control panel at its top right, standing on a waist-high brushed-steel test stand at the center of an anechoic test chamber. One meter in front of the printer, a slim black measurement microphone on a thin tripod points straight at it; a black cable runs from the microphone to a handheld black sound level meter clamped on a short stand beside the tripod. The sound level meter has a wide amber seven-segment display and, below it, a rotary mode selector knob with three positions printed in white: "인쇄", "저소음", "대기".

BACKGROUND: walls and ceiling completely covered in mid-grey, slightly blue-tinted acoustic foam wedges; a suspended steel wire-mesh floor; cool, even white light from square overhead panels; no windows, no people, a quiet clinical atmosphere. The same chamber in all three shots.

STYLE: photoreal, 35 mm lens, slow precise camera moves, cool grey palette; amber is used only for instrument readouts and labels, red only for error marks. Fill the whole 16:9 frame edge to edge. No narration captions, no subtitle bars, no logos, no watermark.
```

---

## F02 · 본편 15.20–21.50초 (소스 0.00–6.30초)

**① 해당 대본**

> 4. 우리 팀은 브라더 프린터 설명서 두 권, 천구십구 쪽으로 기술지원 래그 에이전트를 만들고 있었습니다.  (15.64–21.04)

**② Flow 입력 방식:** **소재 · 이미지 없음 (텍스트 → 동영상)** — 직전 구간은 M01 모션그래픽(측정기 패널)이고 이 장면은 벤치 위 설명서로 하드컷하는 새 구도다. 프레임·이어 붙이기 대상이 없다. 이미 생성한 영상 화면을 소재로 넣지 않는 지침에 따라, 대상 설명 전문으로 같은 무향실을 맞춘다.

**③ 프롬프트 및 적용 방법** — Flow 텍스트 → 동영상, 가로 16:9, 720p, 8초, 이미지 입력 없음. 아래 블록 전체 붙여넣기. 채택 테이크만 1080p 업스케일 후 `F02_1080p.mp4`로 저장.

```text
8-second clip, three hard-cut shots.

Shot 1 (0.0–2.4s): low camera tracking sideways along a brushed-steel side bench next to the printer's test stand. On the bench lie two very thick printed manuals side by side, matte grey covers with no logo. Each spine has one large amber number printed on it: the left spine "466", the right spine "633".

Shot 2 (2.4–4.8s): hard cut to a straight top-down view of the two thick manuals. At 2.6s a single clean amber label "1,099쪽" lights up centered above the two books, and stays.

Shot 3 (4.8–8.0s): hard cut to a medium shot from the side. The page edges of both manuals begin to glow softly amber, and two thin amber lines draw themselves from the books across the bench toward the sound level meter and the printer on its test stand.

SUBJECT (keep identical in every shot): two very thick printed manuals with matte grey covers and no logo, lying side by side on a brushed-steel side bench, spines labeled "466" and "633" in amber. Behind them, a compact matte light-grey office laser printer with no logo and no brand text stands on a waist-high brushed-steel test stand; a slim black measurement microphone on a thin tripod points at it, cabled to a handheld black sound level meter with a wide amber seven-segment display and a rotary mode selector printed "인쇄", "저소음", "대기".

BACKGROUND: walls and ceiling completely covered in mid-grey, slightly blue-tinted acoustic foam wedges; a suspended steel wire-mesh floor; cool, even white light from square overhead panels; no windows, no people, a quiet clinical atmosphere. The same chamber in all three shots.

STYLE: photoreal, 35 mm lens, slow precise camera moves, cool grey palette; amber is used only for instrument readouts and labels, red only for error marks. Fill the whole 16:9 frame edge to edge. No narration captions, no subtitle bars, no logos, no watermark.
```

---

## F03 · 본편 44.30–52.20초 (소스 0.00–7.90초)

**① 해당 대본**

> 8. 그런데 맨 처음 그 소음 질문처럼, 페이지는 맞는데 답이 틀리는 경우가 남아 있었습니다.  (44.56–49.54)
> 9. 찾기는 찾았는데, 왜 틀렸을까요?  (50.24–52.24)

**② Flow 입력 방식:** **소재 · 이미지 없음 (텍스트 → 동영상)** — 직전 구간은 M04 모션그래픽(프로브 B 12/12)이라 이어 붙일 Flow가 없다. 무향실로 하드컷하는 새 구도이며, F01과 같은 대상 설명 전문으로 모양을 맞춘다. F01과 화면이 겹치지 않도록 이번에는 판독창이 아니라 **인쇄 중인 프린터와 모드 다이얼**을 보여 준다.

**③ 프롬프트 및 적용 방법** — Flow 텍스트 → 동영상, 가로 16:9, 720p, 8초, 이미지 입력 없음. 아래 블록 전체 붙여넣기. 채택 테이크만 1080p 업스케일 후 `F03_1080p.mp4`로 저장.

```text
8-second clip, three hard-cut shots.

Shot 1 (0.0–2.6s): medium side view of the printer, camera slowly trucking right. The printer is busy printing: sheets keep sliding out and stacking on the front tray.

Shot 2 (2.6–5.4s): hard cut to a shot over the sound level meter. The rotary mode selector knob is sharp in the foreground and clearly points to "대기"; behind it, the printer is out of focus but visibly still printing, sheets still sliding out.

Shot 3 (5.4–8.0s): hard cut to a macro of the mode selector knob. A thin red ring draws itself around the word "대기" from 5.8s to 6.4s and stays. The printer keeps printing, blurred in the background. Camera holds steady.

SUBJECT (keep identical in every shot): a compact matte light-grey office laser printer with no logo and no brand text anywhere, a front paper output tray, and a small dark control panel at its top right, standing on a waist-high brushed-steel test stand at the center of an anechoic test chamber. One meter in front of the printer, a slim black measurement microphone on a thin tripod points straight at it; a black cable runs from the microphone to a handheld black sound level meter clamped on a short stand beside the tripod. The sound level meter has a wide amber seven-segment display and, below it, a rotary mode selector knob with three positions printed in white: "인쇄", "저소음", "대기".

BACKGROUND: walls and ceiling completely covered in mid-grey, slightly blue-tinted acoustic foam wedges; a suspended steel wire-mesh floor; cool, even white light from square overhead panels; no windows, no people, a quiet clinical atmosphere. The same chamber in all three shots.

STYLE: photoreal, 35 mm lens, slow precise camera moves, cool grey palette; amber is used only for instrument readouts and labels, red only for error marks. Fill the whole 16:9 frame edge to edge. No narration captions, no subtitle bars, no logos, no watermark.
```

---

## F04 · 본편 79.10–86.10초 (소스 0.00–7.00초)

**① 해당 대본**

> 14. 희주님은 그림으로만 그려진 버튼 백오십칠 곳에 이름을 되찾아 주고, 해당하지 않는 모델을 조각 스무 개에 적었습니다.  (79.26–85.58)

**② Flow 입력 방식:** **소재 · 이미지 없음 (텍스트 → 동영상)** — 직전 구간은 M08 모션그래픽(두 번째 사실 누락)이다. 프린터 조작부 근접으로 하드컷하는 새 구도라 프레임 대상이 없다.

**③ 프롬프트 및 적용 방법** — Flow 텍스트 → 동영상, 가로 16:9, 720p, 8초, 이미지 입력 없음. 아래 블록 전체 붙여넣기. 채택 테이크만 1080p 업스케일 후 `F04_1080p.mp4`로 저장.

```text
8-second clip, three hard-cut shots.

Shot 1 (0.0–2.4s): macro of the printer's small dark control panel, camera sliding slowly from left to right. Next to a small dark monochrome screen there is a row of three round buttons marked only with white icons and no text: a house icon, a power icon and an X icon.

Shot 2 (2.4–4.8s): hard cut to a straight-on close-up of the same three buttons. One after another, small clean amber text labels light up directly beside each icon: "홈" next to the house at 2.8s, "전원" next to the power icon at 3.3s, "취소" next to the X at 3.8s. The labels stay.

Shot 3 (4.8–8.0s): hard cut to a slow pull-back from the control panel to the whole printer on its test stand; the three amber labels remain lit beside their buttons.

SUBJECT (keep identical in every shot): a compact matte light-grey office laser printer with no logo and no brand text anywhere, a front paper output tray, and a small dark control panel at its top right, standing on a waist-high brushed-steel test stand at the center of an anechoic test chamber. One meter in front of the printer, a slim black measurement microphone on a thin tripod points straight at it; a black cable runs from the microphone to a handheld black sound level meter clamped on a short stand beside the tripod. The sound level meter has a wide amber seven-segment display and, below it, a rotary mode selector knob with three positions printed in white: "인쇄", "저소음", "대기".

BACKGROUND: walls and ceiling completely covered in mid-grey, slightly blue-tinted acoustic foam wedges; a suspended steel wire-mesh floor; cool, even white light from square overhead panels; no windows, no people, a quiet clinical atmosphere. The same chamber in all three shots.

STYLE: photoreal, 35 mm lens, slow precise camera moves, cool grey palette; amber is used only for instrument readouts and labels, red only for error marks. Fill the whole 16:9 frame edge to edge. No narration captions, no subtitle bars, no logos, no watermark.
```

---

## F05 · 본편 124.60–132.50초 (소스 0.00–7.90초)

**① 해당 대본**

> 20. 돌아보면 두 제출 사이엔 청크와 검색, 생성이 함께 바뀌었고, 문제도 같은 서른 문항이었습니다. 그래서 무엇이 몇 점을 올렸는지는 나눌 수 없습니다.  (124.72–133.82, 132.50 이후는 M15 “분리 불가” 카드)

**② Flow 입력 방식:** **소재 · 이미지 없음 (텍스트 → 동영상)** — 직전 구간은 M14 모션그래픽(지연 게이지)이다. 계측 콘솔로 하드컷하는 새 구도라 프레임 대상이 없다.

**③ 프롬프트 및 적용 방법** — Flow 텍스트 → 동영상, 가로 16:9, 720p, 8초, 이미지 입력 없음. 아래 블록 전체 붙여넣기. 채택 테이크만 1080p 업스케일 후 `F05_1080p.mp4`로 저장.

```text
8-second clip, three hard-cut shots.

Shot 1 (0.0–2.6s): medium shot of a grey measurement console on the steel bench. Its front has three large black rotary knobs in a row, each with a white printed label underneath: "청크", "검색", "생성". Three hands in grey nitrile gloves, one on each knob, turn all three knobs clockwise at exactly the same time. Only gloved hands and forearms are visible, no faces.

Shot 2 (2.6–5.2s): hard cut to a close-up of a large analog needle meter mounted on top of the console. Its white scale runs from 0 to 100 with a small amber tick at 91. The needle swings up from the 91 tick and settles exactly on 100.

Shot 3 (5.2–8.0s): hard cut back to the three knobs, closer. The gloved hands let go at the same moment; the three knobs stay still. At 6.6s a single amber question mark "?" lights up above the three knobs, and stays.

SUBJECT (keep identical in every shot): a grey measurement console standing on a brushed-steel bench, with three large black rotary knobs labeled "청크", "검색", "생성" and a large analog needle meter (white scale 0–100, amber tick at 91) mounted on top. A compact matte light-grey office laser printer with no logo stands on a test stand in the soft background.

BACKGROUND: walls and ceiling completely covered in mid-grey, slightly blue-tinted acoustic foam wedges; a suspended steel wire-mesh floor; cool, even white light from square overhead panels; no windows; no faces, only the gloved hands and forearms; a quiet clinical atmosphere. The same chamber in all three shots.

STYLE: photoreal, 35 mm lens, slow precise camera moves, cool grey palette; amber is used only for instrument readouts and labels, red only for error marks. Fill the whole 16:9 frame edge to edge. No narration captions, no subtitle bars, no logos, no watermark.
```

---

## F06 · 본편 134.40–141.10초 (소스 0.00–6.70초)

**① 해당 대본**

> 21. 두 제출의 청크 수는 똑같이 천오백이십팔 개였습니다. 바뀐 건 숫자 옆에 붙은 조건이었습니다.  (134.64–140.82)

**② Flow 입력 방식:** **소재 · 이미지 없음 (텍스트 → 동영상)** — 직전 구간은 M15 모션그래픽이다. F01과 같은 무향실·같은 앵글로 돌아오는 수미상관 하드컷이며, 연결 목적의 프레임이 아니다. 대상 설명 전문으로 F01과 맞추고, F01 채택본을 보고 앵글 문구를 다듬어 전달한다(F01 먼저 생성 권장).

**③ 프롬프트 및 적용 방법** — Flow 텍스트 → 동영상, 가로 16:9, 720p, 8초, 이미지 입력 없음. 아래 블록 전체 붙여넣기. 채택 테이크만 1080p 업스케일 후 `F06_1080p.mp4`로 저장.

```text
8-second clip, three hard-cut shots.

Shot 1 (0.0–2.4s): wide shot from slightly above, the same angle as an opening establishing shot: the printer on its test stand at the center, the microphone and sound level meter in the foreground. The printer is actively printing; sheets slide out onto the front tray. Camera holds almost still.

Shot 2 (2.4–4.6s): hard cut to a straight-on close-up of the sound level meter display. The amber seven-segment digits read "49.0" with a small amber "dB" next to it, steady.

Shot 3 (4.6–8.0s): hard cut to a close-up that frames the display and the mode selector knob together; the knob points to "인쇄". At 4.9s a thin amber ring draws itself around "인쇄" and stays, so the reading "49.0 dB" and its condition "인쇄" are read together. Slow push-in.

SUBJECT (keep identical in every shot): a compact matte light-grey office laser printer with no logo and no brand text anywhere, a front paper output tray, and a small dark control panel at its top right, standing on a waist-high brushed-steel test stand at the center of an anechoic test chamber. One meter in front of the printer, a slim black measurement microphone on a thin tripod points straight at it; a black cable runs from the microphone to a handheld black sound level meter clamped on a short stand beside the tripod. The sound level meter has a wide amber seven-segment display and, below it, a rotary mode selector knob with three positions printed in white: "인쇄", "저소음", "대기".

BACKGROUND: walls and ceiling completely covered in mid-grey, slightly blue-tinted acoustic foam wedges; a suspended steel wire-mesh floor; cool, even white light from square overhead panels; no windows, no people, a quiet clinical atmosphere. The same chamber in all three shots.

STYLE: photoreal, 35 mm lens, slow precise camera moves, cool grey palette; amber is used only for instrument readouts and labels, red only for error marks. Fill the whole 16:9 frame edge to edge. No narration captions, no subtitle bars, no logos, no watermark.
```

---

# v2 개정 — 끝부분(18~28번 줄) Flow 추가 요청 (2클립)

음성: `narration-v2/local-short-window-v1/narration_balanced.wav` (175.401초 + 여운 1.5초 = 본편 176.9초). 0~104.6초는 v1 그대로(F01~F04 그대로 사용).
기존 클립 재사용: **F05**(본편 109.00–114.25, 소스 0.00–5.25 = 노브 셋을 동시에 돌리는 1·2샷, 3샷의 “?”는 안 씀), **F06**(본편 155.20–159.30, 소스 2.46–6.56 = 49.0 dB → “인쇄” 링).
새로 뽑을 클립: **F07, F08** 두 개. 공통 설정은 위와 같다(16:9 · 720p · 8초 · 채택 테이크만 1080p 업스케일, 돌려줄 파일명 `F07_1080p.mp4`, `F08_1080p.mp4`). 두 클립 모두 직전 구간이 모션그래픽이라 **소재 · 이미지 없음**.

| ID | 본편 구간 | 사용 길이 | 대사 |
|---|---|---|---|
| F05(재사용) | 109.00–114.25 | 5.25초 | 18번 가운데 |
| F07(신규) | 125.40–132.90 | 7.50초 | 20번·21번 |
| F06(재사용) | 155.20–159.30 | 4.10초 | 26번 앞 |
| F08(신규) | 170.30–176.90 | 6.60초 | 28번 + 여운 |

Flow 합계: 앞부분 29.10 + 끝부분 23.45 = 52.55초 / 176.9초 = 29.7%.

---

## F07 · 본편 125.40–132.90초 (소스 0.00–7.50초)

**① 해당 대본**

> 20. 백 점을 받은 뒤, 같은 서른 문항을 같은 서버에 한 번 더 보내 봤습니다.  (125.62–129.18)
> 21. 상위 다섯 근거는 서른 번 모두 같았고, 핵심 답도 그대로였습니다.  (129.62–133.32, 132.90 이후는 M20 30칸 격자)

**② Flow 입력 방식:** **소재 · 이미지 없음 (텍스트 → 동영상)** — 직전 구간은 M19 모션그래픽(질문지 30줄)이라 프레임·이어 붙이기 대상이 없다. 대상 설명 전문으로 F01과 같은 무향실·같은 계측기를 다시 세운다.

**③ 프롬프트 및 적용 방법** — Flow 텍스트 → 동영상, 가로 16:9, 720p, 8초, 이미지 입력 없음. 아래 블록 전체 붙여넣기. 채택 테이크만 1080p 업스케일 후 `F07_1080p.mp4`로 저장. 출력지에 읽히는 글자가 생기면 편집에서 흐린다.

```text
8-second clip, three hard-cut shots.

Shot 1 (0.0–2.5s): close-up of the sound level meter on its short stand. A single hand in a grey nitrile glove enters from the right and presses the round black button under the amber display once, firmly, then withdraws. The amber seven-segment digits blink off and on again. Only the gloved hand and forearm are visible, no face.

Shot 2 (2.5–5.0s): hard cut to a medium side view of the printer on the steel test stand. A narrow white result strip, like a long receipt, feeds smoothly out of the front tray; it is covered in neat rows of short grey printed bars with no readable letters or numbers. The microphone on its tripod stands sharp in the foreground.

Shot 3 (5.0–8.0s): hard cut to a top-down view of the brushed-steel bench. Two identical white result strips lie side by side, perfectly parallel, their rows of grey bars at exactly the same heights. A gloved hand slowly slides a thin transparent amber ruler across both strips; under the ruler, the rows on the left strip and the right strip line up perfectly. The hand lets go at 7.0s and the camera holds still.

SUBJECT (keep identical in every shot): a compact matte light-grey office laser printer with no logo and no brand text anywhere, a front paper output tray, and a small dark control panel at its top right, standing on a waist-high brushed-steel test stand at the center of an anechoic test chamber. One meter in front of the printer, a slim black measurement microphone on a thin tripod points straight at it; a black cable runs from the microphone to a handheld black sound level meter clamped on a short stand beside the tripod. The sound level meter has a wide amber seven-segment display, a round black button below it, and a rotary mode selector knob with three positions printed in white: "인쇄", "저소음", "대기".

BACKGROUND: walls and ceiling completely covered in mid-grey, slightly blue-tinted acoustic foam wedges; a suspended steel wire-mesh floor; cool, even white light from square overhead panels; no windows; no faces, only gloved hands and forearms; a quiet clinical atmosphere. The same chamber in all three shots.

STYLE: photoreal, 35 mm lens, slow precise camera moves, cool grey palette; amber is used only for instrument readouts, the ruler and labels, red only for error marks. Fill the whole 16:9 frame edge to edge. No narration captions, no subtitle bars, no readable text on paper, no logos, no watermark.
```

---

## F08 · 본편 170.30–176.90초 (소스 0.00–6.60초, 마지막 1.98초는 음성 없는 여운)

**① 해당 대본**

> 28. 그래서 다음엔 처음 보는 질문으로, 어느 쪽이 나은지 직접 비교해 보겠습니다.  (170.50–174.92, 이후 여운으로 끝)

**② Flow 입력 방식:** **소재 · 이미지 없음 (텍스트 → 동영상)** — 직전 구간은 M24 모션그래픽(두 선택지 저울)이라 이어 붙일 프레임이 없다. 마지막 샷은 F01 첫 샷과 같은 앵글(약간 위에서 본 전경)로 수미상관을 맞춘다.

**③ 프롬프트 및 적용 방법** — Flow 텍스트 → 동영상, 가로 16:9, 720p, 8초, 이미지 입력 없음. 아래 블록 전체 붙여넣기. 채택 테이크만 1080p 업스케일 후 `F08_1080p.mp4`로 저장. 마지막 샷이 6.6초까지 정지에 가깝게 유지되는 테이크를 고른다.

```text
8-second clip, three hard-cut shots.

Shot 1 (0.0–2.2s): close-up on the brushed-steel bench next to the microphone tripod. A gloved hand sets down a small fresh stack of blank white cards, still wrapped with a thin amber paper band, then pulls the band off. The cards have no printing on them at all.

Shot 2 (2.2–4.4s): hard cut to a straight-on close-up of the sound level meter. The amber display shows three dashes "- - -", waiting. A gloved hand turns the mode selector knob from "대기" to "인쇄" with one smooth click, then withdraws.

Shot 3 (4.4–8.0s): hard cut to a wide shot from slightly above, the same angle as an establishing shot: the printer on its steel stand at the center, the microphone and the sound level meter in the foreground, the stack of blank cards on the bench beside them. Nobody is in frame. The camera very slowly pulls back and then holds completely still; the amber dashes on the meter glow softly. Calm, unfinished, ready for the next test.

SUBJECT (keep identical in every shot): a compact matte light-grey office laser printer with no logo and no brand text anywhere, a front paper output tray, and a small dark control panel at its top right, standing on a waist-high brushed-steel test stand at the center of an anechoic test chamber. One meter in front of the printer, a slim black measurement microphone on a thin tripod points straight at it; a black cable runs from the microphone to a handheld black sound level meter clamped on a short stand beside the tripod. The sound level meter has a wide amber seven-segment display and, below it, a rotary mode selector knob with three positions printed in white: "인쇄", "저소음", "대기".

BACKGROUND: walls and ceiling completely covered in mid-grey, slightly blue-tinted acoustic foam wedges; a suspended steel wire-mesh floor; cool, even white light from square overhead panels; no windows; no faces, only gloved hands and forearms; a quiet clinical atmosphere. The same chamber in all three shots.

STYLE: photoreal, 35 mm lens, slow precise camera moves, cool grey palette; amber is used only for instrument readouts, the paper band and labels, red only for error marks. Fill the whole 16:9 frame edge to edge. No narration captions, no subtitle bars, no logos, no watermark.
```
