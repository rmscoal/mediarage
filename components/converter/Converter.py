from typing import cast, Dict, List, Type, Union
from dataclasses import dataclass
from unittest import case

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QSpacerItem, QSizePolicy, QVBoxLayout

from components.ui import Text
from constant.File import File, Video

from .Option import CRF, Resolution, Preset, FrameRate, VideoForm
from .Select import Select

_spacer = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)  # type: ignore


class Converter(QWidget):
    @dataclass
    class Form:
        element: Union[Type[VideoForm] | QWidget]
        full: bool = False

    # Constant
    forms: Dict[Type[File], List[Form]] = {
        Video: [
            Form(element=Text("Video", size=16, alignment=Qt.AlignmentFlag.AlignLeft), full=True),
            Form(element=CRF), Form(element=Resolution),
            Form(element=Preset), Form(element=FrameRate),
        ]
    }

    # Components
    select: Select
    button: QPushButton

    # State
    input: str  # Input file path
    output: str  # Output file path
    currRow: int = 0
    currColumn: int = 0
    MAX_COLUMN: int = 2

    def __init__(self, *args, **kwargs):
        super(Converter, self).__init__(*args, **kwargs)

        # Reading kwargs
        if "input" in kwargs:
            self.input = kwargs["input"]

        # VBox to house the convert button
        self.vbox = QVBoxLayout()
        self.vbox.setSpacing(20)

        # Grid to house the forms
        form_container = QWidget()
        self.grid = QGridLayout(form_container)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignJustify)
        self.grid.setSpacing(4)
        self.vbox.addWidget(form_container)

        # Select Component
        self.select = Select()
        self.select.onSelected.connect(lambda _: self.__showForm())
        self.__addToGrid(self.select, full=True)
        self.grid.addItem(_spacer)

        # Convert Button
        self.button = QPushButton("Convert")
        self.button.hide()
        self.button.clicked.connect(self.convert)
        self.vbox.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.vbox)

    def __showForm(self):
        for form in self.forms[type(self.select.target)]:
            if isinstance(form.element, type(VideoForm)):
                self.__addToGrid(form.element(self), full=form.full)
            elif isinstance(form.element, Text):
                self.__addToGrid(form.element, full=form.full, alignment=Qt.AlignmentFlag.AlignLeft)
        self.button.show()

    def __addToGrid(self, widget: QWidget, **kwargs):
        """Adds component to grid layout"""
        self.grid = cast(QGridLayout, self.grid)

        full = False
        if "full" in kwargs:
            full = kwargs["full"]

        alignment = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight
        if "alignment" in kwargs:
            alignment = kwargs["alignment"]

        if full:
            self.grid.addWidget(widget, self.currRow, 0, 1, self.MAX_COLUMN, alignment=alignment)
            self.currRow += 1
            self.currColumn = 0
        else:
            self.grid.addWidget(widget, self.currRow, self.currColumn, alignment=alignment)
            self.currColumn += 1
            if self.currColumn >= self.MAX_COLUMN:
                self.currColumn = 0
                self.currRow += 1

    def setInput(self, input_file: str):
        self.input = input_file

    def convert(self):
        # TODO: Complete
        forms = self.findChildren(VideoForm)
        for form in forms:
            pass
        if self.input == "":
            return
