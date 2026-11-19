"""Generate local Korean TTS samples and measure speed/memory; no API calls."""

import argparse
import json
import os
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[1]
os.environ['HF_HOME'] = str(ROOT / '.cache' / 'huggingface')
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['TRANSFORMERS_OFFLINE'] = '1'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--text-file', type=Path, help='Optional UTF-8 narration file')
    parser.add_argument('--split-lines', action='store_true', help='Generate each nonempty line, then join for one speaker')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'outputs' / 'tts-smoke')
    parser.add_argument('--speakers', nargs='+', default=['Sohee'], choices=[
        'Sohee', 'Ryan', 'Aiden', 'Uncle_Fu', 'Dylan', 'Eric', 'Vivian', 'Serena', 'Ono_Anna',
    ])
    args = parser.parse_args()
    if args.split_lines and (not args.text_file or len(args.speakers) != 1):
        parser.error('--split-lines requires --text-file and exactly one speaker')
    samples = [
        ('01_explanation', '복잡한 원리도 순서대로 보면 이해할 수 있습니다. 먼저 전체 모습을 보고, 안쪽 구조를 살펴봅니다. 마지막으로 각 부분이 어떻게 연결되는지 확인합니다.'),
        ('02_numbers', '이번 테스트 영상은 2분 30초입니다. 8초짜리 장면 3개를 연결하면 24초가 됩니다. AI와 API라는 영문 표현, 그리고 3.5퍼센트라는 숫자도 읽어 보겠습니다.'),
        ('03_story', '그럼 크기만 키우면 되는 것 아니냐고요? 잠깐, 진짜 문제는 따로 있습니다. 우리가 놓친 건 크기가 아니라 연결 방식입니다. 그래서 발상을 뒤집어 봅니다.'),
    ]
    if args.text_file:
        text = args.text_file.read_text(encoding='utf-8-sig').strip()
        chunks = [line.strip() for line in text.splitlines() if line.strip()] if args.split_lines else [text]
        if not chunks or any(not chunk or len(chunk) > 600 for chunk in chunks):
            parser.error('Use 1–600 characters per segment; --split-lines supports longer scripts.')
        samples = [(f'part_{i:03d}' if args.split_lines else 'custom', chunk)
                   for i, chunk in enumerate(chunks, 1)]

    import numpy as np
    import soundfile as sf
    import torch
    from qwen_tts import Qwen3TTSModel

    if not torch.cuda.is_available():
        raise RuntimeError('CUDA unavailable; this benchmark requires the configured GPU.')
    # Smoke-test the installed CUDA kernels before loading the larger model.
    assert (torch.ones(4, device='cuda') * 2).sum().item() == 8
    torch.manual_seed(42)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    model_path = ROOT / 'models' / 'Qwen3-TTS-12Hz-0.6B-CustomVoice'
    started = time.perf_counter()
    print('Loading local model with SDPA...', flush=True)
    model = Qwen3TTSModel.from_pretrained(
        str(model_path), device_map='cuda:0', dtype=torch.bfloat16,
        attn_implementation='sdpa', local_files_only=True,
    )
    torch.cuda.synchronize()
    report = {
        'model': model_path.name,
        'revision': '85e237c12c027371202489a0ec509ded67b5e4b5',
        'speakers': args.speakers, 'language': 'Korean', 'attention': 'sdpa', 'seed': 42,
        'torch': torch.__version__, 'cuda': torch.version.cuda,
        'gpu': torch.cuda.get_device_name(),
        'load_seconds': round(time.perf_counter() - started, 3),
        'listening_review': 'pending_user_review',
        'samples': [],
    }
    jobs = [(f'{speaker}_{name}' if args.speakers != ['Sohee'] else name, text, speaker)
            for speaker in dict.fromkeys(args.speakers) for name, text in samples]
    for name, text, speaker in jobs:
        print(f'Generating {name}...', flush=True)
        torch.manual_seed(42)
        torch.cuda.reset_peak_memory_stats()
        started = time.perf_counter()
        with torch.inference_mode():
            waves, rate = model.generate_custom_voice(
                text=text, language='Korean', speaker=speaker, max_new_tokens=1024,
            )
        torch.cuda.synchronize()
        elapsed = time.perf_counter() - started
        wave = np.asarray(waves[0])
        duration = len(wave) / rate
        assert np.isfinite(wave).all() and duration > 0.5, 'Invalid audio'
        assert np.max(np.abs(wave)) > 0.001, 'Silent output'
        path = args.output_dir / f'{name}.wav'
        sf.write(path, wave, rate, subtype='PCM_16')
        saved = sf.info(path)
        assert saved.frames == len(wave) and saved.samplerate == rate
        entry = {
            'file': path.name, 'speaker': speaker, 'text': text, 'sample_rate': rate,
            'duration_seconds': round(duration, 3), 'generation_seconds': round(elapsed, 3),
            'rtf': round(elapsed / duration, 3),
            'peak_allocated_mib': round(torch.cuda.max_memory_allocated() / 2**20, 1),
            'peak_reserved_mib': round(torch.cuda.max_memory_reserved() / 2**20, 1),
            'peak_amplitude': float(np.max(np.abs(wave))),
            'clipped_fraction': float(np.mean(np.abs(wave) >= 1)),
        }
        report['samples'].append(entry)
        (args.output_dir / f'{name}.txt').write_text(text + '\n', encoding='utf-8')
        (args.output_dir / 'report.json').write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8',
        )
        print(json.dumps(entry, ensure_ascii=False), flush=True)
    if args.split_lines:
        audio_parts = []
        frames = 0
        pause_frames = round(rate * 0.18)
        for i, entry in enumerate(report['samples']):
            audio, actual_rate = sf.read(args.output_dir / entry['file'], dtype='float32')
            assert actual_rate == rate and audio.ndim == 1
            entry['timeline_start_seconds'] = frames / rate
            audio_parts.append(audio)
            frames += len(audio)
            entry['timeline_end_seconds'] = frames / rate
            if i < len(report['samples']) - 1:
                audio_parts.append(np.zeros(pause_frames, dtype='float32'))
                frames += pause_frames
        combined = args.output_dir / 'narration.wav'
        sf.write(combined, np.concatenate(audio_parts), rate, subtype='PCM_16')
        assert sf.info(combined).frames == frames
        report['combined'] = {'file': combined.name, 'duration_seconds': frames / rate,
                              'pause_seconds': 0.18, 'segment_count': len(samples)}
        (args.output_dir / 'report.json').write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8',
        )
        print(json.dumps(report['combined']), flush=True)
    print(f'DONE: {args.output_dir}', flush=True)


if __name__ == '__main__':
    main()
