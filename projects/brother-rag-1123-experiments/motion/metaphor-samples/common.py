from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
FX = (ROOT / 'scripts/motion/effects.js').read_text(encoding='utf-8')
FPS = 24
T0, T1 = 89.9, 104.6
RANGE = (round(T0 * FPS), round(T1 * FPS))
# 실제 단어 시각(asr-words.json, 16·17번 줄)
W = dict(직전=90.34, 유형=91.42, 문항=91.66, 하이브리드는=93.10, 열개=93.84, 재정렬은=94.42, 여섯개=95.46,
         그래서=97.14, 제출도=97.88, 하이브리드로=98.26, 저녁=100.04, 칠시=100.26, 사십일분=100.58,
         두번째=101.12, 제출=101.64, 백점=102.06, 순위표=102.82, 일위=103.52)
