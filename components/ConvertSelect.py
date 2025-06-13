from dataclasses import dataclass
from typing import Dict, List, Union

from PySide6.QtWidgets import QComboBox, QHBoxLayout, QWidget
from PySide6.QtCore import Signal

from components.ui import Text
from constant.File import File, Image, Video


class ConvertSelect(QWidget):
    @dataclass
    class SelectedItem:
        source: File
        target: File

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

    # Signal
    onSelected = Signal(SelectedItem, name="convert_selection_on_selected")

    def __init__(self, *args, **kwargs):
        super(ConvertSelect, self).__init__(*args, **kwargs)

        self.sourceComboBox = QComboBox(editable=True)
        self.targetComboBox = QComboBox(editable=True)
        self._initOptions()
        self.sourceComboBox.setCurrentIndex(-1)
        self.targetComboBox.setCurrentIndex(-1)
        self.sourceComboBox.currentIndexChanged.connect(self._onChangeSource)
        self.targetComboBox.currentIndexChanged.connect(self._onChangeTarget)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.addWidget(Text("Convert from"))
        layout.addWidget(self.sourceComboBox)
        layout.addWidget(Text("to"))
        layout.addWidget(self.targetComboBox)
        self.setLayout(layout)

    def _initOptions(self) -> None:
        curr = 0
        for option in self.OPTIONS:
            self.sourceComboBox.addItem(option.key)
            self.sourceComboBox.model().item(curr).setEnabled(False) # type: ignore
            self.sourceComboBox.addItems(option.children)
            curr += len(option.children) + 1
        self.targetComboBox.clear()

    def _findIndexFor(self, value: str) -> int:
        index = 0
        for option in self.OPTIONS:
            index += 1
            for child in option.children:
                if child == value:
                    return index
                index += 1
        return -1

    def setSource(self, fileType: File | None) -> None:
        if not isinstance(fileType, File):
            return
        self.sourceComboBox.setCurrentIndex(self._findIndexFor(fileType.value))

    @property
    def selectedSource(self) -> Union[File, None]:
        idx = self.sourceComboBox.currentIndex()
        if idx < 0:
            return None
        selected: File | None = File.from_str(
            self.sourceComboBox.model().item(idx).text() # type: ignore
        )
        return selected

    @property
    def selectedTarget(self) -> Union[File, None]:
        idx = self.targetComboBox.currentIndex()
        if idx < 0:
            return None
        selected: File | None = File.from_str(
            self.targetComboBox.model().item(idx).text() # type: ignore
        )
        return selected

    def _onChangeSource(self, _: int) -> None:
        self.targetComboBox.clear()
        if self.selectedSource is None:
            return
        curr = 0
        for option in self.PAIRS[self.selectedSource]:
            self.targetComboBox.addItem(option.key)
            self.targetComboBox.model().item(curr).setEnabled(False) # type: ignore
            self.targetComboBox.addItems(option.children)
            curr += len(option.children) + 1
        self.targetComboBox.setCurrentIndex(-1)

    def _onChangeTarget(self, _: int) -> None:
        if self.selectedSource is None or self.selectedTarget is None:
            return
        self.onSelected.emit(ConvertSelect.SelectedItem(
            source=self.selectedSource,
            target=self.selectedTarget,
        ))
