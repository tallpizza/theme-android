from fastapi import FastAPI, File, Form, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
import shutil
import os
import subprocess
from typing import Optional

app = FastAPI()


@app.post("/create_theme")
async def create_theme(
    background_tasks: BackgroundTasks,
    themeName: Optional[str] = Form(None),
    themeId: Optional[str] = Form(None),
    kakaoIcon: Optional[UploadFile] = File(None),
    tabsBgColor: Optional[str] = Form(None),
    tabsBg: Optional[UploadFile] = File(None),
    tabsFrends: Optional[UploadFile] = File(None),
    tabsFrendsSelected: Optional[UploadFile] = File(None),
    tabsChats: Optional[UploadFile] = File(None),
    tabsChatsSelected: Optional[UploadFile] = File(None),
    tabsOpenChats: Optional[UploadFile] = File(None),
    tabsOpenChatsSelected: Optional[UploadFile] = File(None),
    tabsShopping: Optional[UploadFile] = File(None),
    tabsShoppingSelected: Optional[UploadFile] = File(None),
    tabsMore: Optional[UploadFile] = File(None),
    tabsMoreSelected: Optional[UploadFile] = File(None),
    mainBackgroundColor: Optional[str] = Form(None),
    mainBg: Optional[UploadFile] = File(None),
    headerColor: Optional[str] = Form(None),
    nameColor: Optional[str] = Form(None),
    namePressedColor: Optional[str] = Form(None),
    descriptionColor: Optional[str] = Form(None),
    descriptionPressedColor: Optional[str] = Form(None),
    paragraphColor: Optional[str] = Form(None),
    paragraphPressedColor: Optional[str] = Form(None),
    listBgColor: Optional[str] = Form(None),
    listBgPressedColor: Optional[str] = Form(None),
    listBgOpacity: Optional[float] = Form(None),
    listBgPressedOpacity: Optional[float] = Form(None),
    borderColor: Optional[str] = Form(None),
    borderOpacity: Optional[float] = Form(None),
    sectionColor: Optional[str] = Form(None),
    sectionOpacity: Optional[float] = Form(None),
    subBgColor: Optional[str] = Form(None),
    bottomBannerBgColor: Optional[str] = Form(None),
    serviceBtnColor: Optional[str] = Form(None),
    findFriendButton: Optional[UploadFile] = File(None),
    defaultProfile: Optional[UploadFile] = File(None),
    chatRoomBgColor: Optional[str] = Form(None),
    chatRoomBg: Optional[UploadFile] = File(None),
    inputBarBgColor: Optional[str] = Form(None),
    sendBgColor: Optional[str] = Form(None),
    sendBgPressedColor: Optional[str] = Form(None),
    sendIconColor: Optional[str] = Form(None),
    sendIconPressedColor: Optional[str] = Form(None),
    menuButtonColor: Optional[str] = Form(None),
    menuButtonPressedColor: Optional[str] = Form(None),
    bubbleSend1: Optional[UploadFile] = File(None),
    bubbleSend1Selected: Optional[UploadFile] = File(None),
    sendEdgeinsets1: Optional[str] = Form(None),
    bubbleSend2: Optional[UploadFile] = File(None),
    bubbleSend2Selected: Optional[UploadFile] = File(None),
    sendEdgeinsets2: Optional[str] = Form(None),
    textColor: Optional[str] = Form(None),
    textSelectedColor: Optional[str] = Form(None),
    unReadColor: Optional[str] = Form(None),
    bubbleReceive1: Optional[UploadFile] = File(None),
    bubbleReceive1Selected: Optional[UploadFile] = File(None),
    receiveEdgeinsets1: Optional[str] = Form(None),
    bubbleReceive2: Optional[UploadFile] = File(None),
    bubbleReceive2Selected: Optional[UploadFile] = File(None),
    receiveEdgeinsets2: Optional[str] = Form(None),
    receiveTextColor: Optional[str] = Form(None),
    receiveTextSelectedColor: Optional[str] = Form(None),
    receiveUnReadColor: Optional[str] = Form(None),
    passcodeBgColor: Optional[str] = Form(None),
    passcodeBg: Optional[UploadFile] = File(None),
    passcodeTitleColor: Optional[str] = Form(None),
    passcodeImage1: Optional[UploadFile] = File(None),
    passcodeImage2: Optional[UploadFile] = File(None),
    passcodeImage3: Optional[UploadFile] = File(None),
    passcodeImage4: Optional[UploadFile] = File(None),
    passcodeImage1Selected: Optional[UploadFile] = File(None),
    passcodeImage2Selected: Optional[UploadFile] = File(None),
    passcodeImage3Selected: Optional[UploadFile] = File(None),
    passcodeImage4Selected: Optional[UploadFile] = File(None),
    keyPadBgColor: Optional[str] = Form(None),
    keyPadTextColor: Optional[str] = Form(None),
    keyPadPressedImage: Optional[UploadFile] = Form(None),
    alertMessageBgColor: Optional[str] = Form(None),
    alertMessageNameColor: Optional[str] = Form(None),
    alertMessageTextColor: Optional[str] = Form(None),
    alertShareBgColor: Optional[str] = Form(None),
    alertShareNameColor: Optional[str] = Form(None),
    alertShareTextColor: Optional[str] = Form(None),
):
    # 테마 디렉토리 생성
    theme_dir = f"/app/kakao_theme_project/app/src/main/res/drawable-xxhdpi"
    os.makedirs(theme_dir, exist_ok=True)

    # 이미지 파일 저장
    image_files = {}

    for name, file in image_files.items():
        if file:
            with open(f"{theme_dir}/{name}.png", "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

    # colors.xml 파일 수정
    colors_xml_path = "/app/kakao_theme_project/src/main/theme/values/colors.xml"
    update_colors_xml(colors_xml_path, tabsBgColor=tabsBgColor)  # 다른 색상들도 추가

    # APK 빌드
    build_apk()

    # APK 파일 경로
    apk_path = "/app/build/outputs/apk/debug/ONO-theme.apk"

    # APK 파일 전송
    return FileResponse(apk_path, filename="custom_theme.apk")


def update_colors_xml(file_path, **colors):
    # XML 파일 수정 로직 구현
    # 예: colors 딕셔너리의 키-값 쌍을 사용하여 colors.xml 파일 업데이트
    pass


def build_apk():
    # APK 빌드 명령 실행
    result = subprocess.run(
        ["./gradlew", "assembleDebug"],
        cwd="/app/kakao_theme_project",
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Build failed: {result.stderr}")
        raise Exception("APK build failed")

    # 새로운 APK 경로
    apk_path = "/app/build/outputs/apk/debug/ONO-theme.apk"

    # APK 파일이 실제로 생성되었는지 확인
    if not os.path.exists(apk_path):
        raise FileNotFoundError(f"APK file not found at {apk_path}")

    return apk_path


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
