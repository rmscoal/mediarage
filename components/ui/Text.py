from typing import Dict

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel

PREFERRED_FONT_FAMILIES = ["JetBrains Mono", "San Francisco Pro", "Sans-Serif"]
DEFAULT_SIZE = 12


class Text(QLabel):
    normalStyle: Dict[str, str] = dict()
    hoverStyle: Dict[str, str] = dict()

    def __init__(self, text: str, *args, **kwargs):
        super().__init__(text, *args)

        self.setFont(QFont("Sans-Serif", 12))
        if "size" in kwargs:
            font = self.font()
            font.setPointSize(int(kwargs["size"]))
            self.setFont(font)
        if "fontFamily" in kwargs:
            font = self.font()
            font.setFamily(kwargs["fontFamily"])
            self.setFont(font)
        if "bold" in kwargs:
            font = self.font()
            font.setBold(bool(kwargs["bold"]))
            self.setFont(font)

        if "alignment" in kwargs:
            self.setAlignment(kwargs["alignment"])
        if "wrap" in kwargs:
            self.setWordWrap(bool(kwargs["wrap"]))
        if "width" in kwargs:
            self.setFixedWidth(int(kwargs["width"]))
        if "style" in kwargs:
            self.normalStyle.update(kwargs["style"])
