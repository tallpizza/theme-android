# syntax=docker/dockerfile:1.7

ARG BASE_IMAGE=ghcr.io/cirruslabs/android-sdk:34
FROM --platform=linux/amd64 ${BASE_IMAGE}

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y \
        git \
        curl \
        python3 \
        python3-pip \
        python3-venv \
    && rm -rf /var/lib/apt/lists/*

ENV UV_LINK_MODE=copy \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:/root/.local/bin:$PATH" \
    UV_CACHE_DIR=/root/.cache/uv \
    GRADLE_USER_HOME=/root/.gradle \
    ANDROID_HOME=/opt/android-sdk \
    ANDROID_SDK_ROOT=/opt/android-sdk

WORKDIR /app

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

RUN mkdir -p "$ANDROID_HOME/licenses" && \
    echo "24333f8a63b6825ea9c5514f83c2829b004d1fee" > "$ANDROID_HOME/licenses/android-sdk-license"

COPY kakao_theme_android/build.gradle kakao_theme_android/gradlew /app/kakao_theme_android/
COPY kakao_theme_android/gradle /app/kakao_theme_android/gradle
WORKDIR /app/kakao_theme_android
RUN --mount=type=cache,target=/root/.gradle \
    --mount=type=cache,target=/app/kakao_theme_android/.gradle \
    ./gradlew dependencies --no-daemon

WORKDIR /app
COPY . .
RUN chmod +x /app/kakao_theme_android/gradlew

WORKDIR /app/kakao_theme_android
RUN --mount=type=cache,target=/root/.gradle \
    --mount=type=cache,target=/app/kakao_theme_android/.gradle \
    ./gradlew assembleDebug

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
