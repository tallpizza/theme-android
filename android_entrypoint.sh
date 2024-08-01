#!/bin/bash
# /app/kakao_theme_android 디렉토리에 파일이 있는지 확인
if [ "$(ls -A /app/kakao_theme_android)" ]; then
  echo "kakao_theme_android already has files"
else
  echo "Copying initial files to kakao_theme_android"
  cp -r /opt/kakao_theme_android_initial/* /app/kakao_theme_android/
fi

if [ -f "/app/kakao_theme_android/gradlew" ]; then
  chmod +x /app/kakao_theme_android/gradlew
else
  echo "Error: gradlew not found in /app/kakao_theme_android"
fi

# 계속 실행되도록 설정
tail -f /dev/null
