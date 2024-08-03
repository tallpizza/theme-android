FROM thyrlian/android-sdk

# Python 설치
RUN apt-get update && apt-get install -y \
  git \
  curl \
  python3 \
  python3-pip \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python 요구사항 설치
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Android SDK 설정
ENV ANDROID_HOME /opt/android-sdk

# Android SDK 라이선스 동의
RUN mkdir "$ANDROID_HOME/licenses" || true && \
  echo "24333f8a63b6825ea9c5514f83c2829b004d1fee" > "$ANDROID_HOME/licenses/android-sdk-license"


# Android 프로젝트 복사
COPY kakao_theme_android /app/kakao_theme_android

# Python 애플리케이션 복사
COPY . /app
RUN chmod +x /app/kakao_theme_android/gradlew

EXPOSE 8000

CMD ["python3", "main.py"]