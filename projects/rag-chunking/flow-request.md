# Flow 일괄 요청 — RAG 청킹 (6클립)

기준 음성: `narration/narration.wav` 160.780초 (sha256 825b7643…), 문장 시각 `narration/local-short-window-v2/sentence-boundaries.json`. 보정은 시각을 바꾸지 않는다.
공통 설정: Google Flow 웹 · 가로 16:9 · 720p(1280×720) · **8초** 생성 · 채택 테이크만 1080p 업스케일. 돌려줄 파일명: `F01_1080p.mp4` … `F06_1080p.mp4`.
입력 방식(공통 지침 2026-11-19 개정): F01 = 소재 · 이미지 없음, F02~F06 = 소재(이미지 `F01-ingredient.png`). 모든 Flow 클립의 직전 구간이 모션그래픽이고 사진풍 새 구도로 하드컷하므로 프레임·이어 붙이기 대상이 없다. 생성 순서: F01 → 채택 → 소재 이미지 저장 → F02~F06.
장면 안 한글 라벨은 Flow 결과에서 철자를 확인하고, 틀리면 편집에서 덮어 보정한다.

| ID | 본편 구간(초) | 사용 길이 | 생성 |
|---|---|---:|---:|
| F01 | 0.00–8.00 | 8.00 | 8초 |
| F02 | 26.38–34.38 | 8.00 | 8초 |
| F03 | 44.00–52.00 | 8.00 | 8초 |
| F04 | 72.92–80.92 | 8.00 | 8초 |
| F05 | 121.94–129.94 | 8.00 | 8초 |
| F06 | 152.08–160.08 | 8.00 | 8초 |

Flow 합계 48.00초 / 160.78초 = 29.9%.

---

## F01 · 본편 0.00–8.00초

**① 해당 대본**

> 1. 문서에는 분명히 정답이 있는데, AI는 왜 그걸 못 찾을까요?  (0.00–4.02)
> 2. 래그는 AI가 문서를 검색해서, 찾은 근거로 답하게 만드는 방식입니다.  (4.78–8.78, 8.00 이후는 M01 도식으로 이어짐)

**② Flow 입력 방식: 소재 · 이미지 없음 (텍스트 → 동영상)** — 영상의 첫 장면이라 직전 구간이 없고, 참고할 이미지도 아직 없다. 대상 설명 전문으로 장면을 세운다. 이 클립의 채택본이 F02~F06의 소재 이미지가 되므로 **가장 먼저 생성·채택**한다.

**③ 프롬프트 및 적용 방법** — Flow 텍스트 → 동영상, 가로 16:9, 720p, 8초, 이미지 입력 없음. 아래 블록 전체 붙여넣기. 채택 테이크만 1080p 업스케일 후 `F01_1080p.mp4`로 저장하고, Shot 1의 약 1.5초 프레임을 `F01-ingredient.png`로 저장(‘프레임 저장’).

```text
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.6s): high top-down wide shot of the whole long paper on the walnut desk; the camera slowly descends toward the middle. The bold answer line "금요일 오후 6시" catches a faint warm glint from the lamp so the viewer can find it.
Shot 2 (2.6–5.0s): low camera skimming along the paper surface at text height. The thin cyan light bar glides left to right over the rows of text, passes directly over the bold answer line without slowing down, and the answer line stays unlit as the bar moves on. Camera tracks with the bar.
Shot 3 (5.0–8.0s): medium top-down shot. The cyan light bar sweeps back, stops on one paragraph, and that paragraph glows cyan; a translucent glowing copy of the paragraph lifts straight up off the paper toward the camera, while the printed original stays on the paper. A small cyan label "RAG" appears floating beside the lifted copy at 5.6s and stays until the end.

SUBJECT (keep identical in every shot): one long sheet of cream-white paper, A4 width and about 1.2 meters long, lying flat and fully unrolled lengthwise from left to right on a dark walnut desk. The paper is printed with neat rows of small black text arranged in short paragraphs; between paragraphs there are clearly visible empty blank-line gaps. Exactly one line near the middle of the paper is printed in bold black and is the answer line: "금요일 오후 6시". A heavy brass-and-black guillotine paper cutter with one long straight steel blade stands at the right end of the desk. The AI search is always shown as a thin horizontal bar of cyan light that glides just above the paper surface.
BACKGROUND: a quiet library reading room at night; out-of-focus tall wooden bookshelves in deep navy-teal shadow behind the desk; a single warm brass desk lamp lights the paper from the upper left; a few dust motes float in the lamp beam. The background stays the same dim library in all three shots.
STYLE: photoreal tabletop macro cinematography, shallow depth of field, warm lamp light against cool navy shadows, cyan used only for the AI search light, red used only for cut lines and error marks. Fill the whole 16:9 frame edge to edge. No narration captions, no subtitle bars, no watermark.
```

## F02 · 본편 26.38–34.38초

**① 해당 대본**

> 6. 진짜 문제는, 어디서 자르느냐입니다.  (26.38–28.98)
> 7. 가장 단순한 건 글자 수마다 자르는 고정 크기 방식, 다른 하나는 빈 줄마다 자르는 문단 방식입니다.  (29.51–35.48, 34.38 이후는 M03 비교 도식)

**② Flow 입력 방식: 소재 (소재 → 동영상)** — 직전 구간은 M02 모션그래픽(자르기 ≠ 임베딩 도식)다. 도식에서 사진풍 책상 장면으로 하드컷하는 새 구도라 프레임이 아니며, 직전이 Flow가 아니므로 이어 붙이기도 없다. **넣을 이미지 1장: `F01-ingredient.png`** = F01 채택 테이크의 Shot 1 프레임(소스 약 1.5초, 책상·긴 종이·재단기·램프·도서관 배경이 함께 보이는 순간). 출처: F01 채택본에서 Flow ‘프레임 저장’ 또는 F01 파일을 주시면 에이전트가 추출. 고정하는 요소: 책상·종이·재단기·램프·배경의 모양과 색. F01 채택 후 생성한다.

**③ 프롬프트 및 적용 방법** — Flow 소재 → 동영상, 소재 칸에 `F01-ingredient.png` 1장, 가로 16:9, 720p, 8초. 아래 블록 전체 붙여넣기. 채택 테이크만 1080p 업스케일 후 `F02_1080p.mp4`로 저장.

```text
Use the ingredient image only as the reference for the look of the dark walnut desk, the long printed cream paper, the brass guillotine cutter, the brass desk lamp and the dim navy-teal library background. Do not copy its camera angle; compose new shots exactly as described below.
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.6s): low close-up of the guillotine cutter's raised steel blade hanging above the paper; the paper slowly slides under the blade from left to right. Thin red dashed candidate cut lines flicker across the paper at three different positions, one after another, as if choosing where to cut. The blade stays raised.
Shot 2 (2.6–5.4s): straight top-down view of a section of the paper. A brass ruler with evenly spaced tick marks lies along the top edge. Solid red cut lines snap down across the paper at every equal ruler interval, ignoring the text; one red line slices straight through the middle of a printed text line. A white label "고정 크기" appears next to the ruler at 3.0s.
Shot 3 (5.4–8.0s): same top-down view and same ruler. The red cut lines slide up or down until each one sits exactly inside a blank-line gap between paragraphs; the resulting sections now have clearly different heights. The label changes from "고정 크기" to "문단" at 5.8s. The paper does not move.

SUBJECT (keep identical in every shot): one long sheet of cream-white paper, A4 width and about 1.2 meters long, lying flat and fully unrolled lengthwise from left to right on a dark walnut desk. The paper is printed with neat rows of small black text arranged in short paragraphs; between paragraphs there are clearly visible empty blank-line gaps. Exactly one line near the middle of the paper is printed in bold black and is the answer line: "금요일 오후 6시". A heavy brass-and-black guillotine paper cutter with one long straight steel blade stands at the right end of the desk. The AI search is always shown as a thin horizontal bar of cyan light that glides just above the paper surface.
BACKGROUND: a quiet library reading room at night; out-of-focus tall wooden bookshelves in deep navy-teal shadow behind the desk; a single warm brass desk lamp lights the paper from the upper left; a few dust motes float in the lamp beam. The background stays the same dim library in all three shots.
STYLE: photoreal tabletop macro cinematography, shallow depth of field, warm lamp light against cool navy shadows, cyan used only for the AI search light, red used only for cut lines and error marks. Fill the whole 16:9 frame edge to edge. No narration captions, no subtitle bars, no watermark.
```

## F03 · 본편 44.00–52.00초

**① 해당 대본**

> 9. 강의 예시에서 육십 자씩 자르자, 정답 문구인 금요일 오후 여섯 시가 두 조각으로 갈라졌습니다. 검색 결과를 열 개까지 늘려도, 찾지 못했습니다.  (44.00–52.58, 52.00 이후는 M04에서 ‘10개 중 0’ 표시)

**② Flow 입력 방식: 소재 (소재 → 동영상)** — 직전 구간은 M03 모션그래픽(고정 크기 vs 문단 비교)다. 도식에서 사진풍 책상 장면으로 하드컷하는 새 구도라 프레임이 아니며, 직전이 Flow가 아니므로 이어 붙이기도 없다. **넣을 이미지 1장: `F01-ingredient.png`** = F01 채택 테이크의 Shot 1 프레임(소스 약 1.5초, 책상·긴 종이·재단기·램프·도서관 배경이 함께 보이는 순간). 출처: F01 채택본에서 Flow ‘프레임 저장’ 또는 F01 파일을 주시면 에이전트가 추출. 고정하는 요소: 책상·종이·재단기·램프·배경의 모양과 색. F01 채택 후 생성한다.

**③ 프롬프트 및 적용 방법** — Flow 소재 → 동영상, 소재 칸에 `F01-ingredient.png` 1장, 가로 16:9, 720p, 8초. 아래 블록 전체 붙여넣기. 채택 테이크만 1080p 업스케일 후 `F03_1080p.mp4`로 저장.

```text
Use the ingredient image only as the reference for the look of the dark walnut desk, the long printed cream paper, the brass guillotine cutter, the brass desk lamp and the dim navy-teal library background. Do not copy its camera angle; compose new shots exactly as described below.
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.5s): close side view of the guillotine cutter. The brass ruler beside the paper has a red marker at the tick labeled "60". The steel blade comes down fast at that mark and lands exactly across the bold answer line "금요일 오후 6시".
Shot 2 (2.5–5.0s): extreme macro top-down on the cut. The paper separates into two strips and a small dark gap opens between them; the bold answer line is split in two: the left strip shows "금요일 오" and the right strip shows "후 6시". A thin red outline traces the cut edge.
Shot 3 (5.0–8.0s): wide top-down shot. Ten narrow cut paper strips lie side by side in one row on the walnut desk, each with a small white number from 1 to 10 at its top end. The two halves of the answer line are on two different neighboring strips. The cyan light bar sweeps once across all ten strips from left to right; no strip lights up, and the bar fades out at the right edge.

SUBJECT (keep identical in every shot): one long sheet of cream-white paper, A4 width and about 1.2 meters long, lying flat and fully unrolled lengthwise from left to right on a dark walnut desk. The paper is printed with neat rows of small black text arranged in short paragraphs; between paragraphs there are clearly visible empty blank-line gaps. Exactly one line near the middle of the paper is printed in bold black and is the answer line: "금요일 오후 6시". A heavy brass-and-black guillotine paper cutter with one long straight steel blade stands at the right end of the desk. The AI search is always shown as a thin horizontal bar of cyan light that glides just above the paper surface.
BACKGROUND: a quiet library reading room at night; out-of-focus tall wooden bookshelves in deep navy-teal shadow behind the desk; a single warm brass desk lamp lights the paper from the upper left; a few dust motes float in the lamp beam. The background stays the same dim library in all three shots.
STYLE: photoreal tabletop macro cinematography, shallow depth of field, warm lamp light against cool navy shadows, cyan used only for the AI search light, red used only for cut lines and error marks. Fill the whole 16:9 frame edge to edge. No narration captions, no subtitle bars, no watermark.
```

## F04 · 본편 72.92–80.92초

**① 해당 대본**

> 14. 강의의 교육용 실험에서는 오히려 반대였습니다! 겹침을 육십 자로 늘리자 같은 문의 안내가 두 조각에 반복돼 위를 차지했고, 정답 조각은 이 위에서 삼 위로 밀렸습니다.  (72.92–84.00, 80.92 이후는 M06 순위표에서 정확한 2위→3위 비교)

**② Flow 입력 방식: 소재 (소재 → 동영상)** — 직전 구간은 M05 모션그래픽(구분자 사다리·겹침 슬라이더)다. 도식에서 사진풍 책상 장면으로 하드컷하는 새 구도라 프레임이 아니며, 직전이 Flow가 아니므로 이어 붙이기도 없다. **넣을 이미지 1장: `F01-ingredient.png`** = F01 채택 테이크의 Shot 1 프레임(소스 약 1.5초, 책상·긴 종이·재단기·램프·도서관 배경이 함께 보이는 순간). 출처: F01 채택본에서 Flow ‘프레임 저장’ 또는 F01 파일을 주시면 에이전트가 추출. 고정하는 요소: 책상·종이·재단기·램프·배경의 모양과 색. F01 채택 후 생성한다.

**③ 프롬프트 및 적용 방법** — Flow 소재 → 동영상, 소재 칸에 `F01-ingredient.png` 1장, 가로 16:9, 720p, 8초. 아래 블록 전체 붙여넣기. 채택 테이크만 1080p 업스케일 후 `F04_1080p.mp4`로 저장.

```text
Use the ingredient image only as the reference for the look of the dark walnut desk, the long printed cream paper, the brass guillotine cutter, the brass desk lamp and the dim navy-teal library background. Do not copy its camera angle; compose new shots exactly as described below.
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.5s): top-down view. Cut paper strips are laid down one after another so that each new strip overlaps the end of the previous one like roof shingles; every overlapping area is tinted soft amber. A white label "겹침 60" appears at 0.8s near the overlaps.
Shot 2 (2.5–5.0s): front view of a small wooden rack standing on the walnut desk with exactly three horizontal slots, marked with brass numbers 1, 2, 3 from top to bottom. Two strips printed with the same paragraph, each stamped with an identical small blue envelope icon, slide in and fill slot 1 and slot 2.
Shot 3 (5.0–8.0s): same front view of the same rack. The strip carrying the bold answer line "금요일 오후 6시" slides into the bottom slot 3; the camera pushes in slowly on slot 3 while a thin red arrow points downward next to it. The envelope strips stay in slots 1 and 2.

SUBJECT (keep identical in every shot): one long sheet of cream-white paper, A4 width and about 1.2 meters long, lying flat and fully unrolled lengthwise from left to right on a dark walnut desk. The paper is printed with neat rows of small black text arranged in short paragraphs; between paragraphs there are clearly visible empty blank-line gaps. Exactly one line near the middle of the paper is printed in bold black and is the answer line: "금요일 오후 6시". A heavy brass-and-black guillotine paper cutter with one long straight steel blade stands at the right end of the desk. The AI search is always shown as a thin horizontal bar of cyan light that glides just above the paper surface.
BACKGROUND: a quiet library reading room at night; out-of-focus tall wooden bookshelves in deep navy-teal shadow behind the desk; a single warm brass desk lamp lights the paper from the upper left; a few dust motes float in the lamp beam. The background stays the same dim library in all three shots.
STYLE: photoreal tabletop macro cinematography, shallow depth of field, warm lamp light against cool navy shadows, cyan used only for the AI search light, red used only for cut lines and error marks. Fill the whole 16:9 frame edge to edge. No narration captions, no subtitle bars, no watermark.
```

## F05 · 본편 121.94–129.94초

**① 해당 대본**

> 20. 그런데, 근거를 찾았다고 답이 맞는 걸까요?  (121.94–124.36)
> 21. 아닙니다. 모델이 찾은 문단을 잘못 읽거나, 없는 내용을 덧붙일 수도 있습니다.  (125.18–129.86)

**② Flow 입력 방식: 소재 (소재 → 동영상)** — 직전 구간은 M09 모션그래픽(MRR 계산)다. 도식에서 사진풍 책상 장면으로 하드컷하는 새 구도라 프레임이 아니며, 직전이 Flow가 아니므로 이어 붙이기도 없다. **넣을 이미지 1장: `F01-ingredient.png`** = F01 채택 테이크의 Shot 1 프레임(소스 약 1.5초, 책상·긴 종이·재단기·램프·도서관 배경이 함께 보이는 순간). 출처: F01 채택본에서 Flow ‘프레임 저장’ 또는 F01 파일을 주시면 에이전트가 추출. 고정하는 요소: 책상·종이·재단기·램프·배경의 모양과 색. F01 채택 후 생성한다.

**③ 프롬프트 및 적용 방법** — Flow 소재 → 동영상, 소재 칸에 `F01-ingredient.png` 1장, 가로 16:9, 720p, 8초. 아래 블록 전체 붙여넣기. 채택 테이크만 1080p 업스케일 후 `F05_1080p.mp4`로 저장.

```text
Use the ingredient image only as the reference for the look of the dark walnut desk, the long printed cream paper, the brass guillotine cutter, the brass desk lamp and the dim navy-teal library background. Do not copy its camera angle; compose new shots exactly as described below.
8-second clip, three hard-cut shots. In this clip the long paper has already been cut: one retrieved paragraph card (cream paper, same print) lies on the walnut desk under the lamp, and next to it on the right lies a blank white answer card of the same size.
Shot 1 (0.0–2.5s): medium top-down shot of the two cards. The retrieved card shows the bold line "금요일 오후 6시". A glowing cyan check mark hovers above the retrieved card, then flickers and turns into a cyan question mark.
Shot 2 (2.5–5.0s): closer top-down shot of both cards. Three short lines of cyan handwriting appear on the answer card one by one; thin cyan threads connect each written line to a printed line on the retrieved card. One thread snaps and turns red, and a red outline appears around that written line.
Shot 3 (5.0–8.0s): same framing. A fourth cyan line appears at the bottom of the answer card with no thread to the retrieved card; a red dashed box draws around this extra line. The lamp light stays steady.

SUBJECT (keep identical in every shot): one long sheet of cream-white paper, A4 width and about 1.2 meters long, lying flat and fully unrolled lengthwise from left to right on a dark walnut desk. The paper is printed with neat rows of small black text arranged in short paragraphs; between paragraphs there are clearly visible empty blank-line gaps. Exactly one line near the middle of the paper is printed in bold black and is the answer line: "금요일 오후 6시". A heavy brass-and-black guillotine paper cutter with one long straight steel blade stands at the right end of the desk. The AI search is always shown as a thin horizontal bar of cyan light that glides just above the paper surface.
BACKGROUND: a quiet library reading room at night; out-of-focus tall wooden bookshelves in deep navy-teal shadow behind the desk; a single warm brass desk lamp lights the paper from the upper left; a few dust motes float in the lamp beam. The background stays the same dim library in all three shots.
STYLE: photoreal tabletop macro cinematography, shallow depth of field, warm lamp light against cool navy shadows, cyan used only for the AI search light, red used only for cut lines and error marks. Fill the whole 16:9 frame edge to edge. No narration captions, no subtitle bars, no watermark.
```

## F06 · 본편 152.08–160.08초

**① 해당 대본**

> 26. 문서에 정답이 있어도 못 찾는 이유는, 자른 자리에 있을 수 있습니다. 좋은 청킹은 잘게 써는 칼질이 아니라, 근거를 끊지 않는 칼질입니다.  (152.08–160.32, 160.08–160.78은 M12 엔드카드)

**② Flow 입력 방식: 소재 (소재 → 동영상)** — 직전 구간은 M11 모션그래픽(홀드·템퍼러처 도식)다. 도식에서 사진풍 책상 장면으로 하드컷하는 새 구도라 프레임이 아니며, 직전이 Flow가 아니므로 이어 붙이기도 없다. **넣을 이미지 1장: `F01-ingredient.png`** = F01 채택 테이크의 Shot 1 프레임(소스 약 1.5초, 책상·긴 종이·재단기·램프·도서관 배경이 함께 보이는 순간). 출처: F01 채택본에서 Flow ‘프레임 저장’ 또는 F01 파일을 주시면 에이전트가 추출. 고정하는 요소: 책상·종이·재단기·램프·배경의 모양과 색. F01 채택 후 생성한다.

**③ 프롬프트 및 적용 방법** — Flow 소재 → 동영상, 소재 칸에 `F01-ingredient.png` 1장, 가로 16:9, 720p, 8초. 아래 블록 전체 붙여넣기. 채택 테이크만 1080p 업스케일 후 `F06_1080p.mp4`로 저장.

```text
Use the ingredient image only as the reference for the look of the dark walnut desk, the long printed cream paper, the brass guillotine cutter, the brass desk lamp and the dim navy-teal library background. Do not copy its camera angle; compose new shots exactly as described below.
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.6s): high top-down wide shot of the whole long uncut paper on the walnut desk, the guillotine blade is raised at the right end. Slow push-in toward the paragraph that contains the bold answer line "금요일 오후 6시".
Shot 2 (2.6–5.2s): low close-up at the blade. A thin red dashed guide line settles exactly inside the blank-line gap just above the answer paragraph, never touching the text. The steel blade comes down cleanly along that gap.
Shot 3 (5.2–8.0s): front-facing close shot. The cut paragraph card slides forward toward the camera fully intact, with the bold line "금요일 오후 6시" complete and sharp. The cyan light bar passes over it and the whole card lights up cyan. The camera holds steady on the glowing card until the end.

SUBJECT (keep identical in every shot): one long sheet of cream-white paper, A4 width and about 1.2 meters long, lying flat and fully unrolled lengthwise from left to right on a dark walnut desk. The paper is printed with neat rows of small black text arranged in short paragraphs; between paragraphs there are clearly visible empty blank-line gaps. Exactly one line near the middle of the paper is printed in bold black and is the answer line: "금요일 오후 6시". A heavy brass-and-black guillotine paper cutter with one long straight steel blade stands at the right end of the desk. The AI search is always shown as a thin horizontal bar of cyan light that glides just above the paper surface.
BACKGROUND: a quiet library reading room at night; out-of-focus tall wooden bookshelves in deep navy-teal shadow behind the desk; a single warm brass desk lamp lights the paper from the upper left; a few dust motes float in the lamp beam. The background stays the same dim library in all three shots.
STYLE: photoreal tabletop macro cinematography, shallow depth of field, warm lamp light against cool navy shadows, cyan used only for the AI search light, red used only for cut lines and error marks. Fill the whole 16:9 frame edge to edge. No narration captions, no subtitle bars, no watermark.
```

---

## 수령 검수 (2026-11-19)

6개 모두 1920×1080·24fps·190프레임(7.917초). 내용으로 ID 매칭: F01=Cyan_light_scanning…5dbb2ba0, F02=Paper_cutting_animation…0f282662, F03=Guillotine…8f0c455b, F04=Desk_paper…cbf01ce4, F05=Creating_animation…693889c6, F06=Guillotine…2a3cb72a.
- F02 0–2.6초 칼날 샷에 청록 막대 추가(요청 외). 사용.
- F03 5–7.9초 10조각 위 글자 '금요일 오 후 후 6시'로 깨짐(작게 보임). 사용.
- F04 0.75–1.58초(프레임 18–37) 라벨 '겹겹chijm 60' → 편집에서 x1306–1676, y494–562에 '겹침 60' 덮어쓰기.
- F05 2.5–7.9초 답 카드 손글씨가 무의미한 한글로 읽힘 → 재생성 요청(F05 retake, 아래).
- F06 0–2.5초 굵은 정답 줄 2개(작게). 사용.
소재 이미지: media/flow/F01-ingredient.png = F01 채택본 소스 1.2초 프레임.

## F05 retake 프롬프트 (소재 · F01-ingredient.png)

변경점: 손글씨를 읽을 수 없는 물결 획으로, 화면 유일한 글자 = 근거 카드의 '금요일 오후 6시'. 대본 N20–N21, 소재 → 동영상, 16:9·720p·8초, 채택본 F05_1080p.mp4.

```text
Use the ingredient image only as the reference for the look of the dark walnut desk, the cream printed paper, the brass desk lamp and the dim navy-teal library background. Do not copy its camera angle; compose new shots exactly as described below.
8-second clip, three hard-cut shots. The long paper has already been cut: one retrieved paragraph card (cream paper, rows of tiny grey unreadable text, plus exactly one bold black line "금요일 오후 6시") lies on the left of the walnut desk under the lamp, and next to it on the right lies a blank white answer card of the same size. The guillotine cutter is not in view.
Shot 1 (0.0–2.5s): medium top-down shot of the two cards side by side. A glowing cyan check mark hovers above the retrieved card, then flickers and morphs into a glowing cyan question mark. Camera static.
Shot 2 (2.5–5.0s): closer top-down shot of both cards, same left/right layout. Three short cyan ink strokes are drawn one by one on the answer card; they are abstract wavy scribble lines like distant handwriting, with no readable letters or words. Thin cyan threads connect each stroke to a printed row on the retrieved card. At 4.0s the middle thread snaps, both thread ends turn red, and a red rectangle outlines the middle stroke.
Shot 3 (5.0–8.0s): same framing as shot 2. A fourth cyan scribble stroke appears at the bottom of the answer card with no thread to the retrieved card; a red dashed rectangle draws around this extra stroke. The red marks from shot 2 stay visible. The lamp light stays steady and the camera does not move.

SUBJECT: two cards on a dark walnut desk as described above; cream retrieved card on the left, white answer card on the right, both the same size and position in shots 2 and 3. The only readable text in the whole clip is "금요일 오후 6시" on the retrieved card.
BACKGROUND: a quiet library reading room at night; out-of-focus tall wooden bookshelves in deep navy-teal shadow; a single warm brass desk lamp lights the cards from the upper left; a few dust motes float in the lamp beam. Same dim library in all three shots.
STYLE: photoreal tabletop macro cinematography, shallow depth of field, warm lamp light against cool navy shadows, cyan used only for AI marks and strokes, red used only for error marks. Fill the whole 16:9 frame edge to edge. No narration captions, no subtitle bars, no readable handwriting, no watermark.
```
