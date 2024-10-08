import asyncio
import io
import re
from fastapi import FastAPI, File, Form, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
import os
import aiofiles
from typing import Optional, Union
import logging
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)


mipmap_dir = "./kakao_theme_android/src/main"
theme_dir = "./kakao_theme_android/src/main/theme/drawable-xxhdpi"
colors_xml_path = "./kakao_theme_android/src/main/theme/values/colors.xml"
strings_xml_path = "./kakao_theme_android/src/main/theme/values/strings.xml"
strings_ja_xml_path = "./kakao_theme_android/src/main/theme/values-ja/strings.xml"
strings_ko_xml_path = "./kakao_theme_android/src/main/theme/values-ko/strings.xml"


@app.get("/test")
async def test():
    return "Success from android theme"


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

    await update_version_in_gradle()

    # 이미지 파일 저장
    file_names = [
        "commonIcoTheme.png",
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
        "theme_chatroom_bubble_me_01_image.9.png",
        "theme_chatroom_bubble_me_02_image.9.png",
        "theme_chatroom_bubble_you_01_image.9.png",
        "theme_chatroom_bubble_you_02_image.9.png",
        "theme_passcode_background_image.png",
        "theme_passcode_01_image.png",
        "theme_passcode_02_image.png",
        "theme_passcode_03_image.png",
        "theme_passcode_04_image.png",
        "theme_passcode_01_checked_image.png",
        "theme_passcode_02_checked_image.png",
        "theme_passcode_03_checked_image.png",
        "theme_passcode_04_checked_image.png",
    ]

    image_files = [
        kakaoIcon,
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
        bubbleSend2,
        bubbleReceive1,
        bubbleReceive2,
        passcodeBg,
        passcodeImage1,
        passcodeImage2,
        passcodeImage3,
        passcodeImage4,
        passcodeImage1Selected,
        passcodeImage2Selected,
        passcodeImage3Selected,
        passcodeImage4Selected,
    ]

    for image_file, file_name in zip(image_files, file_names):
        if image_file is not None:
            file_path = os.path.join(theme_dir, file_name)
            content = await image_file.read()

            if file_name == "theme_chatroom_bubble_me_01_image.9.png":
                location = sendEdgeinsets1
                content = create_nine_patch(content, location)
            elif file_name == "theme_chatroom_bubble_me_02_image.9.png":
                location = sendEdgeinsets2
                content = create_nine_patch(content, location)
            elif file_name == "theme_chatroom_bubble_you_01_image.9.png":
                location = receiveEdgeinsets1
                content = create_nine_patch(content, location)
            elif file_name == "theme_chatroom_bubble_you_02_image.9.png":
                location = receiveEdgeinsets2
                content = create_nine_patch(content, location)
            elif file_name == "commonIcoTheme.png":
                size_paths = {
                    72: mipmap_dir + "/res/mipmap-hdpi/ic_launcher_background.png",
                    48: mipmap_dir + "/res/mipmap-mdpi/ic_launcher_background.png",
                    96: mipmap_dir + "/res/mipmap-xhdpi/ic_launcher_background.png",
                    144: mipmap_dir + "/res/mipmap-xxhdpi/ic_launcher_background.png",
                    192: mipmap_dir + "/res/mipmap-xxxhdpi/ic_launcher_background.png",
                    512: mipmap_dir + "/ic_launcher-web.png",
                }
                create_mipmaps(content, size_paths)
                continue

            async with aiofiles.open(file_path, "wb") as out_file:
                await out_file.write(content)

    logger.info("theme file saved")

    update_text("theme_title", themeName)
    update_text("app_name", themeName)

    update_color("theme_header_color", headerColor)
    update_color("theme_section_title_color", sectionColor)  # input 필요
    update_color("theme_title_color", nameColor)  # input 필요
    update_color("theme_title_pressed_color", namePressedColor)
    update_color("theme_paragraph_color", paragraphColor)
    update_color("theme_paragraph_pressed_color", paragraphPressedColor)
    update_color("theme_description_color", descriptionColor)
    update_color("theme_description_pressed_color", descriptionPressedColor)
    update_color("theme_feature_primary_color", serviceBtnColor)
    update_color("theme_feature_primary_pressed_color", serviceBtnColor)  # input필요

    update_color("theme_background_color", mainBackgroundColor)
    update_color("theme_header_cell_color", mainBackgroundColor)
    update_color("theme_chatroom_background_color", chatRoomBgColor)
    update_color("theme_passcode_background_color", passcodeBgColor)

    update_color(
        "theme_body_cell_border_color",
        combine_color_and_opacity(borderColor, (borderOpacity)),
    )
    update_color(
        "theme_body_cell_color",
        combine_color_and_opacity(listBgColor, (listBgOpacity)),
    )
    update_color("theme_body_cell_pressed_color", listBgPressedColor)

    update_color("theme_body_secondary_cell_color", subBgColor)
    update_color(
        "theme_maintab_cell_color",
        combine_color_and_opacity(tabsBgColor, (1)),
    )
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
        "theme_passcode_keypad_pressed_background_color",
        combine_color_and_opacity(keyPadBgColor, 0.5),
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

    return FileResponse(apk_path, filename="custom_theme.apk")


def increment_version(version):
    major, minor, patch = map(int, version.split("."))
    patch += 1
    if patch == 1000:
        patch = 0
        minor += 1
        if minor == 1000:
            minor = 0
            major += 1
    return f"{major}.{minor}.{patch}"


async def update_version_in_gradle():
    gradle_file = "/app/kakao_theme_android/build.gradle"
    async with aiofiles.open(gradle_file, "r") as file:
        content = await file.read()

    version_pattern = r'versionName\s+"(\d+\.\d+\.\d+)"'
    match = re.search(version_pattern, content)
    if match:
        current_version = match.group(1)
        new_version = increment_version(current_version)
        content = re.sub(version_pattern, f'versionName "{new_version}"', content)

        async with aiofiles.open(gradle_file, "w") as file:
            await file.write(content)

        logger.info(f"Version updated from {current_version} to {new_version}")
    else:
        logger.warning("Version not found in build.gradle")


def create_mipmaps(image_bytes, size_paths):
    original_image = Image.open(io.BytesIO(image_bytes))

    for size, path in size_paths.items():
        resized_image = original_image.copy()
        resized_image.thumbnail((size, size))

        os.makedirs(os.path.dirname(path), exist_ok=True)

        resized_image.save(path)

        logger.info(f"Saved mipmap {size}x{size} to: {path}")


def update_text(text_name, new_value):
    xml_paths = [strings_xml_path, strings_ja_xml_path, strings_ko_xml_path]

    for path in xml_paths:
        tree = ET.parse(path)
        root = tree.getroot()

        for color_element in root.findall(".//string[@name='{}']".format(text_name)):
            if new_value is not None:
                color_element.text = str(new_value)

        tree.write(path, encoding="utf-8", xml_declaration=True)


def update_color(color_name, new_value):
    # XML 파일 파싱
    tree = ET.parse(colors_xml_path)
    root = tree.getroot()

    # 'name' 속성으로 색상 요소 찾기
    for color_element in root.findall(".//color[@name='{}']".format(color_name)):
        # 새 값으로 업데이트
        if new_value is not None:
            color_element.text = str(new_value)

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
            apk_path = "/app/kakao_theme_android/build/outputs/apk/debug/ONO-theme.apk"
            logger.info("Build successful")
            return apk_path
        else:
            logger.error("Build failed")
            raise Exception("Build process failed")

    except Exception as e:
        logger.exception("An error occurred during the build process")
        raise Exception(f"Build error: {str(e)}")


def opacity_to_hex(opacity: Union[float, int, None] = None) -> str:
    if opacity is None:
        opacity_float = 1.0
    else:
        try:
            opacity_float = float(opacity)
        except ValueError:
            raise ValueError("Opacity must be a number", opacity)

        if not 0 <= opacity_float <= 1:
            raise ValueError("Opacity must be between 0 and 1", opacity)

    hex_value = int(opacity_float * 255)
    return f"{hex_value:02X}"


def combine_color_and_opacity(
    color: Optional[str], opacity: Union[float, int, None]
) -> Optional[str]:
    if color is None:
        return None
    hex_color = color.lstrip("#")
    return "#" + opacity_to_hex(opacity) + hex_color


def create_nine_patch(imageObj, location):
    stretch_width, stretch_height, padding_width, padding_height = map(
        lambda x: int(x.rstrip("px")), location.split()
    )

    # Open the image
    img = Image.open(io.BytesIO(imageObj))

    # Calculate the start and end points for stretch and padding areas
    left_start = (img.width - stretch_width) // 2
    left_end = left_start + stretch_width
    top_start = (img.height - stretch_height) // 2
    top_end = top_start + stretch_height

    right_start = (img.height - padding_height) // 2
    right_end = right_start + padding_height
    bottom_start = (img.width - padding_width) // 2
    bottom_end = bottom_start + padding_width

    # Create a new image with a 1-pixel border
    nine_patch = Image.new("RGBA", (img.width + 2, img.height + 2), (0, 0, 0, 0))

    # Paste the original image into the center
    nine_patch.paste(img, (1, 1))

    # Create a drawing object
    draw = ImageDraw.Draw(nine_patch)

    # Draw the stretchable areas (left and top)
    draw.line([(0, 0), (left_start, 0)], fill=(0, 0, 0, 0))
    draw.line([(left_start, 0), (left_end, 0)], fill="black")
    draw.line([(left_end, 0), (img.width + 1, 0)], fill=(0, 0, 0, 0))

    draw.line([(0, 0), (0, top_start)], fill=(0, 0, 0, 0))
    draw.line([(0, top_start), (0, top_end)], fill="black")
    draw.line([(0, top_end), (0, img.height + 1)], fill=(0, 0, 0, 0))

    # Draw the padding box (right and bottom)
    draw.line([(img.width + 1, 0), (img.width + 1, right_start)], fill=(0, 0, 0, 0))
    draw.line([(img.width + 1, right_start), (img.width + 1, right_end)], fill="black")
    draw.line(
        [(img.width + 1, right_end), (img.width + 1, img.height + 1)], fill=(0, 0, 0, 0)
    )

    draw.line([(0, img.height + 1), (bottom_start, img.height + 1)], fill=(0, 0, 0, 0))
    draw.line(
        [(bottom_start, img.height + 1), (bottom_end, img.height + 1)], fill="black"
    )
    draw.line(
        [(bottom_end, img.height + 1), (img.width + 1, img.height + 1)],
        fill=(0, 0, 0, 0),
    )

    # Save the nine-patch image to a bytes buffer
    buffer = io.BytesIO()
    nine_patch.save(buffer, format="PNG")
    return buffer.getvalue()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
