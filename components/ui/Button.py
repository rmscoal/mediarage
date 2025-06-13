from typing import Literal, Dict

from PySide6.QtWidgets import QPushButton, QWidget
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt


class Button(QPushButton):
    normalStyle: Dict[str, str] = dict()
    hoverStyle: Dict[str, str] = dict()

    def __init__(self, text: str, /, parent: QWidget = None, *args, **kwargs):
        super().__init__(text, parent=parent, *args, **kwargs)
        self.setDefaultStyle()

        if "icon" in kwargs:
            self._setIcon(kwargs["icon"])
        if "style" in kwargs:
            self.normalStyle.update(kwargs["style"])
        if "hoverStyle" in kwargs:
            self.normalStyle.update(kwargs["hoverStyle"])

        self.applyStyle()

    def setDefaultStyle(self):
        self.normalStyle.update({
            "background-color": "#282a36",
            "color": "#f8f8f2",
            "border-radius": "5px",
            "text-align": "center",
            "padding": "4px 12px",
        })

        self.hoverStyle.update({
            "background-color": "#44475a",
            "color": "#fff",
        })

        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _setIcon(self,
                 path: str,
                 position: Literal["left"] | Literal["right"] = "left",
                 size: int = 24,
                 *args, **kwargs):
        self.setIcon(QIcon(path))
        self.setIconSize(QSize(size, size))
        if position == "left":
            self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
            self.normalStyle.update({"text-align": "left"})
        elif position == "right":
            self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    def applyStyle(self):
        normalStyleSheet: str = "QPushButton {"
        for key, value in self.normalStyle.items():
            normalStyleSheet += f"{key}: {value};"
        normalStyleSheet += "}"

        hoverStyleSheet: str = "QPushButton:hover {"
        for key, value in self.hoverStyle.items():
            hoverStyleSheet += f"{key}: {value};"
        hoverStyleSheet += "}"

        self.setStyleSheet("\n".join([normalStyleSheet, hoverStyleSheet]))
