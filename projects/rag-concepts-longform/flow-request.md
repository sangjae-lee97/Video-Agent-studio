# Flow 일괄 요청 — 처음 읽는 래그 (12클립)

기준 음성: `narration/local-short-window-v1/narration_balanced.wav` 625.690초(sha256 4053da30…, 원본 ba6de965…), 문장 시각 `narration/local-short-window-v1/sentence-boundaries.json`. 영상 끝 626.80초(마지막 발화 625.38초 뒤 여운).
공통 설정: Google Flow 웹 · 가로 16:9 · 720p(1280×720) · **8초** 생성 · 채택 테이크만 1080p 업스케일. 돌려줄 파일명: `F01_1080p.mp4` … `F12_1080p.mp4` → `projects/rag-concepts-longform/media/flow/`.
생성 순서: **순서 상관없음.** 12개 모두 하드컷이라 서로의 프레임을 기다리지 않는다.
배분(사용자 합의 2026-11-20): Flow는 장마다 1~2개, 합계 94.3초 / 626.8초 = **15.0%**(공통 지침 30%보다 낮은 롱폼 예외). 나머지 532.5초는 모션그래픽.
디자인 메타포: 물류 센터 출고 라인([template-spec.md](template-spec.md)). Flow 화면의 크라프트 상자·흰 송장·노란 안전선이 모션그래픽과 같은 재료다.
로고·실제 제품 외형은 쓰지 않는다. 장면 안 글자는 짧은 영문/숫자만. 정확한 모델명·수치 비교는 모션그래픽이 맡고, Flow 라벨 철자가 틀리면 편집에서 덮어 보정한다.

| ID | 본편 구간(초) | 사용 | 대본 줄 | 입력 방식 |
|---|---|---:|---|---|
| F01 | 0.00–8.00 | 8.00 | 1 | 소재 · 이미지 없음 |
| F02 | 8.00–16.00 | 8.00 | 1~2 | 소재 · 이미지 없음 |
| F03 | 80.30–88.30 | 8.00 | 12 | 소재 · 이미지 없음 |
| F04 | 147.40–155.40 | 8.00 | 22~23 | 소재 · 이미지 없음 |
| F05 | 171.10–177.90 | 6.80 | 26 | 소재 · 이미지 없음 |
| F06 | 274.80–282.80 | 8.00 | 42 | 소재 · 이미지 없음 |
| F07 | 379.20–387.20 | 8.00 | 57 | 소재 · 이미지 없음 |
| F08 | 394.10–402.10 | 8.00 | 59~60 | 소재 · 이미지 없음 |
| F09 | 428.40–435.90 | 7.50 | 65 | 소재 · 이미지 없음 |
| F10 | 477.10–485.10 | 8.00 | 72~73 | 소재 · 이미지 없음 |
| F11 | 515.20–523.20 | 8.00 | 78 | 소재 · 이미지 없음 |
| F12 | 612.40–620.40 | 8.00 | 90~91 | 소재 · 이미지 없음 |

**입력 방식 판단(전 클립 공통):** F01은 첫 장면. F02는 F01(두 복합기 근접)에서 물류 센터 전경으로 바뀌는 하드컷 새 구도. F03~F12는 모두 직전 구간이 모션그래픽이고 도식에서 사진풍 장면으로 넘어가는 하드컷이라 프레임 연결이 어렵다 → 지침대로 대상 설명 전문으로 연속성을 맞추는 **소재 · 이미지 없음**. F12는 F01과 같은 두 복합기지만, 이미 생성된 화면을 소재 칸에 넣지 않는다는 규칙에 따라 같은 대상 문장(PRINTERS)을 그대로 반복해 맞춘다.

## 공통 대상 문장 (해당 클립 프롬프트에 그대로 포함됨)

- **PRINTERS** (F01·F12): two identical compact monochrome laser multifunction printers, each about 40 cm wide: matte charcoal-black body with a lighter grey top, a flatbed scanner lid with an empty automatic document feeder tray on top, a small black-and-white touchscreen on the front right, and a closed paper cassette at the bottom front; no brand logo or brand name anywhere. In front of each printer stands a small white plastic desk name plate: left plate "MFC-L2805DW", right plate "MFC-L2885DW", bold black letters except the differing digit (the "0" on the left plate, the "8" on the right plate), which is printed in amber.
- **ORDER CARD** (F02·F07·F08·F10): a white A6 paper order card with a thin safety-yellow band across the top and the large bold black code "L2805" printed in the middle.
- **BOXES**: small shoebox-size kraft-brown cardboard boxes, each with one white thermal shipping label on its front showing a black barcode and one short bold code.
- **BACKGROUND** (전 클립): a bright, tidy logistics fulfillment center in daytime: pale polished concrete floor with yellow safety lane lines, tall grey steel shelving racks filled with kraft-brown boxes, roller conveyors, soft even skylight from above; calm and clean.

---

## F01 · 0.00–8.00

**① 대본**
> 1. 모델 번호 한 글자만 다른 프린터 두 대, 엠에프씨 엘 이팔공오와 이팔팔오. 같은 질문을 던지면, AI는 내 모델의 답을 정확히 찾아낼 수 있을까요? (0.00–9.22, 8.00부터 F02)

**② 입력 방식: 소재 · 이미지 없음** — 첫 장면, 참고 이미지 없음.

**③ 적용** — 텍스트 → 동영상, 16:9, 720p, 8초. 채택본만 1080p → `F01_1080p.mp4`. 본편 0–8.00초 전부 사용. 명판 철자(특히 0/8)를 확인한다. 틀리면 편집에서 명판만 덮어 보정한다.

```text
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.5s): eye-level wide shot of the two printers standing side by side, 30 cm apart, on a brushed steel workbench at the end of an outbound packing line. Slow dolly-in toward the gap between them.
Shot 2 (2.5–5.0s): low close-up gliding left to right along the two name plates at plate height, camera steady at the end. The amber digit on each plate — "0" on the left, "8" on the right — is clearly visible; nothing else differs.
Shot 3 (5.0–8.0s): medium shot from slightly above, both printers in frame. Both touchscreens light up at the same moment showing the same simple white speech-bubble icon with a question mark on a dark screen. The camera slowly pulls back.

SUBJECT (identical in every shot): two identical compact monochrome laser multifunction printers, each about 40 cm wide: matte charcoal-black body with a lighter grey top, a flatbed scanner lid with an empty automatic document feeder tray on top, a small black-and-white touchscreen on the front right, and a closed paper cassette at the bottom front; no brand logo or brand name anywhere. In front of each printer stands a small white plastic desk name plate: left plate "MFC-L2805DW", right plate "MFC-L2885DW", bold black letters except the differing digit (the "0" on the left plate, the "8" on the right plate), which is printed in amber. Same size, same color, both facing the camera.
BACKGROUND: a bright, tidy logistics fulfillment center in daytime behind the workbench: pale polished concrete floor with yellow safety lane lines, tall grey steel shelving racks filled with kraft-brown boxes, a roller conveyor, soft even skylight from above. Out of focus, the same in all shots.
STYLE: photoreal, 35 mm lens, shallow depth of field, clean daylight, calm steady camera. Fill the whole 16:9 frame edge to edge. Plate text crisp and legible.
EXCLUSIONS: no subtitles, no caption bar, no bottom text overlay, no burned-in captions, no brand logos, no watermark.
```

## F02 · 8.00–16.00

**① 대본**
> 1. …같은 질문을 던지면, AI는 내 모델의 답을 정확히 찾아낼 수 있을까요? (–9.22)
> 2. 오늘은 천 쪽이 넘는 프린터 매뉴얼로 질문에 답하는 AI를 예로 들어, 래그가 어떻게 움직이는지 처음부터 끝까지 따라가 보겠습니다. (9.94–17.80, 16.00부터 모션 ‘세 덩어리’)

**② 입력 방식: 소재 · 이미지 없음** — F01 근접에서 물류 센터 전경으로 바뀌는 하드컷 새 구도.

**③ 적용** — 텍스트 → 동영상, 16:9, 720p, 8초 → `F02_1080p.mp4`. 0–8.00초 전부 사용.

```text
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.6s): high wide establishing shot over the whole fulfillment center: long rows of tall steel shelving packed with kraft-brown boxes, roller conveyors weaving between them. A large white hanging banner near the ceiling reads "1,099 PAGES" in bold black letters. Slow forward crane move.
Shot 2 (2.6–5.2s): close-up at waist height at an intake station marked by a yellow floor sign "ORDER IN". A gloved hand places the order card flat onto the start of a moving roller conveyor. The card's code "L2805" faces up and is readable.
Shot 3 (5.2–8.0s): low tracking shot following the order card as it rides away along the conveyor toward the shelving aisles; the camera keeps pace just behind it, the aisles growing larger ahead.

ORDER CARD: a white A6 paper order card with a thin safety-yellow band across the top and the large bold black code "L2805" printed in the middle.
BACKGROUND: a bright, tidy logistics fulfillment center in daytime: pale polished concrete floor with yellow safety lane lines, tall grey steel shelving racks filled with kraft-brown boxes, roller conveyors, soft even skylight from above; calm and clean, no people's faces.
STYLE: photoreal, 35 mm lens, clean daylight, calm conveyor-like camera moves. Fill the whole 16:9 frame edge to edge. Banner and card text crisp.
EXCLUSIONS: no subtitles, no caption bar, no bottom text overlay, no burned-in captions, no brand logos, no watermark.
```

## F03 · 80.30–88.30

**① 대본**
> 12. 다음은 청킹. 긴 문서를 검색하기 좋은 조각으로 나누는 겁니다. 천 쪽을 매번 통째로 AI에게 넣을 수는 없으니까요. (80.54–88.02)

**② 입력 방식: 소재 · 이미지 없음** — 직전은 모션(파싱 도식), 하드컷.

**③ 적용** — 텍스트 → 동영상, 16:9, 720p, 8초 → `F03_1080p.mp4`. 0–8.00초.

```text
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.5s): top-down shot of a light wooden packing workbench. A thick printed manual with a plain dark-blue cover and no title lies in the center. Gloved hands open it to the middle; the pages show columns of grey text and a printed table with a visible grid.
Shot 2 (2.5–5.0s): closer top-down shot. The hands lift out one small stack of a few pages that includes the table page, with a small yellow sticky note still stuck to the table page, and lay the whole stack into an open small kraft-brown box. The note stays attached to its page.
Shot 3 (5.0–8.0s): low side shot sliding along a row of six small kraft boxes on the bench, each now holding one stack of pages. A gloved hand presses a white thermal shipping label with a black barcode and a small amber square onto the front of each box as the camera passes.

BOXES: small shoebox-size kraft-brown cardboard boxes, each with one white thermal shipping label on its front.
BACKGROUND: the same bright, tidy logistics fulfillment center in daytime behind the bench: pale concrete floor with yellow safety lane lines, grey steel shelving racks with kraft boxes, soft even skylight; slightly out of focus.
STYLE: photoreal, 35 mm lens, clean daylight, calm steady camera. Fill the whole 16:9 frame edge to edge.
EXCLUSIONS: no subtitles, no caption bar, no bottom text overlay, no burned-in captions, no brand logos, no watermark, no readable paragraphs of fake text.
```

## F04 · 147.40–155.40

**① 대본**
> 22. 벡터 검색은 질문도 벡터로 바꾼 뒤, 저장된 조각들과 얼마나 가까운지 비교해서 찾습니다. (147.66–152.62)
> 23. 여러 장 연속 스캔과 자동 문서 공급 장치처럼, 단어는 달라도 관련된 표현을 찾아내는 게 장점입니다. (153.02–158.42, 155.40부터 모션)

**② 입력 방식: 소재 · 이미지 없음** — 직전 모션(임베딩 좌표), 하드컷. 벡터 검색 = '비슷한 물건끼리 모인 선반 구역'. 청록 스티커가 모션의 벡터 색(#138A8A)과 이어진다.

**③ 적용** — 텍스트 → 동영상, 16:9, 720p, 8초 → `F04_1080p.mp4`. 0–8.00초.

```text
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.6s): eye-level shot down a shelving aisle whose floor is painted with a broad teal zone stripe. A small grey picking cart with a clip holding the white order card (yellow top band, bold "L2805") rolls into the aisle. Camera dollies along beside it.
Shot 2 (2.6–5.2s): close-up of one shelf section: neighbouring boxes of different shapes all carry the same round teal sticker on their labels, grouped together. A gloved hand takes two of these teal-sticker boxes from adjacent slots, one after the other.
Shot 3 (5.2–8.0s): top-down shot of the cart's basket: three kraft boxes with teal stickers now sit inside, and the cart keeps rolling forward along the teal floor stripe.

BOXES: small shoebox-size kraft-brown cardboard boxes, each with one white thermal shipping label showing a black barcode; the grouped ones carry a round teal sticker.
BACKGROUND: the same bright, tidy logistics fulfillment center in daytime: pale concrete floor with yellow safety lane lines and the teal zone stripe in this aisle, tall grey steel shelving racks filled with kraft boxes, soft even skylight.
STYLE: photoreal, 35 mm lens, clean daylight, smooth steady moves. Fill the whole 16:9 frame edge to edge.
EXCLUSIONS: no subtitles, no caption bar, no bottom text overlay, no burned-in captions, no brand logos, no watermark.
```

## F05 · 171.10–177.90

**① 대본**
> 26. 두 번째 방법은 비엠이십오. 검색어가 문서에서 얼마나 중요한지 계산해 순위를 매기는 키워드 검색입니다. (171.32–177.18, 177.90부터 모션 ‘세 요소’)

**② 입력 방식: 소재 · 이미지 없음** — 직전 모션, 하드컷. BM25 = 품번을 정확히 읽는 바코드 스캐너. 주황은 모션의 BM25 색(#E2701E).

**③ 적용** — 텍스트 → 동영상, 16:9, 720p, 8초 → `F05_1080p.mp4`. **0–6.80초만 사용**(Shot 3는 6.8초까지 보이면 충분).

```text
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.4s): close-up of a gloved hand aiming a yellow handheld barcode scanner at the white shipping label of a kraft box on a shelf; a thin red scan line crosses the black barcode and the bold code "L2805" on the label. The scanner's small screen flashes orange.
Shot 2 (2.4–4.8s): side tracking shot along a shelf row: the scanner sweeps label after label; on boxes whose label code matches, a small orange light on the scanner blinks and the hand sticks an orange dot on that label.
Shot 3 (4.8–8.0s): top-down shot of a steel table with three numbered slots painted "1", "2", "3"; the hand sets the orange-dot boxes into the slots in order. Camera steady.

BOXES: small shoebox-size kraft-brown cardboard boxes, each with one white thermal shipping label showing a black barcode and one short bold code.
BACKGROUND: the same bright, tidy logistics fulfillment center in daytime: pale concrete floor with yellow safety lane lines, grey steel shelving racks with kraft boxes, soft even skylight.
STYLE: photoreal, 35 mm macro-to-medium framing, clean daylight, crisp focus on labels. Fill the whole 16:9 frame edge to edge.
EXCLUSIONS: no subtitles, no caption bar, no bottom text overlay, no burned-in captions, no brand logos, no watermark.
```

## F06 · 274.80–282.80

**① 대본**
> 42. 그럼 이 조각과 벡터는, 실제로 어디에 담을까요? 여기서는 포스트그레스큐엘 기반의 관리형 데이터베이스, 수파베이스를 씁니다. (274.98–282.70)

**② 입력 방식: 소재 · 이미지 없음** — 3장 끝 모션에서 4장 첫 장면으로 하드컷. 데이터베이스 = 행·열 번호가 붙은 보관 랙, 파이썬 계산 = 옆 작업대(방법 A). 'Supabase' 글자는 모션에서 표시하고 Flow에는 상표명을 넣지 않는다.

**③ 적용** — 텍스트 → 동영상, 16:9, 720p, 8초 → `F06_1080p.mp4`. 0–8.00초.

```text
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.6s): wide frontal shot of a tall wall of grey steel storage racks laid out as a clean grid: painted row letters "A", "B", "C", "D" down the left side and column numbers "01" to "06" along the top; every slot holds one kraft box with a white label. Slow push-in.
Shot 2 (2.6–5.2s): side dolly along one row at eye level: each slot has a small white plate with its address such as "B-03"; a gloved hand slides a labeled box into an empty slot and it fits exactly.
Shot 3 (5.2–8.0s): the camera pulls back and pans right to reveal a wooden workbench right beside the racks, with an open laptop showing rows of numbers and a clipboard; a person (hands and torso only, no face) writes a short column of scores on the clipboard.

BOXES: small shoebox-size kraft-brown cardboard boxes, each with one white thermal shipping label showing a black barcode.
BACKGROUND: the same bright, tidy logistics fulfillment center in daytime: pale concrete floor with yellow safety lane lines, soft even skylight, more shelving receding behind.
STYLE: photoreal, 35 mm lens, clean daylight, orderly symmetric framing, calm moves. Fill the whole 16:9 frame edge to edge. Row letters, column numbers and slot plates crisp.
EXCLUSIONS: no subtitles, no caption bar, no bottom text overlay, no burned-in captions, no brand logos, no product names, no watermark.
```

## F07 · 379.20–387.20

**① 대본**
> 57. 답에 붙은 근거 번호가 실제로 찾은 조각인지, 그 조각이 질문한 모델에 해당하는지, 수치와 조건이 원문에 있는지를 확인합니다. (379.46–386.90, 387.20부터 모션 ‘교차 모델 인용 X’)

**② 입력 방식: 소재 · 이미지 없음** — 직전 모션(인용 vs 검증 체크 3칸), 하드컷. 송장 대조 = 인용 검증.

**③ 적용** — 텍스트 → 동영상, 16:9, 720p, 8초 → `F07_1080p.mp4`. 0–8.00초.

```text
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.6s): close-up on an outbound packing desk: the white order card (yellow top band, bold "L2805") is held by a gloved hand right next to the white shipping label of a closed kraft box whose bold code also reads "L2805". The camera racks focus from the card to the label.
Shot 2 (2.6–5.2s): the hand lifts the box flap slightly; inside, a small stack of printed pages with a table page and a yellow sticky note. A green ink stamp comes down on the label, leaving a green check mark.
Shot 3 (5.2–8.0s): medium shot: the checked box slides onto the outbound roller conveyor; a second box beside it, whose label code reads "L2885", stays on the desk under the inspector's hand. Camera steady.

ORDER CARD: a white A6 paper order card with a thin safety-yellow band across the top and the large bold black code "L2805" printed in the middle.
BOXES: small shoebox-size kraft-brown cardboard boxes, each with one white thermal shipping label showing a black barcode and one short bold code.
BACKGROUND: the same bright, tidy logistics fulfillment center in daytime: pale concrete floor with yellow safety lane lines, grey steel shelving racks with kraft boxes, soft even skylight; slightly out of focus behind the desk.
STYLE: photoreal, 35 mm lens, clean daylight, crisp label text. Fill the whole 16:9 frame edge to edge.
EXCLUSIONS: no subtitles, no caption bar, no bottom text overlay, no burned-in captions, no brand logos, no watermark.
```

## F08 · 394.10–402.10

**① 대본**
> 59. 그럼, 근거를 끝내 찾지 못하면 어떻게 할까요? (394.30–396.54)
> 60. 그럴듯하게 지어내지 않고, 답을 보류합니다. 이걸 앱스텐션이라고 합니다. (397.48–401.80)

**② 입력 방식: 소재 · 이미지 없음** — 직전 모션, 하드컷. 보류 = 빈 칸 앞에서 'HOLD' 도장. 빨강은 모션의 보류 색(#C8372D).

**③ 적용** — 텍스트 → 동영상, 16:9, 720p, 8초 → `F08_1080p.mp4`. 0–8.00초.

```text
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.6s): eye-level shot of a picker's grey cart stopping in front of one shelf slot. The slot is completely empty — bare steel, nothing inside — while the neighbouring slots are full of kraft boxes. The order card is clipped to the cart. Slow push-in on the empty slot.
Shot 2 (2.6–5.2s): close-up of the order card (yellow top band, bold "L2805") lying on a clipboard; a gloved hand presses a red rubber stamp onto it, leaving a bold red rectangular stamp reading "HOLD".
Shot 3 (5.2–8.0s): medium shot: the stamped card is placed into a red plastic tray beside the conveyor; the tray's front reads "HOLD" in white; the conveyor keeps running past it.

ORDER CARD: a white A6 paper order card with a thin safety-yellow band across the top and the large bold black code "L2805" printed in the middle.
BACKGROUND: the same bright, tidy logistics fulfillment center in daytime: pale concrete floor with yellow safety lane lines, tall grey steel shelving racks filled with kraft-brown boxes, roller conveyors, soft even skylight.
STYLE: photoreal, 35 mm lens, clean daylight, calm and matter-of-fact. Fill the whole 16:9 frame edge to edge.
EXCLUSIONS: no subtitles, no caption bar, no bottom text overlay, no burned-in captions, no brand logos, no watermark.
```

## F09 · 428.40–435.90

**① 대본**
> 65. 첫째, 캐싱. 이미 계산한 결과를 저장해 두고, 같은 요청이 오면 다시 계산하지 않고 꺼내 씁니다. (428.68–435.18)

**② 입력 방식: 소재 · 이미지 없음** — 직전 모션(최적화 장 표지), 하드컷. 캐시 = 출고대 바로 옆 앞칸 선반.

**③ 적용** — 텍스트 → 동영상, 16:9, 720p, 8초 → `F09_1080p.mp4`. **0–7.50초 사용.**

```text
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.6s): long shot down an aisle: a worker (back view, no face) walks far into the shelving, pulls one kraft box labeled with bold "L2805" from a high slot and carries it back toward the camera.
Shot 2 (2.6–5.2s): medium shot at the outbound desk: the worker sets that box on a small white shelf standing right beside the desk; the shelf's header plate reads "FREQUENT".
Shot 3 (5.2–8.0s): close-up: a new identical order card (yellow top band, bold "L2805") drops into the desk tray, and a gloved hand immediately takes the box from the "FREQUENT" shelf without walking anywhere. Camera steady.

ORDER CARD: a white A6 paper order card with a thin safety-yellow band across the top and the large bold black code "L2805" printed in the middle.
BOXES: small shoebox-size kraft-brown cardboard boxes, each with one white thermal shipping label showing a black barcode and one short bold code.
BACKGROUND: the same bright, tidy logistics fulfillment center in daytime: pale concrete floor with yellow safety lane lines, tall grey steel shelving racks with kraft boxes, soft even skylight.
STYLE: photoreal, 35 mm lens, clean daylight, calm steady camera. Fill the whole 16:9 frame edge to edge.
EXCLUSIONS: no subtitles, no caption bar, no bottom text overlay, no burned-in captions, no brand logos, no watermark.
```

## F10 · 477.10–485.10

**① 대본**
> 72. 이팔공오로 원본을 연속 스캔할 때, 몇 장까지 넣을 수 있냐는 질문이 들어옵니다. (477.34–482.16)
> 73. 먼저 모델 코드를 따로 뽑아내고, 같은 질문의 저장된 답이 있는지 캐시를 확인합니다. (482.60–487.72, 485.10부터 모션 경로 지도)

**② 입력 방식: 소재 · 이미지 없음** — 직전 모션(7장 표지), 하드컷. 주문 카드 한 장을 따라가는 추적 샷.

**③ 적용** — 텍스트 → 동영상, 16:9, 720p, 8초 → `F10_1080p.mp4`. 0–8.00초.

```text
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.6s): close-up: the order card (yellow top band, bold "L2805") drops onto the start of a moving roller conveyor at the "ORDER IN" station; the camera starts tracking it at belt height.
Shot 2 (2.6–5.2s): the card passes under a grey overhead scanner arch; a small amber light on the arch flashes and a small display on the arch shows "L2805". Camera keeps tracking alongside.
Shot 3 (5.2–8.0s): the conveyor carries the card past a small white shelf labeled "FREQUENT" standing beside the line; the shelf holds a few kraft boxes but none matching; the card continues on toward the shelving aisles, camera following.

ORDER CARD: a white A6 paper order card with a thin safety-yellow band across the top and the large bold black code "L2805" printed in the middle.
BACKGROUND: the same bright, tidy logistics fulfillment center in daytime: pale concrete floor with yellow safety lane lines, tall grey steel shelving racks with kraft-brown boxes, roller conveyors, soft even skylight.
STYLE: photoreal, 35 mm lens, smooth continuous tracking like a conveyor, clean daylight. Fill the whole 16:9 frame edge to edge.
EXCLUSIONS: no subtitles, no caption bar, no bottom text overlay, no burned-in captions, no brand logos, no watermark.
```

## F11 · 515.20–523.20

**① 대본**
> 78. 마지막은 평가입니다. 물어볼 건 여섯 가지예요. 찾았나, 답이 맞나, 근거가 맞나, 거부 판단이 맞나, 얼마나 느리고 비싼가, 그리고 정상적으로 돌아갔나. (515.46–525.92, 523.20부터 모션 검사표)

**② 입력 방식: 소재 · 이미지 없음** — 직전 모션(경로·로그), 하드컷. 평가 = 출고 품질 검사. 여섯 항목의 정확한 이름은 이어지는 모션 검사표가 표시한다.

**③ 적용** — 텍스트 → 동영상, 16:9, 720p, 8초 → `F11_1080p.mp4`. 0–8.00초.

```text
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.6s): top-down close-up of a quality-check clipboard on a steel desk: a printed checklist with exactly six empty square checkboxes in one column; a pen ticks the first three boxes one by one.
Shot 2 (2.6–5.2s): close-up of a silver mechanical stopwatch on the desk; a gloved hand clicks it on as a kraft box rolls past on the conveyor behind it; the second hand starts sweeping.
Shot 3 (5.2–8.0s): medium-wide shot of the quality-check desk at the end of the outbound line: an inspector (torso and hands, no face) holds the clipboard while boxes pass one by one; camera slowly pulls back.

BACKGROUND: the same bright, tidy logistics fulfillment center in daytime: pale concrete floor with yellow safety lane lines, tall grey steel shelving racks with kraft-brown boxes, roller conveyors, soft even skylight.
STYLE: photoreal, 35 mm lens, clean daylight, precise and calm. Fill the whole 16:9 frame edge to edge.
EXCLUSIONS: no subtitles, no caption bar, no bottom text overlay, no burned-in captions, no brand logos, no watermark, no readable paragraphs of fake text.
```

## F12 · 612.40–620.40

**① 대본**
> 90. 모델 번호 한 글자 차이. 이걸 구별해 내는 건, 똑똑한 모델 하나가 아닙니다. (612.56–617.12)
> 91. 제대로 꺼내고, 맞는 모델의 조각을 찾고, 근거로 답하고, 그 근거를 확인하고, 실패까지 기록하는 과정 전체입니다. (617.60–625.38, 620.40부터 모션 정거장 요약)

**② 입력 방식: 소재 · 이미지 없음** — 직전 모션(평가 마무리), 하드컷. F01과 같은 두 복합기·명판을 같은 대상 문장으로 다시 세운다(첫 질문으로 돌아오는 결말).

**③ 적용** — 텍스트 → 동영상, 16:9, 720p, 8초 → `F12_1080p.mp4`. 0–8.00초.

```text
8-second clip, three hard-cut shots.
Shot 1 (0.0–2.6s): eye-level medium shot of the two printers side by side on the brushed steel workbench at the end of the outbound line, name plates in front. Camera steady, then a slow push-in.
Shot 2 (2.6–5.2s): low close-up along a short roller conveyor that ends at the workbench: a kraft box whose white label reads bold "L2805" rolls in and stops exactly in front of the left printer and its "MFC-L2805DW" plate.
Shot 3 (5.2–8.0s): the left printer's touchscreen shows a simple green check mark while the right printer's screen stays dark; the camera rises and pulls back over the workbench, revealing the whole outbound line and the shelving behind.

SUBJECT (identical in every shot): two identical compact monochrome laser multifunction printers, each about 40 cm wide: matte charcoal-black body with a lighter grey top, a flatbed scanner lid with an empty automatic document feeder tray on top, a small black-and-white touchscreen on the front right, and a closed paper cassette at the bottom front; no brand logo or brand name anywhere. In front of each printer stands a small white plastic desk name plate: left plate "MFC-L2805DW", right plate "MFC-L2885DW", bold black letters except the differing digit (the "0" on the left plate, the "8" on the right plate), which is printed in amber. Same size, same color, both facing the camera.
BACKGROUND: a bright, tidy logistics fulfillment center in daytime: pale polished concrete floor with yellow safety lane lines, tall grey steel shelving racks filled with kraft-brown boxes, roller conveyors, soft even skylight from above.
STYLE: photoreal, 35 mm lens, clean daylight, calm steady camera. Fill the whole 16:9 frame edge to edge. Plate and label text crisp.
EXCLUSIONS: no subtitles, no caption bar, no bottom text overlay, no burned-in captions, no brand logos, no watermark.
```
