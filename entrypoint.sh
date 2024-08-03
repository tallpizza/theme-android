#!/bin/bash
if [ -f "/app/kakao_theme_android/gradlew" ]; then
  chmod +x /app/kakao_theme_android/gradlew
else
  echo "Error: gradlew not found in /app/kakao_theme_android"
fi
