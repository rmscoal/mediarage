from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

from components.FileInput import FileInput
from components.ui import Text


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

        fileInput = FileInput(parent=central)
        layout.addWidget(fileInput)

        self.setCentralWidget(central)
