from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

from components.ConvertSelect import ConvertSelect
from components.FileInput import FileInput
from components.VideoOptions import VideoOptions
from components.ui import Text
from constant.File import File


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mediarage")

        central = QWidget(parent=self)
        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignJustify)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(10)

        layout.addWidget(Text(
            "Mediarage",
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter,
            size=32, bold=True,
        ))
        layout.addWidget(Text(
            "Welcome to Mediarage — locally built for speed, built for creators. Trim, compress, and convert without touching the cloud.",
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter,
            size=10, wrap=True,
        ))

        self.convertSelection = ConvertSelect(parent=central, visible=False)  # type: ignore
        self.videoOption = VideoOptions(parent=central, visible=False)
        self.fileInput = FileInput(parent=central)
        self.fileInput.onChange.connect(self._handleFileSelected)
        self.convertSelection.onSelected.connect(self._handleConvertOptionSelected)

        layout.addWidget(self.fileInput)
        layout.addWidget(self.convertSelection, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.videoOption, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(central)

    def _handleFileSelected(self, path: str):
        self.convertSelection.setSource(File.from_path(path))
        self.convertSelection.show()

    def _handleConvertOptionSelected(self):
        self.videoOption.show()

