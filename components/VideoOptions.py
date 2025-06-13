# Video:
# | Option                   | Description                                               |
# | ------------------------ | --------------------------------------------------------- |
# | `-c:v libx264`           | Use H.264 video codec (recommended for MP4)               |
# | `-crf 23`                | Constant Rate Factor (quality, 0–51, lower = better)      |
# | `-preset fast`           | Encoding speed/efficiency tradeoff (ultrafast → veryslow) |
# | `-b:v 1000k`             | Set video bitrate (use with `-c:v libx264`)               |
# | `-vf scale=WIDTH:HEIGHT` | Resize video (e.g., `-vf scale=1280:720`)                 |
# | `-r 30`                  | Frame rate (frames per second)                            |
# | `-pix_fmt yuv420p`       | Pixel format (for compatibility with players)             |
#
# Audio:
# | Option      | Description                             |
# | ----------- | --------------------------------------- |
# | `-c:a aac`  | Use AAC audio codec                     |
# | `-b:a 128k` | Set audio bitrate                       |
# | `-ar 44100` | Audio sample rate                       |
# | `-ac 2`     | Number of audio channels (e.g., stereo) |
#
# Filter:
# | Option               | Description                                       |
# | -------------------- | ------------------------------------------------- |
# | `-vf "transpose=1"`  | Rotate video (e.g., 90° clockwise)                |
# | `-vf "fps=30"`       | Force specific frame rate                         |
# | `-vf "crop=w:h:x:y"` | Crop video (`w=width`, `h=height`, `x/y=offsets`) |
# | `-vf "scale=-1:720"` | Resize to 720px height while keeping aspect ratio |
#
# Advanced:
# | Option         | Description                                  |
# | -------------- | -------------------------------------------- |
# | `-map 0`       | Include all streams (audio, video, subtitle) |
# | `-threads 4`   | Number of threads to use                     |
# | `-t 00:00:10`  | Duration (cut to first 10 seconds)           |
# | `-ss 00:00:05` | Start time (skip first 5 seconds)            |

from typing import cast, List, Optional
from dataclasses import dataclass

from PySide6.QtCore import Qt, QSize, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QWidget, QGridLayout, QComboBox, QLineEdit, QVBoxLayout

from components.ui import Text

INPUT_FIXED_WIDTH: int = 200
INPUT_FIXED_HEIGHT: int = 25


class VideoOptions(QWidget):
    NUM_COLUMNS: int = 4
    currRow: int = 0
    currColumn: int = 0

    def __init__(self, /, parent=None):
        super(VideoOptions, self).__init__(parent)

        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignJustify)
        layout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(layout)

        # Basic Video Options
        layout.addWidget(Text("Video", size=16), self.currRow, 0, 1, 4)
        self.currRow += 1
        self.currColumn = 0
        CRFOption(parent=self)
        ResolutionOption(parent=self)
        PresetOption(parent=self)
        FrameRateOption(parent=self)
        self.currRow += 1

        # Trim Options
        layout.addWidget(Text("Trim", size=16), self.currRow, 0, 1, 4)
        self.currRow += 1
        self.currColumn = 0
        TrimOption(parent=self)


class VideoOptionForm(QWidget):

    def __init__(self, /,
                 parent: QWidget | None = None,
                 name: str = "",
                 description: Optional[str] = None,
                 autoLayout: bool = True):
        super().__init__(parent)

        self.label = Text(name, size=12, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.label.setWordWrap(True)

        self.input: QWidget = QComboBox()
        self.input.setFixedSize(QSize(INPUT_FIXED_WIDTH, INPUT_FIXED_HEIGHT))
        self.initOptions()

        inputContainer = QWidget()
        inputContainerLayout = QVBoxLayout(inputContainer)
        inputContainerLayout.setContentsMargins(0, 0, 0, 0)
        inputContainerLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        inputContainerLayout.addWidget(self.input)

        if description:
            helper = Text(description, size=10, alignment=Qt.AlignmentFlag.AlignLeft)
            helper.setWordWrap(True)
            helper.setStyleSheet("color: grey;")
            helper.setFixedWidth(200)
            inputContainerLayout.addWidget(helper)

        if autoLayout and self.parent():
            parent = cast(QWidget, self.parent())
            if not isinstance(parent, VideoOptions):
                raise ValueError("Parent must be a VideoOptions instance")

            parentLayout = parent.layout()
            if not isinstance(parentLayout, QGridLayout):
                raise ValueError("Parent's layout must be a QGridLayout instance")

            if parent.currColumn >= parent.NUM_COLUMNS:
                parent.currRow += 1
                parent.currColumn = 0
            parentLayout.addWidget(self.label, parent.currRow, parent.currColumn)
            parentLayout.addWidget(inputContainer, parent.currRow, parent.currColumn + 1)
            parent.currColumn += 2

    def initOptions(self) -> None:
        if isinstance(self.input, QComboBox):
            raise NotImplementedError("Subclasses must implement initOptions")

    def toCmdLineStr(self) -> str:
        raise NotImplementedError("Subclasses must implement toCmdLineStr")


class CRFOption(VideoOptionForm):
    input: QComboBox   # type: ignore

    def __init__(self, parent=None):
        super().__init__(parent,
                         "Constant Quality\n(CRF)",
                         "The CRF value sets the video quality between 0-51. Lower values means better quality but longer conversion times.")

    def initOptions(self):
        for i in range(0, 52):
            if i == 0:
                self.input.addItem(f"{i} (lossless compression)")
            elif i == 18:
                self.input.addItem(f"{i} (high quality)")
            elif i == 23:
                self.input.addItem(f"{i} (normal quality)")
                # Sets as default value
                self.input.setCurrentIndex(i)
            elif i == 28:
                self.input.addItem(f"{i} (low quality)")
            elif i == 51:
                self.input.addItem(f"{i} (worst quality)")
            else:
                self.input.addItem(f"{i}")

    def toCmdLineStr(self) -> str:
        return f"-crf {self.input.currentIndex()}"


class ResolutionOption(VideoOptionForm):
    @dataclass
    class Option:
        name: str
        width: int
        height: int
        aspectRatio: float

    OPTIONS: List[Option] = [
        Option(
            name="no change",
            width=0,
            height=0,
            aspectRatio=0,
        ),
        Option(
            name="640x480 (4:3)",
            width=640,
            height=480,
            aspectRatio=4 / 3,
        ),
        Option(
            name="640x640 (1:1)",
            width=640,
            height=640,
            aspectRatio=1,
        ),
        Option(
            name="800x600 (4:3)",
            width=800,
            height=600,
            aspectRatio=4 / 3,
        ),
        Option(
            name="960x720 (4:3)",
            width=960,
            height=720,
            aspectRatio=4 / 3,
        ),
        Option(
            name="1024x768 (4:3)",
            width=1024,
            height=768,
            aspectRatio=4 / 3,
        ),
        Option(
            name="1024x1024 (1:1)",
            width=1024,
            height=1024,
            aspectRatio=1,
        ),
        Option(
            name="1280x720 (16:9)",
            width=1280,
            height=720,
            aspectRatio=16 / 9,
        ),
        Option(
            name="1280x960 (4:3)",
            width=1280,
            height=960,
            aspectRatio=4 / 3,
        ),
        Option(
            name="1280x1280 (1:1)",
            width=1280,
            height=1280,
            aspectRatio=1,
        ),
        Option(
            name="1440x1080 (4:3)",
            width=1440,
            height=1080,
            aspectRatio=4 / 3,
        ),
        Option(
            name="1600x1200 (4:3)",
            width=1600,
            height=1200,
            aspectRatio=4 / 3,
        ),
        Option(
            name="1600x1600 (1:1)",
            width=1600,
            height=1600,
            aspectRatio=1,
        ),
        Option(
            name="1920x1080 (16:9)",
            width=1920,
            height=1080,
            aspectRatio=16 / 9,
        ),
        Option(
            name="1920x1440 (4:3)",
            width=1920,
            height=1440,
            aspectRatio=4 / 3,
        ),
        # TODO: Implement these later ⬇️
        # "1920x1920 (1:1)",
        # "2560x1440 (16:9)",
        # "2560x1920 (4:3)",
        # "2560x2560 (1:1)",
        # "3840x2160 (16:9)",
        # "3840x2880 (4:3)",
        # "3840x3840 (1:1)"
    ]

    input: QComboBox   # type: ignore

    def __init__(self, parent=None):
        super().__init__(parent, "Resolution")

    def initOptions(self):
        for option in self.OPTIONS:
            self.input.addItem(option.name, userData=option)
        self.input.setCurrentIndex(0)

    def toCmdLineStr(self) -> str:
        option = self.input.currentData()
        if option.name == "no change":
            return ""
        return f"-vf scale={option.width}:{option.height}"


class PresetOption(VideoOptionForm):
    OPTIONS: List[str] = [
        "ultrafast",
        "superfast",
        "veryfast",
        "faster",
        "fast",
        "medium",
        "slow",
        "slower",
        "veryslow",
    ]

    input: QComboBox   # type: ignore

    def __init__(self, parent=None):
        super().__init__(parent, "Preset")

    def initOptions(self):
        for option in self.OPTIONS:
            self.input.addItem(option)
            if option == "medium":
                # Sets as default value
                self.input.setCurrentIndex(self.input.count() - 1)

    def toCmdLineStr(self):
        return f"-preset {self.input.currentText()}"


class FrameRateOption(VideoOptionForm):
    OPTIONS: List[int | str] = [
        "auto",
        60,
        30,
        24,
        15,
        12,
        10,
        8,
        6,
        5,
    ]

    input: QComboBox   # type: ignore

    def __init__(self, parent=None):
        super().__init__(parent, "Frame Rate")

    def initOptions(self):
        for option in self.OPTIONS:
            self.input.addItem(str(option), userData=option)
            if option == "auto":
                # Sets as default value
                self.input.setCurrentIndex(self.input.count() - 1)

    def toCmdLineStr(self):
        option = self.input.currentData()
        if option == "auto":
            return ""
        return f"-r {option}"


class TrimOption(VideoOptionForm):
    input: None   # type: ignore

    def __init__(self, parent=None):
        super().__init__(parent, "Trim", autoLayout=False)

        # Clear the inherited input
        self.input = None   # type: ignore

        self.trimStart = QLineEdit()
        self.trimStart.setPlaceholderText("HH:MM:SS")
        self.trimStart.setFixedSize(QSize(INPUT_FIXED_WIDTH, INPUT_FIXED_HEIGHT))
        self.trimEnd = QLineEdit()
        self.trimEnd.setPlaceholderText("HH:MM:SS")
        self.trimEnd.setFixedSize(QSize(INPUT_FIXED_WIDTH, INPUT_FIXED_HEIGHT))

        validator = QRegularExpressionValidator(QRegularExpression(r"^\d{2}:\d{2}:\d{2}$"))
        self.trimStart.setValidator(validator)
        self.trimEnd.setValidator(validator)

        # Directly append to the parent's layout
        parent = self.parent()
        if not isinstance(parent, VideoOptions):
            raise ValueError("Parent must be a VideoOptions instance")

        parentLayout = parent.layout()
        if not isinstance(parentLayout, QGridLayout):
            raise ValueError("Parent's layout must be a QGridLayout instance")

        parent.currRow += 1
        parent.currColumn = 0
        parentLayout.addWidget(Text("Trim Start"), parent.currRow, 0)
        parentLayout.addWidget(self.trimStart, parent.currRow, 1)
        parentLayout.addWidget(Text("Trim End"), parent.currRow, 2)
        parentLayout.addWidget(self.trimEnd, parent.currRow, 3)
        parent.currRow += 1

    def initOptions(self) -> None:
        pass

    def toCmdLineStr(self) -> str:
        start = self.trimStart.text()
        end = self.trimEnd.text()

        if not start and not end:
            return ""

        result = []
        if start:
            result.append(f"-ss {start}")
        if end:
            if start:
                # Calculate duration when both start and end are provided
                from datetime import datetime
                time_format = "%H:%M:%S"
                duration = datetime.strptime(end, time_format) - datetime.strptime(start, time_format)
                result.append(f"-t {duration}")
            else:
                # Use end time directly if only the end is provided
                result.append(f"-t {end}")

        return " ".join(result)
