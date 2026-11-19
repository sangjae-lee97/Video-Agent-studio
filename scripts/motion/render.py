"""모션그래픽 렌더러 (Playwright + FFmpeg, 모든 편 공통).

사용법 (저장소 루트):
  python scripts/motion/render.py projects/<편명>/motion/scenes.py projects/<편명>/motion/out            # 전 장면 mp4
  python scripts/motion/render.py <scenes.py> <out_dir> --preview                                         # 장면마다 마지막 프레임 jpg
  python scripts/motion/render.py <scenes.py> <out_dir> --only M01 M03 --fps 24

scenes.py 규칙: 딕셔너리 S = {"M01": (시작프레임, 끝프레임, "<html 조각>"), ...}
  - 프레임 번호는 편 타임라인(fps 기준) 절대값. data-* 시각은 절대 초. → 실제 발화 시각을 그대로 쓴다.
  - 선택: CSS_EXTRA = "..." (편별 색·폰트 덮어쓰기)
필요: pip install playwright && python -m playwright install chromium, ffmpeg(PATH 또는 imageio-ffmpeg).
Claude Cowork의 클라우드 작업 공간에는 둘 다 설치돼 있다. 한글 폰트: Noto Sans CJK KR / Noto Sans KR.
"""
import argparse
import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import base  # noqa: E402


def ffmpeg_bin() -> str:
    if os.environ.get('FFMPEG_BINARY'):
        return os.environ['FFMPEG_BINARY']
    if shutil.which('ffmpeg'):
        return shutil.which('ffmpeg')
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('scenes'); ap.add_argument('out')
    ap.add_argument('--preview', action='store_true'); ap.add_argument('--only', nargs='*', default=[])
    ap.add_argument('--fps', type=int, default=24)
    a = ap.parse_args()
    spec = importlib.util.spec_from_file_location('scenes', a.scenes)
    sc = importlib.util.module_from_spec(spec); spec.loader.exec_module(sc)
    css = base.CSS + getattr(sc, 'CSS_EXTRA', '')
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1920, 'height': 1080})
        for k, (s, e, html) in sc.S.items():
            if a.only and k not in a.only:
                continue
            pg.set_content(f"<html><head><meta charset=utf-8><style>{css}</style></head><body>{html}<script>{base.JS}</script></body></html>")
            pg.evaluate('document.fonts.ready')

            def shot(T):
                pg.evaluate(f'R({T})')
                return pg.screenshot(type='jpeg', quality=92)
            if a.preview:
                (out / f'prev_{k}.jpg').write_bytes(shot((e - 1) / a.fps)); print('preview', k); continue
            tmp = out / f'{k}.tmp.mp4'
            ff = subprocess.Popen([ffmpeg_bin(), '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(a.fps), '-i', '-',
                                   '-c:v', 'libx264', '-crf', '16', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', str(a.fps), str(tmp)],
                                  stdin=subprocess.PIPE)
            for i in range(s, e):
                ff.stdin.write(shot(i / a.fps))
            ff.stdin.close()
            if ff.wait() == 0:
                os.replace(tmp, out / f'{k}.mp4'); print('ok', k, e - s, 'frames', flush=True)
        b.close()


if __name__ == '__main__':
    main()
