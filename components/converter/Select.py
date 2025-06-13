from dataclasses import dataclass
from typing import Dict, List, Union

from PySide6.QtWidgets import QComboBox, QHBoxLayout, QWidget
from PySide6.QtCore import Signal

from components.ui import Text
from constant.File import File, Image, Video


class Select(QWidget):
    @dataclass
    class Selected:
        source: File
        target: File

    @dataclass
    class Item:
        key: str
        children: List[str]

    ITEMS: List[Item] = [
        Item(key="Image", children=[image.value for image in Image]),
        Item(key="Video", children=[video.value for video in Video]),
    ]

    PAIRS: Dict[File, List[Item]] = {
        # Images
        Image.JPEG: [
            Item(key="Image", children=[Image.PNG.value]),
        ],
        Image.JPG: [
            Item(key="Image", children=[Image.JPEG.value, Image.PNG.value]),
        ],

        # Videos
        Video.AVI: [
            Item(key="Video", children=[Video.MOV.value, Video.MP4.value, Video.MPEG.value]),
        ],
        Video.MOV: [
            Item(key="Image", children=[Image.GIF.value]),
            Item(key="Video", children=[Video.MP4.value, Video.MPEG.value])
        ],
        Video.MP4: [
            Item(key="Image", children=[Image.GIF.value]),
            Item(key="Video", children=[Video.MOV.value, Video.MPEG.value])
        ],
        Video.MPEG: [
            Item(key="Image", children=[Image.GIF.value]),
            Item(key="Video", children=[Video.MOV.value, Video.MP4.value])
        ],
    }

    # Signal
    onSelected = Signal(Selected, name="on_converter_selected_item")

    def __init__(self, *args, **kwargs):
        super(Select, self).__init__(*args, **kwargs)

        self.sourceComboBox = QComboBox(editable=True)
        self.targetComboBox = QComboBox(editable=True)
        self.__initItems()
        self.sourceComboBox.setCurrentIndex(-1)
        self.targetComboBox.setCurrentIndex(-1)
        self.sourceComboBox.currentIndexChanged.connect(self.__onChangeSource)
        self.targetComboBox.currentIndexChanged.connect(self.__onChangeTarget)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.addWidget(Text("Convert from"))
        layout.addWidget(self.sourceComboBox)
        layout.addWidget(Text("to"))
        layout.addWidget(self.targetComboBox)
        self.setLayout(layout)

    def __initItems(self) -> None:
        curr = 0
        for option in self.ITEMS:
            self.sourceComboBox.addItem(option.key)
            self.sourceComboBox.model().item(curr).setEnabled(False) # type: ignore
            self.sourceComboBox.addItems(option.children)
            curr += len(option.children) + 1
        self.targetComboBox.clear()

    def setSource(self, fileType: File | None) -> None:
        if not isinstance(fileType, File):
            return
        self.sourceComboBox.setCurrentIndex(self.__findIndexFor(fileType.value))

    def __findIndexFor(self, value: str) -> int:
        index = 0
        for option in self.ITEMS:
            index += 1
            for child in option.children:
                if child == value:
                    return index
                index += 1
        return -1

    @property
    def source(self) -> Union[File, None]:
        idx = self.sourceComboBox.currentIndex()
        if idx < 0:
            return None
        selected: File | None = File.from_str(
            self.sourceComboBox.model().item(idx).text() # type: ignore
        )
        return selected

    @property
    def target(self) -> Union[File, None]:
        idx = self.targetComboBox.currentIndex()
        if idx < 0:
            return None
        selected: File | None = File.from_str(
            self.targetComboBox.model().item(idx).text() # type: ignore
        )
        return selected

    def __onChangeSource(self, _: int) -> None:
        self.targetComboBox.clear()
        if self.source is None:
            return
        curr = 0
        for option in self.PAIRS[self.source]:
            self.targetComboBox.addItem(option.key)
            self.targetComboBox.model().item(curr).setEnabled(False) # type: ignore
            self.targetComboBox.addItems(option.children)
            curr += len(option.children) + 1
        self.sourceComboBox.clearFocus()
        self.targetComboBox.setCurrentIndex(-1)
        self.targetComboBox.setFocus()

    def __onChangeTarget(self, _: int) -> None:
        if self.source is None or self.target is None:
            return
        self.onSelected.emit(Select.Selected(
            source=self.source,
            target=self.target,
        ))
        self.targetComboBox.clearFocus()
