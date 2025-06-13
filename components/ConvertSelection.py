from dataclasses import dataclass
from typing import Dict, List, Union

from PySide6.QtWidgets import QWidget, QComboBox, QHBoxLayout

from components.ui import Text
from constant.Types import Video, Image, File


class ConvertSelection(QWidget):
    @dataclass
    class Option:
        key: str
        children: List[str]

    OPTIONS: List[Option] = [
        Option(key="Image", children=[image.value for image in Image]),
        Option(key="Video", children=[video.value for video in Video]),
    ]

    PAIRS: Dict[File, List[Option]] = {
        # Images
        Image.JPEG: [
            Option(key="Image", children=[Image.PNG.value]),
        ],
        Image.JPG: [
            Option(key="Image", children=[Image.JPEG.value, Image.PNG.value]),
        ],

        # Videos
        Video.AVI: [
            Option(key="Video", children=[Video.MOV.value, Video.MP4.value, Video.MPEG.value]),
        ],
        Video.MOV: [
            Option(key="Image", children=[Image.GIF.value]),
            Option(key="Video", children=[Video.MP4.value, Video.MPEG.value])
        ],
        Video.MP4: [
            Option(key="Image", children=[Image.GIF.value]),
            Option(key="Video", children=[Video.MOV.value, Video.MPEG.value])
        ],
        Video.MPEG: [
            Option(key="Image", children=[Image.GIF.value]),
            Option(key="Video", children=[Video.MOV.value, Video.MP4.value])
        ],
    }

    def __init__(self, parent=None):
        super(ConvertSelection, self).__init__(parent)

        self.leftComboBox = QComboBox(editable=True)
        self.rightComboBox = QComboBox(editable=True)
        self._initOptions()
        self.leftComboBox.currentIndexChanged.connect(self.onChangeLeftComboBox)
        self.rightComboBox.currentIndexChanged.connect(self.onChangeRightComboBox)
        self.leftComboBox.setCurrentIndex(-1), self.rightComboBox.setCurrentIndex(-1)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.addWidget(Text("Convert from"))
        layout.addWidget(self.leftComboBox)
        layout.addWidget(Text("to"))
        layout.addWidget(self.rightComboBox)
        self.setLayout(layout)

    def _initOptions(self) -> None:
        curr = 0
        for option in self.OPTIONS:
            self.leftComboBox.addItem(option.key)
            self.leftComboBox.model().item(curr).setEnabled(False)
            self.leftComboBox.addItems(option.children)
            curr += len(option.children) + 1
        self.rightComboBox.clear()

    @property
    def getSelectedLeftComboBox(self) -> Union[File, None]:
        idx = self.leftComboBox.currentIndex()
        if idx < 0:
            return None
        selected: File | None = File.from_str(
            self.leftComboBox.model().item(idx).text()
        )
        return selected

    @property
    def getSelectedRightComboBox(self) -> Union[File, None]:
        idx = self.rightComboBox.currentIndex()
        if idx < 0:
            return None
        selected: File | None = File.from_str(
            self.rightComboBox.model().item(idx).text()
        )
        return selected

    def onChangeLeftComboBox(self, _: int):
        """
        As the right combo box has been chosen, we adjust the left combobox.
        """
        self.rightComboBox.clear()

        curr = 0
        for option in self.PAIRS[self.getSelectedLeftComboBox]:
            self.rightComboBox.addItem(option.key)
            self.rightComboBox.model().item(curr).setEnabled(False)
            self.rightComboBox.addItems(option.children)
            curr += len(option.children) + 1
        self.rightComboBox.setCurrentIndex(-1)

    def onChangeRightComboBox(self, _: int):
        print("Selected Left: ", self.getSelectedLeftComboBox, " Selected Right: ", self.getSelectedRightComboBox)
