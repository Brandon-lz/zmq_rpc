"""Take screenshots and video recordings from webcam."""

import time
from pathlib import Path
from urllib.request import urlopen
from PIL import Image

import reflex as rx
import reflex_webcam as webcam


# # Identifies a particular webcam component in the DOM
WEBCAM_REF = "webcam"
VIDEO_FILE_NAME = "video.webm"

# The path containing the app
APP_PATH = Path(__file__)
APP_MODULE_DIR = APP_PATH.parent
SOURCE_CODE = [
    APP_MODULE_DIR.parent.parent / "pages/test/__init__.py",
    APP_PATH,
    APP_MODULE_DIR.parent / "requirements.txt",
]

# Mark Upload as used so StaticFiles can get mounted on /_upload
rx.upload()


class TestState(rx.State):
    last_screenshot: Image.Image | None = None
    last_screenshot_timestamp: str = ""
    loading: bool = False
    recording: bool = False

    def handle_screenshot(self, img_data_uri: str):
        """Webcam screenshot upload handler.
        Args:
            img_data_uri: The data uri of the screenshot (from upload_screenshot).
        """
        if self.loading:
            return
        self.last_screenshot_timestamp = time.strftime("%H:%M:%S")
        with urlopen(img_data_uri) as img:
            self.last_screenshot = Image.open(img)
            self.last_screenshot.load()
            # convert to webp during serialization for smaller size
            self.last_screenshot.format = "WEBP"  # type: ignore

    def _video_path(self) -> Path:
        return Path(rx.get_upload_dir()) / VIDEO_FILE_NAME

    @rx.cached_var
    def video_exists(self) -> bool:
        if not self.recording:
            return self._video_path().exists()
        return False

    def on_start_recording(self):
        self.recording = True
        print("Started recording")
        with self._video_path().open("wb") as f:
            f.write(b"")

    def _strip_codec_part(self, chunk: str) -> str:
        parts = chunk.split(";")
        for part in parts:
            if "codecs=" in part:
                parts.remove(part)
                break
        return ";".join(parts)

    def handle_video_chunk(self, chunk: str):
        print("Got video chunk", len(chunk))
        with self._video_path().open("ab") as f:
            with urlopen(self._strip_codec_part(chunk)) as vid:
                f.write(vid.read())

    def on_stop_recording(self):
        print(f"Stopped recording: {self._video_path()}")
        self.recording = False

    def start_recording(self, ref: str):
        """Start recording a video."""
        return webcam.start_recording(
            ref,
            on_data_available=TestState.handle_video_chunk,
            on_start=TestState.on_start_recording,
            on_stop=TestState.on_stop_recording,
            timeslice=1000,
        )


def last_screenshot_widget() -> rx.Component:
    """Widget for displaying the last screenshot and timestamp."""
    return rx.box(
        rx.cond(
            TestState.last_screenshot,
            rx.fragment(
                rx.image(src=TestState.last_screenshot),
                rx.text(TestState.last_screenshot_timestamp),
            ),
            rx.center(
                rx.text("Click image to capture.", size="4"),
            ),
        ),
        height="270px",
    )


def webcam_upload_component(ref: str) -> rx.Component:
    """Component for displaying webcam preview and uploading screenshots.
    Args:
        ref: The ref of the webcam component.
    Returns:
        A reflex component.
    """
    return rx.vstack(
        webcam.webcam(
            id=ref,
            audio=True,
            width="100%",
            height="100%",
        ),
        rx.hstack(
            rx.button(
                "take screenshot",
                on_click=webcam.upload_screenshot(
                    ref=ref,
                    handler=TestState.handle_screenshot,  # type: ignore
                ),
                color_scheme="tomato",
                size="4",
            ),
            rx.cond(
                ~TestState.recording,
                rx.button(
                    "🟢 Start Recording",
                    on_click=TestState.start_recording(ref),
                    color_scheme="green",
                    size="4",
                ),
                rx.button(
                    "🟤 Stop Recording",
                    on_click=webcam.stop_recording(ref),
                    color_scheme="tomato",
                    size="4",
                ),
            ),
            justify="center",
        ),
        rx.cond(
            TestState.video_exists,
            rx.link(
                "Download Last Video", href=rx.get_upload_url(VIDEO_FILE_NAME), size="4"
            ),
        ),
        last_screenshot_widget(),  # 显示拍照照片和时间戳
        width="320px",
        align="center",
    )


def index() -> rx.Component:
    return rx.fragment(
        rx.icon_button(
            rx.color_mode.icon(), on_click=rx.style.toggle_color_mode, float="right"
        ),
        # rx.color_mode.button(rx.color_mode.icon(), float="right"),
        rx.center(
            webcam_upload_component(WEBCAM_REF),
            padding_top="3em",
        ),
        *[
            rx.vstack(
                rx.heading(f"Source Code: {p.name}"),
                rx.code_block(
                    p.read_text(),
                    language="python",
                    width="90%",
                    overflow_x="auto",
                ),
                margin_top="5em",
                padding_x="1em",
                width="100vw",
                align="center",
            )
            for p in SOURCE_CODE
        ],
        width="100vw",
    )
