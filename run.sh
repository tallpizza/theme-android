docker run -v "$(pwd)/kakao_theme_android:/app" -v "$(pwd)/apk_output:/app/build/outputs/apk" -w /app --rm android-theme-builder ./gradlew assembleDebug
