#!/usr/bin/env python3
"""영상에서 대표 프레임을 고르게 추출한다.

사용법: python extract_frames.py <영상경로> <출력폴더> [프레임수=8]
Windows, macOS, Linux 공통. ffmpeg는 다음 순서로 찾는다:
  1) 환경변수 FFMPEG_BINARY  2) PATH의 ffmpeg
  3) imageio-ffmpeg 번들(설치돼 있으면)  4) 저장소 .venv-supertonic의 번들 ffmpeg
ffprobe는 필요 없다(길이는 ffmpeg 출력에서 읽는다).
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]  # 저장소 루트


def find_ffmpeg() -> str:
    if os.environ.get("FFMPEG_BINARY"):
        return os.environ["FFMPEG_BINARY"]
    if shutil.which("ffmpeg"):
        return shutil.which("ffmpeg")
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        pass
    for pattern in (".venv-supertonic/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg*.exe",
                    ".venv-supertonic/lib/python*/site-packages/imageio_ffmpeg/binaries/ffmpeg*"):
        hits = sorted(ROOT.glob(pattern))
        if hits:
            return str(hits[0])
    sys.exit("ffmpeg를 찾을 수 없습니다. scripts/setup.ps1을 실행하거나 FFMPEG_BINARY를 지정하세요.")


def duration_of(ffmpeg: str, video: str) -> float:
    err = subprocess.run([ffmpeg, "-hide_banner", "-i", video], capture_output=True,
                         text=True, encoding="utf-8", errors="replace").stderr
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", err)
    if not m:
        sys.exit(f"영상 길이를 읽지 못했습니다: {video}")
    h, mi, s = m.groups()
    return int(h) * 3600 + int(mi) * 60 + float(s)


def main() -> None:
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    video = sys.argv[1]
    out = Path(sys.argv[2])
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    out.mkdir(parents=True, exist_ok=True)
    ffmpeg = find_ffmpeg()
    duration = duration_of(ffmpeg, video)

    for i in range(1, n + 1):
        t = duration * (i - 0.5) / n
        subprocess.run([
            ffmpeg, "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", video,
            "-frames:v", "1", "-vf", "scale=960:-2",
            str(out / f"frame_{i:02d}.jpg"),
        ], check=True)
    print(f"추출 완료: {out} ({n}장, ffmpeg: {ffmpeg})")


if __name__ == "__main__":
    main()
