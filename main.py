import asyncio
from fastapi import FastAPI, File, Form, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
import os
import aiofiles
from typing import Optional
import logging
import xml.etree.ElementTree as ET


app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

theme_dir = "./kakao_theme_android/src/main/theme/drawable-xxhdpi"
colors_xml_path = "./kakao_theme_android/src/main/theme/values/colors.xml"


@app.post("/upload")
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
    os.makedirs(theme_dir, exist_ok=True)

    # 이미지 파일 저장
    file_names = [
        # "commonIcoTheme.png",
        "theme_background_image.png",
        "theme_maintab_ico_friends_image.png",
        "theme_maintab_ico_friends_focused_image.png",
        "theme_maintab_ico_chats_image.png",
        "theme_maintab_ico_chats_focused_image.png",
        "theme_maintab_ico_openchat_image.png",
        "theme_maintab_ico_openchat_focused_image.png",
        "theme_maintab_ico_shopping_image.png",
        "theme_maintab_ico_shopping_focused_image.png",
        "theme_maintab_ico_more_image.png",
        "theme_maintab_ico_more_focused_image.png",
        "theme_background_image.png",  # 안드로이드에선 탭이랑 메인이랑 차이가없음
        "theme_find_add_friend_button_image.png",  # pressed필요
        "theme_profile_01_image.png",
        "theme_chatroom_background_image.png",
        "theme_chatroom_bubble_me_01_image.9.png",  # 9.png로 변환필요
        "theme_chatroom_bubble_me_02_image.9.png",  # 9.png로 변환필요
        "theme_chatroom_bubble_you_01_image.9.png",  # 9.png로 변환필요
        "theme_chatroom_bubble_you_02_image.9.png",  # 9.png로 변환필요
        "theme_passcode_background_image.png",
        "theme_passcode_01_image.png",
        "theme_passcode_02_image.png",
        "theme_passcode_03_image.png",
        "theme_passcode_04_image.png",
        "theme_passcode_01_checked_image.png",
        "theme_passcode_02_checked_image.png",
        "theme_passcode_03_checked_image.png",
        "theme_passcode_04_checked_image.png",
        "passcodeKeypadPressed@3x.png",  # 안드로이드에선 사용안함
    ]

    image_files = [
        # kakaoIcon, #TODO: mipmap으로 변환 필요
        tabsBg,
        tabsFrends,
        tabsFrendsSelected,
        tabsChats,
        tabsChatsSelected,
        tabsOpenChats,
        tabsOpenChatsSelected,
        tabsShopping,
        tabsShoppingSelected,
        tabsMore,
        tabsMoreSelected,
        mainBg,
        findFriendButton,
        defaultProfile,
        chatRoomBg,
        bubbleSend1,
        bubbleSend1Selected,
        bubbleSend2,
        bubbleSend2Selected,
        bubbleReceive1,
        bubbleReceive1Selected,
        bubbleReceive2,
        bubbleReceive2Selected,
        passcodeBg,
        passcodeImage1,
        passcodeImage2,
        passcodeImage3,
        passcodeImage4,
        passcodeImage1Selected,
        passcodeImage2Selected,
        passcodeImage3Selected,
        passcodeImage4Selected,
        keyPadPressedImage,
    ]

    for image_file, file_name in zip(image_files, file_names):
        if image_file is not None:
            file_path = os.path.join(theme_dir, file_name)
            content = await image_file.read()
            async with aiofiles.open(file_path, "wb") as out_file:
                await out_file.write(content)

    logger.info("theme file saved")

    # colors.xml 파일 수정
    update_color("theme_header_color", headerColor)
    update_color("theme_section_title_color", "007FFF")  # input 필요
    update_color("theme_title_color", nameColor)  # input 필요
    update_color("theme_title_pressed_color", namePressedColor)
    update_color("theme_paragraph_color", paragraphColor)
    update_color("theme_paragraph_pressed_color", paragraphPressedColor)
    update_color("theme_description_color", descriptionColor)
    update_color("theme_description_pressed_color", descriptionPressedColor)
    update_color("theme_feature_primary_color", serviceBtnColor)
    update_color("theme_feature_primary_pressed_color", serviceBtnColor)  # input필요

    update_color("theme_background_color", mainBackgroundColor)
    update_color("theme_chatroom_background_color", chatRoomBgColor)
    update_color("theme_passcode_background_color", passcodeBgColor)

    update_color("theme_body_cell_border_color", borderColor)

    update_color("theme_body_cell_color", listBgColor)
    update_color("theme_body_cell_pressed_color", listBgPressedColor)

    update_color("theme_body_secondary_cell_color", subBgColor)
    update_color("theme_maintab_cell_color", tabsBgColor)
    update_color("theme_tab_bannerbadge_background_color", bottomBannerBgColor)

    update_color("theme_direct_share_color", alertShareTextColor)
    update_color("theme_direct_share_button_color", alertShareNameColor)
    update_color("theme_direct_share_background_color", alertShareBgColor)

    update_color("theme_notification_color", alertMessageTextColor)
    update_color("theme_notification_background_color", alertMessageBgColor)
    update_color(
        "theme_notification_background_pressed_color", alertMessageBgColor
    )  # input 없음

    update_color("theme_passcode_color", passcodeTitleColor)
    update_color("theme_passcode_keypad_color", keyPadTextColor)
    update_color("theme_passcode_keypad_pressed_color", keyPadTextColor)
    update_color("theme_passcode_keypad_background_color", keyPadBgColor)
    update_color(
        "theme_passcode_keypad_pressed_background_color", keyPadBgColor
    )  # input 필요
    update_color("theme_passcode_pattern_line_color", keyPadTextColor)  # input 필요

    update_color("theme_chatroom_bubble_me_color", textColor)
    update_color("theme_chatroom_bubble_you_color", receiveTextColor)
    update_color("theme_chatroom_unread_count_color", unReadColor)

    update_color("theme_chatroom_input_bar_background_color", inputBarBgColor)
    update_color("theme_chatroom_input_bar_send_button_color", sendBgColor)
    update_color("theme_chatroom_input_bar_send_icon_color", sendIconColor)
    update_color("theme_chatroom_input_bar_menu_icon_color", menuButtonColor)

    logger.info("update theme colors completed")

    apk_path = await build_apk()

    # APK 파일 전송
    return FileResponse(apk_path, filename="custom_theme.apk")


def update_color(color_name, new_value):
    # XML 파일 파싱
    tree = ET.parse(colors_xml_path)
    root = tree.getroot()

    # 'name' 속성으로 색상 요소 찾기
    for color_element in root.findall(".//color[@name='{}']".format(color_name)):
        # 새 값으로 업데이트
        if new_value is not None:
            color_element.text = new_value

    # 변경사항 저장
    tree.write(colors_xml_path, encoding="utf-8", xml_declaration=True)


async def build_apk():
    try:
        process = await asyncio.create_subprocess_exec(
            "./gradlew",
            "assembleDebug",
            cwd="/app/kakao_theme_android",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        async def log_stream(stream, log_func):
            while True:
                line = await stream.readline()
                if not line:
                    break
                log_func(line.decode().strip())

        await asyncio.gather(
            log_stream(process.stdout, logger.info),
            log_stream(process.stderr, logger.error),
        )

        await process.wait()

        if process.returncode == 0:
            apk_path = (
                "/app/kakao_theme_android/app/build/outputs/apk/debug/ONO-theme.apk"
            )
            logger.info("Build successful")
            return apk_path
        else:
            logger.error("Build failed")
            raise Exception("Build process failed")

    except Exception as e:
        logger.exception("An error occurred during the build process")
        raise Exception(f"Build error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
