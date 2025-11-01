# KakaoTalk 안드로이드 테마 백엔드 (android_theme)

FastAPI 기반으로 안드로이드용 테마를 생성하는 서비스입니다.  
이제 Astral의 `uv`를 사용해 의존성과 실행 환경을 관리합니다.

## 사전 준비

1. [uv 설치 가이드](https://docs.astral.sh/uv/getting-started/installation/)를 참고해 `uv`를 설치합니다.
2. 설치 확인:
   ```bash
   uv --version
   ```

## 의존성 설치 & 가상환경

프로젝트 루트(`android_theme/`)에서 다음 명령을 실행하면 `.venv/`가 생성되고 의존성이 설치됩니다.

```bash
cd android_theme
uv sync
```

- `uv run`은 가상환경 활성화 없이도 `uv`가 관리하는 환경을 사용합니다.
- 필요 시 `source .venv/bin/activate`로 직접 활성화할 수 있습니다.

## 서버 실행

- 개발 모드 (자동 리로드):
  ```bash
  uv run uvicorn main:app --reload --port 8001
  ```
- 배포와 동일한 실행 파라미터:
  ```bash
  uv run uvicorn main:app --host 0.0.0.0 --port 8001
  ```

## Docker 및 `uv.lock`

`Dockerfile`은 `pyproject.toml`과 `uv.lock`을 기반으로 같은 의존성을 설치합니다.  
의존성을 변경했다면 아래 명령으로 잠금 파일을 갱신하세요.

```bash
uv lock --upgrade
```

특정 패키지만 갱신하려면 `uv lock --upgrade-package <패키지명>`을 사용할 수 있습니다.

## 레거시 requirements.txt

과거 워크플로우와의 호환성을 위해 `requirements.txt`를 유지하고 있습니다.  
필요 시 아래 명령으로 갱신하세요.

```bash
uv export --format requirements-txt > requirements.txt
```

새로운 워크플로우에서는 `uv sync`와 `uv run` 사용을 권장합니다.
