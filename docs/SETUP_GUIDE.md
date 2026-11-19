# 처음 시작하기 — 내 PC에서 같은 방식으로 영상 만들기

이 저장소는 **주제 한 줄이나 문서 하나**에서 약 2분짜리 한국어 지식 영상(16:9, 1080p)을 만드는 작업 방식과 도구를 담고 있다. 실제 제작은 AI 에이전트(Claude Cowork 또는 Codex)가 `AGENTS.md`와 [공통 제작 지침](VIDEO_PRODUCTION_GUIDE.md)을 읽고 진행하며, 사람은 **음성 합성 실행(필요할 때)**, **Google Flow 영상 생성**, **결과 확인**을 맡는다.

저장소에는 코드·지침·대본·편집 기록만 있다. 음성·영상·이미지·모델 파일은 용량과 저작권 때문에 올리지 않았다(`.gitignore` 참고). 기존 편(`projects/…`)을 다시 렌더하려면 해당 Flow 영상과 음성을 직접 다시 만들어야 한다.

## 전체 흐름

```
주제/문서 → 분석 문서 → 낭독 대본 → Typecast 내레이션 → 로컬 정렬·보정
→ 편집표 → Flow 요청(사람이 생성) → 모션그래픽 → 자막 → 완성 MP4·썸네일
```

| 단계 | 누가 | 어디서 |
|---|---|---|
| 분석·대본·편집표·Flow 프롬프트 | 에이전트 | 편 폴더 `projects/<편명>/` |
| Typecast 합성 | 에이전트 또는 **사람(PowerShell)** | 아래 ‘Typecast’ 참고 |
| 정렬·음량 보정 | 에이전트 (또는 PowerShell) | `.venv-supertonic` |
| Flow 영상 생성 | **사람** | Google Flow 웹 |
| 모션그래픽·자막·조립·썸네일 | 에이전트 | Claude 클라우드 작업 공간(Playwright·FFmpeg) 또는 로컬 |

## 1. 준비물

- Windows 10/11, PowerShell
- [Python 3.12](https://www.python.org/downloads/) (설치 시 `py` 런처 포함)
- Git
- Typecast API 키 — [Typecast API 콘솔](https://studio.typecast.ai/developers/api). API 구독과 웹 구독은 별개다. 1글자 = 1크레딧(대본 약 1,100자 = 약 1,100크레딧/회).
- Google Flow를 쓸 수 있는 Google 계정·구독 (https://labs.google/fx/tools/flow)
- Claude 데스크톱 앱(Cowork) 또는 Codex 같은 파일·셸을 다룰 수 있는 에이전트
- 자막 폰트: **Noto Sans KR**(가변 폰트 `NotoSansKR-VF.ttf`)를 Windows에 설치. [Google Fonts](https://fonts.google.com/noto/specimen/Noto+Sans+KR)에서 받아 ‘모든 사용자용으로 설치’. `scripts/apply_captions.py`가 `C:\Windows\Fonts\NotoSansKR-VF.ttf`를 찾는다.

## 2. 설치

```powershell
git clone https://github.com/sangjae-lee97/Video-Agent-studio.git C:\dev\Video-Agent-studio
cd C:\dev\Video-Agent-studio
.\scripts\setup.ps1
```

`setup.ps1`이 하는 일: `.venv-supertonic` 가상환경 생성과 `scripts/requirements-pipeline.txt` 설치, Whisper small(정렬용)·Silero VAD(보정용) 모델을 고정 리비전으로 `models/`에 내려받기, `.env` 생성, 단위 테스트 실행.

그다음 `.env`를 메모장으로 열어 `TYPECAST_API_KEY=` 뒤에 키를 넣는다. **키를 채팅창에 붙여 넣지 않는다.**

## 3. 에이전트 연결 (Claude Cowork 기준)

1. Claude 데스크톱 앱에서 새 작업을 열고 **폴더 추가**로 `C:\dev\Video-Agent-studio`를 연결한다.
2. 첫 메시지 예시: `AGENTS.md와 README.md, docs/VIDEO_PRODUCTION_GUIDE.md를 읽고 이 주제로 영상 만들어줘: <주제 또는 문서>`
3. 에이전트는 `projects/<편명>/`에 분석 문서와 대본을 먼저 저장한 뒤 음성 합성으로 넘어간다.

Codex 등 다른 에이전트도 루트의 `AGENTS.md`를 따른다.

## 4. Typecast 내레이션 — 에이전트가 API에 못 닿으면 PowerShell로

기본값: 화자 필재, 모델 SSFM 3.1, **1.0배속**, 내용별 감정 배치([NARRATION_STYLE.md](NARRATION_STYLE.md), [narration-defaults.json](narration-defaults.json)).

Claude Cowork는 클라우드 작업 공간과 PC의 리눅스 VM 모두 **허용 도메인 목록에 없는 주소에 접속할 수 없다.** `api.typecast.ai`가 허용돼 있지 않으면 에이전트가 직접 합성하지 못한다([자세한 원인](TYPECAST_INTEGRATION.md)). 이때는 셋 중 하나를 쓴다.

**A. PowerShell로 직접 실행 (가장 확실, 추가 설정 없음)**
에이전트가 편 폴더에 합성 요청(`narration/request.json`)과 실행 스크립트(`narration/run_narration.ps1`)를 만들어 준다. 저장소 루트에서 실행한다.

```powershell
cd C:\dev\Video-Agent-studio
.\projects\<편명>\narration\run_narration.ps1
```

요청은 한 번만 보내고 실패해도 자동 재시도하지 않는다(이중 과금 방지). 이미 `narration.wav`나 `request-started.json`이 있으면 실행을 거부한다. 끝나면 에이전트에게 “실행했어”라고 알리면 정렬·보정부터 이어서 한다. 자동 정렬이 실패하면(ASR이 문장 끝 단어를 잘못 들은 경우) 에이전트가 단어 시각을 다시 뽑아 수동으로 맞춘다.

**B. 허용 도메인에 추가**
claude.ai 웹 → 설정 → Capabilities에서 `api.typecast.ai`를 허용한다(팀/엔터프라이즈는 조직 관리자가 Organization settings → Capabilities에서). 새 작업부터 에이전트가 직접 합성할 수 있다.

**C. 공식 Typecast MCP를 로컬로 연결**
[Typecast MCP 문서](https://typecast.ai/docs/ko/integrations/mcp-server). uv 설치 후 Claude 데스크톱 설정(`%APPDATA%\Claude\claude_desktop_config.json`)의 `mcpServers`에 추가한다.

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

```json
{
  "mcpServers": {
    "typecast": {
      "command": "C:\\Users\\<사용자>\\.local\\bin\\uvx.exe",
      "args": ["--from", "git+https://github.com/neosapience/typecast-api-mcp-server.git", "typecast-api-mcp-server"],
      "env": { "TYPECAST_API_KEY": "<키>", "TYPECAST_OUTPUT_DIR": "C:\\dev\\Video-Agent-studio\\outputs\\typecast-mcp" }
    }
  }
}
```

앱을 트레이에서 완전히 종료 후 다시 켜고 **새 작업**에서 도구가 보이는지 확인한다. MCP에는 여러 구간을 한 번에 합성하는 Compose가 없어 구간별로 합성한 뒤 이어 붙인다. (2026-11-19 기준 이 방식은 아직 이 저장소에서 실제 합성까지 검증되지 않았다. 검증된 경로는 A다.)

## 5. Google Flow 설정 — 빠짐없이

에이전트가 편 폴더의 `flow-request.md`에 필요한 클립 전부를 한 번에 정리해 준다. 클립마다 **① 해당 대본 ② 입력 방식 ③ 복붙용 영문 프롬프트·적용 방법**이 있다.

### 공통 설정 (모든 클립)

| 항목 | 값 |
|---|---|
| 화면 비율 | **가로 16:9** |
| 생성 해상도 | **720p (1280×720)** |
| 길이 | **8초** |
| 프롬프트 | `flow-request.md`의 ```text 블록을 **통째로** 붙여 넣기(배경·제외 문구 포함, 수정하지 않기) |
| 채택 | 여러 테이크 중 하나를 고른 뒤 **채택본만 1080p 업스케일** |
| 업스케일 | **유료 요금제는 360p→720p, 720p→1080p 업스케일이 무료**다(2026-11 사용자 확인). 720p로 생성해 채택본만 1080p로 올리면 생성 비용 외 추가 크레딧이 들지 않는다 |
| 파일 | 1080p를 내려받아 `projects/<편명>/media/flow/F01_1080p.mp4` … 처럼 **장면 ID 이름**으로 저장하거나, 채팅에 그대로 올리고 “F03이야”처럼 알려준다 |

자막 여백·하단 안전영역은 지시하지 않는다. 자막은 편집에서 얹는다.

### 입력 방식 4가지 — `flow-request.md`의 ②에 적힌 대로

| 적힌 방식 | Flow에서 할 일 |
|---|---|
| **소재 · 이미지 없음** | 텍스트 → 동영상. 이미지 없이 프롬프트만 넣는다 |
| **소재 (이미지 있음)** | 소재(재료) → 동영상. 지정된 이미지 파일을 소재 칸에 넣는다. 이어지지 않는 새 구도에서 대상의 생김새만 맞출 때 쓴다 |
| **프레임 · 시작 프레임 업로드** | 프레임 → 동영상. **시작 프레임** 칸에 에이전트가 준 PNG(앞 영상의 실제 편집점 화면)를 넣고 끝 프레임은 비운다. 직접 다른 순간을 골라 넣지 않는다 |
| **프레임 · 이어 붙이기** | 장면 빌더에서 지정된 앞 클립 뒤에 **확장(Extend)**. 이미지 업로드 없음. 확장된 8초만 업스케일해서 보낸다 |

**앞 영상의 이미지를 넣어 이어지게 하는 것은 소재가 아니라 프레임이다.**

### 생성 순서와 확인

- `flow-request.md` 맨 위의 **생성 순서**를 지킨다. 프레임·이어 붙이기 클립은 앞 클립을 먼저 채택해야 만들 수 있다.
- 받은 파일은 에이전트가 장면 ID·길이·해상도·내용을 대조한다. 글자 변형, 로고, 의미가 틀어지는 구간은 편집으로 보완하거나 재생성 프롬프트를 다시 준다.
- 크레딧이 부족하면 “그냥 진행”이라고 말하면 된다. 에이전트가 알려진 한계를 기록하고 편집으로 최대한 보완한다.

## 6. 모션그래픽·자막·완성본

- 모션그래픽은 에이전트가 HTML 장면을 프레임마다 그려(Playwright) 실제 발화 시각에 맞춘다. 색과 밝기는 같은 편 Flow 장면 톤에 맞춘다.
- 자막: 에이전트가 화면용 표기(예: ‘래그’→RAG, ‘육십 초’→60초)로 `captions.ko.srt`를 검증한 뒤 공통 프로그램으로 합성한다.

  ```powershell
  .\.venv-supertonic\Scripts\python.exe scripts\apply_captions.py 입력.mp4 projects\<편명>\captions.ko.srt 출력.mp4
  ```

- 완성 파일: `projects/<편명>/renders/<주제>_완성본_1080p.mp4`, 16:9 썸네일, 유튜브 제목·설명(근거 자료 URL 포함)을 함께 받는다.

## 7. 저장소 구조

| 경로 | 내용 |
|---|---|
| `AGENTS.md` | 에이전트 작업 기준 |
| `docs/VIDEO_PRODUCTION_GUIDE.md` | 공통 제작 지침 (새 편마다 에이전트가 전문을 읽는다) |
| `docs/NARRATION_STYLE.md`, `docs/narration-defaults.json` | 내레이션 감정·속도·보정 기준 |
| `docs/TYPECAST_INTEGRATION.md` | Typecast API·MCP·접속 제한 기록 |
| `scripts/` | 정렬(`transcribe_narration.py`), 보정(`balance_narration_phrases.py`), 자막(`apply_captions.py`), 설치(`setup.ps1`) |
| `projects/<편명>/` | 편별 분석·대본·편집표·Flow 요청·자막·모션 장면 코드·진행 기록 (영상·음성 제외) |
| `legacy/` | 초기 실험 코드(현재 사양 근거 아님) |

## 자주 막히는 곳

- **`py -3.12`를 못 찾음**: Python 3.12를 설치하고 PowerShell을 새로 연다.
- **`run_narration.ps1` 실행 정책 오류**: `powershell -ExecutionPolicy Bypass -File .\projects\<편명>\narration\run_narration.ps1`
- **‘Existing output or previous attempt found’**: 이미 한 번 합성을 시도한 폴더다. 다시 합성하려면 에이전트에게 새 폴더(예: `narration-v2/`)로 요청을 만들어 달라고 한다.
- **자막 폰트 오류**: Noto Sans KR 가변 폰트를 설치한다.
