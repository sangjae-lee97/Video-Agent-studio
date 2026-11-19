import argparse
import os
from pathlib import Path
from dotenv import load_dotenv
from video_agent.pipeline import live_plan, mock_plan, output_path, review, save_outputs


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description='Video Agent Studio, Phase 1')
    parser.add_argument('topic', help='영상 주제')
    parser.add_argument('--mode', choices=['mock', 'live'], default='mock')
    parser.add_argument('--model', default=os.getenv('OPENAI_MODEL', 'gpt-4.1-mini'))
    parser.add_argument('--output-dir', default='outputs')
    parser.add_argument('--ai-scenes', type=int, choices=range(1,10), metavar='1-9', default=6,
                        help='10개 장면 중 AI 생성 영상 장면 수 (기본 6개)')
    args = parser.parse_args()
    if args.mode == 'live' and not os.getenv('OPENAI_API_KEY'):
        parser.error('live 모드에 OPENAI_API_KEY가 필요합니다. .env를 확인하세요.')
    plan, sources = (mock_plan(args.topic, args.ai_scenes) if args.mode == 'mock'
                     else live_plan(args.topic, args.model, args.ai_scenes))
    report = review(plan, sources, args.mode, args.ai_scenes)
    folder = save_outputs(plan, sources, report, output_path(args.topic, Path(args.output_dir)))
    print(f'[완료] {folder.resolve()}')
    print(f'[구조 검사] {"PASS" if report["structural_pass"] else "FAIL"}')
    print(f'[출처] {len(sources)}건 / [상태] {report["approval"]}')
    print('파일: script.txt, storyboard.md, plan.json, sources.json, review.json, production_manifest.json, flow_prompts/')
    if report['errors']:
        print('[검토 오류] ' + ' | '.join(report['errors']))


if __name__ == '__main__':
    main()
