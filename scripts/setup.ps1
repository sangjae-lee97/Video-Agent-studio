# Video Agent Studio 첫 설치 (Windows PowerShell)
# 저장소 루트에서 실행: .\scripts\setup.ps1
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)

# 1) Python 3.12 가상환경 (스크립트들이 .venv-supertonic 이름을 사용한다)
if (-not (Test-Path .venv-supertonic)) { py -3.12 -m venv .venv-supertonic }
$py = '.\.venv-supertonic\Scripts\python.exe'
& $py -m pip install --upgrade pip
& $py -m pip install -r scripts\requirements-pipeline.txt

# 2) 로컬 Whisper small (문장·단어 시각 정렬용, 고정 리비전)
New-Item -ItemType Directory -Force models | Out-Null
& $py -c "from huggingface_hub import snapshot_download as d; d('Systran/faster-whisper-small', revision='536b0662742c02347bc0e980a01041f333bce120', local_dir='models/faster-whisper-small')"

# 3) Silero VAD (로컬 음량 보정용, 고정 리비전)
New-Item -ItemType Directory -Force models\silero-vad | Out-Null
Invoke-WebRequest 'https://raw.githubusercontent.com/snakers4/silero-vad/066409f3d9db45a30d21dfcbf9147826ffdd7052/src/silero_vad/data/silero_vad.onnx' -OutFile models\silero-vad\silero_vad.onnx
$h = (Get-FileHash models\silero-vad\silero_vad.onnx -Algorithm SHA256).Hash.ToLower()
if ($h -ne '1a153a22f4509e292a94e67d6f9b85e8deb25b4988682b7e174c65279d8788e3') { throw "silero_vad.onnx 해시 불일치: $h" }

# 4) .env 준비
if (-not (Test-Path .env)) { Copy-Item .env.example .env; Write-Host '.env를 만들었습니다. TYPECAST_API_KEY 값을 넣으세요.' }
New-Item -ItemType Directory -Force outputs | Out-Null

# 5) 확인
& $py -m unittest discover -s tests -p "test_*.py"
Write-Host '설치 완료. 자막 폰트(Noto Sans KR)가 없으면 docs/SETUP_GUIDE.md의 폰트 항목을 보세요.'
