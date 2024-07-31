# Android 개발을 위한 기본 이미지
FROM thyrlian/android-sdk

# 작업 디렉토리 설정
WORKDIR /app

# 호스트 머신에서 애플리케이션 소스 코드를 컨테이너로 복사
COPY kakao_theme_project /app

# 필요한 환경변수 설정
ENV ANDROID_HOME /opt/android-sdk

# Android SDK 라이선스 동의
RUN mkdir "$ANDROID_HOME/licenses" || true && \
    echo "24333f8a63b6825ea9c5514f83c2829b004d1fee" > "$ANDROID_HOME/licenses/android-sdk-license"

# gradlew 파일에 실행 권한 부여
RUN chmod +x ./gradlew

# 빌드 스크립트 실행
RUN ./gradlew assembleDebug
